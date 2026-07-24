from __future__ import annotations

import io
import json
import unittest
from array import array

from raw_cases import (
    CANONICAL_ZERO,
    DUPLICATE_DIRECT_KEY,
    DUPLICATE_ESCAPE_EQUIVALENT_KEY,
    EMPTY,
    EXPONENT,
    FRACTIONAL,
    INVALID_ESCAPE,
    INVALID_UTF8,
    LEADING_ZERO,
    MAXIMUM_INTEGER,
    MULTIPLE_DOCUMENTS,
    NEGATIVE_INTEGER,
    NEGATIVE_ZERO,
    OVERFLOW_INTEGER,
    TRAILING_CONTENT,
    UNPAIRED_HIGH_SURROGATE,
    UNPAIRED_LOW_SURROGATE,
    UTF8_BOM,
    VALID_SURROGATE_PAIR,
)
from support import base_document, json_bytes

from structural_spike_loader.bounded_json import (
    MAX_INPUT_BYTES,
    MAX_INPUT_RECORDS,
    NumericToken,
    ParsedDocument,
    parse_bounded_json,
)
from structural_spike_loader.diagnostics import DiagnosticCode, DiagnosticReason
from structural_spike_loader.loader import load_structural_input
from structural_spike_loader.model import LoadFailure, LoadSuccess


def assert_failure(
    testcase: unittest.TestCase,
    result: object,
    code: DiagnosticCode,
    reason: DiagnosticReason,
) -> LoadFailure:
    testcase.assertIsInstance(result, LoadFailure)
    failure = result
    assert isinstance(failure, LoadFailure)
    testcase.assertEqual(len(failure.ordered_diagnostics), 1)
    testcase.assertEqual(failure.ordered_diagnostics[0].code, code)
    testcase.assertEqual(failure.ordered_diagnostics[0].reason, reason)
    testcase.assertEqual(failure.omitted_diagnostic_count, 0)
    return failure


class TrackingReader:
    def __init__(self, payload: bytes) -> None:
        self._payload = payload
        self._position = 0
        self.requested: list[int] = []
        self.served = 0

    def read(self, count: int) -> bytes:
        self.requested.append(count)
        end = min(len(self._payload), self._position + count)
        chunk = self._payload[self._position:end]
        self._position = end
        self.served += len(chunk)
        return chunk


