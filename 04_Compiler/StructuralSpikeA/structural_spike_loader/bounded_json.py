from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, BinaryIO

from .diagnostics import (
    DiagnosticCode,
    DiagnosticReason,
    InputDiagnostic,
    JsonPointerToken,
)
from .model import LoadFailure


MAX_INPUT_BYTES = 10_485_760
MAX_JSON_DEPTH = 32
MAX_INPUT_RECORDS = 1_000_000
MAX_CANONICAL_INTEGER = 2_147_483_647
_READ_CHUNK_BYTES = 65_536
_JSON_WHITESPACE = " \t\r\n"
_CANONICAL_INTEGER = re.compile(r"(?:0|[1-9][0-9]*)\Z")


@dataclass(frozen=True, slots=True)
class NumericToken:
    pointer: tuple[JsonPointerToken, ...]
    spelling: str


@dataclass(frozen=True, slots=True)
class ParsedDocument:
    value: Any
    numeric_tokens: tuple[NumericToken, ...]
    byte_count: int
    record_count: int
    maximum_depth: int


@dataclass(slots=True)
class _Frame:
    kind: str
    pointer: tuple[JsonPointerToken, ...]
    depth: int
    state: str
    builder: Any
    seen_keys: set[str] = field(default_factory=set)
    current_key: str | None = None
    next_index: int = 0


class _ParseFailure(Exception):
    def __init__(self, diagnostic: InputDiagnostic) -> None:
        super().__init__(diagnostic.reason.value)
        self.diagnostic = diagnostic


def _failure(
    code: DiagnosticCode,
    reason: DiagnosticReason,
    pointer: tuple[JsonPointerToken, ...] = (),
) -> _ParseFailure:
    return _ParseFailure(InputDiagnostic(code=code, reason=reason, pointer=pointer))


def _read_bounded_bytes(
    source: bytes | bytearray | memoryview | BinaryIO,
    maximum_bytes: int,
) -> bytes:
    if isinstance(source, bytes):
        if len(source) > maximum_bytes:
            raise _failure(
                DiagnosticCode.LIMIT,
                DiagnosticReason.BYTE_LIMIT_EXCEEDED,
            )
        return source
    if isinstance(source, (bytearray, memoryview)):
        byte_count = source.nbytes if isinstance(source, memoryview) else len(source)
        if byte_count > maximum_bytes:
            raise _failure(
                DiagnosticCode.LIMIT,
                DiagnosticReason.BYTE_LIMIT_EXCEEDED,
            )
        return bytes(source)

    reader = getattr(source, "read", None)
    if reader is None or not callable(reader):
        raise _failure(
            DiagnosticCode.SYNTAX,
            DiagnosticReason.INVALID_SOURCE_TYPE,
        )

    chunks: list[bytes] = []
    total = 0
    try:
        while True:
            remaining_probe = maximum_bytes + 1 - total
            if remaining_probe <= 0:
                raise _failure(
                    DiagnosticCode.LIMIT,
                    DiagnosticReason.BYTE_LIMIT_EXCEEDED,
                )
            requested = min(_READ_CHUNK_BYTES, remaining_probe)
            chunk = reader(requested)
            if not isinstance(chunk, bytes):
                raise _failure(
                    DiagnosticCode.SYNTAX,
                    DiagnosticReason.INVALID_SOURCE_TYPE,
                )
            if not chunk:
                break
            if len(chunk) > requested or total + len(chunk) > maximum_bytes:
                raise _failure(
                    DiagnosticCode.LIMIT,
                    DiagnosticReason.BYTE_LIMIT_EXCEEDED,
                )
            chunks.append(chunk)
            total += len(chunk)
    except _ParseFailure:
        raise
    except Exception:
        raise _failure(
            DiagnosticCode.SYNTAX,
            DiagnosticReason.INVALID_SOURCE_TYPE,
        ) from None
    return b"".join(chunks)


