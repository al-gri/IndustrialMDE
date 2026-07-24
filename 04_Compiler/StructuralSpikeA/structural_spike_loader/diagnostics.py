from __future__ import annotations

import json
from dataclasses import dataclass
from enum import StrEnum
from typing import Iterable


class DiagnosticCode(StrEnum):
    SYNTAX = "INPUT_SYNTAX_001"
    SCHEMA = "INPUT_SCHEMA_001"
    LIMIT = "INPUT_LIMIT_001"
    INTEGRITY = "INPUT_INTEGRITY_001"


class DiagnosticReason(StrEnum):
    BYTE_LIMIT_EXCEEDED = "byte-limit-exceeded"
    INVALID_SOURCE_TYPE = "invalid-source-type"
    INVALID_UTF8 = "invalid-utf8"
    UTF8_BOM = "utf8-bom"
    EMPTY_DOCUMENT = "empty-document"
    UNEXPECTED_TOKEN = "unexpected-token"
    TRAILING_CONTENT = "trailing-content"
    DUPLICATE_KEY = "duplicate-key"
    INVALID_STRING_ESCAPE = "invalid-string-escape"
    UNPAIRED_SURROGATE = "unpaired-surrogate"
    NONCANONICAL_INTEGER = "noncanonical-integer"
    INTEGER_OUT_OF_RANGE = "integer-out-of-range"
    DEPTH_LIMIT_EXCEEDED = "depth-limit-exceeded"
    RECORD_LIMIT_EXCEEDED = "record-limit-exceeded"
    SCHEMA_REQUIRED = "schema-required"
    SCHEMA_ADDITIONAL_PROPERTIES = "schema-additional-properties"
    SCHEMA_TYPE = "schema-type"
    SCHEMA_CONST = "schema-const"
    SCHEMA_ENUM = "schema-enum"
    SCHEMA_PATTERN = "schema-pattern"
    SCHEMA_MINIMUM = "schema-minimum"
    SCHEMA_MAXIMUM = "schema-maximum"
    SCHEMA_MIN_ITEMS = "schema-min-items"
    SCHEMA_MAX_ITEMS = "schema-max-items"
    SCHEMA_UNIQUE_ITEMS = "schema-unique-items"
    SCHEMA_MIN_LENGTH = "schema-min-length"
    SCHEMA_MAX_LENGTH = "schema-max-length"
    SCHEMA_ONE_OF = "schema-one-of"
    SCHEMA_NOT = "schema-not"
    SCHEMA_VIOLATION = "schema-violation"
    PACKAGE_VERSION_COMPONENT_LIMIT = "package-version-component-limit"
    PORTABLE_PATH_INVALID = "portable-path-invalid"
    PORTABLE_PATH_CASE_COLLISION = "portable-path-case-collision"
    SOURCE_ROOT_OVERLAP = "source-root-overlap"
    DUPLICATE_PACKAGE_IDENTITY = "duplicate-package-identity"
    DEPENDENCY_CONSUMER_MISSING = "dependency-consumer-missing"
    DEPENDENCY_TARGET_MISSING = "dependency-target-missing"
    DEPENDENCY_ALIAS_DUPLICATE = "dependency-alias-duplicate"
    DEPENDENCY_TARGET_DUPLICATE = "dependency-target-duplicate"
    DEPENDENCY_SELF_REFERENCE = "dependency-self-reference"
    DEPENDENCY_UNREACHABLE = "dependency-unreachable"
    DEPENDENCY_CYCLE = "dependency-cycle"
    MODULE_IDENTITY_DUPLICATE = "module-identity-duplicate"
    MODULE_IDENTITY_CASE_COLLISION = "module-identity-case-collision"
    MODULE_PACKAGE_MISSING = "module-package-missing"
    MODULE_EDGE_ENDPOINT_MISSING = "module-edge-endpoint-missing"
    MODULE_EDGE_CROSS_PACKAGE = "module-edge-cross-package"
    MODULE_CYCLE = "module-cycle"
    COMPILATION_UNIT_DUPLICATE = "compilation-unit-duplicate"
    COMPILATION_UNIT_MODULE_MISSING = "compilation-unit-module-missing"
    SOURCE_IDENTITY_DUPLICATE = "source-identity-duplicate"
    LANGUAGE_VERSION_MISMATCH = "language-version-mismatch"
    SOURCE_ORIGIN_IDENTITY_MISMATCH = "source-origin-identity-mismatch"
    SOURCE_ORIGIN_RANGE_INVALID = "source-origin-range-invalid"
    TOO_MANY_DIRECT_ORIGINS = "too-many-direct-origins"
    MARKER_SPAN_LIMIT_EXCEEDED = "marker-span-limit-exceeded"
    MARKER_RANGE_INVALID = "marker-range-invalid"
    MARKER_RFC_MISMATCH = "marker-rfc-mismatch"
    MARKER_OWNER_MISMATCH = "marker-owner-mismatch"
    FORBIDDEN_PHASE_FIELD = "forbidden-phase-field"


JsonPointerToken = str | int


def encode_json_pointer(tokens: tuple[JsonPointerToken, ...]) -> str:
    if not tokens:
        return ""
    encoded = []
    for token in tokens:
        text = str(token).replace("~", "~0").replace("/", "~1")
        encoded.append(text)
    return "/" + "/".join(encoded)


def escape_untrusted(value: str, maximum_characters: int = 256) -> str:
    bounded = value[:maximum_characters]
    escaped = json.dumps(bounded, ensure_ascii=True)[1:-1]
    if len(value) > maximum_characters:
        escaped += "\\u2026"
    return escaped


@dataclass(frozen=True, slots=True)
class InputDiagnostic:
    code: DiagnosticCode
    reason: DiagnosticReason
    pointer: tuple[JsonPointerToken, ...] = ()
    detail: str | None = None

    @property
    def pointer_text(self) -> str:
        return encode_json_pointer(self.pointer)

    def sort_key(self) -> tuple[bytes, str, str]:
        return (
            self.pointer_text.encode("utf-8"),
            self.code.value,
            self.reason.value,
        )


def bound_diagnostics(
    diagnostics: Iterable[InputDiagnostic],
    cap: int,
) -> tuple[tuple[InputDiagnostic, ...], int]:
    ordered = sorted(diagnostics, key=InputDiagnostic.sort_key)
    retained = tuple(ordered[:cap])
    return retained, max(0, len(ordered) - len(retained))


def render_diagnostic(diagnostic: InputDiagnostic) -> str:
    base = (
        f"{diagnostic.code.value} {diagnostic.reason.value} "
        f"{diagnostic.pointer_text or '/'}"
    )
    if diagnostic.detail is None:
        return base
    return f'{base} detail="{escape_untrusted(diagnostic.detail)}"'
