from __future__ import annotations

import copy
import random
from dataclasses import dataclass
from typing import Any

from support import (
    ROOT_PACKAGE,
    ROOT_SOURCE_IDENTITY,
    SOURCE_LENGTH,
    assembly,
    base_document,
    compilation_unit,
    connection,
    definition,
    endpoint,
    find_declaration,
    instance,
    json_bytes,
    module,
    non_source_origin,
    package_identity,
    package_revision,
    replace_source_identity,
    selector_candidate,
    unsupported_marker,
)

from structural_spike_loader.bounded_json import (
    MAX_INPUT_BYTES,
    MAX_INPUT_RECORDS,
)
from structural_spike_loader.diagnostics import DiagnosticCode


FAILURE_EXPECTATIONS = {
    "input_04_schema_unknown_kind": DiagnosticCode.SCHEMA,
    "input_05_duplicate_key": DiagnosticCode.SYNTAX,
    "input_38_loader_byte_limit": DiagnosticCode.LIMIT,
    "input_39_loader_depth_limit": DiagnosticCode.LIMIT,
    "input_40_loader_record_limit": DiagnosticCode.LIMIT,
    "input_41_marker_span_limit": DiagnosticCode.LIMIT,
    "input_42_loader_diagnostic_limit": DiagnosticCode.SCHEMA,
    "input_43_origin_integrity": DiagnosticCode.INTEGRITY,
    "input_44_project_graph_integrity": DiagnosticCode.INTEGRITY,
}


@dataclass(frozen=True, slots=True)
class ScenarioMaterial:
    identifier: str
    source: bytes
    expected_code: DiagnosticCode | None

    @property
    def expects_success(self) -> bool:
        return self.expected_code is None


def _root_unit(document: dict[str, Any]) -> dict[str, Any]:
    return document["compilation_units"][0]


def _replace_declarations(
    document: dict[str, Any],
    declarations: list[dict[str, Any]],
) -> None:
    _root_unit(document)["declarations"] = declarations


def _add_dependency_context(
    document: dict[str, Any],
    *,
    dependency_name: str = "library",
    alias: str = "Library",
    assembly_name: str = "DepMain",
) -> tuple[dict[str, str], dict[str, Any]]:
    identity = package_identity(dependency_name)
    source_identity = [
        "org.example",
        dependency_name,
        "Core",
        "libsrc/main.plant",
        "sha256:" + "3" * 64,
    ]
    revision = package_revision(
        identity,
        digest_character="3",
        kind="immutable-artifact",
    )
    document["project_context"]["dependency_package_revisions"].append(revision)
    document["project_context"]["dependency_edges"].append(
        {
            "consumer": copy.deepcopy(ROOT_PACKAGE),
            "alias": alias,
            "dependency": copy.deepcopy(identity),
            "origin": non_source_origin(
                "build-metadata",
                f"fixture/dependency-lock.json#/{dependency_name}",
            ),
        }
    )
    document["project_context"]["modules"].append(
        module(identity, "Core", "libsrc", f"{dependency_name}-module")
    )
    dep_definition = definition(
        source_identity,
        "DepPump",
        [endpoint(source_identity, "status", "output")],
    )
    dep_assembly = assembly(
        source_identity,
        assembly_name,
        [instance(source_identity, "dep_pump", "DepPump")],
    )
    unit = compilation_unit(
        identity,
        "Core",
        "libsrc/main.plant",
        source_identity,
        [dep_definition, dep_assembly],
    )
    document["compilation_units"].append(unit)
    return identity, unit


