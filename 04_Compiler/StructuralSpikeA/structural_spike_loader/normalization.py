from __future__ import annotations

import copy
import json
from typing import Any


_ORIGIN_KIND_RANK = {
    "source": 0,
    "project-manifest": 1,
    "fixture-metadata": 2,
    "build-metadata": 3,
    "invocation": 4,
}
_DECLARATION_KIND_RANK = {
    "definition": 0,
    "application-assembly": 1,
    "unsupported-marker": 2,
}


def _text(value: str) -> bytes:
    return value.encode("utf-8")


def _record_tiebreaker(value: Any) -> bytes:
    """Order unequal records that share a reviewed semantic collection key."""
    return json.dumps(
        value,
        ensure_ascii=True,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("ascii")


def package_identity_key(identity: dict[str, Any]) -> tuple[Any, ...]:
    authority_labels = tuple(_text(label) for label in identity["authority"].split("."))
    return authority_labels, _text(identity["name"])


def package_revision_key(revision: dict[str, Any]) -> tuple[Any, ...]:
    content = revision["content_identity"]
    version = tuple(int(component) for component in revision["version"].split("."))
    return (
        package_identity_key(revision["package_identity"]),
        version,
        _text(content["kind"]),
        _text(content["digest_algorithm"]),
        _text(content["digest"]),
    )


def module_identity_key(identity: dict[str, Any]) -> tuple[Any, ...]:
    return (
        package_identity_key(identity["package_identity"]),
        _text(identity["module_name"]),
    )


def origin_key(origin: dict[str, Any] | None) -> tuple[Any, ...]:
    if origin is None:
        return 5, (), 0, 0
    kind = origin["kind"]
    rank = _ORIGIN_KIND_RANK[kind]
    if kind == "source":
        identity = tuple(_text(component) for component in origin["source_identity_components"])
        return rank, identity, origin["raw_start"], origin["raw_end"]
    return rank, (_text(origin["identity"]),), 0, 0


def _selector_component(value: Any, key_function: Any = None) -> tuple[int, Any]:
    if value is None:
        return 1, ()
    if key_function is not None:
        return 0, key_function(value)
    if isinstance(value, list):
        return 0, tuple(_text(component) for component in value)
    return 0, _text(value)


def selector_candidate_key(candidate: dict[str, Any]) -> tuple[Any, ...]:
    target = candidate.get("target")
    if target is None:
        completeness_rank = 2
        target = {}
    else:
        complete = all(
            field in target
            for field in (
                "package_identity",
                "namespace_path",
                "owner_path",
                "identifier",
            )
        )
        completeness_rank = 0 if complete else 1
    return (
        completeness_rank,
        _selector_component(target.get("package_identity"), package_identity_key),
        _selector_component(target.get("namespace_path")),
        _selector_component(target.get("owner_path")),
        _selector_component(target.get("identifier")),
        origin_key(candidate["origin"]),
        _text(candidate["raw_spelling"]),
    )


def import_key(import_record: dict[str, Any]) -> tuple[Any, ...]:
    return (
        tuple(_text(segment) for segment in import_record["target_reference"]["segments"]),
        _text(import_record["alias"] or ""),
        origin_key(import_record["origin"]),
    )


def declaration_key(declaration: dict[str, Any]) -> tuple[Any, ...]:
    return (
        _DECLARATION_KIND_RANK[declaration["kind"]],
        _text(declaration.get("name", "")),
        origin_key(declaration["origin"]),
    )


def compilation_unit_key(unit: dict[str, Any]) -> tuple[Any, ...]:
    identity = unit["unit_identity"]
    return (
        package_identity_key(identity["package_identity"]),
        _text(identity["module_name"]),
        _text(identity["portable_package_path"]),
    )


def normalize_input(instance: dict[str, Any]) -> dict[str, Any]:
    normalized = copy.deepcopy(instance)
    project = normalized["project_context"]

    project["dependency_package_revisions"].sort(
        key=lambda revision: (
            package_revision_key(revision),
            _record_tiebreaker(revision),
        )
    )
    project["dependency_edges"].sort(
        key=lambda edge: (
            package_identity_key(edge["consumer"]),
            _text(edge["alias"]),
            package_identity_key(edge["dependency"]),
            _record_tiebreaker(edge),
        )
    )
    for module in project["modules"]:
        module["source_roots"].sort(key=_text)
    project["modules"].sort(
        key=lambda module: (
            module_identity_key(module["identity"]),
            _record_tiebreaker(module),
        )
    )
    project["module_edges"].sort(
        key=lambda edge: (
            module_identity_key(edge["consumer"]),
            module_identity_key(edge["dependency"]),
            _record_tiebreaker(edge),
        )
    )

    normalized["selector_request"]["candidates"].sort(
        key=lambda candidate: (
            selector_candidate_key(candidate),
            _record_tiebreaker(candidate),
        )
    )
    for unit in normalized["compilation_units"]:
        unit["imports"].sort(
            key=lambda import_record: (
                import_key(import_record),
                _record_tiebreaker(import_record),
            )
        )
        unit["declarations"].sort(
            key=lambda declaration: (
                declaration_key(declaration),
                _record_tiebreaker(declaration),
            )
        )
    normalized["compilation_units"].sort(
        key=lambda unit: (
            compilation_unit_key(unit),
            _record_tiebreaker(unit),
        )
    )
    return normalized
