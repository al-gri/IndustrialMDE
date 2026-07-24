from __future__ import annotations

import copy
import unittest
from dataclasses import FrozenInstanceError
from typing import Any

from scenario_factory import randomized_set_variant, scenario_document
from support import (
    ROOT_PACKAGE,
    ROOT_SOURCE_IDENTITY,
    base_document,
    connection,
    find_declaration,
    json_bytes,
    module,
    name_reference,
    non_source_origin,
    package_identity,
    package_revision,
    unsupported_marker,
)

from structural_spike_loader.diagnostics import DiagnosticCode, DiagnosticReason
from structural_spike_loader.integrity import (
    MAX_MARKER_PAYLOAD_SPAN,
    validate_integrity,
    validate_marker_limits,
)
from structural_spike_loader.loader import load_structural_input
from structural_spike_loader.model import (
    FrozenRecord,
    LoadFailure,
    LoadSuccess,
)


def reasons(document: dict[str, Any]) -> set[DiagnosticReason]:
    return {diagnostic.reason for diagnostic in validate_integrity(document)}


def root_module_identity() -> dict[str, Any]:
    return {
        "package_identity": copy.deepcopy(ROOT_PACKAGE),
        "module_name": "Core",
    }


def dependency_document() -> dict[str, Any]:
    return scenario_document("input_14_selector_dependency")


def add_dependency_revision(
    document: dict[str, Any],
    name: str,
    digest_character: str,
) -> dict[str, str]:
    identity = package_identity(name)
    project = document["project_context"]
    project["dependency_package_revisions"].append(
        package_revision(
            identity,
            digest_character=digest_character,
            kind="immutable-artifact",
        )
    )
    project["modules"].append(module(identity, "Core", name, f"{name}-module"))
    return identity


def dependency_edge(
    consumer: dict[str, str],
    dependency: dict[str, str],
    alias: str,
) -> dict[str, Any]:
    return {
        "consumer": copy.deepcopy(consumer),
        "alias": alias,
        "dependency": copy.deepcopy(dependency),
        "origin": non_source_origin(
            "build-metadata",
            f"fixture/dependency-lock.json#/{alias}",
        ),
    }


def module_edge(
    consumer: dict[str, Any],
    dependency: dict[str, Any],
) -> dict[str, Any]:
    return {
        "consumer": copy.deepcopy(consumer),
        "dependency": copy.deepcopy(dependency),
        "origin": non_source_origin(
            "project-manifest",
            "fixture/project.json#/module-edge",
        ),
    }


def reverse_object_key_order(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: reverse_object_key_order(child)
            for key, child in reversed(tuple(value.items()))
        }
    if isinstance(value, list):
        return [reverse_object_key_order(child) for child in value]
    return value


def assert_load_success(
    testcase: unittest.TestCase,
    document: dict[str, Any],
) -> LoadSuccess:
    result = load_structural_input(json_bytes(document))
    testcase.assertIsInstance(result, LoadSuccess)
    assert isinstance(result, LoadSuccess)
    return result