def _chain_document(levels: int) -> dict[str, Any]:
    document = base_document()
    definitions: list[dict[str, Any]] = []
    for index in range(levels):
        members: list[dict[str, Any]] = []
        if index + 1 < levels:
            members.append(
                instance(
                    ROOT_SOURCE_IDENTITY,
                    f"next_{index}",
                    f"Depth_{index + 1}",
                    raw_start=200 + index,
                )
            )
        definitions.append(
            definition(
                ROOT_SOURCE_IDENTITY,
                f"Depth_{index}",
                members,
                raw_start=50 + index,
            )
        )
    main = assembly(
        ROOT_SOURCE_IDENTITY,
        "Main",
        [instance(ROOT_SOURCE_IDENTITY, "root", "Depth_0")],
    )
    _replace_declarations(document, definitions + [main])
    return document


def _entity_document(endpoint_count: int) -> dict[str, Any]:
    document = base_document()
    definitions: list[dict[str, Any]] = []
    for index in range(18):
        members: list[dict[str, Any]] = []
        if index == 0:
            for endpoint_index in range(endpoint_count):
                members.append(
                    endpoint(
                        ROOT_SOURCE_IDENTITY,
                        f"budget_{endpoint_index}",
                        "input",
                        raw_start=100 + endpoint_index,
                    )
                )
        if index < 17:
            members.extend(
                [
                    instance(
                        ROOT_SOURCE_IDENTITY,
                        "left",
                        f"Entity_{index + 1}",
                        raw_start=300 + index,
                    ),
                    instance(
                        ROOT_SOURCE_IDENTITY,
                        "right",
                        f"Entity_{index + 1}",
                        raw_start=500 + index,
                    ),
                ]
            )
        definitions.append(
            definition(
                ROOT_SOURCE_IDENTITY,
                f"Entity_{index}",
                members,
                raw_start=50 + index,
            )
        )
    main = assembly(
        ROOT_SOURCE_IDENTITY,
        "Main",
        [instance(ROOT_SOURCE_IDENTITY, "root", "Entity_0")],
    )
    _replace_declarations(document, definitions + [main])
    return document


def _reverse_object_order(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: _reverse_object_order(child)
            for key, child in reversed(tuple(value.items()))
        }
    if isinstance(value, list):
        return [_reverse_object_order(child) for child in value]
    return value


def randomized_set_variant(
    document: dict[str, Any],
    seed: int,
) -> dict[str, Any]:
    variant = copy.deepcopy(document)
    generator = random.Random(seed)
    project = variant["project_context"]
    for collection in (
        project["dependency_package_revisions"],
        project["dependency_edges"],
        project["modules"],
        project["module_edges"],
        variant["selector_request"]["candidates"],
        variant["compilation_units"],
    ):
        generator.shuffle(collection)
    for unit in variant["compilation_units"]:
        generator.shuffle(unit["imports"])
        generator.shuffle(unit["declarations"])
    return _reverse_object_order(variant)


