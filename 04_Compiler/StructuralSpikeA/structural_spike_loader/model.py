from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterator

from .diagnostics import InputDiagnostic


@dataclass(frozen=True, slots=True)
class FrozenRecord:
    fields: tuple[tuple[str, Any], ...]

    def __getitem__(self, key: str) -> Any:
        for candidate, value in self.fields:
            if candidate == key:
                return value
        raise KeyError(key)

    def get(self, key: str, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def __iter__(self) -> Iterator[str]:
        return (key for key, _ in self.fields)

    def items(self) -> tuple[tuple[str, Any], ...]:
        return self.fields


def deep_freeze(value: Any) -> Any:
    if isinstance(value, dict):
        fields = tuple(
            (key, deep_freeze(child))
            for key, child in sorted(
                value.items(),
                key=lambda item: item[0].encode("utf-8"),
            )
        )
        return FrozenRecord(fields)
    if isinstance(value, list):
        return tuple(deep_freeze(child) for child in value)
    if value is None or isinstance(value, (bool, int, str)):
        return value
    raise TypeError(f"unsupported published value type: {type(value).__name__}")


@dataclass(frozen=True, slots=True)
class ResolvedCompilationUnitFixture:
    unit_identity: FrozenRecord
    source_identity_components: tuple[str, ...]
    source_length_bytes: int


@dataclass(frozen=True, slots=True)
class ResolvedProjectContextFixture:
    input_contract_identifier: str
    project_context: FrozenRecord
    compilation_units: tuple[ResolvedCompilationUnitFixture, ...]


@dataclass(frozen=True, slots=True)
class CollectedStructuralInputFixture:
    input_contract_identifier: str
    selector_request: FrozenRecord
    compilation_units: tuple[FrozenRecord, ...]


@dataclass(frozen=True, slots=True)
class LoadSuccess:
    resolved_project_context: ResolvedProjectContextFixture
    collected_structural_input: CollectedStructuralInputFixture


@dataclass(frozen=True, slots=True)
class LoadFailure:
    ordered_diagnostics: tuple[InputDiagnostic, ...]
    omitted_diagnostic_count: int


LoadResult = LoadSuccess | LoadFailure