class _Parser:
    def __init__(
        self,
        text: str,
        *,
        maximum_depth: int,
        maximum_records: int,
    ) -> None:
        self._text = text
        self._length = len(text)
        self._position = 0
        self._maximum_depth_limit = maximum_depth
        self._maximum_records = maximum_records
        self._record_count = 0
        self._maximum_depth_seen = 0
        self._numeric_tokens: list[NumericToken] = []
        self._stack: list[_Frame] = []
        self._root_is_set = False
        self._root: Any = None

    def parse(self, byte_count: int) -> ParsedDocument:
        self._skip_whitespace()
        if self._position == self._length:
            raise _failure(
                DiagnosticCode.SYNTAX,
                DiagnosticReason.EMPTY_DOCUMENT,
            )

        self._parse_value(())
        while self._stack:
            frame = self._stack[-1]
            self._skip_whitespace()
            if frame.kind == "object":
                self._advance_object(frame)
            else:
                self._advance_array(frame)

        self._skip_whitespace()
        if self._position != self._length:
            raise _failure(
                DiagnosticCode.SYNTAX,
                DiagnosticReason.TRAILING_CONTENT,
            )
        if not self._root_is_set:
            raise RuntimeError("parser completed without a root value")
        return ParsedDocument(
            value=self._root,
            numeric_tokens=tuple(self._numeric_tokens),
            byte_count=byte_count,
            record_count=self._record_count,
            maximum_depth=self._maximum_depth_seen,
        )

    def _skip_whitespace(self) -> None:
        while (
            self._position < self._length
            and self._text[self._position] in _JSON_WHITESPACE
        ):
            self._position += 1

    def _value_pointer(self, frame: _Frame) -> tuple[JsonPointerToken, ...]:
        if frame.kind == "object":
            if frame.current_key is None:
                raise RuntimeError("object value has no current key")
            return frame.pointer + (frame.current_key,)
        return frame.pointer + (frame.next_index,)

    def _advance_object(self, frame: _Frame) -> None:
        if frame.state in {"key-or-end", "key"}:
            if self._position >= self._length:
                raise _failure(
                    DiagnosticCode.SYNTAX,
                    DiagnosticReason.UNEXPECTED_TOKEN,
                    frame.pointer,
                )
            if self._text[self._position] == "}":
                if frame.state != "key-or-end":
                    raise _failure(
                        DiagnosticCode.SYNTAX,
                        DiagnosticReason.UNEXPECTED_TOKEN,
                        frame.pointer,
                    )
                self._position += 1
                self._finish_container()
                return
            if self._text[self._position] != '"':
                raise _failure(
                    DiagnosticCode.SYNTAX,
                    DiagnosticReason.UNEXPECTED_TOKEN,
                    frame.pointer,
                )
            key = self._parse_string(frame.pointer)
            if key in frame.seen_keys:
                raise _failure(
                    DiagnosticCode.SYNTAX,
                    DiagnosticReason.DUPLICATE_KEY,
                    frame.pointer + (key,),
                )
            frame.seen_keys.add(key)
            frame.current_key = key
            frame.state = "colon"
            return

        if frame.state == "colon":
            if (
                self._position >= self._length
                or self._text[self._position] != ":"
            ):
                raise _failure(
                    DiagnosticCode.SYNTAX,
                    DiagnosticReason.UNEXPECTED_TOKEN,
                    frame.pointer + ((frame.current_key or ""),),
                )
            self._position += 1
            frame.state = "value"
            return

        if frame.state == "value":
            self._skip_whitespace()
            self._parse_value(self._value_pointer(frame))
            return

        if frame.state == "comma-or-end":
            if self._position >= self._length:
                raise _failure(
                    DiagnosticCode.SYNTAX,
                    DiagnosticReason.UNEXPECTED_TOKEN,
                    frame.pointer,
                )
            token = self._text[self._position]
            if token == ",":
                self._position += 1
                frame.state = "key"
                return
            if token == "}":
                self._position += 1
                self._finish_container()
                return
            raise _failure(
                DiagnosticCode.SYNTAX,
                DiagnosticReason.UNEXPECTED_TOKEN,
                frame.pointer,
            )
        raise RuntimeError(f"unknown object state {frame.state}")

    def _advance_array(self, frame: _Frame) -> None:
        if frame.state in {"value-or-end", "value"}:
            if self._position >= self._length:
                raise _failure(
                    DiagnosticCode.SYNTAX,
                    DiagnosticReason.UNEXPECTED_TOKEN,
                    frame.pointer,
                )
            if (
                frame.state == "value-or-end"
                and self._text[self._position] == "]"
            ):
                self._position += 1
                self._finish_container()
                return
            self._parse_value(self._value_pointer(frame))
            return

        if frame.state == "comma-or-end":
            if self._position >= self._length:
                raise _failure(
                    DiagnosticCode.SYNTAX,
                    DiagnosticReason.UNEXPECTED_TOKEN,
                    frame.pointer,
                )
            token = self._text[self._position]
            if token == ",":
                self._position += 1
                frame.state = "value"
                return
            if token == "]":
                self._position += 1
                self._finish_container()
                return
            raise _failure(
                DiagnosticCode.SYNTAX,
                DiagnosticReason.UNEXPECTED_TOKEN,
                frame.pointer,
            )
        raise RuntimeError(f"unknown array state {frame.state}")

    def _parse_value(self, pointer: tuple[JsonPointerToken, ...]) -> None:
        self._skip_whitespace()
        if self._position >= self._length:
            raise _failure(
                DiagnosticCode.SYNTAX,
                DiagnosticReason.UNEXPECTED_TOKEN,
                pointer,
            )
        token = self._text[self._position]

        if token in "[{":
            depth = 1 if not self._stack else self._stack[-1].depth + 1
            if depth > self._maximum_depth_limit:
                raise _failure(
                    DiagnosticCode.LIMIT,
                    DiagnosticReason.DEPTH_LIMIT_EXCEEDED,
                    pointer,
                )
            self._admit_record(pointer)
            self._maximum_depth_seen = max(self._maximum_depth_seen, depth)
            self._position += 1
            if token == "{":
                self._stack.append(
                    _Frame(
                        kind="object",
                        pointer=pointer,
                        depth=depth,
                        state="key-or-end",
                        builder={},
                    )
                )
            else:
                self._stack.append(
                    _Frame(
                        kind="array",
                        pointer=pointer,
                        depth=depth,
                        state="value-or-end",
                        builder=[],
                    )
                )
            return

        self._admit_record(pointer)
        if token == '"':
            value = self._parse_string(pointer)
        elif token == "t" and self._text.startswith("true", self._position):
            self._position += 4
            value = True
        elif token == "f" and self._text.startswith("false", self._position):
            self._position += 5
            value = False
        elif token == "n" and self._text.startswith("null", self._position):
            self._position += 4
            value = None
        elif token == "-" or token.isdigit():
            value = self._parse_integer(pointer)
        else:
            raise _failure(
                DiagnosticCode.SYNTAX,
                DiagnosticReason.UNEXPECTED_TOKEN,
                pointer,
            )
        self._accept_value(value)

    def _admit_record(self, pointer: tuple[JsonPointerToken, ...]) -> None:
        if self._record_count >= self._maximum_records:
            raise _failure(
                DiagnosticCode.LIMIT,
                DiagnosticReason.RECORD_LIMIT_EXCEEDED,
                pointer,
            )
        self._record_count += 1

    def _parse_string(self, pointer: tuple[JsonPointerToken, ...]) -> str:
        self._position += 1
        characters: list[str] = []
        while self._position < self._length:
            character = self._text[self._position]
            self._position += 1
            if character == '"':
                return "".join(characters)
            if ord(character) < 0x20:
                raise _failure(
                    DiagnosticCode.SYNTAX,
                    DiagnosticReason.UNEXPECTED_TOKEN,
                    pointer,
                )
            if character != "\\":
                characters.append(character)
                continue
            if self._position >= self._length:
                raise _failure(
                    DiagnosticCode.SYNTAX,
                    DiagnosticReason.INVALID_STRING_ESCAPE,
                    pointer,
                )
            escape = self._text[self._position]
            self._position += 1
            simple = {
                '"': '"',
                "\\": "\\",
                "/": "/",
                "b": "\b",
                "f": "\f",
                "n": "\n",
                "r": "\r",
                "t": "\t",
            }
            if escape in simple:
                characters.append(simple[escape])
                continue
            if escape != "u":
                raise _failure(
                    DiagnosticCode.SYNTAX,
                    DiagnosticReason.INVALID_STRING_ESCAPE,
                    pointer,
                )
            code_unit = self._parse_hex_code_unit(pointer)
            if 0xD800 <= code_unit <= 0xDBFF:
                if not self._text.startswith("\\u", self._position):
                    raise _failure(
                        DiagnosticCode.SYNTAX,
                        DiagnosticReason.UNPAIRED_SURROGATE,
                        pointer,
                    )
                self._position += 2
                low = self._parse_hex_code_unit(pointer)
                if not 0xDC00 <= low <= 0xDFFF:
                    raise _failure(
                        DiagnosticCode.SYNTAX,
                        DiagnosticReason.UNPAIRED_SURROGATE,
                        pointer,
                    )
                scalar = 0x10000 + ((code_unit - 0xD800) << 10) + (low - 0xDC00)
                characters.append(chr(scalar))
            elif 0xDC00 <= code_unit <= 0xDFFF:
                raise _failure(
                    DiagnosticCode.SYNTAX,
                    DiagnosticReason.UNPAIRED_SURROGATE,
                    pointer,
                )
            else:
                characters.append(chr(code_unit))
        raise _failure(
            DiagnosticCode.SYNTAX,
            DiagnosticReason.UNEXPECTED_TOKEN,
            pointer,
        )

    def _parse_hex_code_unit(
        self,
        pointer: tuple[JsonPointerToken, ...],
    ) -> int:
        end = self._position + 4
        if end > self._length:
            raise _failure(
                DiagnosticCode.SYNTAX,
                DiagnosticReason.INVALID_STRING_ESCAPE,
                pointer,
            )
        spelling = self._text[self._position:end]
        if any(character not in "0123456789abcdefABCDEF" for character in spelling):
            raise _failure(
                DiagnosticCode.SYNTAX,
                DiagnosticReason.INVALID_STRING_ESCAPE,
                pointer,
            )
        self._position = end
        return int(spelling, 16)

    def _parse_integer(self, pointer: tuple[JsonPointerToken, ...]) -> int:
        start = self._position
        while (
            self._position < self._length
            and self._text[self._position] not in _JSON_WHITESPACE + ",]}"
        ):
            self._position += 1
        spelling = self._text[start:self._position]
        if _CANONICAL_INTEGER.fullmatch(spelling) is None:
            raise _failure(
                DiagnosticCode.SYNTAX,
                DiagnosticReason.NONCANONICAL_INTEGER,
                pointer,
            )
        value = int(spelling)
        if value > MAX_CANONICAL_INTEGER:
            raise _failure(
                DiagnosticCode.SYNTAX,
                DiagnosticReason.INTEGER_OUT_OF_RANGE,
                pointer,
            )
        self._numeric_tokens.append(NumericToken(pointer, spelling))
        return value

    def _finish_container(self) -> None:
        frame = self._stack.pop()
        self._accept_value(frame.builder)

    def _accept_value(self, value: Any) -> None:
        if not self._stack:
            if self._root_is_set:
                raise RuntimeError("attempted to set the root twice")
            self._root = value
            self._root_is_set = True
            return
        frame = self._stack[-1]
        if frame.kind == "object":
            if frame.state != "value" or frame.current_key is None:
                raise RuntimeError("object is not ready to accept a value")
            frame.builder[frame.current_key] = value
            frame.current_key = None
            frame.state = "comma-or-end"
            return
        if frame.state not in {"value", "value-or-end"}:
            raise RuntimeError("array is not ready to accept a value")
        frame.builder.append(value)
        frame.next_index += 1
        frame.state = "comma-or-end"


def parse_bounded_json(
    source: bytes | bytearray | memoryview | BinaryIO,
    *,
    maximum_bytes: int = MAX_INPUT_BYTES,
    maximum_depth: int = MAX_JSON_DEPTH,
    maximum_records: int = MAX_INPUT_RECORDS,
) -> ParsedDocument | LoadFailure:
    try:
        raw = _read_bounded_bytes(source, maximum_bytes)
        if raw.startswith(b"\xef\xbb\xbf"):
            raise _failure(
                DiagnosticCode.SYNTAX,
                DiagnosticReason.UTF8_BOM,
            )
        try:
            text = raw.decode("utf-8", errors="strict")
        except UnicodeDecodeError:
            raise _failure(
                DiagnosticCode.SYNTAX,
                DiagnosticReason.INVALID_UTF8,
            ) from None
        parser = _Parser(
            text,
            maximum_depth=maximum_depth,
            maximum_records=maximum_records,
        )
        return parser.parse(len(raw))
    except _ParseFailure as failure:
        return LoadFailure((failure.diagnostic,), 0)