class BoundedJsonSyntaxTests(unittest.TestCase):
    def test_invalid_utf8_is_syntax_failure(self) -> None:
        assert_failure(
            self,
            parse_bounded_json(INVALID_UTF8),
            DiagnosticCode.SYNTAX,
            DiagnosticReason.INVALID_UTF8,
        )

    def test_utf8_bom_is_rejected(self) -> None:
        assert_failure(
            self,
            parse_bounded_json(UTF8_BOM),
            DiagnosticCode.SYNTAX,
            DiagnosticReason.UTF8_BOM,
        )

    def test_empty_input_is_rejected(self) -> None:
        assert_failure(
            self,
            parse_bounded_json(EMPTY),
            DiagnosticCode.SYNTAX,
            DiagnosticReason.EMPTY_DOCUMENT,
        )

    def test_multiple_documents_are_rejected(self) -> None:
        assert_failure(
            self,
            parse_bounded_json(MULTIPLE_DOCUMENTS),
            DiagnosticCode.SYNTAX,
            DiagnosticReason.TRAILING_CONTENT,
        )

    def test_trailing_non_whitespace_is_rejected(self) -> None:
        assert_failure(
            self,
            parse_bounded_json(TRAILING_CONTENT),
            DiagnosticCode.SYNTAX,
            DiagnosticReason.TRAILING_CONTENT,
        )

    def test_duplicate_direct_key_is_rejected(self) -> None:
        failure = assert_failure(
            self,
            parse_bounded_json(DUPLICATE_DIRECT_KEY),
            DiagnosticCode.SYNTAX,
            DiagnosticReason.DUPLICATE_KEY,
        )
        self.assertEqual(failure.ordered_diagnostics[0].pointer_text, "/name")

    def test_duplicate_escape_equivalent_key_is_rejected_after_decoding(self) -> None:
        failure = assert_failure(
            self,
            parse_bounded_json(DUPLICATE_ESCAPE_EQUIVALENT_KEY),
            DiagnosticCode.SYNTAX,
            DiagnosticReason.DUPLICATE_KEY,
        )
        self.assertEqual(failure.ordered_diagnostics[0].pointer_text, "/name")

    def test_valid_surrogate_pair_is_combined(self) -> None:
        parsed = parse_bounded_json(VALID_SURROGATE_PAIR)
        self.assertIsInstance(parsed, ParsedDocument)
        assert isinstance(parsed, ParsedDocument)
        self.assertEqual(parsed.value, "🚀")

    def test_unpaired_surrogates_are_rejected(self) -> None:
        for source in (UNPAIRED_HIGH_SURROGATE, UNPAIRED_LOW_SURROGATE):
            with self.subTest(source=source):
                assert_failure(
                    self,
                    parse_bounded_json(source),
                    DiagnosticCode.SYNTAX,
                    DiagnosticReason.UNPAIRED_SURROGATE,
                )

    def test_invalid_string_escape_is_rejected(self) -> None:
        assert_failure(
            self,
            parse_bounded_json(INVALID_ESCAPE),
            DiagnosticCode.SYNTAX,
            DiagnosticReason.INVALID_STRING_ESCAPE,
        )

    def test_valid_rfc8259_samples_match_standard_library_values(self) -> None:
        samples = (
            b"null",
            b"true",
            b"false",
            b'"text\\n\\u263a"',
            b"[]",
            b"{}",
            b'[0,1,2147483647,"x",true,false,null]',
            b'{"a":[{"b":0}],"escaped":"\\/"}',
            b" \t\r\n {\"whitespace\":0} \r\n",
        )
        for source in samples:
            with self.subTest(source=source):
                parsed = parse_bounded_json(source)
                self.assertIsInstance(parsed, ParsedDocument)
                assert isinstance(parsed, ParsedDocument)
                self.assertEqual(parsed.value, json.loads(source))

    def test_invalid_container_state_samples_are_rejected(self) -> None:
        samples = (
            b"[",
            b"{",
            b"[,]",
            b"[0,]",
            b'{"a"}',
            b'{"a":}',
            b'{"a":0,}',
            b"{0:1}",
            b'"unescaped\ncontrol"',
            b"{}\x0b",
        )
        for source in samples:
            with self.subTest(source=source):
                result = parse_bounded_json(source)
                self.assertIsInstance(result, LoadFailure)
                assert isinstance(result, LoadFailure)
                self.assertEqual(
                    result.ordered_diagnostics[0].code,
                    DiagnosticCode.SYNTAX,
                )

    def test_non_byte_source_is_rejected(self) -> None:
        assert_failure(
            self,
            parse_bounded_json(io.StringIO("{}")),  # type: ignore[arg-type]
            DiagnosticCode.SYNTAX,
            DiagnosticReason.INVALID_SOURCE_TYPE,
        )


class CanonicalIntegerTests(unittest.TestCase):
    def test_canonical_zero_retains_lexeme(self) -> None:
        parsed = parse_bounded_json(CANONICAL_ZERO)
        self.assertIsInstance(parsed, ParsedDocument)
        assert isinstance(parsed, ParsedDocument)
        self.assertEqual(parsed.value, 0)
        self.assertEqual(parsed.numeric_tokens, (NumericToken((), "0"),))

    def test_noncanonical_integer_forms_are_rejected(self) -> None:
        for source in (
            LEADING_ZERO,
            NEGATIVE_ZERO,
            NEGATIVE_INTEGER,
            FRACTIONAL,
            EXPONENT,
        ):
            with self.subTest(source=source):
                assert_failure(
                    self,
                    parse_bounded_json(source),
                    DiagnosticCode.SYNTAX,
                    DiagnosticReason.NONCANONICAL_INTEGER,
                )

    def test_exact_maximum_integer_retains_lexeme_without_binary64(self) -> None:
        parsed = parse_bounded_json(MAXIMUM_INTEGER)
        self.assertIsInstance(parsed, ParsedDocument)
        assert isinstance(parsed, ParsedDocument)
        self.assertEqual(parsed.value, 2_147_483_647)
        self.assertEqual(parsed.numeric_tokens[0].spelling, "2147483647")

    def test_integer_overflow_is_rejected(self) -> None:
        assert_failure(
            self,
            parse_bounded_json(OVERFLOW_INTEGER),
            DiagnosticCode.SYNTAX,
            DiagnosticReason.INTEGER_OUT_OF_RANGE,
        )