class ProjectIntegrityTests(unittest.TestCase):
    def test_package_version_component_bounds(self) -> None:
        document = base_document()
        document["project_context"]["root_package_revision"]["version"] = (
            "2147483648.0.0"
        )
        self.assertIn(
            DiagnosticReason.PACKAGE_VERSION_COMPONENT_LIMIT,
            reasons(document),
        )

    def test_portable_paths_reject_traversal_backslash_and_reserved_devices(
        self,
    ) -> None:
        for path in ("src/../main.plant", "src\\main.plant", "CON/file.plant"):
            with self.subTest(path=path):
                document = base_document()
                document["compilation_units"][0]["unit_identity"][
                    "portable_package_path"
                ] = path
                self.assertIn(
                    DiagnosticReason.PORTABLE_PATH_INVALID,
                    reasons(document),
                )

    def test_source_roots_detect_case_collisions_and_overlap(self) -> None:
        document = base_document()
        project = document["project_context"]
        project["modules"].extend(
            [
                module(ROOT_PACKAGE, "Case", "SRC", "case-module"),
                module(ROOT_PACKAGE, "Nested", "src/nested", "nested-module"),
            ]
        )
        found = reasons(document)
        self.assertIn(DiagnosticReason.PORTABLE_PATH_CASE_COLLISION, found)
        self.assertIn(DiagnosticReason.SOURCE_ROOT_OVERLAP, found)

    def test_package_revisions_must_be_unique(self) -> None:
        document = dependency_document()
        revision = copy.deepcopy(
            document["project_context"]["dependency_package_revisions"][0]
        )
        revision["content_identity"]["digest"] = "9" * 64
        document["project_context"]["dependency_package_revisions"].append(revision)
        self.assertIn(
            DiagnosticReason.DUPLICATE_PACKAGE_IDENTITY,
            reasons(document),
        )

    def test_dependency_endpoints_aliases_and_reachability(self) -> None:
        document = dependency_document()
        project = document["project_context"]
        library = package_identity("library")
        orphan = add_dependency_revision(document, "orphan", "4")
        missing = package_identity("missing")
        project["dependency_edges"].extend(
            [
                dependency_edge(missing, library, "MissingConsumer"),
                dependency_edge(ROOT_PACKAGE, missing, "MissingTarget"),
                dependency_edge(ROOT_PACKAGE, orphan, "Library"),
                dependency_edge(ROOT_PACKAGE, library, "library"),
                dependency_edge(ROOT_PACKAGE, library, "AlternateLibrary"),
            ]
        )
        found = reasons(document)
        self.assertIn(DiagnosticReason.DEPENDENCY_CONSUMER_MISSING, found)
        self.assertIn(DiagnosticReason.DEPENDENCY_TARGET_MISSING, found)
        self.assertIn(DiagnosticReason.DEPENDENCY_ALIAS_DUPLICATE, found)
        self.assertIn(DiagnosticReason.DEPENDENCY_TARGET_DUPLICATE, found)
        # Orphan becomes reachable through its edge; a separate revision proves reachability.
        unreachable = add_dependency_revision(document, "unreachable", "5")
        self.assertEqual(unreachable["name"], "unreachable")
        self.assertIn(DiagnosticReason.DEPENDENCY_UNREACHABLE, reasons(document))

    def test_dependency_graph_direct_and_indirect_cycles(self) -> None:
        library = package_identity("library")

        direct = dependency_document()
        direct["project_context"]["dependency_edges"].append(
            dependency_edge(library, library, "Self")
        )
        direct_reasons = reasons(direct)
        self.assertIn(DiagnosticReason.DEPENDENCY_SELF_REFERENCE, direct_reasons)
        self.assertIn(DiagnosticReason.DEPENDENCY_CYCLE, direct_reasons)

        indirect = dependency_document()
        second = add_dependency_revision(indirect, "second", "4")
        indirect["project_context"]["dependency_edges"].extend(
            [
                dependency_edge(library, second, "Second"),
                dependency_edge(second, library, "LibraryBack"),
            ]
        )
        self.assertIn(DiagnosticReason.DEPENDENCY_CYCLE, reasons(indirect))

    def test_module_identity_ownership_and_cross_package_edges(self) -> None:
        document = dependency_document()
        project = document["project_context"]
        project["modules"].append(copy.deepcopy(project["modules"][0]))
        project["modules"].append(
            module(ROOT_PACKAGE, "core", "case-only", "case-only-module")
        )
        missing_package = package_identity("not-participating")
        project["modules"].append(
            module(missing_package, "Ghost", "ghost", "ghost-module")
        )
        project["module_edges"].append(
            module_edge(
                root_module_identity(),
                {
                    "package_identity": package_identity("library"),
                    "module_name": "Core",
                },
            )
        )
        found = reasons(document)
        self.assertIn(DiagnosticReason.MODULE_IDENTITY_DUPLICATE, found)
        self.assertIn(DiagnosticReason.MODULE_IDENTITY_CASE_COLLISION, found)
        self.assertIn(DiagnosticReason.MODULE_PACKAGE_MISSING, found)
        self.assertIn(DiagnosticReason.MODULE_EDGE_CROSS_PACKAGE, found)

    def test_module_graph_missing_endpoint_and_direct_indirect_cycles(self) -> None:
        direct = base_document()
        core = root_module_identity()
        direct["project_context"]["module_edges"].append(module_edge(core, core))
        self.assertIn(DiagnosticReason.MODULE_CYCLE, reasons(direct))

        indirect = base_document()
        project = indirect["project_context"]
        project["modules"].extend(
            [
                module(ROOT_PACKAGE, "Aux", "aux", "aux-module"),
                module(ROOT_PACKAGE, "Extra", "extra", "extra-module"),
            ]
        )
        aux = {
            "package_identity": copy.deepcopy(ROOT_PACKAGE),
            "module_name": "Aux",
        }
        extra = {
            "package_identity": copy.deepcopy(ROOT_PACKAGE),
            "module_name": "Extra",
        }
        project["module_edges"].extend(
            [
                module_edge(core, aux),
                module_edge(aux, extra),
                module_edge(extra, aux),
            ]
        )
        self.assertIn(DiagnosticReason.MODULE_CYCLE, reasons(indirect))

        missing = base_document()
        missing["project_context"]["module_edges"].append(
            module_edge(
                core,
                {
                    "package_identity": copy.deepcopy(ROOT_PACKAGE),
                    "module_name": "Missing",
                },
            )
        )
        self.assertIn(
            DiagnosticReason.MODULE_EDGE_ENDPOINT_MISSING,
            reasons(missing),
        )


