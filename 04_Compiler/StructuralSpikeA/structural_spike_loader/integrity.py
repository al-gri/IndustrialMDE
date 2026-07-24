from __future__ import annotations

import re
from collections import defaultdict, deque
from typing import Any, Iterable

from .diagnostics import (
    DiagnosticCode,
    DiagnosticReason,
    InputDiagnostic,
    JsonPointerToken,
)


MAX_VERSION_COMPONENT = 2_147_483_647
MAX_DIRECT_SOURCE_ORIGINS = 3
MAX_MARKER_PAYLOAD_SPAN = 1_048_576
_PATH_SEGMENT = re.compile(r"[A-Za-z0-9_](?:[A-Za-z0-9._-]*[A-Za-z0-9_])?\Z")
_RESERVED_DEVICE_STEMS = {
    "CON",
    "PRN",
    "AUX",
    "NUL",
    *(f"COM{number}" for number in range(1, 10)),
    *(f"LPT{number}" for number in range(1, 10)),
}
_CATEGORY_RFC = {
    "expression": "RFC-0003",
    "constant": "RFC-0003",
    "parameter": "RFC-0003",
    "configuration-expression": "RFC-0003",
    "state": "RFC-0004",
    "behavior": "RFC-0004",
    "interface": "RFC-0006",
    "replication": "RFC-0006",
    "deployment": "RFC-0007",
    "target": "RFC-0007",
    "deployment-mapping": "RFC-0007",
}
_REFERENCE_FIELDS = {
    "target_reference",
    "definition_reference",
    "type_reference",
    "source_reference",
    "destination_reference",
}
_FORBIDDEN_PHASE_FIELDS = {
    "resolved_identity",
    "declaration_identity",
    "type_identity",
    "selected_assembly",
    "structural_validation_closure",
    "expansion_closure",
    "occurrence_identity",
    "expanded_node",
    "expanded_graph",
    "expression_payload",
    "runtime_fact",
    "snapshot",
    "snapshot_provenance",
    "provenance",
}


def _diagnostic(
    reason: DiagnosticReason,
    pointer: tuple[JsonPointerToken, ...],
    *,
    code: DiagnosticCode = DiagnosticCode.INTEGRITY,
) -> InputDiagnostic:
    return InputDiagnostic(code=code, reason=reason, pointer=pointer)


def _package_identity(identity: dict[str, Any]) -> tuple[str, str]:
    return identity["authority"], identity["name"]


def _module_identity(
    identity: dict[str, Any],
) -> tuple[tuple[str, str], str]:
    return _package_identity(identity["package_identity"]), identity["module_name"]


def _unit_identity(
    identity: dict[str, Any],
) -> tuple[tuple[str, str], str, str]:
    return (
        _package_identity(identity["package_identity"]),
        identity["module_name"],
        identity["portable_package_path"],
    )


def _portable_path_is_valid(path: str) -> bool:
    if (
        not path
        or path.startswith("/")
        or path.endswith("/")
        or "\\" in path
        or "\x00" in path
        or "://" in path
    ):
        return False
    segments = path.split("/")
    for segment in segments:
        if (
            segment in {".", ".."}
            or _PATH_SEGMENT.fullmatch(segment) is None
            or segment.split(".", 1)[0].upper() in _RESERVED_DEVICE_STEMS
        ):
            return False
    return True


def _has_cycle(
    nodes: Iterable[Any],
    adjacency: dict[Any, set[Any]],
) -> bool:
    node_set = set(nodes)
    indegree = {node: 0 for node in node_set}
    for consumer, dependencies in adjacency.items():
        if consumer not in node_set:
            continue
        for dependency in dependencies:
            if dependency in node_set:
                indegree[dependency] += 1
    ready = deque(sorted((node for node, degree in indegree.items() if degree == 0)))
    visited = 0
    while ready:
        node = ready.popleft()
        visited += 1
        for dependency in sorted(adjacency.get(node, ())):
            if dependency not in indegree:
                continue
            indegree[dependency] -= 1
            if indegree[dependency] == 0:
                ready.append(dependency)
    return visited != len(node_set)