def scenario_document(identifier: str) -> dict[str, Any]:
    document = base_document()
    pump = find_declaration(document, "Pump")
    main = find_declaration(document, "Main")

    if identifier == "input_01_valid_flat":
        return document
    if identifier == "input_02_valid_nested":
        wrapper = definition(
            ROOT_SOURCE_IDENTITY,
            "Wrapper",
            [instance(ROOT_SOURCE_IDENTITY, "nested_pump", "Pump")],
        )
        main["members"] = [instance(ROOT_SOURCE_IDENTITY, "wrapper", "Wrapper")]
        _root_unit(document)["declarations"].insert(1, wrapper)
        return document
    if identifier == "input_03_empty_assembly":
        main["members"] = []
        return document
    if identifier == "input_04_schema_unknown_kind":
        pump["members"][0]["kind"] = "endpont"
        return document
    if identifier == "input_06_marker_hit":
        pump["members"].append(
            unsupported_marker(
                ROOT_SOURCE_IDENTITY,
                "expression",
                "RFC-0003",
                "definition",
                "Pump",
            )
        )
        return document
    if identifier == "input_07_marker_miss":
        unused = definition(
            ROOT_SOURCE_IDENTITY,
            "Unused",
            [
                unsupported_marker(
                    ROOT_SOURCE_IDENTITY,
                    "state",
                    "RFC-0004",
                    "definition",
                    "Unused",
                )
            ],
        )
        _root_unit(document)["declarations"].insert(1, unused)
        return document
    if identifier == "input_08_deployment_mapping":
        main["members"].append(
            unsupported_marker(
                ROOT_SOURCE_IDENTITY,
                "deployment-mapping",
                "RFC-0007",
                "application-assembly",
                "Main",
                raw_start=1_610_000,
            )
        )
        return document
    if identifier == "input_09_selector_missing":
        document["selector_request"]["candidates"] = []
        return document
    if identifier == "input_10_selector_multiple":
        document["selector_request"]["candidates"].append(
            selector_candidate(raw_spelling="org.example/control::Process.Other")
        )
        return document
    if identifier == "input_11_selector_incomplete":
        candidate = document["selector_request"]["candidates"][0]
        candidate["target"] = {"package_identity": copy.deepcopy(ROOT_PACKAGE)}
        return document
    if identifier == "input_12_selector_unresolved":
        document["selector_request"]["candidates"][0]["target"]["identifier"] = "Missing"
        return document
    if identifier == "input_13_selector_wrong_kind":
        document["selector_request"]["candidates"][0]["target"]["identifier"] = "Pump"
        return document
    if identifier == "input_14_selector_dependency":
        dependency, _ = _add_dependency_context(document)
        document["selector_request"]["candidates"] = [
            selector_candidate(
                dependency,
                "DepMain",
                raw_spelling="org.example/library::Process.DepMain",
            )
        ]
        return document
    if identifier == "input_15_selector_private_root":
        main["visibility"] = "private"
        return document
    if identifier == "input_16_multiple_roots":
        main["members"].append(
            instance(ROOT_SOURCE_IDENTITY, "pump_2", "Pump", raw_start=240)
        )
        return document
    if identifier == "input_17_containment_direct_cycle":
        pump["members"].append(
            instance(ROOT_SOURCE_IDENTITY, "self_child", "Pump", raw_start=300)
        )
        return document
    if identifier == "input_18_containment_indirect_cycle":
        alpha = definition(
            ROOT_SOURCE_IDENTITY,
            "Alpha",
            [instance(ROOT_SOURCE_IDENTITY, "beta", "Beta")],
        )
        beta = definition(
            ROOT_SOURCE_IDENTITY,
            "Beta",
            [instance(ROOT_SOURCE_IDENTITY, "alpha", "Alpha")],
        )
        main["members"] = [instance(ROOT_SOURCE_IDENTITY, "alpha", "Alpha")]
        _replace_declarations(document, [alpha, beta, main])
        return document
    if identifier == "input_19_connection_contexts":
        main["members"].extend(
            [
                instance(ROOT_SOURCE_IDENTITY, "pump_2", "Pump", raw_start=240),
                connection(
                    ROOT_SOURCE_IDENTITY,
                    "sibling",
                    ["pump_1", "status"],
                    ["pump_2", "command"],
                ),
            ]
        )
        wrapper = definition(
            ROOT_SOURCE_IDENTITY,
            "Wrapper",
            [
                endpoint(ROOT_SOURCE_IDENTITY, "inlet", "input"),
                instance(ROOT_SOURCE_IDENTITY, "child", "Pump"),
                connection(
                    ROOT_SOURCE_IDENTITY,
                    "owner_child",
                    ["self", "inlet"],
                    ["child", "command"],
                ),
            ],
        )
        _root_unit(document)["declarations"].insert(1, wrapper)
        return document
    if identifier == "input_20_reach_through":
        main["members"].append(
            connection(
                ROOT_SOURCE_IDENTITY,
                "reach_through",
                ["wrapper", "pump", "status"],
                ["pump_1", "command"],
            )
        )
        return document
    if identifier == "input_21_unresolved_references":
        pump["members"][0]["type_reference"]["segments"] = ["MissingType"]
        main["members"][0]["definition_reference"]["segments"] = ["MissingDefinition"]
        main["members"].append(
            connection(
                ROOT_SOURCE_IDENTITY,
                "missing_endpoints",
                ["missing", "source"],
                ["missing", "destination"],
            )
        )
        return document
    if identifier == "input_22_wrong_kinds":
        main["members"][0]["definition_reference"]["segments"] = ["Main"]
        pump["members"][0]["type_reference"]["segments"] = ["Pump"]
        main["members"].append(
            connection(
                ROOT_SOURCE_IDENTITY,
                "wrong_kind",
                ["pump_1", "pump_1"],
                ["pump_1", "command"],
            )
        )
        return document
    if identifier == "input_23_direction":
        main["members"].append(
            connection(
                ROOT_SOURCE_IDENTITY,
                "wrong_direction",
                ["pump_1", "command"],
                ["pump_1", "status"],
            )
        )
        return document
    if identifier == "input_24_type_mismatch":
        pump["members"].append(
            endpoint(ROOT_SOURCE_IDENTITY, "count", "input", "INT", raw_start=180)
        )
        main["members"].append(
            connection(
                ROOT_SOURCE_IDENTITY,
                "type_mismatch",
                ["pump_1", "status"],
                ["pump_1", "count"],
            )
        )
        return document
    if identifier == "input_25_fan_out":
        main["members"].extend(
            [
                instance(ROOT_SOURCE_IDENTITY, "pump_2", "Pump", raw_start=240),
                instance(ROOT_SOURCE_IDENTITY, "pump_3", "Pump", raw_start=280),
                connection(
                    ROOT_SOURCE_IDENTITY,
                    "fan_1",
                    ["pump_1", "status"],
                    ["pump_2", "command"],
                ),
                connection(
                    ROOT_SOURCE_IDENTITY,
                    "fan_2",
                    ["pump_1", "status"],
                    ["pump_3", "command"],
                    raw_start=380,
                ),
            ]
        )
        return document
    if identifier == "input_26_duplicate_driver":
        main["members"].extend(
            [
                instance(ROOT_SOURCE_IDENTITY, "pump_2", "Pump", raw_start=240),
                instance(ROOT_SOURCE_IDENTITY, "pump_3", "Pump", raw_start=280),
                connection(
                    ROOT_SOURCE_IDENTITY,
                    "driver_1",
                    ["pump_1", "status"],
                    ["pump_3", "command"],
                ),
                connection(
                    ROOT_SOURCE_IDENTITY,
                    "driver_2",
                    ["pump_2", "status"],
                    ["pump_3", "command"],
                    raw_start=380,
                ),
            ]
        )
        return document
    if identifier == "input_27_unconnected_endpoint":
        return document
    if identifier == "input_28_marker_categories":
        mapping = [
            ("expression", "RFC-0003"),
            ("state", "RFC-0004"),
            ("interface", "RFC-0006"),
            ("replication", "RFC-0006"),
            ("deployment", "RFC-0007"),
            ("target", "RFC-0007"),
        ]
        for index, (category, rfc) in enumerate(mapping):
            pump["members"].append(
                unsupported_marker(
                    ROOT_SOURCE_IDENTITY,
                    category,
                    rfc,
                    "definition",
                    "Pump",
                    raw_start=10_000 + index * 100,
                )
            )
        return document
    if identifier == "input_29_randomized_sets":
        _add_dependency_context(document)
        return randomized_set_variant(document, seed=29_000_001)
    if identifier == "input_30_origin_order":
        document["selector_request"]["candidates"][0]["origin"] = non_source_origin(
            "invocation",
            "invocation/selector/0",
        )
        return document
    if identifier == "input_31_ordinal_gap":
        pump["members"].insert(
            1,
            unsupported_marker(
                ROOT_SOURCE_IDENTITY,
                "expression",
                "RFC-0003",
                "definition",
                "Pump",
            ),
        )
        return document
    if identifier == "input_32_delimiter_components":
        document["selector_request"]["candidates"] = [
            selector_candidate(raw_spelling="A_B.Main"),
            selector_candidate(raw_spelling="A.B.Main"),
        ]
        document["selector_request"]["candidates"][0]["target"]["namespace_path"] = ["A_B"]
        document["selector_request"]["candidates"][1]["target"]["namespace_path"] = ["A", "B"]
        return document
    if identifier == "input_33_source_relocation":
        unit = _root_unit(document)
        old_identity = list(unit["source_identity_components"])
        new_identity = [
            "org.example",
            "control",
            "Core",
            "relocated/main.plant",
            old_identity[-1],
        ]
        unit["unit_identity"]["portable_package_path"] = "relocated/main.plant"
        unit["source_identity_components"] = list(new_identity)
        document["project_context"]["modules"][0]["source_roots"] = ["relocated"]
        replace_source_identity(unit, old_identity, new_identity)
        return document
    if identifier == "input_34_depth_exact":
        return _chain_document(64)
    if identifier == "input_35_depth_overflow":
        return _chain_document(65)
    if identifier == "input_36_entity_exact":
        return _entity_document(1)
    if identifier == "input_37_entity_overflow":
        return _entity_document(2)
    if identifier == "input_41_marker_span_limit":
        pump["members"].append(
            unsupported_marker(
                ROOT_SOURCE_IDENTITY,
                "expression",
                "RFC-0003",
                "definition",
                "Pump",
                raw_start=10_000,
                payload_start=10_001,
                payload_end=10_001 + 1_048_577,
            )
        )
        return document
    if identifier == "input_42_loader_diagnostic_limit":
        document["project_context"]["active_limits"]["maximum_diagnostics"] = 2
        document["compilation_units"].extend([{}, {}, {}])
        return document
    if identifier == "input_43_origin_integrity":
        pump["origin"]["source_identity_components"] = ["another", "source"]
        pump["origin"]["raw_end"] = SOURCE_LENGTH + 1
        return document
    if identifier == "input_44_project_graph_integrity":
        dependency, _ = _add_dependency_context(document)
        duplicate = package_revision(
            dependency,
            digest_character="4",
            kind="immutable-artifact",
        )
        orphan = package_identity("orphan")
        document["project_context"]["dependency_package_revisions"].extend(
            [
                duplicate,
                package_revision(
                    orphan,
                    digest_character="5",
                    kind="immutable-artifact",
                ),
            ]
        )
        document["project_context"]["dependency_edges"].append(
            {
                "consumer": copy.deepcopy(dependency),
                "alias": "Root",
                "dependency": copy.deepcopy(ROOT_PACKAGE),
                "origin": non_source_origin(
                    "build-metadata",
                    "fixture/dependency-lock.json#/cycle",
                ),
            }
        )
        return document
    raise KeyError(identifier)


def materialize_scenario(identifier: str) -> ScenarioMaterial:
    if identifier == "input_05_duplicate_key":
        source = (
            b'{"schema":"experimental-structural-input/0",'
            b'"schema":"experimental-structural-input/0"}'
        )
    elif identifier == "input_38_loader_byte_limit":
        source = b" " * (MAX_INPUT_BYTES + 1)
    elif identifier == "input_39_loader_depth_limit":
        source = b"[" * 33 + b"0" + b"]" * 33
    elif identifier == "input_40_loader_record_limit":
        scalar_count = MAX_INPUT_RECORDS
        source = b"[" + b"0," * (scalar_count - 1) + b"0]"
    else:
        source = json_bytes(scenario_document(identifier))
    return ScenarioMaterial(
        identifier=identifier,
        source=source,
        expected_code=FAILURE_EXPECTATIONS.get(identifier),
    )
