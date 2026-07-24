# ADR0005: Structural Spike A Fixture Loader Technology

**Status:** Accepted

**Date:** 2026-07-24

**Acceptance Date:** 2026-07-24

**Accepted Review Baseline:** `9bffef773a8af159db482ca19e5e8f9a789b4c3d`

**Acceptance Evidence:** `AUDIT-PR14-PHASE-A` — `GO`

**Implementation Review:** `AUDIT-PR15-PHASE-B` — `IMPLEMENTATION GO / COMPILER HOLD`

**Accepted Implementation Head:** `d60fb889b5313143c2afacbdd376ea1d55f19178`

**Decision Scope:** Disposable `experimental-structural-input/0` fixture loader only

**Decision Owner:** IndustrialMDE Project Owner

## 1. Context

The reviewed [`Spike_A_Experimental_Input.md`](../Spike_A_Experimental_Input.md) defines one closed, expression-free JSON fixture contract before Structural Reference Spike A pipeline step 1.

The loader must accept untrusted bytes and enforce exact byte, nesting, record, numeric-token, duplicate-key, schema, integrity, ordering, and diagnostic rules before publishing either immutable input artifact. Ordinary materializing JSON APIs cannot alone satisfy the requirement to reject depth and record overflow before constructing an over-limit tree. APIs that decode numbers directly to binary floating-point also cannot prove the contract's canonical integer-token rule.

Approved Project Constitution version 2.1 requires concrete implementation language, parser, internal serialization, process topology, library, and tool choices to be recorded in ADRs. `ADR0001_TechStack.md` remains empty and its indexed Python, textX, and Jinja2 directions remain incomplete. This ADR must not accept those production choices by implication.

The independent input-contract audit is recorded in [`10_Structural_Input_Contract_Review_Decision.md`](../../00_Project_Brain/10_Structural_Input_Contract_Review_Decision.md). It approves the 44-case fixture matrix but does not authorize implementation.

## 2. Decision Drivers

The fixture loader needs:

- exact inspection of JSON number lexemes before numeric conversion;
- duplicate-key detection after JSON string escape decoding and before object construction;
- pre-materialization byte, depth, and record enforcement;
- a complete Draft 2020-12 validator;
- offline, deterministic `$ref` behavior;
- bounded deterministic diagnostic collection;
- immutable success artifacts and an explicit failure result;
- deterministic generated boundary fixtures;
- no path, URL, shell, template, or expression execution;
- minimal dependencies and a reviewable lock;
- a short implementation path suitable for a disposable architectural spike; and
- isolation from the production compiler's language and parser decisions.

Performance is not a conformance claim. Correct limit admission, deterministic failure, and phase isolation take priority over throughput.

## 3. Decision

Implement the disposable fixture loader with the following stack, subject to the separate Phase B authorization gate in section 7.

### 3.1 Runtime

Use:

```text
CPython 3.12.13
```

The project metadata must constrain the loader to:

```text
requires-python = "==3.12.*"
```

Validation evidence must record the complete runtime identity, including implementation and patch version. A different Python minor version requires an ADR amendment. A later `3.12.x` security release may replace `3.12.13` only through a reviewed lock refresh and complete loader regression run.

Python 3.12 is selected for this spike because the exact runtime is available to the implementation environment, remains under upstream security maintenance, supports the selected validation library, and permits a small dependency surface. This choice is not evidence for a production compiler runtime.

### 3.2 Project and Lock Tool

Use:

```text
uv 0.11.29
pyproject.toml
uv.lock
```

`uv` is a build-time tool, not a runtime dependency. Validation and CI must use:

```text
uv sync --locked
uv run python -m unittest discover
```

The loader project must set:

```toml
[tool.uv]
package = false
```

The spike is not published as a Python distribution. It has no package index release, wheel, console script, or stable API.

`uv.lock` must be committed. Unlocked resolution, implicit dependency upgrades, alternate indexes, URL dependencies, editable third-party dependencies, and VCS dependencies are prohibited.

### 3.3 Runtime Dependencies

The only direct third-party runtime dependency is:

| Package | Version | License | Use |
| --- | --- | --- | --- |
| `jsonschema` | `4.26.0` | MIT | Draft 2020-12 schema checking and deterministic enumeration of schema violations |

No `jsonschema` extras are enabled. In particular, no external format-checker dependency is needed.

The expected complete resolved dependency set for CPython 3.12 is:

| Package | Version | License |
| --- | --- | --- |
| `attrs` | `26.1.0` | MIT |
| `jsonschema` | `4.26.0` | MIT |
| `jsonschema-specifications` | `2025.9.1` | MIT |
| `referencing` | `0.37.0` | MIT |
| `rpds-py` | `2026.6.3` | MIT |
| `typing-extensions` | `4.16.0` | PSF-2.0 |