def _iter_markers(
    instance: dict[str, Any],
) -> Iterable[
    tuple[
        dict[str, Any],
        tuple[JsonPointerToken, ...],
        dict[str, Any],
        dict[str, Any],
    ]
]:
    for unit_index, unit in enumerate(instance["compilation_units"]):
        unit_pointer: tuple[JsonPointerToken, ...] = ("compilation_units", unit_index)
        for declaration_index, declaration in enumerate(unit["declarations"]):
            declaration_pointer = unit_pointer + ("declarations", declaration_index)
            kind = declaration["kind"]
            if kind == "unsupported-marker":
                expected_owner = {"kind": "compilation-unit", "identifier": None}
                yield declaration, declaration_pointer, unit, expected_owner
                continue
            if kind not in {"definition", "application-assembly"}:
                continue
            expected_owner = {"kind": kind, "identifier": declaration["name"]}
            for member_index, member in enumerate(declaration["members"]):
                if member["kind"] == "unsupported-marker":
                    yield (
                        member,
                        declaration_pointer + ("members", member_index),
                        unit,
                        expected_owner,
                    )


def validate_marker_limits(instance: dict[str, Any]) -> list[InputDiagnostic]:
    diagnostics: list[InputDiagnostic] = []
    for marker, pointer, _, _ in _iter_markers(instance):
        payload = marker["opaque_payload_range"]
        span = payload["raw_end"] - payload["raw_start"]
        if span > MAX_MARKER_PAYLOAD_SPAN:
            diagnostics.append(
                _diagnostic(
                    DiagnosticReason.MARKER_SPAN_LIMIT_EXCEEDED,
                    pointer + ("opaque_payload_range",),
                    code=DiagnosticCode.LIMIT,
                )
            )
    return diagnostics


