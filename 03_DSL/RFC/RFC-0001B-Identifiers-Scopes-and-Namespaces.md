# RFC-0001B: Identifiers, Scopes, and Namespaces

**Status:** Proposed

**Authors:** IndustrialMDE Project

**Created:** 2026-07-19

**Last Updated:** 2026-07-20

**Target Language Version:** Pre-1.0

**Dependencies:** RFC-0000, RFC-0001, RFC-0001A

**Supersedes:** None

**Superseded By:** None

**Implementation Status:** Not Started

**Review:** [Pull Request #6](https://github.com/al-gri/IndustrialMDE/pull/6); [RFC-0001B Review Decision](../../00_Project_Brain/07_RFC-0001B_Review_Decision.md)

## 1. Summary

This RFC defines how IndustrialMDE source identifiers become deterministic semantic names. It specifies namespace directives, declaration and member scopes, collision domains, qualified-name resolution, explicit import bindings, naming conventions, and the separation between semantic identity, external engineering tags, and generated target names.

The design deliberately favors explicit qualification and stable lookup over convenience features that can change meaning when dependencies evolve. Wildcard imports, relative imports, implicit parent-namespace search, and implicit shadowing are not part of language version `0.1`.

RFC-0000, RFC-0001, and RFC-0001A are currently Proposed. This RFC is a non-normative Proposed specification and cannot become Accepted until its normative dependencies and the RFC governance contract are Accepted.

## 2. Motivation

Industrial projects remain in service for decades and are compiled against changing libraries, targets, and engineering environments. A name-resolution rule that depends on file discovery order, hash-map order, import order, filesystem layout, or newly published wildcard symbols can silently change an old model.

IndustrialMDE also needs to preserve several distinct identities:

- a source identifier used by the language;
- a stable semantic declaration or instance identity;
- an external P&ID, asset, HMI, or SCADA tag; and
- a target-specific generated symbol.

Conflating those identities would embed target restrictions in the vendor-neutral core and make migrations or traceability unreliable. This RFC establishes the source and semantic naming boundary before compilation units, packages, types, expressions, or target lowering are designed.

## 3. Goals

This RFC is intended to provide:

- deterministic namespace and name-resolution behavior;
- one explicit namespace context for every source file;
- stable declaration identities independent of physical file placement;
- precise owner scopes for Definitions, Application Assemblies, and Deployment Models;
- explicit, file-local imports without wildcard exposure;
- portable collision rules for case-sensitive source and case-insensitive targets;
- qualified access to member declarations and expanded instance members;
- clear naming conventions for declarations, instances, values, and constants;
- stable diagnostics for duplicate, ambiguous, inaccessible, and unresolved names;
- incremental-compilation inputs suitable for RFC-0001C.

## 4. Non-Goals

This RFC does not define:

- project manifests, package identities, dependency versions, or source discovery;
- module boundaries, module initialization, or import-cycle policy;
- package root ownership or package-alias syntax;
- public API export lists, re-export, or the final `public` and `private` contract;
- type lookup, overload resolution, conversions, or expression-local variables;
- inheritance, interface implementation, or member override;
- attribute, annotation, external-tag, or generated-name syntax;
- Profile Role registration or profile namespace governance;
- the complete grammar for semantic declarations;
- target-specific normalization, reserved words, or name mangling;
- runtime lookup or dynamic dispatch.

## 5. Terminology

This RFC uses terms from the [IndustrialMDE Glossary](../Glossary.md).

- **Identifier Spelling** — the exact ASCII token spelling accepted by RFC-0001.
- **Namespace Path** — a non-empty ordered sequence of identifier spellings naming a logical namespace within one Package Identity.
- **Scope** — an identity-bearing owner that contains one deterministic set of named declarations.
- **Collision Domain** — the set of bindings that must have distinct exact and case-folded spellings.
- **Ordinary Symbol** — a namespace child, semantic declaration, or member declaration participating in the unified ordinary-symbol collision rules.
- **Binding** — an association from one source-visible identifier to one resolved semantic identity.
- **Import Environment** — the file-local set of bindings introduced by explicit import directives.
- **Qualified Name** — two or more identifier segments separated by ASCII dots.
- **Canonical Identity Key** — the structured, implementation-independent identity tuple used for semantic equality and deterministic ordering.
- **Member View** — the named members exposed by a Definition, Instance Declaration, or expanded Instance for qualified traversal.
- **ASCII Case-Folded Key** — an identifier spelling with `A` through `Z` mapped to `a` through `z`, with every other permitted character unchanged.

An Import Environment is not a semantic owner and does not change the identity of the imported declaration. An external tag and a generated target name are not bindings in a language scope.

## 6. Normative Specification

### 6.1 Identifier Foundation

Every identifier used by this RFC MUST satisfy RFC-0001:

```regex
^[A-Za-z_][A-Za-z0-9_]*$
```

The maximum source identifier length is 255 ASCII characters. User declarations MUST NOT use the reserved double-underscore prefix. Reserved keywords for the effective language version MUST NOT be used as identifiers.

Identifier equality is exact, case-sensitive ASCII equality. An implementation MUST NOT apply Unicode normalization, locale-sensitive comparison, or filesystem case rules to semantic names.

The ASCII Case-Folded Key is used only to detect prohibited portability collisions. It does not replace the exact spelling and does not make the language case-insensitive.

### 6.2 Namespace Directive Syntax

RFC-0001B owns the following syntax fragment:

```text
NamespaceDirective ::= "namespace" QualifiedName ";"
QualifiedName      ::= Identifier ("." Identifier)*
```

A source file compiled under this RFC MUST contain exactly one Namespace Directive. It MUST occur after the required language-version directive and optional metadata block, and before every import or semantic declaration.

The Namespace Path is interpreted from the current Package Identity's namespace root. It is not relative to a directory, another source file, or a previously declared namespace, and no import binding participates in its interpretation.

The combined source prefix is:

```text
language-version directive
optional metadata block
namespace directive
zero or more import directives
remaining declarations defined by their owning RFCs
```

Comments and whitespace MAY occur between those constructs. A namespace path MUST contain at least one segment. Leading dots, trailing dots, empty segments, and relative path segments such as `.` or `..` are prohibited.

A lexical-only RFC-0001 conformance fixture is not required to contain a Namespace Directive. A `.plant` file participating in semantic compilation under RFC-0001B is required to contain one even when it declares no ordinary symbols.

### 6.3 Logical Namespace Identity and Merge

A logical Namespace Identity is the tuple:

```text
(Package Identity, Namespace Path)
```

Package Identity is defined by RFC-0001C. A namespace path alone is not globally unique.

Source files with the same Package Identity and exact Namespace Path contribute to one merged logical namespace. Their physical directories and filenames do not create or alter namespace identity.

Source files from different Package Identities MUST NOT merge namespaces, even when their Namespace Paths have identical spellings. Cross-package visibility requires dependency and import rules defined jointly by this RFC and RFC-0001C.

Every namespace segment is itself a named child in its parent namespace collision domain. A child namespace and an ordinary declaration in the same parent namespace MUST NOT have the same exact spelling or ASCII Case-Folded Key.

Namespace merging MUST NOT depend on source discovery order. Duplicate and collision checks apply across all source files contributing to the merged namespace.

A tool MAY warn when a Namespace Path does not follow a project's directory convention, but directory structure MUST NOT change semantic resolution.

### 6.4 Identity-Bearing Scopes

The foundational model defines these identity-bearing scopes:

| Scope owner | Direct named contents |
| --- | --- |
| Package root | Root namespace segments and package-level declarations authorized by RFC-0001C |
| Logical Namespace | Child namespaces and top-level semantic declarations |
| Definition | Member Declarations owned by that Definition |
| Application Assembly | Root Instance Declarations, Connection Declarations, and other authorized application entries |
| Deployment Model | Deployment Mappings and other authorized deployment entries |

Every named declaration MUST belong to exactly one identity-bearing scope. Every such scope has one unified ordinary-symbol collision domain unless a later Accepted RFC explicitly defines a separate named category.

Definitions, Application Assemblies, and Deployment Models do not lexically inherit the member declarations of other owners. Two different Definitions may each declare a member named `status`; those members occupy different scopes and do not shadow each other.

An expanded Instance does not create source declarations. It exposes the Member View of its referenced Definition under the Instance Identity path defined by RFC-0001A.

Metadata keys, documentation headings, external tags, generated target names, and diagnostic codes are not ordinary symbols in these scopes.

Profile Role identities occupy registries defined by their profile contracts. They MUST be explicitly qualified and MUST NOT silently enter an ordinary-symbol collision domain.

### 6.5 Unified Ordinary-Symbol Namespace

Within one identity-bearing scope, every ordinary symbol shares one collision domain regardless of semantic entity kind.

For example, a Definition and an Application Assembly in the same logical Namespace cannot share one spelling, and an Endpoint Declaration and Instance Declaration in the same Definition cannot share one spelling.

This rule prevents a reference from changing meaning merely because its expected semantic kind changes. If a resolved reference has the wrong kind, the compiler reports the kind mismatch required by RFC-0001A rather than performing a second lookup in another hidden symbol namespace.

A later RFC that needs labels, generic parameters, or behavior-local names MUST define whether they join an existing collision domain or form a new one. It MUST NOT create an undocumented parallel namespace.

### 6.6 Duplicate and Case-Only Collisions

Two ordinary symbols in the same collision domain MUST NOT have identical Identifier Spellings.

Two ordinary symbols in the same collision domain also MUST NOT have identical ASCII Case-Folded Keys. Therefore these declarations cannot coexist in one logical scope:

```text
Pump
pump
PUMP
```

Case-only collision checks apply to:

- declarations merged from different source files;
- child namespace segments;
- file-local import bindings;
- collisions between an import binding and a directly visible declaration; and
- any later binding category that participates in the ordinary-symbol lookup set.

Unrelated owner scopes MAY reuse the same spelling. A target profile MAY apply stricter normalization and reserved-name checks during target validation, but MUST NOT weaken the core case-only collision prohibition.

### 6.7 Naming Conventions

The recommended source conventions are:

| Category | Convention | Illustrative pattern | Example |
| --- | --- | --- | --- |
| Built-in type | `UPPER_CASE` | `^[A-Z][A-Z0-9_]*$` | `REAL` |
| User-defined Definition or type | `PascalCase` | `^[A-Z][A-Za-z0-9]*$` | `MotorVfd` |
| Application Assembly | `PascalCase` | `^[A-Z][A-Za-z0-9]*$` | `WaterTreatment` |
| Deployment Model | `PascalCase` | `^[A-Z][A-Za-z0-9]*$` | `PlantController` |
| Namespace segment | `PascalCase` | `^[A-Z][A-Za-z0-9]*$` | `WaterTreatment` |
| Instance, Endpoint, Parameter, State, or local value | `snake_case` | `^[a-z][a-z0-9]*(?:_[a-z0-9]+)*$` | `main_pump` |
| Compile-time Constant | `UPPER_SNAKE_CASE` | `^[A-Z][A-Z0-9]*(?:_[A-Z0-9]+)*$` | `DEFAULT_TIMEOUT` |

These conventions classify source presentation; they do not define semantic entity kind. A compiler MUST NOT infer a Definition, Constant, role, or target binding from capitalization.

In the pre-1.0 Proposed contract, a convention violation produces `IMDE3013` as a Warning and does not change identity or resolution. The diagnostic configuration MAY promote the Warning to an Error as an explicit build input. Whether a Stabilized production profile makes any convention mandatory remains an unresolved decision.

Import aliases SHOULD follow the convention of the imported target. A namespace alias uses `PascalCase`.

External engineering tags are validated strings governed by their registering contract and do not follow these identifier conventions.

### 6.8 Canonical Declaration Identity

A declaration's Canonical Identity Key MUST be structured data, not a concatenated string. It contains at least:

```text
Package Identity
Namespace Path segments
Owning declaration path segments
Declaration Identifier Spelling
Semantic Entity Kind
```

The exact package component is defined by RFC-0001C. Each segment is retained separately so that punctuation escaping cannot create identity collisions.

Physical source path, line number, declaration order, import alias, external tag, generated target name, process identifier, timestamp, and random UUID MUST NOT participate in semantic identity.

Changing the package identity, Namespace Path, owner path, declaration spelling, or semantic entity kind changes the declaration identity. Moving a file without changing those components preserves identity.

The human-readable qualified display name MAY join namespace and owner segments with dots. That display form is not a substitute for the structured Canonical Identity Key.

### 6.9 Qualified Names and Traversal

A Qualified Name contains identifier segments separated by dots:

```plant
Process.WaterTreatment.PumpStation
station_1.main_pump.start_command
Sensors.AnalogSensor
```

The first segment is resolved through exactly one applicable lexical binding environment. Every later segment is resolved in the explicit Namespace or Member View reached by the preceding segment.

Resolution MUST proceed left to right without backtracking. A compiler MUST NOT reinterpret an earlier segment as a different package, namespace, declaration, instance, external tag, or generated target name merely because a later segment fails.

A segment MUST NOT be traversed unless the resolved entity exposes a Namespace or Member View valid in that syntactic and semantic context. Otherwise the reference is invalid qualification.

Qualification through an Instance Declaration or expanded Instance follows the referenced Definition's Member View while retaining the instance path for occurrence identity. Qualification through a Definition denotes declarations, not runtime occurrences. The owning semantic RFC determines which form is legal for a particular reference.

External tags and generated target names MUST NOT participate in Qualified Name traversal.

### 6.10 Unqualified Resolution

Name resolution MUST be independent of source declaration order. A compiler collects the complete binding set for an applicable scope before resolving references in that scope.

For an unqualified reference, the resolver considers only the binding environments explicitly authorized for that reference context:

1. the current identity-bearing owner scope, when the reference form permits owner members;
2. the current merged logical Namespace;
3. the current source file's explicit Import Environment; and
4. an explicitly specified language prelude, if a later Accepted RFC defines one.

The sets above do not establish a shadowing priority. Collision rules MUST prevent two eligible unqualified bindings from silently competing. If more than one distinct eligible identity remains, resolution fails as ambiguous.

The resolver MUST NOT search parent Namespace Paths implicitly. A file in `Process.WaterTreatment.Control` does not gain unqualified access to declarations in `Process.WaterTreatment` or `Process`.

The resolver MUST NOT search sibling namespaces, transitive dependencies, filesystem directories, or all loaded packages. Access requires the current namespace, explicit qualification, or an explicit import.

A syntactic context MAY require one semantic entity kind. Kind filtering MUST NOT be used to legitimize duplicate ordinary symbols in one collision domain. A uniquely resolved identity of the wrong kind produces `IMDE2009` or a more specific diagnostic from the owning semantic RFC.

### 6.11 Import Directive Syntax

RFC-0001B owns the following syntax fragment:

```text
ImportDirective ::= "import" QualifiedName ("as" Identifier)? ";"
```

Every Import Directive MUST occur after the Namespace Directive and before the first semantic declaration in the source file.

An import targets exactly one exported semantic declaration or exactly one logical namespace. It does not textually include another file and does not copy declarations into the current namespace.

The import target Qualified Name is resolved as an export path through the current package and the direct dependencies made available by RFC-0001C. It MUST NOT begin with or otherwise depend on a binding introduced by another Import Directive. Import directive order therefore has no resolution semantics.

Examples:

```plant
import Common.Motors.MotorVfd;
import Legacy.Systems.Pump as LegacyPump;
import Common.Sensors as Sensors;
```

A declaration import without `as` introduces one file-local binding using the target's final identifier segment. A declaration import with `as` introduces the explicit alias.

A namespace import MUST use `as` and introduces only the namespace alias. It MUST NOT inject the namespace's members as unqualified bindings.

Wildcard, glob, group, relative, and recursive imports are prohibited in language version `0.1`. These forms are invalid, including:

```plant
import Common.Sensors.*;
import .Local.Sensor;
import Common.{Motor, Valve};
```

An import is file-local. It does not become visible to another file contributing to the same merged namespace.

An import does not itself declare a package dependency. The imported target's package MUST be available through the explicit Project dependency graph defined by RFC-0001C.

Public import and re-export are not defined in language version `0.1`.

### 6.12 Import Binding Validation

Every Import Directive MUST resolve to exactly one accessible target identity. Resolution to zero targets is unresolved; resolution to multiple package or declaration identities is ambiguous.

An import alias participates in the file's Import Environment collision domain. It MUST NOT collide exactly or by ASCII Case-Folded Key with:

- another import binding in that file;
- a directly visible declaration in the current merged namespace; or
- another binding made unqualified by an Accepted language prelude.

Two textually identical imports of the same target and alias produce `IMDE3009` as a redundant-import Warning. They introduce only one binding.

Two imports that request the same binding spelling for different targets are an Error. Source order MUST NOT select a winner.

An unused import produces `IMDE3010` as a Warning. Removing an unused import MUST NOT change the resolved Semantic Model.

The import target's visibility and package availability are validated under RFC-0001C. A transitive dependency is not automatically importable unless the Project dependency contract explicitly exposes it.

### 6.13 Shadowing and Override

IndustrialMDE language version `0.1` has no implicit shadowing mechanism.

A declaration or import MUST NOT silently hide another binding that is eligible for the same unqualified reference context. Such a conflict is rejected even when a conventional language might choose the nearest declaration.

This prohibition does not apply to equal spellings in independent owner scopes. For example, `Motor.status` and `Valve.status` are distinct qualified members, and `station_1.status` and `station_2.status` are distinct occurrence paths.

Namespace nesting is not lexical inheritance. A declaration in a child namespace may reuse a spelling from a parent namespace because parent members are not found by implicit unqualified lookup. Tools SHOULD encourage qualification when similarly named APIs could confuse readers.

Member override, interface implementation binding, and parameter override are not redeclaration or shadowing facilities:

- inheritance and member override are not authorized by this RFC;
- interface member binding is reserved for RFC-0006;
- an instance parameter binding supplies a value to an existing Parameter Declaration and does not create another declaration.

Any future override feature MUST use explicit syntax, identify the overridden declaration, preserve traceability, and define compatibility behavior.

### 6.14 Forward References and Declaration Order

Forward references within one resolved scope MAY be supported by the semantic RFC that owns the reference kind. When supported, they MUST resolve exactly as references to earlier declarations.

Name collection MUST complete for a scope before order-independent references are resolved. A compiler MUST NOT make a valid reference depend on whether another contributing file was discovered first.

Source order MAY remain observable for formatting, documentation, explicitly ordered declarations, or traceability. It MUST NOT break duplicate-name ties, choose among ambiguous bindings, or establish semantic identity.

Runtime initialization order, module initialization, and cyclic semantic dependencies are outside this RFC.

### 6.15 Visibility Boundary

The reserved keywords `public` and `private` do not acquire declaration syntax from this RFC.

RFC-0001C MUST define package and module visibility before cross-package import conformance can be Accepted. Whatever visibility model is selected:

- an import MUST NOT bypass it;
- visibility MUST be explicit and deterministic;
- inaccessible declarations MUST NOT participate as successful resolution candidates;
- a diagnostic SHOULD identify an inaccessible matching declaration when doing so does not leak protected information across a tooling trust boundary; and
- public re-export MUST NOT occur implicitly.

### 6.16 External and Generated Names

An External Tag is validated data and MUST NOT replace an Identifier Spelling or Canonical Identity Key. Two declarations with distinct semantic identities MAY have equal External Tags only when the registering contract explicitly permits it.

A Generated Target Name is produced during target lowering. It MAY differ from the source spelling to satisfy target length, character, case, or reserved-word constraints.

Target name mangling MUST be deterministic within the reproducibility envelope, collision-free in the target collision domain, and traceable back to the Canonical Identity Key. A target profile MUST report an error if it cannot produce a valid unique name.

Source lookup MUST NOT use a Generated Target Name.

### 6.17 Resource Bounds

Compilers MUST bound:

- namespace segment count;
- Qualified Name segment count;
- imports per source file;
- ordinary symbols per scope;
- total indexed symbols; and
- candidate identities retained for one ambiguous lookup.

Active limits are deterministic build inputs. Exceeding a limit MUST produce `IMDE3015` and MUST NOT produce a partial resolved Semantic Model.

Required minimum production limits are deferred to the compiler conformance specification. A reference spike MAY use lower declared limits and identify itself as non-conforming.

### 6.18 Diagnostic Expectations

The following diagnostic codes are reserved by this Proposed specification and may be refined before acceptance.

| Code | Severity | Condition | Required facts |
| --- | --- | --- | --- |
| `IMDE3001` | Error | Missing, duplicate, empty, or misplaced Namespace Directive | Failure span and required placement |
| `IMDE3002` | Error | Exact duplicate ordinary symbol in one collision domain | Both declaration identities and spans |
| `IMDE3003` | Error | ASCII case-only collision | Both exact spellings, identities, and spans |
| `IMDE3004` | Error | Unresolved name or import target | Unresolved spelling and searched explicit environments |
| `IMDE3005` | Error | Ambiguous name or import target | Candidate identities and declaration spans |
| `IMDE3006` | Error | Import binding or declaration would create implicit shadowing | Conflicting bindings and scopes |
| `IMDE3007` | Error | Invalid qualified traversal | Failing segment, resolved prefix, and expected view |
| `IMDE3008` | Error | Wildcard, relative, group, or recursive import | Entire unsupported import form |
| `IMDE3009` | Warning | Redundant identical import | Redundant import and first import span |
| `IMDE3010` | Warning | Unused import | Import directive and introduced binding |
| `IMDE3011` | Error | Namespace import lacks alias, target is inaccessible, or target kind is invalid | Import, target facts when available, and required form |
| `IMDE3012` | Error | Import is misplaced after a declaration | Import span and required prefix location |
| `IMDE3013` | Warning | Identifier violates its category's naming convention | Identifier, expected convention, and entity category |
| `IMDE3014` | Error | Namespace contributions cannot merge under one Package Identity | Namespace paths, package facts, and contributing spans |
| `IMDE3015` | Error | Name-index or resolution resource limit exceeded | Active limit, observed count, and affected scope or source |

The general reference-kind mismatch remains `IMDE2009` under RFC-0001A. Later semantic RFCs MAY define a more specific diagnostic for a particular invalid reference context.

Cross-file diagnostics MUST choose primary and related spans deterministically. Until RFC-0001C defines Canonical Source Identity, conformance fixtures MUST provide explicit source identities. Once defined, the declaration with the lexicographically greater `(Canonical Source Identity, raw start, raw end)` tuple is the primary duplicate span and the lower tuple is related information.

A fix-it is optional. A compiler MUST NOT silently rename a declaration, qualify a reference, remove an import, or change capitalization.

## 7. Determinism and Ordering

Given identical source bytes, language versions, Package Identities, dependency graph, compiler configuration, and resource limits, a conforming resolver MUST produce identical:

- Namespace Identities and merge groups;
- binding sets and collision results;
- Canonical Identity Keys;
- import targets and aliases;
- resolution results and ambiguity candidate sets;
- semantic dependency edges introduced by names;
- diagnostic codes, severities, primary spans, related spans, and ordering.

Canonical semantic ordering MUST compare structured identity components in this order:

1. Package Identity according to RFC-0001C;
2. Namespace Path segments by exact ASCII byte sequence;
3. owning declaration path segments by exact ASCII byte sequence;
4. Identifier Spelling by exact ASCII byte sequence; and
5. a stable semantic entity-kind ordinal defined by the Semantic Model contract.

The ASCII Case-Folded Key is used for collision detection, not canonical ordering.

Filesystem traversal, source-file discovery, declaration order, import order, thread scheduling, locale, target case rules, and hash-map iteration MUST NOT choose a resolution result.

Diagnostics follow the global deterministic ordering contract from RFC-0000. Candidate lists inside a diagnostic MUST use Canonical Identity Key ordering.

## 8. Compatibility and Migration

### 8.1 Stable Identity Changes

Renaming a declaration, moving it to another namespace, moving it below another owner, changing its semantic entity kind, or moving it to another Package Identity changes its Canonical Identity Key.

Such a change requires impact analysis for:

- imports and qualified references;
- Instance Identity paths;
- deployment mappings;
- retained or persistent storage identities when later defined;
- generated target names; and
- external traceability references.

Physical file relocation alone is identity-preserving when Package Identity, Namespace Path, owner path, spelling, and entity kind remain unchanged.

### 8.2 Import Stability

Adding a new declaration to an imported namespace does not change existing unqualified resolution because namespace imports expose only their alias and wildcard imports are prohibited.

Adding a declaration whose spelling collides with an existing explicit import binding in a consuming file produces a deterministic conflict rather than silently changing lookup priority. Library authors SHOULD treat public namespace additions as compatibility-sensitive when common import aliases are affected.

### 8.3 Case and Naming Style

Case-only renaming changes semantic identity and is prohibited when the old and new declarations coexist in one collision domain. Migration tooling SHOULD treat case-only renames as explicit identity migrations, especially on case-insensitive filesystems and targets.

Changing a naming-style Warning policy does not change semantic identity. Promoting a Warning to an Error in a build profile changes build acceptance and MUST be an explicit versioned configuration change.

### 8.4 Future Syntax

Introducing wildcard import behavior into a Stabilized language version would change dependency exposure and requires a new language-version contract. A later RFC SHOULD prefer explicit namespace aliases rather than adding wildcard imports.

## 9. Safety and Security Considerations

- ASCII identifiers and ASCII-only case folding avoid locale and Unicode-confusable resolution differences.
- Case-only collisions are rejected before target lowering, reducing cross-target symbol collapse.
- Explicit imports prevent dependency additions from silently injecting symbols.
- No parent-namespace or filesystem search prevents environment-dependent lookup.
- Unified ordinary-symbol collision domains prevent hidden type-versus-value reinterpretation.
- Resource limits protect the symbol index and ambiguity reporting from adversarial graphs.
- Import resolution MUST treat manifests and packages as untrusted input under RFC-0001C.
- Diagnostics MUST NOT expose inaccessible dependency contents across a tooling trust boundary.
- External tags and generated names remain outside source resolution, preserving reviewed semantic identity.

These rules do not establish process safety, target safety, package authenticity, or generated-symbol correctness. Those properties require their owning RFCs and engineering validation.

## 10. Tooling and Incremental Compilation

Tooling SHOULD retain, for every binding and reference:

- exact Identifier Spelling;
- ASCII Case-Folded Key;
- Canonical Identity Key when resolved;
- declaration and reference raw spans;
- identity-bearing owner scope;
- file-local Import Environment;
- resolution state and candidate identities; and
- semantic dependency edges.

A namespace index SHOULD be reusable across source files that contribute to the same logical namespace. Its cache key MUST include Package Identity, Namespace Path, contributing public binding fingerprints, effective language versions, and relevant configuration.

Changing an import directive invalidates at least the importing source file's name-resolution result. Changing a declaration spelling or owner invalidates references to the old identity and collision checks in the affected scope. Adding a member to one Definition does not invalidate unrelated owner scopes unless their semantic dependency graph references that Definition's Member View.

An IDE rename operation MUST resolve the target identity before editing and MUST distinguish declaration references from coincidentally equal strings, metadata, comments, external tags, and generated names.

Go-to-definition and find-references SHOULD expose import aliases as indirections while preserving the imported declaration identity.

The concrete compilation-unit boundary, public API hash, cache serialization, and invalidation graph are defined by RFC-0001C and the compiler specification.

## 11. Examples

Declaration syntax outside namespace and import directives is conceptual unless owned by another RFC.

### 11.1 Positive: Explicit Namespace and Imports

```plant
dsl "0.1";

namespace Process.WaterTreatment;

import Common.Motors.MotorVfd;
import Common.Sensors as Sensors;
import Legacy.Systems.Pump as LegacyPump;
```

The file receives one Namespace Identity under its Package Identity. It has three file-local bindings: `MotorVfd`, `Sensors`, and `LegacyPump`. Members of `Common.Sensors` are available only through `Sensors.<name>`.

### 11.2 Positive: Merged Namespace Across Files

File `Pumps.plant`:

```plant
dsl "0.1";
namespace Process.WaterTreatment;

// Conceptual declaration syntax.
definition PumpStation { }
```

File `Tanks.plant` in the same package:

```plant
dsl "0.1";
namespace Process.WaterTreatment;

definition BufferTank { }
```

Both declarations belong to one merged logical namespace. Swapping discovery order does not change their identities or order.

### 11.3 Positive: Repeated Members in Independent Scopes

```text
definition Motor {
    endpoint status;
}

definition Valve {
    endpoint status;
}
```

`Motor.status` and `Valve.status` are legal because each Definition owns a separate member scope. Neither declaration shadows the other.

### 11.4 Positive: Instance Member Traversal

```text
application WaterTreatment {
    instance station_1 : PumpStation;
}

reference WaterTreatment.station_1.main_pump.start_command;
```

Resolution proceeds left to right. The final path identifies an Endpoint occurrence through explicit Application Assembly, root Instance, child Instance, and Endpoint member views.

### 11.5 Negative: Duplicate Across Namespace Contributions

Two files in the same package and namespace each declare:

```text
definition PumpStation { }
```

Expected result: one deterministic `IMDE3002` with both declaration spans. File discovery order does not select a winner.

### 11.6 Negative: Case-Only Collision

```text
definition Pump { }
definition pump { }
```

Expected result: `IMDE3003`, even though RFC-0001 token spelling is case-sensitive.

### 11.7 Negative: Wildcard Import

```plant
dsl "0.1";
namespace Process.WaterTreatment;
import Common.Sensors.*;
```

Expected result: `IMDE3008`. The applicable migration is a namespace alias or explicit declaration import.

### 11.8 Negative: Namespace Import Without Alias

```plant
dsl "0.1";
namespace Process.WaterTreatment;
import Common.Sensors;
```

If `Common.Sensors` resolves to a logical namespace, expected result is `IMDE3011`. A namespace import must declare an alias, for example `import Common.Sensors as Sensors;`.

### 11.9 Negative: Import Binding Conflict

```plant
dsl "0.1";
namespace Process.WaterTreatment;

import Common.Motors.MotorVfd as Pump;
import Legacy.Pumps.Pump;
```

Expected result: `IMDE3006`. Import order does not select either binding.

### 11.10 Negative: No Implicit Parent Namespace Search

```plant
dsl "0.1";
namespace Process.WaterTreatment.Control;

// PumpStation exists in Process.WaterTreatment only.
```

An unqualified reference to `PumpStation` produces `IMDE3004` unless the declaration is explicitly imported or qualified. The resolver does not search `Process.WaterTreatment` automatically.

### 11.11 Naming-Convention Diagnostics

```text
definition Motor_VFD { }
instance MainPump : MotorVfd;
constant default_timeout;
```

Each identifier is lexically valid. Under the Proposed convention policy, each produces `IMDE3013` as a Warning with the expected category convention. The compiler does not infer or alter entity kind from capitalization.

### 11.12 Boundary Fixtures

Conformance fixtures MUST include:

- namespace and alias segments of exactly 255 ASCII characters;
- one 256-character segment rejected lexically by RFC-0001;
- the active maximum number of Qualified Name segments and one above it;
- the active maximum imports per file and one above it;
- exact duplicates and case-only collisions across separate source files;
- identical namespace paths in the same and in different Package Identities;
- namespace-versus-declaration collisions in one parent scope;
- a qualified path that fails at its first, middle, and final segment;
- redundant identical imports and conflicting import aliases;
- repeated member spellings in independent Definition scopes; and
- randomized file discovery and hash insertion order producing identical results.

### 11.13 Compatibility Fixture

Version 1 imports a namespace alias:

```plant
import Common.Sensors as Sensors;
```

Version 2 of the dependency adds `FlowSensor`. Existing unqualified bindings in the consumer do not change because the new declaration is accessible only as `Sensors.FlowSensor` when referenced explicitly.

## 12. Alternatives Considered

### 12.1 Wildcard Imports

Rejected because adding a public declaration to a dependency could make unchanged consumer source ambiguous or silently redirect a binding.

### 12.2 Filesystem-Derived Namespaces

Rejected because checkout layout, source roots, case behavior, and build-system conventions would become semantic inputs without explicit source declarations.

### 12.3 Globally Merged Namespace Paths

Rejected because unrelated packages could inject declarations into one logical scope. Namespace Identity includes Package Identity.

### 12.4 Case-Insensitive Source Names

Rejected because source spelling remains significant for readability, APIs, and traceability. The language is case-sensitive but prohibits case-only siblings for target portability.

### 12.5 Deferring Case Collisions to Target Lowering

Rejected because a model valid for one target could contain two semantically distinct names that collapse on another. The core prevents the most common portable collision; targets may add stricter rules.

### 12.6 Separate Type and Value Symbol Namespaces

Rejected for the foundational model because the same spelling could resolve differently as syntax evolves. One ordinary-symbol collision domain per owner gives safer diagnostics and simpler tooling.

### 12.7 Absolute Anti-Shadowing Across All Owners

Rejected because natural member names such as `status`, `enable`, and `value` must be reusable in independent Definitions and Instance paths. Shadowing is prohibited only where bindings compete for the same unqualified reference context.

### 12.8 Implicit Parent Namespace Search

Rejected because moving a file or adding a declaration to a parent namespace could change unqualified resolution. Parent access requires explicit qualification or import.

## 13. Unresolved Questions and Delegated Decisions

The following table records the remaining design gates. At Proposed status, each gate has a precise review disposition or an explicit owning dependency. Before this RFC becomes Accepted, every gate that changes normative behavior MUST be resolved by compatible Accepted contracts.

| Topic | Current Proposed direction | Owner |
| --- | --- | --- |
| Package root ownership | Namespace Identity includes Package Identity; manifest rules remain undefined | RFC-0001C |
| Package-qualified import syntax | Imports use a Qualified Name; disambiguation among packages remains undefined | RFC-0001C and this RFC revision |
| Module scope | No module scope is introduced here | RFC-0001C |
| Import-cycle policy | Name imports do not authorize cycles; graph node and cycle rules remain undefined | RFC-0001C |
| Visibility defaults | Imports cannot bypass visibility; `public` and `private` semantics remain undefined | RFC-0001C |
| Public re-export | Prohibited in `0.1` unless a later revision defines an explicit form | RFC-0001C and compatibility review |
| Language prelude | No implicit prelude is assumed by this Proposed specification | RFC-0002 and RFC-0011 |
| Behavior-local scopes | Must not introduce implicit shadowing | RFC-0003 and RFC-0004 |
| Interface member binding | Must be explicit and distinct from redeclaration | RFC-0006 |
| Naming-style severity | Warning in this Proposed specification; Stabilized production policy unresolved | This RFC review |
| Minimum name-resource limits | Limits are required but minimum production values are unset | Compiler conformance specification |

An unresolved item MUST NOT be filled by implementation-specific behavior. Until its owning contract is Accepted, tools MUST reject forms that require the missing semantics or identify them as non-conforming experimental behavior.

## 14. Conformance Requirements

An implementation conforms to an Accepted version of this RFC only if it:

- requires one correctly placed Namespace Directive in every semantically compiled source file;
- constructs Namespace Identities from Package Identity and exact Namespace Path segments;
- merges namespace contributions only inside one Package Identity;
- rejects exact and ASCII case-only collisions in every required collision domain;
- uses one ordinary-symbol namespace per identity-bearing owner;
- resolves qualified names left to right without backtracking;
- performs no implicit parent, sibling, filesystem, or transitive-dependency search;
- supports explicit declaration and namespace-alias imports with file-local bindings;
- rejects wildcard, relative, group, and recursive imports;
- prevents implicit shadowing while permitting repeated names in independent owner scopes;
- constructs stable structured Canonical Identity Keys;
- keeps external and generated names outside source resolution;
- emits the required deterministic diagnostic facts;
- enforces deterministic resource limits; and
- passes the positive, negative, boundary, compatibility, and randomized-order fixtures.

Conformance to this RFC alone does not establish conformance to a complete IndustrialMDE language release. Cross-package import conformance additionally requires RFC-0001C.

## 15. Non-Normative Implementation Notes

A compiler will commonly use separate implementation structures for:

- a merged namespace index;
- owner-member symbol tables;
- file-local import environments;
- exact-spelling and ASCII-folded collision indexes;
- structured identity interning; and
- resolved-reference dependency edges.

Those structures are implementation choices. Published phase artifacts MUST remain immutable under the governing compiler contracts.

The resolver can avoid quadratic collision checks by indexing both exact spellings and ASCII Case-Folded Keys. It SHOULD retain all candidates for deterministic diagnostics rather than whichever candidate was inserted first.

No parser framework, object-model library, hash implementation, or filesystem API is part of this language contract.

## 16. Change Log

### Proposed — 2026-07-20

- Advanced from Draft after the project-owner semantic audit approved the complete text without normative changes.
- Recorded the language-prelude governance risk as delegated to RFC-0002 and RFC-0011.
- Updated status metadata, glossary entries, and Project Brain tracking without changing language semantics.

### Draft — 2026-07-19

- Created the initial identifier, scope, namespace, qualification, import, collision, and naming-convention proposal.
- Preserved the 255-character ASCII identifier contract from RFC-0001.
- Preserved Definition, Instance Declaration, expanded Instance, Endpoint, and identity distinctions from RFC-0001A.
- Delegated package, module, dependency, visibility, and import-cycle semantics to RFC-0001C.
