from __future__ import annotations

import json
import unittest
from typing import Any

from scenario_factory import materialize_scenario, scenario_document
from support import REPOSITORY_ROOT, base_document, find_declaration, json_bytes

from structural_spike_loader.diagnostics import (
    DiagnosticCode,
    DiagnosticReason,
    InputDiagnostic,
    bound_diagnostics,
)
from structural_spike_loader.loader import load_structural_input
from structural_spike_loader.model import LoadFailure, LoadSuccess
from structural_spike_loader.schema_validation import (
    FIXED_DIAGNOSTIC_CEILING,
    effective_diagnostic_cap,
    executable_schema,
    executable_schema_path,
    schema_diagnostics,
)


def embedded_reviewed_schema() -> dict[str, Any]:
    contract_path = (
        REPOSITORY_ROOT / "02_Architecture" / "Spike_A_Experimental_Input.md"
    )
    contract = contract_path.read_text(encoding="utf-8")
    section = contract.split("## 10. Closed Draft 2020-12 JSON Schema", 1)[1]
    block = section.split("```json", 1)[1].split("```", 1)[0]
    return json.loads(block)


def schema_object_nodes(root: Any) -> list[dict[str, Any]]:
    found: list[dict[str, Any]] = []
    stack = [root]
    while stack:
        node = stack.pop()
        if isinstance(node, dict):
            if node.get("type") == "object":
                found.append(node)
            stack.extend(node.values())
        elif isinstance(node, list):
            stack.extend(node)
    return found


class ExecutableSchemaProjectionTests(unittest.TestCase):
    def test_executable_projection_has_no_drift_from_reviewed_markdown(self) -> None:
        self.assertEqual(executable_schema(), embedded_reviewed_schema())

    def test_executable_schema_is_a_standalone_reviewable_json_file(self) -> None:
        path = executable_schema_path()
        self.assertEqual(
            path.name,
            "experimental-structural-input-0.schema.json",
        )
        self.assertEqual(json.loads(path.read_text(encoding="utf-8")), executable_schema())

    def test_all_38_defs_exist_and_every_reference_resolves_internally(self) -> None:
        schema = executable_schema()
        definitions = schema["$defs"]
        self.assertEqual(len(definitions), 38)
        references: list[str] = []
        stack: list[Any] = [schema]
        while stack:
            node = stack.pop()
            if isinstance(node, dict):
                if "$ref" in node:
                    references.append(node["$ref"])
                stack.extend(node.values())
            elif isinstance(node, list):
                stack.extend(node)
        self.assertTrue(references)
        for reference in references:
            with self.subTest(reference=reference):
                self.assertTrue(reference.startswith("#/$defs/"))
                self.assertIn(reference.removeprefix("#/$defs/"), definitions)

    def test_every_object_schema_is_closed(self) -> None:
        objects = schema_object_nodes(executable_schema())
        self.assertGreater(len(objects), 30)
        for index, node in enumerate(objects):
            with self.subTest(index=index, title=node.get("title")):
                self.assertIs(node.get("additionalProperties"), False)

    def test_minimal_reviewed_fixture_validates_and_publishes(self) -> None:
        document = base_document()
        self.assertEqual(schema_diagnostics(document), [])
        self.assertIsInstance(
            load_structural_input(json_bytes(document)),
            LoadSuccess,
        )