def validate_integrity(instance: dict[str, Any]) -> list[InputDiagnostic]:
    diagnostics: list[InputDiagnostic] = []
    project = instance["project_context"]

    revisions: list[tuple[dict[str, Any], tuple[JsonPointerToken, ...]]] = [
        (
            project["root_package_revision"],
            ("project_context", "root_package_revision"),
        )
    ]
    revisions.extend(
        (
            revision,
            ("project_context", "dependency_package_revisions", index),
        )
        for index, revision in enumerate(project["dependency_package_revisions"])
    )
    for revision, pointer in revisions:
        components = revision["version"].split(".")
        if any(int(component) > MAX_VERSION_COMPONENT for component in components):
            diagnostics.append(
                _diagnostic(
                    DiagnosticReason.PACKAGE_VERSION_COMPONENT_LIMIT,
                    pointer + ("version",),
                )
            )

    root_identity = _package_identity(project["root_package_revision"]["package_identity"])
    dependency_identities: set[tuple[str, str]] = set()
    participating: set[tuple[str, str]] = set()
    revision_pointers: dict[tuple[str, str], tuple[JsonPointerToken, ...]] = {}
    for revision, pointer in revisions:
        identity = _package_identity(revision["package_identity"])
        if identity in participating:
            diagnostics.append(
                _diagnostic(
                    DiagnosticReason.DUPLICATE_PACKAGE_IDENTITY,
                    pointer + ("package_identity",),
                )
            )
        else:
            participating.add(identity)
            revision_pointers[identity] = pointer
        if pointer[1] == "dependency_package_revisions":
            dependency_identities.add(identity)

    dependency_adjacency: dict[tuple[str, str], set[tuple[str, str]]] = defaultdict(set)
    aliases: dict[tuple[str, str], set[str]] = defaultdict(set)
    folded_aliases: dict[tuple[str, str], set[str]] = defaultdict(set)
    aliased_targets: dict[
        tuple[str, str],
        dict[tuple[str, str], str],
    ] = defaultdict(dict)
    for edge_index, edge in enumerate(project["dependency_edges"]):
        pointer = ("project_context", "dependency_edges", edge_index)
        consumer = _package_identity(edge["consumer"])
        dependency = _package_identity(edge["dependency"])
        if consumer not in participating:
            diagnostics.append(
                _diagnostic(
                    DiagnosticReason.DEPENDENCY_CONSUMER_MISSING,
                    pointer + ("consumer",),
                )
            )
        if dependency not in dependency_identities:
            diagnostics.append(
                _diagnostic(
                    DiagnosticReason.DEPENDENCY_TARGET_MISSING,
                    pointer + ("dependency",),
                )
            )
        alias = edge["alias"]
        folded_alias = alias.lower()
        if (
            alias in aliases[consumer]
            or folded_alias in folded_aliases[consumer]
        ):
            diagnostics.append(
                _diagnostic(
                    DiagnosticReason.DEPENDENCY_ALIAS_DUPLICATE,
                    pointer + ("alias",),
                )
            )
        aliases[consumer].add(alias)
        folded_aliases[consumer].add(folded_alias)
        earlier_alias = aliased_targets[consumer].get(dependency)
        if earlier_alias is not None and earlier_alias != alias:
            diagnostics.append(
                _diagnostic(
                    DiagnosticReason.DEPENDENCY_TARGET_DUPLICATE,
                    pointer + ("dependency",),
                )
            )
        else:
            aliased_targets[consumer][dependency] = alias
        if consumer == dependency:
            diagnostics.append(
                _diagnostic(
                    DiagnosticReason.DEPENDENCY_SELF_REFERENCE,
                    pointer,
                )
            )
        if consumer in participating and dependency in participating:
            dependency_adjacency[consumer].add(dependency)

    reachable = {root_identity}
    worklist = [root_identity]
    while worklist:
        consumer = worklist.pop()
        for dependency in sorted(dependency_adjacency.get(consumer, ())):
            if dependency not in reachable:
                reachable.add(dependency)
                worklist.append(dependency)
    for dependency in sorted(dependency_identities):
        if dependency not in reachable:
            diagnostics.append(
                _diagnostic(
                    DiagnosticReason.DEPENDENCY_UNREACHABLE,
                    revision_pointers[dependency] + ("package_identity",),
                )
            )
    if _has_cycle(participating, dependency_adjacency):
        diagnostics.append(
            _diagnostic(
                DiagnosticReason.DEPENDENCY_CYCLE,
                ("project_context", "dependency_edges"),
            )
        )

    modules: dict[tuple[tuple[str, str], str], tuple[JsonPointerToken, ...]] = {}
    folded_module_names: dict[tuple[str, str], set[str]] = defaultdict(set)
    source_roots: dict[
        tuple[str, str],
        list[tuple[str, tuple[JsonPointerToken, ...]]],
    ] = defaultdict(list)
    for module_index, module in enumerate(project["modules"]):
        pointer = ("project_context", "modules", module_index)
        identity = _module_identity(module["identity"])
        exact_duplicate = identity in modules
        if exact_duplicate:
            diagnostics.append(
                _diagnostic(
                    DiagnosticReason.MODULE_IDENTITY_DUPLICATE,
                    pointer + ("identity",),
                )
            )
        else:
            modules[identity] = pointer
        package = identity[0]
        folded_module_name = identity[1].lower()
        if (
            folded_module_name in folded_module_names[package]
            and not exact_duplicate
        ):
            diagnostics.append(
                _diagnostic(
                    DiagnosticReason.MODULE_IDENTITY_CASE_COLLISION,
                    pointer + ("identity",),
                )
            )
        folded_module_names[package].add(folded_module_name)
        if package not in participating:
            diagnostics.append(
                _diagnostic(
                    DiagnosticReason.MODULE_PACKAGE_MISSING,
                    pointer + ("identity", "package_identity"),
                )
            )
        for root_index, path in enumerate(module["source_roots"]):
            path_pointer = pointer + ("source_roots", root_index)
            if not _portable_path_is_valid(path):
                diagnostics.append(
                    _diagnostic(
                        DiagnosticReason.PORTABLE_PATH_INVALID,
                        path_pointer,
                    )
                )
            source_roots[package].append((path, path_pointer))

    for roots in source_roots.values():
        for index, (path, pointer) in enumerate(roots):
            folded = path.lower()
            for earlier_path, earlier_pointer in roots[:index]:
                earlier_folded = earlier_path.lower()
                if folded == earlier_folded and path != earlier_path:
                    diagnostics.append(
                        _diagnostic(
                            DiagnosticReason.PORTABLE_PATH_CASE_COLLISION,
                            pointer,
                        )
                    )
                earlier_prefix = earlier_folded.rstrip("/") + "/"
                current_prefix = folded.rstrip("/") + "/"
                if (
                    folded == earlier_folded
                    or folded.startswith(earlier_prefix)
                    or earlier_folded.startswith(current_prefix)
                ):
                    diagnostics.append(
                        _diagnostic(
                            DiagnosticReason.SOURCE_ROOT_OVERLAP,
                            pointer,
                        )
                    )

    module_adjacency: dict[
        tuple[tuple[str, str], str],
        set[tuple[tuple[str, str], str]],
    ] = defaultdict(set)
    for edge_index, edge in enumerate(project["module_edges"]):
        pointer = ("project_context", "module_edges", edge_index)
        consumer = _module_identity(edge["consumer"])
        dependency = _module_identity(edge["dependency"])
        if consumer not in modules or dependency not in modules:
            diagnostics.append(
                _diagnostic(
                    DiagnosticReason.MODULE_EDGE_ENDPOINT_MISSING,
                    pointer,
                )
            )
            continue
        if consumer[0] != dependency[0]:
            diagnostics.append(
                _diagnostic(
                    DiagnosticReason.MODULE_EDGE_CROSS_PACKAGE,
                    pointer,
                )
            )
            continue
        module_adjacency[consumer].add(dependency)
    modules_by_package: dict[
        tuple[str, str],
        set[tuple[tuple[str, str], str]],
    ] = defaultdict(set)
    for identity in modules:
        modules_by_package[identity[0]].add(identity)
    for package, package_modules in modules_by_package.items():
        if _has_cycle(package_modules, module_adjacency):
            diagnostics.append(
                _diagnostic(
                    DiagnosticReason.MODULE_CYCLE,
                    ("project_context", "module_edges"),
                )
            )

    unit_identities: set[tuple[tuple[str, str], str, str]] = set()
    source_identities: set[tuple[str, ...]] = set()
    unit_paths_by_package: dict[
        tuple[str, str],
        list[tuple[str, tuple[JsonPointerToken, ...]]],
    ] = defaultdict(list)
    for unit_index, unit in enumerate(instance["compilation_units"]):
        pointer = ("compilation_units", unit_index)
        identity = _unit_identity(unit["unit_identity"])
        if identity in unit_identities:
            diagnostics.append(
                _diagnostic(
                    DiagnosticReason.COMPILATION_UNIT_DUPLICATE,
                    pointer + ("unit_identity",),
                )
            )
        unit_identities.add(identity)
        expected_module = (identity[0], identity[1])
        if expected_module not in modules:
            diagnostics.append(
                _diagnostic(
                    DiagnosticReason.COMPILATION_UNIT_MODULE_MISSING,
                    pointer + ("unit_identity",),
                )
            )
        path = identity[2]
        path_pointer = pointer + ("unit_identity", "portable_package_path")
        if not _portable_path_is_valid(path):
            diagnostics.append(
                _diagnostic(
                    DiagnosticReason.PORTABLE_PATH_INVALID,
                    path_pointer,
                )
            )
        unit_paths_by_package[identity[0]].append((path, path_pointer))

        source_identity = tuple(unit["source_identity_components"])
        if source_identity in source_identities:
            diagnostics.append(
                _diagnostic(
                    DiagnosticReason.SOURCE_IDENTITY_DUPLICATE,
                    pointer + ("source_identity_components",),
                )
            )
        source_identities.add(source_identity)
        if unit["language_version"] != project["language_version"]:
            diagnostics.append(
                _diagnostic(
                    DiagnosticReason.LANGUAGE_VERSION_MISMATCH,
                    pointer + ("language_version",),
                )
            )
        diagnostics.extend(
            _validate_unit_origins(
                unit,
                pointer,
                source_identity,
                unit["source_length_bytes"],
            )
        )

    for paths in unit_paths_by_package.values():
        folded_seen: dict[str, str] = {}
        for path, pointer in paths:
            folded = path.lower()
            earlier = folded_seen.get(folded)
            if earlier is not None and earlier != path:
                diagnostics.append(
                    _diagnostic(
                        DiagnosticReason.PORTABLE_PATH_CASE_COLLISION,
                        pointer,
                    )
                )
            else:
                folded_seen[folded] = path

    for marker, pointer, unit, expected_owner in _iter_markers(instance):
        diagnostics.extend(
            _validate_marker(marker, pointer, unit, expected_owner)
        )

    stack: list[tuple[Any, tuple[JsonPointerToken, ...]]] = [(instance, ())]
    while stack:
        node, pointer = stack.pop()
        if isinstance(node, dict):
            for key, value in node.items():
                child_pointer = pointer + (key,)
                if key in _FORBIDDEN_PHASE_FIELDS:
                    diagnostics.append(
                        _diagnostic(
                            DiagnosticReason.FORBIDDEN_PHASE_FIELD,
                            child_pointer,
                        )
                    )
                stack.append((value, child_pointer))
        elif isinstance(node, list):
            stack.extend(
                (value, pointer + (index,))
                for index, value in enumerate(node)
            )
    return diagnostics


