from __future__ import annotations

from typing import BinaryIO

from .bounded_json import ParsedDocument, parse_bounded_json
from .diagnostics import bound_diagnostics
from .integrity import validate_integrity, validate_marker_limits
from .model import (
    CollectedStructuralInputFixture,
    FrozenRecord,
    LoadFailure,
    LoadResult,
    LoadSuccess,
    ResolvedCompilationUnitFixture,
    ResolvedProjectContextFixture,
    deep_freeze,
)
from .normalization import normalize_input
from .schema_validation import effective_diagnostic_cap, schema_diagnostics


def _failed(diagnostics: list, cap: int) -> LoadFailure:
    retained, omitted = bound_diagnostics(diagnostics, cap)
    return LoadFailure(retained, omitted)


def load_structural_input(
    source: bytes | bytearray | memoryview | BinaryIO,
) -> LoadResult:
    parsed = parse_bounded_json(source)
    if isinstance(parsed, LoadFailure):
        return parsed
    if not isinstance(parsed, ParsedDocument):
        raise RuntimeError("bounded parser returned an unknown result")

    instance = parsed.value
    cap = effective_diagnostic_cap(instance)
    schema_errors = schema_diagnostics(instance)
    if schema_errors:
        return _failed(schema_errors, cap)

    if not isinstance(instance, dict):
        raise RuntimeError("schema-valid top-level input is not an object")

    marker_limit_errors = validate_marker_limits(instance)
    if marker_limit_errors:
        return _failed(marker_limit_errors, cap)

    integrity_errors = validate_integrity(instance)
    if integrity_errors:
        return _failed(integrity_errors, cap)

    normalized = normalize_input(instance)
    identifier = normalized["schema"]
    project_context = deep_freeze(normalized["project_context"])
    selector_request = deep_freeze(normalized["selector_request"])
    if not isinstance(project_context, FrozenRecord):
        raise RuntimeError("project context did not freeze as a record")
    if not isinstance(selector_request, FrozenRecord):
        raise RuntimeError("selector request did not freeze as a record")

    ownership_units: list[ResolvedCompilationUnitFixture] = []
    collected_units: list[FrozenRecord] = []
    for unit in normalized["compilation_units"]:
        frozen_identity = deep_freeze(unit["unit_identity"])
        frozen_unit = deep_freeze(unit)
        if not isinstance(frozen_identity, FrozenRecord):
            raise RuntimeError("unit identity did not freeze as a record")
        if not isinstance(frozen_unit, FrozenRecord):
            raise RuntimeError("compilation unit did not freeze as a record")
        ownership_units.append(
            ResolvedCompilationUnitFixture(
                unit_identity=frozen_identity,
                source_identity_components=tuple(unit["source_identity_components"]),
                source_length_bytes=unit["source_length_bytes"],
            )
        )
        collected_units.append(frozen_unit)

    return LoadSuccess(
        resolved_project_context=ResolvedProjectContextFixture(
            input_contract_identifier=identifier,
            project_context=project_context,
            compilation_units=tuple(ownership_units),
        ),
        collected_structural_input=CollectedStructuralInputFixture(
            input_contract_identifier=identifier,
            selector_request=selector_request,
            compilation_units=tuple(collected_units),
        ),
    )