class CompilationUnitAndOriginIntegrityTests(unittest.TestCase):
    def test_compilation_unit_identity_module_and_source_identity_invariants(
        self,
    ) -> None:
        document = base_document()
        duplicate = copy.deepcopy(document["compilation_units"][0])
        duplicate["unit_identity"]["portable_package_path"] = "src/other.plant"
        document["compilation_units"].append(duplicate)
        found = reasons(document)
        self.assertIn(DiagnosticReason.SOURCE_IDENTITY_DUPLICATE, found)

        document["compilation_units"][0]["unit_identity"]["module_name"] = "Missing"
        self.assertIn(
            DiagnosticReason.COMPILATION_UNIT_MODULE_MISSING,
            reasons(document),
        )

        exact_duplicate = copy.deepcopy(document["compilation_units"][0])
        document["compilation_units"].append(exact_duplicate)
        self.assertIn(
            DiagnosticReason.COMPILATION_UNIT_DUPLICATE,
            reasons(document),
        )

    def test_project_wide_language_version_must_match(self) -> None:
        document = base_document()
        document["compilation_units"][0]["language_version"] = "0.2"
        self.assertIn(
            DiagnosticReason.LANGUAGE_VERSION_MISMATCH,
            reasons(document),
        )

    def test_source_origin_identity_and_range_are_owned_by_unit(self) -> None:
        document = scenario_document("input_43_origin_integrity")
        found = reasons(document)
        self.assertIn(DiagnosticReason.SOURCE_ORIGIN_IDENTITY_MISMATCH, found)
        self.assertIn(DiagnosticReason.SOURCE_ORIGIN_RANGE_INVALID, found)

    def test_at_most_three_source_origins_attach_directly_to_a_record(self) -> None:
        document = base_document()
        main = find_declaration(document, "Main")
        record = connection(
            ROOT_SOURCE_IDENTITY,
            "four-origins",
            ["pump_1", "status"],
            ["pump_1", "command"],
        )
        record["target_reference"] = name_reference(
            ROOT_SOURCE_IDENTITY,
            ["Pump"],
            500,
        )
        main["members"].append(record)
        self.assertIn(DiagnosticReason.TOO_MANY_DIRECT_ORIGINS, reasons(document))

    def test_marker_span_exact_boundary_passes_and_next_byte_is_limit_failure(
        self,
    ) -> None:
        exact = base_document()
        pump = find_declaration(exact, "Pump")
        start = 10_001
        pump["members"].append(
            unsupported_marker(
                ROOT_SOURCE_IDENTITY,
                "expression",
                "RFC-0003",
                "definition",
                "Pump",
                raw_start=10_000,
                payload_start=start,
                payload_end=start + MAX_MARKER_PAYLOAD_SPAN,
            )
        )
        self.assertEqual(validate_marker_limits(exact), [])
        self.assertIsInstance(
            load_structural_input(json_bytes(exact)),
            LoadSuccess,
        )

        overflow = scenario_document("input_41_marker_span_limit")
        diagnostics = validate_marker_limits(overflow)
        self.assertEqual(len(diagnostics), 1)
        self.assertEqual(diagnostics[0].code, DiagnosticCode.LIMIT)
        self.assertEqual(
            diagnostics[0].reason,
            DiagnosticReason.MARKER_SPAN_LIMIT_EXCEEDED,
        )

    def test_marker_rfc_owner_and_range_must_match_placement(self) -> None:
        document = scenario_document("input_06_marker_hit")
        marker = find_declaration(document, "Pump")["members"][-1]
        marker["owning_future_rfc"] = "RFC-0007"
        marker["owner_context"]["identifier"] = "Other"
        marker["opaque_payload_range"]["raw_start"] = marker["origin"]["raw_start"] - 1
        found = reasons(document)
        self.assertIn(DiagnosticReason.MARKER_RFC_MISMATCH, found)
        self.assertIn(DiagnosticReason.MARKER_OWNER_MISMATCH, found)
        self.assertIn(DiagnosticReason.MARKER_RANGE_INVALID, found)

    def test_forbidden_later_phase_fields_are_detected_before_publication(
        self,
    ) -> None:
        document = base_document()
        find_declaration(document, "Pump")["runtime_fact"] = "must-not-pass"
        self.assertIn(DiagnosticReason.FORBIDDEN_PHASE_FIELD, reasons(document))
        result = load_structural_input(json_bytes(document))
        self.assertIsInstance(result, LoadFailure)