class ExactPreMaterializationLimitTests(unittest.TestCase):
    def test_exact_byte_limit_admits_an_otherwise_valid_fixture(self) -> None:
        encoded = json_bytes(base_document())
        source = encoded + b" " * (MAX_INPUT_BYTES - len(encoded))
        self.assertEqual(len(source), 10_485_760)
        result = load_structural_input(source)
        self.assertIsInstance(result, LoadSuccess)

    def test_next_byte_stops_after_maximum_plus_one_probe(self) -> None:
        reader = TrackingReader(b" " * (MAX_INPUT_BYTES + 8_192))
        result = parse_bounded_json(reader)
        assert_failure(
            self,
            result,
            DiagnosticCode.LIMIT,
            DiagnosticReason.BYTE_LIMIT_EXCEEDED,
        )
        self.assertEqual(reader.served, MAX_INPUT_BYTES + 1)
        self.assertLess(reader.served, len(reader._payload))
        self.assertLessEqual(max(reader.requested), 65_536)

    def test_depth_32_is_admitted(self) -> None:
        source = b"[" * 32 + b"0" + b"]" * 32
        parsed = parse_bounded_json(source)
        self.assertIsInstance(parsed, ParsedDocument)
        assert isinstance(parsed, ParsedDocument)
        self.assertEqual(parsed.maximum_depth, 32)
        self.assertEqual(parsed.record_count, 33)

    def test_depth_33_rejects_next_container(self) -> None:
        source = b"[" * 33 + b"0" + b"]" * 33
        failure = assert_failure(
            self,
            parse_bounded_json(source),
            DiagnosticCode.LIMIT,
            DiagnosticReason.DEPTH_LIMIT_EXCEEDED,
        )
        self.assertEqual(
            failure.ordered_diagnostics[0].pointer,
            tuple(0 for _ in range(32)),
        )

    def test_exact_record_limit_is_admitted_before_schema(self) -> None:
        scalar_count = MAX_INPUT_RECORDS - 1
        source = b"[" + b"0," * (scalar_count - 1) + b"0]"
        parsed = parse_bounded_json(source)
        self.assertIsInstance(parsed, ParsedDocument)
        assert isinstance(parsed, ParsedDocument)
        self.assertEqual(parsed.record_count, 1_000_000)
        self.assertEqual(len(parsed.value), 999_999)

    def test_record_one_million_and_one_is_rejected_before_admission(self) -> None:
        scalar_count = MAX_INPUT_RECORDS
        source = b"[" + b"0," * (scalar_count - 1) + b"0]"
        failure = assert_failure(
            self,
            parse_bounded_json(source),
            DiagnosticCode.LIMIT,
            DiagnosticReason.RECORD_LIMIT_EXCEEDED,
        )
        self.assertEqual(failure.ordered_diagnostics[0].pointer, (999_999,))

    def test_bytearray_memoryview_and_binary_stream_are_supported(self) -> None:
        for source in (bytearray(b"{}"), memoryview(b"{}"), io.BytesIO(b"{}")):
            with self.subTest(source_type=type(source).__name__):
                parsed = parse_bounded_json(source)
                self.assertIsInstance(parsed, ParsedDocument)

    def test_memoryview_limit_uses_byte_count_not_element_count(self) -> None:
        source = memoryview(array("I", [0, 0]))
        self.assertEqual(len(source), 2)
        self.assertEqual(source.nbytes, 8)
        assert_failure(
            self,
            parse_bounded_json(source, maximum_bytes=7),
            DiagnosticCode.LIMIT,
            DiagnosticReason.BYTE_LIMIT_EXCEEDED,
        )
