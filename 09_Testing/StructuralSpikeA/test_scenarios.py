from __future__ import annotations

import json
import unittest

from scenario_factory import FAILURE_EXPECTATIONS, materialize_scenario
from support import REPOSITORY_ROOT

from structural_spike_loader.loader import load_structural_input
from structural_spike_loader.model import LoadFailure, LoadSuccess


MANIFEST_PATH = (
    REPOSITORY_ROOT / "09_Testing" / "StructuralSpikeA" / "fixture_manifest.json"
)


def load_manifest() -> dict:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


class ReviewedFixtureCorpusTests(unittest.TestCase):
    def test_manifest_contains_exactly_the_44_reviewed_identifiers(self) -> None:
        manifest = load_manifest()
        identifiers = [scenario["id"] for scenario in manifest["scenarios"]]
        self.assertEqual(manifest["scenario_count"], 44)
        self.assertEqual(len(identifiers), 44)
        self.assertEqual(len(set(identifiers)), 44)
        self.assertEqual(
            identifiers,
            [
                f"input_{index:02d}_{suffix}"
                for index, suffix in enumerate(
                    [
                        "valid_flat",
                        "valid_nested",
                        "empty_assembly",
                        "schema_unknown_kind",
                        "duplicate_key",
                        "marker_hit",
                        "marker_miss",
                        "deployment_mapping",
                        "selector_missing",
                        "selector_multiple",
                        "selector_incomplete",
                        "selector_unresolved",
                        "selector_wrong_kind",
                        "selector_dependency",
                        "selector_private_root",
                        "multiple_roots",
                        "containment_direct_cycle",
                        "containment_indirect_cycle",
                        "connection_contexts",
                        "reach_through",
                        "unresolved_references",
                        "wrong_kinds",
                        "direction",
                        "type_mismatch",
                        "fan_out",
                        "duplicate_driver",
                        "unconnected_endpoint",
                        "marker_categories",
                        "randomized_sets",
                        "origin_order",
                        "ordinal_gap",
                        "delimiter_components",
                        "source_relocation",
                        "depth_exact",
                        "depth_overflow",
                        "entity_exact",
                        "entity_overflow",
                        "loader_byte_limit",
                        "loader_depth_limit",
                        "loader_record_limit",
                        "marker_span_limit",
                        "loader_diagnostic_limit",
                        "origin_integrity",
                        "project_graph_integrity",
                    ],
                    start=1,
                )
            ],
        )

    def test_manifest_records_exact_35_success_9_failure_partition(self) -> None:
        manifest = load_manifest()
        scenarios = manifest["scenarios"]
        success = [item for item in scenarios if item["expected_loader"] == "success"]
        failure = [item for item in scenarios if item["expected_loader"] == "failure"]
        self.assertEqual(manifest["loader_partition"], {"success": 35, "failure": 9})
        self.assertEqual(len(success), 35)
        self.assertEqual(len(failure), 9)
        self.assertEqual(
            {item["id"] for item in failure},
            set(FAILURE_EXPECTATIONS),
        )
        self.assertTrue(all("expected_code" in item for item in failure))
        self.assertTrue(all("later_owner" in item for item in success))

    def test_generated_boundaries_and_seeds_are_recorded(self) -> None:
        scenarios = {
            item["id"]: item
            for item in load_manifest()["scenarios"]
        }
        self.assertEqual(
            scenarios["input_29_randomized_sets"]["parameters"]["seed"],
            29_000_001,
        )
        self.assertEqual(
            scenarios["input_38_loader_byte_limit"]["parameters"]["byte_count"],
            10_485_761,
        )
        self.assertEqual(
            scenarios["input_39_loader_depth_limit"]["parameters"]["json_depth"],
            33,
        )
        self.assertEqual(
            scenarios["input_40_loader_record_limit"]["parameters"]["record_count"],
            1_000_001,
        )
        self.assertEqual(
            scenarios["input_41_marker_span_limit"]["parameters"][
                "payload_span_bytes"
            ],
            1_048_577,
        )
        self.assertEqual(
            scenarios["input_42_loader_diagnostic_limit"]["parameters"][
                "independent_schema_errors"
            ],
            24,
        )

    def test_all_44_scenarios_have_the_reviewed_loader_verdict(self) -> None:
        manifest = load_manifest()
        successes = 0
        failures = 0
        for entry in manifest["scenarios"]:
            identifier = entry["id"]
            with self.subTest(identifier=identifier):
                material = materialize_scenario(identifier)
                result = load_structural_input(material.source)
                if entry["expected_loader"] == "success":
                    self.assertIsInstance(result, LoadSuccess)
                    assert isinstance(result, LoadSuccess)
                    self.assertEqual(
                        result.resolved_project_context.input_contract_identifier,
                        "experimental-structural-input/0",
                    )
                    self.assertEqual(
                        result.collected_structural_input.input_contract_identifier,
                        "experimental-structural-input/0",
                    )
                    successes += 1
                else:
                    self.assertIsInstance(result, LoadFailure)
                    assert isinstance(result, LoadFailure)
                    self.assertTrue(result.ordered_diagnostics)
                    self.assertEqual(
                        {
                            diagnostic.code
                            for diagnostic in result.ordered_diagnostics
                        },
                        {material.expected_code},
                    )
                    failures += 1
        self.assertEqual((successes, failures), (35, 9))

    def test_semantic_depth_and_entity_limit_facts_are_carried_not_consumed(
        self,
    ) -> None:
        expected_declaration_counts = {
            "input_34_depth_exact": 65,
            "input_35_depth_overflow": 66,
            "input_36_entity_exact": 19,
            "input_37_entity_overflow": 19,
        }
        expected_top_endpoint_counts = {
            "input_36_entity_exact": 1,
            "input_37_entity_overflow": 2,
        }
        for identifier, declaration_count in expected_declaration_counts.items():
            with self.subTest(identifier=identifier):
                result = load_structural_input(
                    materialize_scenario(identifier).source
                )
                self.assertIsInstance(result, LoadSuccess)
                assert isinstance(result, LoadSuccess)
                declarations = (
                    result.collected_structural_input.compilation_units[0][
                        "declarations"
                    ]
                )
                self.assertEqual(len(declarations), declaration_count)
                if identifier in expected_top_endpoint_counts:
                    first_definition = next(
                        declaration
                        for declaration in declarations
                        if declaration.get("name") == "Entity_0"
                    )
                    endpoint_count = sum(
                        member["kind"] == "endpoint"
                        for member in first_definition["members"]
                    )
                    self.assertEqual(
                        endpoint_count,
                        expected_top_endpoint_counts[identifier],
                    )