class ClosedSchemaBoundaryTests(unittest.TestCase):
    def test_exact_schema_identifier_is_required(self) -> None:
        document = base_document()
        document["schema"] = "experimental-structural-input/1"
        result = load_structural_input(json_bytes(document))
        self.assertIsInstance(result, LoadFailure)
        assert isinstance(result, LoadFailure)
        self.assertTrue(
            any(
                diagnostic.reason == DiagnosticReason.SCHEMA_CONST
                for diagnostic in result.ordered_diagnostics
            )
        )

    def test_unknown_field_is_schema_failure(self) -> None:
        document = base_document()
        document["unknown"] = "inert"
        result = load_structural_input(json_bytes(document))
        self.assertIsInstance(result, LoadFailure)
        assert isinstance(result, LoadFailure)
        self.assertEqual(
            {diagnostic.code for diagnostic in result.ordered_diagnostics},
            {DiagnosticCode.SCHEMA},
        )
        self.assertIn(
            DiagnosticReason.SCHEMA_ADDITIONAL_PROPERTIES,
            {diagnostic.reason for diagnostic in result.ordered_diagnostics},
        )

    def test_unknown_member_kind_is_schema_failure(self) -> None:
        material = materialize_scenario("input_04_schema_unknown_kind")
        result = load_structural_input(material.source)
        self.assertIsInstance(result, LoadFailure)
        assert isinstance(result, LoadFailure)
        self.assertEqual(result.ordered_diagnostics[0].code, DiagnosticCode.SCHEMA)

    def test_unknown_marker_category_is_schema_failure(self) -> None:
        document = scenario_document("input_06_marker_hit")
        marker = find_declaration(document, "Pump")["members"][-1]
        marker["category"] = "future-magic"
        result = load_structural_input(json_bytes(document))
        self.assertIsInstance(result, LoadFailure)
        assert isinstance(result, LoadFailure)
        self.assertEqual(
            {diagnostic.code for diagnostic in result.ordered_diagnostics},
            {DiagnosticCode.SCHEMA},
        )

    def test_zero_partial_one_and_multiple_selector_candidates_are_valid(self) -> None:
        cases = (
            "input_09_selector_missing",
            "input_11_selector_incomplete",
            "input_01_valid_flat",
            "input_10_selector_multiple",
        )
        for identifier in cases:
            with self.subTest(identifier=identifier):
                document = scenario_document(identifier)
                self.assertEqual(schema_diagnostics(document), [])
                self.assertIsInstance(
                    load_structural_input(json_bytes(document)),
                    LoadSuccess,
                )


class DiagnosticBoundTests(unittest.TestCase):
    def test_active_diagnostic_limit_is_trusted_only_when_locally_valid(self) -> None:
        document = base_document()
        self.assertEqual(effective_diagnostic_cap(document), 1_024)
        document["project_context"]["active_limits"]["maximum_diagnostics"] = 5_000
        self.assertEqual(
            effective_diagnostic_cap(document),
            FIXED_DIAGNOSTIC_CEILING,
        )
        document["project_context"]["active_limits"]["maximum_diagnostics"] = 0
        self.assertEqual(
            effective_diagnostic_cap(document),
            FIXED_DIAGNOSTIC_CEILING,
        )
        self.assertEqual(effective_diagnostic_cap([]), FIXED_DIAGNOSTIC_CEILING)

    def test_effective_cap_retains_deterministic_prefix_and_exact_omitted_count(
        self,
    ) -> None:
        result = load_structural_input(
            materialize_scenario("input_42_loader_diagnostic_limit").source
        )
        self.assertIsInstance(result, LoadFailure)
        assert isinstance(result, LoadFailure)
        self.assertEqual(len(result.ordered_diagnostics), 2)
        self.assertEqual(result.omitted_diagnostic_count, 22)
        self.assertEqual(
            tuple(diagnostic.sort_key() for diagnostic in result.ordered_diagnostics),
            tuple(
                sorted(
                    diagnostic.sort_key()
                    for diagnostic in result.ordered_diagnostics
                )
            ),
        )

    def test_fixed_ceiling_bounds_pre_schema_diagnostics(self) -> None:
        diagnostics = [
            InputDiagnostic(
                DiagnosticCode.SCHEMA,
                DiagnosticReason.SCHEMA_REQUIRED,
                ("missing", index),
            )
            for index in range(FIXED_DIAGNOSTIC_CEILING + 7)
        ]
        retained, omitted = bound_diagnostics(
            diagnostics,
            FIXED_DIAGNOSTIC_CEILING,
        )
        self.assertEqual(len(retained), 4_096)
        self.assertEqual(omitted, 7)
        self.assertEqual(
            tuple(item.sort_key() for item in retained),
            tuple(sorted(item.sort_key() for item in diagnostics)[:4_096]),
        )

    def test_diagnostic_order_uses_rfc6901_pointer_utf8_bytes_then_code_reason(
        self,
    ) -> None:
        diagnostics = [
            InputDiagnostic(
                DiagnosticCode.INTEGRITY,
                DiagnosticReason.PORTABLE_PATH_INVALID,
                ("é",),
            ),
            InputDiagnostic(
                DiagnosticCode.SCHEMA,
                DiagnosticReason.SCHEMA_TYPE,
                ("z",),
            ),
            InputDiagnostic(
                DiagnosticCode.SCHEMA,
                DiagnosticReason.SCHEMA_TYPE,
                ("a/b", "~"),
            ),
        ]
        retained, omitted = bound_diagnostics(diagnostics, 10)
        self.assertEqual(omitted, 0)
        self.assertEqual(
            tuple(item.pointer_text for item in retained),
            ("/a~1b/~0", "/z", "/é"),
        )