def _validate_unit_origins(
    unit: dict[str, Any],
    unit_pointer: tuple[JsonPointerToken, ...],
    source_identity: tuple[str, ...],
    source_length: int,
) -> list[InputDiagnostic]:
    diagnostics: list[InputDiagnostic] = []
    stack: list[tuple[Any, tuple[JsonPointerToken, ...]]] = [(unit, unit_pointer)]
    while stack:
        node, pointer = stack.pop()
        if isinstance(node, dict):
            if node.get("kind") == "source":
                if tuple(node["source_identity_components"]) != source_identity:
                    diagnostics.append(
                        _diagnostic(
                            DiagnosticReason.SOURCE_ORIGIN_IDENTITY_MISMATCH,
                            pointer + ("source_identity_components",),
                        )
                    )
                if not (
                    0
                    <= node["raw_start"]
                    <= node["raw_end"]
                    <= source_length
                ):
                    diagnostics.append(
                        _diagnostic(
                            DiagnosticReason.SOURCE_ORIGIN_RANGE_INVALID,
                            pointer,
                        )
                    )
                continue
            direct_origins = 0
            origin = node.get("origin")
            if isinstance(origin, dict) and origin.get("kind") == "source":
                direct_origins += 1
            language_origin = node.get("language_version_origin")
            if (
                isinstance(language_origin, dict)
                and language_origin.get("kind") == "source"
            ):
                direct_origins += 1
            for key in _REFERENCE_FIELDS:
                reference = node.get(key)
                if (
                    isinstance(reference, dict)
                    and isinstance(reference.get("origin"), dict)
                    and reference["origin"].get("kind") == "source"
                ):
                    direct_origins += 1
            if direct_origins > MAX_DIRECT_SOURCE_ORIGINS:
                diagnostics.append(
                    _diagnostic(
                        DiagnosticReason.TOO_MANY_DIRECT_ORIGINS,
                        pointer,
                    )
                )
            stack.extend(
                (value, pointer + (key,))
                for key, value in node.items()
            )
        elif isinstance(node, list):
            stack.extend(
                (value, pointer + (index,))
                for index, value in enumerate(node)
            )
    return diagnostics


def _validate_marker(
    marker: dict[str, Any],
    pointer: tuple[JsonPointerToken, ...],
    unit: dict[str, Any],
    expected_owner: dict[str, Any],
) -> list[InputDiagnostic]:
    diagnostics: list[InputDiagnostic] = []
    expected_rfc = _CATEGORY_RFC[marker["category"]]
    if marker["owning_future_rfc"] != expected_rfc:
        diagnostics.append(
            _diagnostic(
                DiagnosticReason.MARKER_RFC_MISMATCH,
                pointer + ("owning_future_rfc",),
            )
        )
    if marker["owner_context"] != expected_owner:
        diagnostics.append(
            _diagnostic(
                DiagnosticReason.MARKER_OWNER_MISMATCH,
                pointer + ("owner_context",),
            )
        )
    origin = marker["origin"]
    payload = marker["opaque_payload_range"]
    if not (
        origin["raw_start"]
        <= payload["raw_start"]
        <= payload["raw_end"]
        <= origin["raw_end"]
        <= unit["source_length_bytes"]
    ):
        diagnostics.append(
            _diagnostic(
                DiagnosticReason.MARKER_RANGE_INVALID,
                pointer + ("opaque_payload_range",),
            )
        )
    return diagnostics