This set was resolved on 2026-07-24 with CPython 3.12.13 and `uv` 0.11.29. Installed package metadata was inspected for each listed license.

Phase B must regenerate `uv.lock` with the accepted tool/runtime, verify that the resolved set exactly matches this table, record artifact hashes through the lock, and stop for ADR review if resolution differs.

The dependency manager is:

| Tool | Version | License |
| --- | --- | --- |
| `uv` | `0.11.29` | MIT OR Apache-2.0 |

The test runner is Python standard-library `unittest`; no third-party test framework or property-testing library is selected.

### 3.4 JSON Parser

Implement one local, single-purpose, non-recursive JSON parser for the experimental contract.

The parser must:

1. consume a binary stream through an interface that permits bounded reads;
2. stop at byte `10,485,761` for an over-limit input;
3. decode UTF-8 strictly;
4. reject a UTF-8 byte-order mark;
5. admit exactly one RFC 8259 JSON text with only JSON whitespace before or after it;
6. reject unescaped control characters and non-JSON whitespace;
7. decode escape sequences, combine valid UTF-16 surrogate pairs, and reject unpaired surrogate escapes that cannot participate in the required UTF-8 ordering;
8. recognize strings, escapes, objects, arrays, literals, and number tokens with an explicit iterative state machine;
9. count the root at JSON depth `1`;
10. check depth before admitting the next object or array;
11. count every array value and object-member value, including containers and scalars, plus the root;
12. check the record limit before admitting the next value;
13. preserve each number token's original spelling;
14. admit only `0` or a non-zero decimal digit followed by decimal digits;
15. reject negative, negative-zero, leading-zero, fractional, exponent, and greater-than-`2147483647` numeric tokens;
16. decode an object key before checking that object's key set;
17. reject direct and escape-equivalent duplicate keys before adding the member to the object builder;
18. materialize only already-admitted bounded values; and
19. return structured syntax or limit failures without leaking partial builders.

Mutable lists, dictionaries, key sets, parser stacks, and graph worklists may exist only inside the loader phase. They must not escape through a success or failure result.

Do not use `json.loads`, `JSONDecoder.raw_decode`, or another materializing decoder as the contract parser. The standard library decoder may be used only in differential tests over inputs that the bounded parser has already classified; it is not a semantic authority.

The custom parser is deliberately not reusable production `.plant` infrastructure. It accepts JSON fixtures only and must be deleted with contract schema `0` when the spike is replaced.

### 3.5 Schema Validation

The executable schema must be structurally identical to the reviewed JSON object embedded in `Spike_A_Experimental_Input.md`.

Use:

```python
jsonschema.Draft202012Validator
```

The implementation must:

- call `Draft202012Validator.check_schema` during validation;
- instantiate the validator explicitly rather than selecting a draft implicitly;
- use only the reviewed schema's internal `#/$defs/...` references;
- provide no remote HTTP, file, package, or dynamic resolver;
- enable no implicit format checker;
- enumerate independent errors through `iter_errors`;
- map library error paths to RFC 6901 JSON Pointers;
- map validator details to loader-owned stable reason identifiers; and
- sort and cap diagnostics independently of library enumeration order.

The validator library does not own diagnostic order, wording, or publication. Library exception text must not become a stable reason identifier.

### 3.6 Integrity Validation and Normalization

Implement only section 11 items 1 through 11 and 14 of the input contract.

Do not diagnose declaration or import collisions in the loader. Contract section 11 item 12 remains pipeline step 1. Selector cardinality, completeness, resolution, kind, and root-Package ownership remain step 2b.

Use iterative, explicitly bounded graph algorithms for:

- dependency reachability;
- Package dependency acyclicity; and
- per-Package Module acyclicity.

Normalize only the set-like arrays identified by the contract. Preserve Definition and Application Assembly `members` exactly. Derive every member ordinal from the complete input index.

### 3.7 Immutable Artifacts

Represent published records with:

```text
@dataclass(frozen=True, slots=True)
```

Every nested collection in a published artifact must be a tuple or another immutable value owned by the loader package. Published artifacts must contain no `list`, `dict`, mutable `set`, parser node, schema-validator object, iterator, generator, file handle, or callback.

Use explicit result variants:

```text
LoadSuccess
  resolved_project_context
  collected_structural_input

LoadFailure
  ordered_diagnostics
  omitted_diagnostic_count
```

Expected untrusted-input failures return `LoadFailure`; they do not use uncaught exceptions as control flow. Internal invariant failures may raise an implementation exception and fail the test or calling process; they must never be converted into a misleading `INPUT_*` diagnostic.

