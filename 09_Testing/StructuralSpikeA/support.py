from __future__ import annotations

import copy
import json
import sys
from pathlib import Path
from typing import Any


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
COMPILER_ROOT = REPOSITORY_ROOT / "04_Compiler" / "StructuralSpikeA"
if str(COMPILER_ROOT) not in sys.path:
    sys.path.insert(0, str(COMPILER_ROOT))


ROOT_PACKAGE = {"authority": "org.example", "name": "control"}
ROOT_SOURCE_IDENTITY = [
    "org.example",
    "control",
    "Core",
    "src/main.plant",
    "sha256:" + "2" * 64,
]
SOURCE_LENGTH = 2_000_000


def package_identity(
    name: str = "control",
    authority: str = "org.example",
) -> dict[str, str]:
    return {"authority": authority, "name": name}


def non_source_origin(kind: str, identity: str) -> dict[str, str]:
    return {"kind": kind, "identity": identity}


def source_origin(
    source_identity: list[str],
    raw_start: int,
    raw_end: int,
) -> dict[str, Any]:
    return {
        "kind": "source",
        "source_identity_components": list(source_identity),
        "raw_start": raw_start,
        "raw_end": raw_end,
    }


def name_reference(
    source_identity: list[str],
    segments: list[str],
    raw_start: int = 100,
) -> dict[str, Any]:
    return {
        "segments": segments,
        "origin": source_origin(source_identity, raw_start, raw_start + 8),
    }


def endpoint(
    source_identity: list[str],
    name: str,
    direction: str,
    type_name: str = "BOOL",
    raw_start: int = 100,
) -> dict[str, Any]:
    return {
        "kind": "endpoint",
        "name": name,
        "direction": direction,
        "type_reference": name_reference(
            source_identity,
            [type_name],
            raw_start + 10,
        ),
        "origin": source_origin(source_identity, raw_start, raw_start + 30),
    }


def instance(
    source_identity: list[str],
    name: str,
    definition_name: str,
    raw_start: int = 200,
) -> dict[str, Any]:
    return {
        "kind": "instance",
        "name": name,
        "definition_reference": name_reference(
            source_identity,
            [definition_name],
            raw_start + 10,
        ),
        "origin": source_origin(source_identity, raw_start, raw_start + 30),
    }


def endpoint_reference(
    source_identity: list[str],
    segments: list[str],
    raw_start: int,
) -> dict[str, Any]:
    return {
        "segments": segments,
        "origin": source_origin(source_identity, raw_start, raw_start + 12),
    }


def connection(
    source_identity: list[str],
    name: str,
    source_segments: list[str],
    destination_segments: list[str],
    raw_start: int = 300,
) -> dict[str, Any]:
    return {
        "kind": "connection",
        "name": name,
        "source_reference": endpoint_reference(
            source_identity,
            source_segments,
            raw_start + 10,
        ),
        "destination_reference": endpoint_reference(
            source_identity,
            destination_segments,
            raw_start + 30,
        ),
        "origin": source_origin(source_identity, raw_start, raw_start + 60),
    }


def unsupported_marker(
    source_identity: list[str],
    category: str,
    owning_future_rfc: str,
    owner_kind: str,
    owner_identifier: str | None,
    raw_start: int = 10_000,
    payload_start: int | None = None,
    payload_end: int | None = None,
) -> dict[str, Any]:
    if payload_start is None:
        payload_start = raw_start + 2
    if payload_end is None:
        payload_end = raw_start + 10
    origin_end = max(raw_start + 20, payload_end)
    return {
        "kind": "unsupported-marker",
        "category": category,
        "owning_future_rfc": owning_future_rfc,
        "owner_context": {
            "kind": owner_kind,
            "identifier": owner_identifier,
        },
        "origin": source_origin(source_identity, raw_start, origin_end),
        "opaque_payload_range": {
            "raw_start": payload_start,
            "raw_end": payload_end,
        },
    }


def definition(
    source_identity: list[str],
    name: str,
    members: list[dict[str, Any]],
    raw_start: int = 50,
) -> dict[str, Any]:
    return {
        "kind": "definition",
        "name": name,
        "visibility": "private",
        "members": members,
        "origin": source_origin(source_identity, raw_start, raw_start + 1_500_000),
    }


def assembly(
    source_identity: list[str],
    name: str,
    members: list[dict[str, Any]],
    raw_start: int = 1_600_000,
) -> dict[str, Any]:
    return {
        "kind": "application-assembly",
        "name": name,
        "visibility": "private",
        "members": members,
        "origin": source_origin(source_identity, raw_start, raw_start + 300_000),
    }