class DeterministicNormalizationTests(unittest.TestCase):
    def test_randomized_set_like_order_produces_equal_immutable_artifacts(
        self,
    ) -> None:
        source = scenario_document("input_29_randomized_sets")
        first = randomized_set_variant(source, seed=29_000_001)
        second = randomized_set_variant(source, seed=29_000_002)
        self.assertEqual(
            assert_load_success(self, first),
            assert_load_success(self, second),
        )

    def test_json_object_key_order_does_not_change_artifacts(self) -> None:
        document = base_document()
        reversed_document = reverse_object_key_order(document)
        self.assertEqual(
            assert_load_success(self, document),
            assert_load_success(self, reversed_document),
        )

    def test_colliding_step_1_declaration_keys_do_not_restore_input_order(
        self,
    ) -> None:
        first = base_document()
        pump = find_declaration(first, "Pump")
        collision = copy.deepcopy(pump)
        collision["visibility"] = "public"
        collision["members"] = list(reversed(collision["members"]))
        first["compilation_units"][0]["declarations"].insert(1, collision)
        second = copy.deepcopy(first)
        second["compilation_units"][0]["declarations"][0:2] = reversed(
            second["compilation_units"][0]["declarations"][0:2]
        )
        self.assertEqual(
            assert_load_success(self, first),
            assert_load_success(self, second),
        )

    def test_definition_and_assembly_member_arrays_retain_exact_order(self) -> None:
        document = base_document()
        pump = find_declaration(document, "Pump")
        pump["members"].reverse()
        result = assert_load_success(self, document)
        declarations = result.collected_structural_input.compilation_units[0][
            "declarations"
        ]
        published_pump = next(
            declaration
            for declaration in declarations
            if declaration.get("name") == "Pump"
        )
        self.assertEqual(
            tuple(member["name"] for member in published_pump["members"]),
            ("status", "command"),
        )

    def test_unsupported_marker_consumes_member_index_and_creates_ordinal_gap(
        self,
    ) -> None:
        result = assert_load_success(
            self,
            scenario_document("input_31_ordinal_gap"),
        )
        declarations = result.collected_structural_input.compilation_units[0][
            "declarations"
        ]
        pump = next(
            declaration
            for declaration in declarations
            if declaration.get("name") == "Pump"
        )
        self.assertEqual(
            tuple(member["kind"] for member in pump["members"]),
            ("endpoint", "unsupported-marker", "endpoint"),
        )
        endpoint_ordinals = tuple(
            index
            for index, member in enumerate(pump["members"])
            if member["kind"] == "endpoint"
        )
        self.assertEqual(endpoint_ordinals, (0, 2))
        self.assertFalse(any("declaration_ordinal" in member for member in pump["members"]))

    def test_structured_delimiter_components_do_not_collapse_to_strings(self) -> None:
        result = assert_load_success(
            self,
            scenario_document("input_32_delimiter_components"),
        )
        candidates = result.collected_structural_input.selector_request["candidates"]
        namespaces = {candidate["target"]["namespace_path"] for candidate in candidates}
        self.assertEqual(namespaces, {("A_B",), ("A", "B")})

    def test_physical_source_relocation_preserves_declaration_semantics(self) -> None:
        original = assert_load_success(
            self,
            scenario_document("input_01_valid_flat"),
        )
        relocated = assert_load_success(
            self,
            scenario_document("input_33_source_relocation"),
        )

        def semantic_signature(result: LoadSuccess) -> tuple[Any, ...]:
            unit = result.collected_structural_input.compilation_units[0]
            return (
                unit["namespace"]["segments"],
                tuple(
                    (
                        declaration["kind"],
                        declaration.get("name"),
                        tuple(
                            (member["kind"], member.get("name"))
                            for member in declaration.get("members", ())
                        ),
                    )
                    for declaration in unit["declarations"]
                ),
            )

        self.assertEqual(
            semantic_signature(original),
            semantic_signature(relocated),
        )
        self.assertNotEqual(
            original.resolved_project_context.compilation_units[0].unit_identity,
            relocated.resolved_project_context.compilation_units[0].unit_identity,
        )

    def test_published_artifacts_are_recursively_immutable(self) -> None:
        result = assert_load_success(self, base_document())

        def assert_immutable_tree(value: Any) -> None:
            stack = [value]
            while stack:
                node = stack.pop()
                self.assertNotIsInstance(node, (dict, list, set))
                if isinstance(node, FrozenRecord):
                    stack.extend(child for _, child in node.items())
                elif isinstance(node, tuple):
                    stack.extend(node)

        assert_immutable_tree(result.resolved_project_context.project_context)
        assert_immutable_tree(result.collected_structural_input.selector_request)
        with self.assertRaises(FrozenInstanceError):
            result.collected_structural_input.input_contract_identifier = "changed"  # type: ignore[misc]