### 3.8 Diagnostics

Represent diagnostics with frozen records containing at least:

- one of the four `INPUT_*` codes;
- a stable reason enumeration;
- an RFC 6901 pointer represented internally as decoded tokens;
- an optional bounded origin already present in the input; and
- bounded related detail that cannot expose host state.

Sort by:

1. the RFC 6901 pointer encoded with `~0` and `~1`, compared by exact UTF-8 bytes;
2. diagnostic code; and
3. stable reason identifier.

Retain the deterministic prefix and exact omitted count when the active or fixed cap is exceeded.

No library message, localized exception string, dictionary order, filesystem path, process identity, clock, or random value may affect a diagnostic.

### 3.9 Testing

Use standard-library:

```text
unittest
```

Tests must include:

- small raw byte fixtures for ordinary, invalid UTF-8, duplicate-key, framing, and numeric cases;
- deterministic generator functions for large byte, record, diagnostic, and order-permutation cases;
- exact before-admission boundary assertions;
- differential syntax tests against CPython's standard JSON decoder where the contracts overlap;
- parser state-transition tests;
- all 44 reviewed scenario identifiers;
- the required nine-loader-failure and 35-loader-success partition;
- schema-drift verification;
- graph-integrity and deterministic-normalization tests;
- deep immutability checks;
- no-path-open and no-network tests; and
- phase-boundary assertions proving that no step-1 or later fact is produced.

Randomized-order tests must use explicit recorded seeds. Test generation must not become a runtime dependency.

### 3.10 Process and I/O Topology

The loader runs in-process for the disposable spike. This is architectural isolation, not a security sandbox.

The entry point accepts an already-open bounded binary source or an in-memory byte sequence supplied by the test harness. It does not accept a path or URL.

The loader:

- performs no network access;
- discovers no plugins;
- starts no subprocess;
- reads no environment variable for semantic behavior;
- opens no fixture-supplied path;
- writes no file;
- imports no project code dynamically; and
- executes no fixture content.

## 4. Alternatives Considered

### 4.1 CPython standard `json` followed by a validation walk

Rejected because a materializing decoder constructs the complete generic tree before a post-walk can enforce JSON depth and input-record limits. It also converts number tokens before the loader can prove canonical lexical spelling.

`object_pairs_hook` can help identify duplicates, but it does not solve pre-materialization resource enforcement.

### 4.2 Streaming third-party JSON parser plus a separate numeric scanner

Rejected for schema `0`.

Candidate event parsers reduce tree materialization, but their backends may normalize number values, vary in duplicate-member handling, or require a second token scanner to recover lexical spelling. Combining two syntax authorities increases disagreement and dependency risk for a short-lived contract.

A future contract may revisit this decision if it requires larger documents or a maintained production serialization.

### 4.3 Node.js with a streaming tokenizer and Ajv

Viable but not selected.

Ajv already demonstrated that the reviewed schema compiles under Draft 2020-12. However, ordinary `JSON.parse` loses duplicate keys and numeric lexemes, so Node.js still needs a custom tokenizer or another dependency. Selecting a second language runtime solely for the loader would add lock, immutability, packaging, and cross-runtime maintenance work without reducing the critical parser obligation.

This rejection does not establish Python as the production compiler language.

### 4.4 Rust with Serde and a JSON Schema crate

Viable but not selected.

Rust offers strong ownership and bounded builder control. A Serde visitor would still require explicit duplicate-key and raw-number handling, while adding a second build toolchain and a larger one-off implementation cost. The spike does not have a performance requirement that justifies that cost.

This alternative should be reconsidered only if evidence shows the selected implementation cannot enforce the contract safely.

### 4.5 Reuse RFC-0001D public manifest parsing

Rejected because the fixture is explicitly non-interoperable and not the RFC-0001D public format. Sharing an implementation now would risk coupling disposable input behavior to a future public compatibility surface.

## 5. Consequences

### 5.1 Positive

- Raw numeric spelling, duplicate keys, depth, and record admission have one explicit owner.
- The generic tree is bounded before publication and before schema/integrity processing.
- Draft 2020-12 behavior uses a maintained validator rather than a custom schema engine.
- Only one direct runtime dependency is introduced.
- Published artifacts can enforce deep immutability with ordinary language features.
- The test stack has no additional dependency.
- The implementation remains isolated from textX, expressions, resolution, expansion, and production compiler architecture.

### 5.2 Negative