def package_revision(
    identity: dict[str, str],
    *,
    digest_character: str,
    kind: str,
) -> dict[str, Any]:
    return {
        "package_identity": copy.deepcopy(identity),
        "version": "0.1.0",
        "content_identity": {
            "kind": kind,
            "digest_algorithm": "sha256",
            "digest": digest_character * 64,
        },
    }


def module(
    identity: dict[str, str],
    module_name: str,
    source_root: str,
    suffix: str,
) -> dict[str, Any]:
    return {
        "identity": {
            "package_identity": copy.deepcopy(identity),
            "module_name": module_name,
        },
        "exposure": "internal",
        "source_roots": [source_root],
        "origin": non_source_origin(
            "project-manifest",
            f"fixture/project.json#/{suffix}",
        ),
    }


def compilation_unit(
    identity: dict[str, str],
    module_name: str,
    path: str,
    source_identity: list[str],
    declarations: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "unit_identity": {
            "package_identity": copy.deepcopy(identity),
            "module_name": module_name,
            "portable_package_path": path,
        },
        "source_identity_components": list(source_identity),
        "source_length_bytes": SOURCE_LENGTH,
        "language_version": "0.1",
        "language_version_origin": source_origin(source_identity, 0, 8),
        "namespace": {
            "segments": ["Process"],
            "origin": source_origin(source_identity, 9, 27),
        },
        "imports": [],
        "declarations": declarations,
    }


def selector_candidate(
    target_package: dict[str, str] | None = None,
    identifier: str = "Main",
    *,
    raw_spelling: str = "org.example/control::Process.Main",
    origin_kind: str = "fixture-metadata",
) -> dict[str, Any]:
    target = {
        "package_identity": copy.deepcopy(target_package or ROOT_PACKAGE),
        "namespace_path": ["Process"],
        "owner_path": [],
        "identifier": identifier,
    }
    return {
        "target": target,
        "raw_spelling": raw_spelling,
        "origin": non_source_origin(
            origin_kind,
            "fixture/input.json#/selector_request/candidates/0",
        ),
    }


def base_document() -> dict[str, Any]:
    pump = definition(
        ROOT_SOURCE_IDENTITY,
        "Pump",
        [
            endpoint(ROOT_SOURCE_IDENTITY, "command", "input", raw_start=100),
            endpoint(ROOT_SOURCE_IDENTITY, "status", "output", raw_start=140),
        ],
    )
    main = assembly(
        ROOT_SOURCE_IDENTITY,
        "Main",
        [instance(ROOT_SOURCE_IDENTITY, "pump_1", "Pump")],
    )
    unit = compilation_unit(
        ROOT_PACKAGE,
        "Core",
        "src/main.plant",
        ROOT_SOURCE_IDENTITY,
        [pump, main],
    )
    return {
        "schema": "experimental-structural-input/0",
        "project_context": {
            "language_version": "0.1",
            "root_package_revision": package_revision(
                ROOT_PACKAGE,
                digest_character="0",
                kind="workspace-snapshot",
            ),
            "dependency_package_revisions": [],
            "dependency_edges": [],
            "modules": [module(ROOT_PACKAGE, "Core", "src", "root-module")],
            "module_edges": [],
            "project_manifest_origin": non_source_origin(
                "project-manifest",
                "fixture/project.json",
            ),
            "dependency_lock_origin": non_source_origin(
                "build-metadata",
                "fixture/dependency-lock.json",
            ),
            "project_resolution_fingerprint": {
                "algorithm": "sha256",
                "value": "1" * 64,
            },
            "active_limits": {
                "maximum_expansion_depth": 64,
                "maximum_expanded_semantic_entities": 262_144,
                "maximum_diagnostics": 1_024,
            },
        },
        "selector_request": {
            "origin": non_source_origin(
                "fixture-metadata",
                "fixture/input.json#/selector_request",
            ),
            "candidates": [selector_candidate()],
        },
        "compilation_units": [unit],
    }


def json_bytes(document: dict[str, Any], *, sort_keys: bool = False) -> bytes:
    return json.dumps(
        document,
        ensure_ascii=True,
        separators=(",", ":"),
        sort_keys=sort_keys,
    ).encode("utf-8")


def find_declaration(document: dict[str, Any], name: str) -> dict[str, Any]:
    for unit in document["compilation_units"]:
        for declaration_record in unit["declarations"]:
            if declaration_record.get("name") == name:
                return declaration_record
    raise KeyError(name)


def replace_source_identity(
    node: Any,
    old_identity: list[str],
    new_identity: list[str],
) -> None:
    stack = [node]
    while stack:
        current = stack.pop()
        if isinstance(current, dict):
            if (
                current.get("kind") == "source"
                and current.get("source_identity_components") == old_identity
            ):
                current["source_identity_components"] = list(new_identity)
            stack.extend(current.values())
        elif isinstance(current, list):
            stack.extend(current)
