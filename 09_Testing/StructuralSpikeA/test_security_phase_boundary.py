from __future__ import annotations

import inspect
import os
import socket
import unittest
from dataclasses import fields, is_dataclass
from typing import Any
from unittest import mock

from scenario_factory import scenario_document
from support import base_document, find_declaration, json_bytes

from structural_spike_loader import __all__ as public_loader_names
from structural_spike_loader.diagnostics import (
    DiagnosticCode,
    DiagnosticReason,
    InputDiagnostic,
    render_diagnostic,
)
from structural_spike_loader.loader import load_structural_input
from structural_spike_loader.model import FrozenRecord, LoadFailure, LoadSuccess


def published_keys(value: Any) -> set[str]:
    keys: set[str] = set()
    stack = [value]
    while stack:
        node = stack.pop()
        if isinstance(node, FrozenRecord):
            for key, child in node.items():
                keys.add(key)
                stack.append(child)
        elif isinstance(node, tuple):
            stack.extend(node)
        elif is_dataclass(node):
            for field in fields(node):
                keys.add(field.name)
                stack.append(getattr(node, field.name))
    return keys


class SecurityIsolationTests(unittest.TestCase):
    def test_path_url_shell_environment_and_template_text_remain_inert_data(
        self,
    ) -> None:
        inert = (
            "/etc/passwd ../secret https://example.invalid/x "
            "$(touch /tmp/no) ${STRUCTURAL_SECRET} {{danger}}"
        )
        document = base_document()
        document["selector_request"]["candidates"][0]["raw_spelling"] = inert
        result = load_structural_input(json_bytes(document))
        self.assertIsInstance(result, LoadSuccess)
        assert isinstance(result, LoadSuccess)
        self.assertEqual(
            result.collected_structural_input.selector_request["candidates"][0][
                "raw_spelling"
            ],
            inert,
        )

    def test_loader_opens_no_fixture_supplied_path(self) -> None:
        document = base_document()
        candidate = document["selector_request"]["candidates"][0]
        candidate["raw_spelling"] = "/must/not/be/opened"
        candidate["origin"]["identity"] = "../../also-not-opened"
        with mock.patch("builtins.open", side_effect=AssertionError("unexpected open")):
            result = load_structural_input(json_bytes(document))
        self.assertIsInstance(result, LoadSuccess)

    def test_loader_performs_no_network_access(self) -> None:
        document = base_document()
        document["selector_request"]["candidates"][0][
            "raw_spelling"
        ] = "https://example.invalid/never-fetch"
        with (
            mock.patch.object(
                socket,
                "socket",
                side_effect=AssertionError("unexpected socket"),
            ),
            mock.patch.object(
                socket,
                "create_connection",
                side_effect=AssertionError("unexpected connection"),
            ),
        ):
            result = load_structural_input(json_bytes(document))
        self.assertIsInstance(result, LoadSuccess)

    def test_diagnostic_rendering_escapes_untrusted_selector_spelling(self) -> None:
        raw_spelling = 'bad"\n\x1b[31m${TOKEN}{{template}}'
        rendered = render_diagnostic(
            InputDiagnostic(
                DiagnosticCode.SCHEMA,
                DiagnosticReason.SCHEMA_PATTERN,
                ("selector_request", "candidates", 0, "raw_spelling"),
                raw_spelling,
            )
        )
        self.assertNotIn("\n", rendered)
        self.assertNotIn("\x1b", rendered)
        self.assertIn('\\"', rendered)
        self.assertIn("\\n", rendered)
        self.assertIn("\\u001b", rendered)

    def test_errors_do_not_expose_host_environment_or_paths(self) -> None:
        sentinel = "STRUCTURAL-SECRET-DO-NOT-LEAK"
        with mock.patch.dict(os.environ, {"STRUCTURAL_SECRET": sentinel}):
            document = base_document()
            document["selector_request"]["candidates"][0][
                "raw_spelling"
            ] = "${STRUCTURAL_SECRET}"
            document["unexpected"] = sentinel
            result = load_structural_input(json_bytes(document))
        self.assertIsInstance(result, LoadFailure)
        assert isinstance(result, LoadFailure)
        rendered = "\n".join(
            render_diagnostic(diagnostic)
            for diagnostic in result.ordered_diagnostics
        )
        self.assertNotIn(sentinel, rendered)
        self.assertNotIn(str(os.getcwd()), rendered)
        self.assertNotIn(".cache", rendered)

    def test_opaque_payload_content_is_neither_accepted_nor_reported(self) -> None:
        payload = "__import__('os').system('never-run')"
        document = scenario_document("input_06_marker_hit")
        marker = find_declaration(document, "Pump")["members"][-1]
        marker["opaque_payload"] = payload
        result = load_structural_input(json_bytes(document))
        self.assertIsInstance(result, LoadFailure)
        assert isinstance(result, LoadFailure)
        rendered = "\n".join(
            render_diagnostic(diagnostic)
            for diagnostic in result.ordered_diagnostics
        )
        self.assertNotIn(payload, rendered)
        self.assertEqual(
            {diagnostic.code for diagnostic in result.ordered_diagnostics},
            {DiagnosticCode.SCHEMA},
        )


class LoaderPhaseBoundaryTests(unittest.TestCase):
    def test_success_publishes_only_two_input_boundary_artifacts(self) -> None:
        result = load_structural_input(json_bytes(base_document()))
        self.assertIsInstance(result, LoadSuccess)
        assert isinstance(result, LoadSuccess)
        self.assertEqual(
            {field.name for field in fields(result)},
            {"resolved_project_context", "collected_structural_input"},
        )

    def test_no_later_phase_fields_are_published(self) -> None:
        result = load_structural_input(json_bytes(base_document()))
        self.assertIsInstance(result, LoadSuccess)
        assert isinstance(result, LoadSuccess)
        keys = published_keys(result)
        forbidden = {
            "resolved_identity",
            "declaration_identity",
            "type_identity",
            "selected_assembly",
            "structural_validation_closure",
            "expansion_closure",
            "occurrence_identity",
            "expanded_graph",
            "snapshot",
            "snapshot_provenance",
            "provenance",
        }
        self.assertTrue(forbidden.isdisjoint(keys))

    def test_failure_is_all_or_nothing_and_has_no_downstream_callback(self) -> None:
        signature = inspect.signature(load_structural_input)
        self.assertEqual(tuple(signature.parameters), ("source",))
        document = base_document()
        document["schema"] = "wrong"
        result = load_structural_input(json_bytes(document))
        self.assertIsInstance(result, LoadFailure)
        assert isinstance(result, LoadFailure)
        self.assertFalse(hasattr(result, "resolved_project_context"))
        self.assertFalse(hasattr(result, "collected_structural_input"))

    def test_loader_diagnostic_namespace_is_exactly_the_four_input_codes(
        self,
    ) -> None:
        self.assertEqual(
            {code.value for code in DiagnosticCode},
            {
                "INPUT_SYNTAX_001",
                "INPUT_SCHEMA_001",
                "INPUT_LIMIT_001",
                "INPUT_INTEGRITY_001",
            },
        )
        self.assertFalse(
            any(
                name.startswith("SPIKEA") or name.startswith("IMDE")
                for name in (code.value for code in DiagnosticCode)
            )
        )

    def test_public_api_contains_no_resolver_selector_compiler_or_publisher(
        self,
    ) -> None:
        forbidden_terms = (
            "resolve_declaration",
            "resolve_type",
            "select_assembly",
            "build_closure",
            "expand",
            "publish_snapshot",
            "compile",
        )
        self.assertTrue(
            all(name not in public_loader_names for name in forbidden_terms)
        )
