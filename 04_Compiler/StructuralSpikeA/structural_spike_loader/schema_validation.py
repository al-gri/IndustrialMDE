from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from .diagnostics import (
    DiagnosticCode,
    DiagnosticReason,
    InputDiagnostic,
)


FIXED_DIAGNOSTIC_CEILING = 4_096
_SCHEMA_PATH = (
    Path(__file__).resolve().parent.parent
    / "schema"
    / "experimental-structural-input-0.schema.json"
)


def _load_schema() -> dict[str, Any]:
    schema = json.loads(_SCHEMA_PATH.read_text(encoding="utf-8"))
    if len(schema.get("$defs", {})) != 38:
        raise RuntimeError("executable structural-input schema must contain 38 $defs")
    stack: list[Any] = [schema]
    while stack:
        node = stack.pop()
        if isinstance(node, dict):
            reference = node.get("$ref")
            if reference is not None and not reference.startswith("#/$defs/"):
                raise RuntimeError("executable schema contains a non-internal reference")
            stack.extend(node.values())
        elif isinstance(node, list):
            stack.extend(node)
    Draft202012Validator.check_schema(schema)
    return schema


_SCHEMA = _load_schema()
_VALIDATOR = Draft202012Validator(_SCHEMA)


_REASON_BY_VALIDATOR = {
    "required": DiagnosticReason.SCHEMA_REQUIRED,
    "additionalProperties": DiagnosticReason.SCHEMA_ADDITIONAL_PROPERTIES,
    "type": DiagnosticReason.SCHEMA_TYPE,
    "const": DiagnosticReason.SCHEMA_CONST,
    "enum": DiagnosticReason.SCHEMA_ENUM,
    "pattern": DiagnosticReason.SCHEMA_PATTERN,
    "minimum": DiagnosticReason.SCHEMA_MINIMUM,
    "maximum": DiagnosticReason.SCHEMA_MAXIMUM,
    "minItems": DiagnosticReason.SCHEMA_MIN_ITEMS,
    "maxItems": DiagnosticReason.SCHEMA_MAX_ITEMS,
    "uniqueItems": DiagnosticReason.SCHEMA_UNIQUE_ITEMS,
    "minLength": DiagnosticReason.SCHEMA_MIN_LENGTH,
    "maxLength": DiagnosticReason.SCHEMA_MAX_LENGTH,
    "oneOf": DiagnosticReason.SCHEMA_ONE_OF,
    "not": DiagnosticReason.SCHEMA_NOT,
}


def executable_schema() -> dict[str, Any]:
    return copy.deepcopy(_SCHEMA)


def executable_schema_path() -> Path:
    return _SCHEMA_PATH


def schema_diagnostics(instance: Any) -> list[InputDiagnostic]:
    diagnostics: list[InputDiagnostic] = []
    for error in _VALIDATOR.iter_errors(instance):
        reason = _REASON_BY_VALIDATOR.get(
            str(error.validator),
            DiagnosticReason.SCHEMA_VIOLATION,
        )
        diagnostics.append(
            InputDiagnostic(
                code=DiagnosticCode.SCHEMA,
                reason=reason,
                pointer=tuple(error.absolute_path),
            )
        )
    return diagnostics


def effective_diagnostic_cap(instance: Any) -> int:
    if not isinstance(instance, dict):
        return FIXED_DIAGNOSTIC_CEILING
    project_context = instance.get("project_context")
    if not isinstance(project_context, dict):
        return FIXED_DIAGNOSTIC_CEILING
    active_limits = project_context.get("active_limits")
    if not isinstance(active_limits, dict):
        return FIXED_DIAGNOSTIC_CEILING
    candidate = active_limits.get("maximum_diagnostics")
    if (
        type(candidate) is int
        and 1 <= candidate <= 1_000_000
    ):
        return min(candidate, FIXED_DIAGNOSTIC_CEILING)
    return FIXED_DIAGNOSTIC_CEILING