- A custom JSON parser is security-sensitive and requires extensive lexical, Unicode, escape, state-machine, and differential tests.
- CPython 3.12 is in security-maintenance mode rather than feature/bugfix mode.
- The transitive schema-validator graph includes `rpds-py`, a native-extension wheel.
- `jsonschema` error enumeration cannot be exposed directly; mapping and sorting code is required.
- This work is intentionally disposable and may be deleted rather than migrated.

### 5.3 Risks and Mitigations

| Risk | Mitigation |
| --- | --- |
| Parser accepts invalid JSON | Grammar-state unit tests, RFC 8259 corpus cases, and differential tests |
| Parser rejects valid JSON | Positive escape, Unicode, whitespace, container, and differential tests |
| Surrogate escape behavior diverges by host | Combine pairs explicitly and reject unpaired surrogates before UTF-8 comparison |
| Duplicate escape-equivalent key bypass | Compare fully decoded key strings before builder insertion |
| Numeric spelling lost | Preserve token slices and validate before integer conversion |
| Over-limit tree materialized | Instrument admission callbacks and generated boundary sources |
| Validator fetches external resources | Explicit validator class, internal-only references, no resolver or format extras, and no-network tests |
| Library order leaks into diagnostics | Convert to stable reason IDs and sort by contract keys |
| Mutable value escapes | Frozen slotted records, tuples, deep immutability tests |
| Spike stack becomes production precedent | Explicit scope, no public package/CLI, no textX reuse, and mandatory replacement review |
| Dependency drift | Exact versions in `uv.lock`, `uv sync --locked`, and lock-diff review |

## 6. Compliance Rules

The following rules apply to any separately authorized Phase B implementation:

- Phase B must use the exact contract head and accepted gate commit named in its authorization;
- all implementation paths must remain inside the Phase B Task Envelope;
- the parser and schema projection remain internal to Structural Spike A;
- no code may parse `.plant`;
- no code may resolve a reference or selector;
- no code may construct closures or occurrences;
- no code may emit `SPIKEA` or `IMDE` diagnostics;
- no loader budget may consume or weaken RFC-0006 semantic limits;
- no fixture string may cause filesystem or network access;
- no schema or dependency may be retrieved remotely at runtime;
- no public compatibility or performance claim may be made; and
- every divergence from this ADR requires an amendment before implementation.

## 7. Implementation Gate

The Project Owner accepted this ADR after independent audit
`AUDIT-PR14-PHASE-A` returned `GO` against exact Phase A head
`9bffef773a8af159db482ca19e5e8f9a789b4c3d`.

The Project Owner subsequently issued the exact Phase B authorization against
accepted Gate A commit `4591552fa478f53c65ee3b1f4342a0e3d7a9b938`.
The resulting implementation at exact head
`d60fb889b5313143c2afacbdd376ea1d55f19178` received independent
`AUDIT-PR15-PHASE-B` verdict `IMPLEMENTATION GO / COMPILER HOLD`, which the
Project Owner accepted in
[`11_Structural_Fixture_Loader_Implementation_Review_Decision.md`](../../00_Project_Brain/11_Structural_Fixture_Loader_Implementation_Review_Decision.md).

The issued implementation authorization was:

```text
AUTHORIZE TE-STRUCTURAL-LOADER-01 PHASE B AT 4591552fa478f53c65ee3b1f4342a0e3d7a9b938
```

The ADR acceptance and accepted Phase B implementation evidence close only the
disposable fixture-loader gate. They do not authorize Structural Reference
Spike A step 1 or any later compiler phase.

## 8. Replacement and Supersession

This ADR does not supersede `ADR0001_TechStack.md`, `ADR0002_IR_Design.md`, or `ADR0003_CompilerArchitecture.md`.

It applies only while contract identifier `experimental-structural-input/0` exists. Deleting or replacing schema `0` triggers review of the loader and this ADR. Production parser or compiler work must use separately accepted ADRs and must not cite this spike-only choice as implicit precedent.

## 9. Decision Evidence

The proposal was prepared against:

- independent audit `AUDIT-PR14-PHASE-A` of exact Phase A head `9bffef773a8af159db482ca19e5e8f9a789b4c3d`;
- [Python 3.12.13 documentation](https://docs.python.org/3.12/);
- [Python version status](https://devguide.python.org/versions/);
- [`jsonschema` 4.26.0 package metadata](https://pypi.org/project/jsonschema/);
- [`Draft202012Validator` API](https://python-jsonschema.readthedocs.io/en/stable/api/jsonschema/validators/);
- [`uv` 0.11.29 package metadata](https://pypi.org/project/uv/0.11.29/);
- [`uv` lock and sync documentation](https://docs.astral.sh/uv/concepts/projects/sync/); and
- the reviewed contract and audit record in this repository.

External documentation supports the replaceable implementation choice. It does not override the repository contract or create language semantics.
