# RFC-0007: Application and Deployment

**Status:** Draft

**Authors:** IndustrialMDE Project

**Created:** 2026-07-23

**Last Updated:** 2026-07-23

**Target Language Version:** Pre-1.0; experimental language version `0.1` structural subset

**Dependencies:** RFC-0000, RFC-0001, RFC-0001A, RFC-0001B, RFC-0001C, RFC-0005 Structural Layer, RFC-0006 Structural Layer

**Supersedes:** None

**Superseded By:** None

**Implementation Status:** Not Started

**Review:** Draft review artifact for Structural Reference Spike A

## 1. Summary

This RFC drafts the minimum Application Assembly contract required to select and expand one target-neutral structural graph in Structural Reference Spike A.

An Application Assembly is a named semantic owner distinct from Project, Package, Definition, Instance, and Deployment Model. It may own zero or more root Instance Declarations and zero or more application-level Connection Declarations between immediate root Instance Endpoints.

One compiler invocation must select exactly one Application Assembly by complete resolved Declaration Identity. Selection is an extralinguistic build input supplied by an invocation or future Project metadata contract. This Draft introduces no Application Assembly selector grammar.

Deployment Models, Target Profiles, physical resources, addresses, and mappings remain deferred. This Draft is non-normative and does not authorize production deployment or target implementation.

## 2. Motivation

RFC-0001A establishes Application Assembly as the target-neutral semantic graph root and explicitly permits multiple root Instance Declarations and application-level Connections. RFC-0001C establishes Project and root Package Revision as build boundaries. RFC-0006 requires one selected Assembly to own the expansion forest.

Without an explicit selection contract, an implementation might:

- assume a single synthetic root Instance;
- choose the first Assembly in source or filesystem order;
- infer an entry from a spelling such as `main`;
- select the only currently visible Assembly and change behavior when another is added;
- enter a dependency Package accidentally; or
- treat a Deployment Model or target as the structural root.

Those choices would make expansion dependent on source organization or implementation defaults. The minimum subset needs a deterministic, target-neutral entry boundary without prematurely defining language grammar or deployment semantics.

## 3. Goals

- Define Application Assembly as a distinct named semantic owner.
- Preserve zero-to-many root Instance Declarations.
- Preserve application-level Connections between immediate roots.
- Select exactly one Assembly per structural compilation invocation.
- Require selection by complete resolved Declaration Identity.
- Restrict Spike A entry points to the root Package Revision.
- Permit dedicated entry lookup of a private root-Package Assembly.
- Prohibit implicit selection, discovery, and source-order fallback.
- Keep the selector outside `.plant` language grammar.
- Keep deployment, target mapping, and physical resources outside the structural subset.

## 4. Non-Goals

This structural revision does not define:

- final Application Assembly source syntax;
- selector CLI spelling, environment-variable spelling, or manifest JSON field;
- discovery of a default or conventional Assembly;
- deployment grammar or Deployment Model serialization;
- Target Profiles, target capabilities, hardware resources, memory, tasks, networks, or addresses;
- mappings from logical identities to physical resources;
- generated names, vendor projects, or emitters;
- coordinated multi-Assembly deployment;
- runtime startup, execution order, scheduling, or shutdown;
- configuration expressions, values, initializers, or overrides;
- public visibility rules beyond the dedicated root-entry restriction; or
- Canonical IR, Target IR, or production artifacts.

## 5. Terminology

- **Application Assembly** — a named, target-neutral semantic owner of root Instance Declarations and application-level Connection Declarations.
- **Assembly Declaration Identity** — the complete RFC-0001B/RFC-0001C Declaration Identity of one Application Assembly.
- **Assembly Selector** — an extralinguistic build input naming exactly one Assembly Declaration Identity.
- **Root Instance Declaration** — an Instance Declaration owned directly by an Application Assembly.
- **Root Instance Occurrence** — the parentless Instance occurrence produced from a root Instance Declaration.
- **Root Package Revision** — the exact root Package selected by the RFC-0001C Project.
- **Dependency Assembly** — an Application Assembly declared by a resolved dependency Package Revision.
- **Deployment Model** — a target-specific binding root established by RFC-0001A and deferred here.

## 6. Normative Specification

### 6.1 Application Assembly Kind

An Application Assembly MUST:

- be explicitly named;
- have one stable Declaration Identity after resolution;
- belong to exactly one Package Revision and compilation ownership context;
- preserve its declaration origin;
- own an ordered collection of zero or more root Instance Declarations;
- own an ordered collection of zero or more application-level Connection Declarations; and
- remain target-neutral.

An Application Assembly is not:

- a Project or Project Manifest;
- a Package or Module;
- a Definition;
- an Instance or synthetic root Instance;
- a Deployment Model; or
- a target artifact.

The Assembly acts as a virtual owner over an Instance forest. Implementations MUST NOT invent a semantic wrapper Definition or wrapper Instance merely to obtain a single tree root.

### 6.2 Root Instance Declarations

Each root Instance Declaration MUST satisfy RFC-0006 and reference exactly one resolved named Definition.

An Application Assembly MAY own `0..N` root Instance Declarations. Multiple roots are valid and retain independent Instance Occurrence Identities whose declaration paths begin with their respective root Instance Declaration Identities.

A root Instance occurrence has:

- the selected Assembly Declaration Identity;
- a declaration path beginning with its creating root Instance Declaration Identity; and
- no parent Instance Occurrence Identity.

The order of root declarations is retained as declaration ordinal but is not substituted for structured identity.

### 6.3 Application-Level Connections

An Application Assembly MAY own `0..N` application-level Connection Declarations.

Each application-level Connection MUST:

- be explicitly named;
- reference Endpoints owned by immediate root Instance occurrences only;
- obey the Application Assembly row of the RFC-0005 direction table;
- obey exact RFC-0002 type compatibility;
- participate in duplicate-driver validation; and
- retain the Assembly Declaration Identity as its Owner Context Identity.

An application-level Connection MUST NOT:

- reference a grandchild or deeper descendant;
- reference an implicit Assembly Endpoint;
- cross into another Application Assembly;
- cross into a Deployment Model or target resource;
- contain an expression, value, conversion, or transformation; or
- imply runtime transfer order.

### 6.4 Exactly One Selected Assembly

Every Spike A structural compilation invocation MUST contain exactly one Assembly Selector.

The selector MUST resolve to exactly one Application Assembly Declaration Identity. The compiler MUST reject:

- a missing selector;
- more than one selector;
- an unresolved identity;
- an identity that resolves to a non-Assembly kind;
- an ambiguous or incomplete identity;
- a dependency-Package Assembly; and
- a selector whose Package Revision is not the Project's root Package Revision.

Selection occurs after Project, Package, Module, Namespace, and declaration resolution have established the complete candidate identity. It occurs before RFC-0006 expansion.

### 6.5 Complete Identity, Not Discovery

The selector MUST carry the complete Canonical Declaration Identity required by RFC-0001B and RFC-0001C. A display name alone is insufficient when it omits Package, Namespace, or owner components.

The implementation MUST NOT select an Assembly by:

- implicit spelling such as `main`, `default`, or the Project name;
- choosing the only Assembly currently found;
- source order;
- file discovery order;
- directory or filename convention;
- export order;
- target selection;
- a Deployment Model encountered in source; or
- a cached selector from an earlier invocation.

Adding, removing, or reordering unrelated source files MUST NOT change entry selection.

### 6.6 Root-Package Restriction

For the experimental language version `0.1` subset, the selected Application Assembly MUST belong to the root Package Revision selected by the Project.

An Assembly declared by a dependency Package Revision MUST NOT be an entry point, even when it is otherwise public or name-resolvable.

The dedicated Assembly entry lookup MAY select a private Assembly declared in the root Package Revision. This lookup is an invocation operation, not ordinary cross-Package reference visibility and not an implicit export.

This restriction avoids treating dependency examples, templates, or test Assemblies as executable project roots. A future RFC may revise the rule only with explicit packaging, visibility, compatibility, and security analysis.

### 6.7 Extralinguistic Selector Boundary

The selector is not part of `.plant` source grammar in this Draft.

An experimental implementation MAY receive it through:

- a compiler invocation parameter;
- test-fixture metadata;
- build-system metadata; or
- a future explicitly versioned Project Manifest field owned by RFC-0001D or a compatible amendment.

The concrete spelling and serialization of these channels are implementation or owning-contract concerns. No example in this RFC authorizes a source-language keyword or production CLI option.

The effective selector is a complete build input. It MUST participate in reproducibility, cache keys, diagnostic context, and snapshot provenance.

### 6.8 Empty Assembly

An explicitly selected Application Assembly with zero root Instance Declarations and zero Connections is structurally valid.

The empty Assembly expands to an empty forest and empty Connection overlay. Profiles, products, or future deployment contracts MAY require a non-empty Assembly, but Spike A MUST NOT invent that requirement.

### 6.9 Expansion Boundary

After successful selection:

1. the selected Assembly becomes the virtual owner context;
2. RFC-0006 expands every root Instance Declaration;
3. Definition-owned Connections are instantiated in their Instance contexts;
4. application-level Connections are instantiated in the Assembly context;
5. RFC-0005 validates the complete Connection overlay; and
6. the Spike A publication gate decides whether to emit the experimental snapshot.

Unselected Assemblies MAY be resolved sufficiently for ordinary declaration diagnostics, but they MUST NOT contribute occurrences to the selected Assembly's snapshot.

One Assembly's root Instances, Endpoints, and Connections MUST NOT be merged with another Assembly's graph.

### 6.10 Deployment Separation

The Application Assembly Plane MUST remain target-neutral.

The structural subset MUST reject or classify as unsupported:

- Deployment Models;
- Deployment Mappings;
- Target Profile selections;
- target capability data;
- controller, rack, slot, channel, network, address, memory, or task bindings;
- generated vendor names; and
- physical communication routes.

Target selection MUST NOT influence Assembly selection, occurrence identity, structural validation, or the experimental snapshot.

The complete RFC-0007 may later define Deployment Models that reference one Application Assembly as required by RFC-0001A. That future layer is not defined by this Draft.

### 6.11 Selection Diagnostics

Spike A MUST use the experimental diagnostic domain defined by `Spike_A_Experimental_Snapshot.md` for selector failures. This Draft registers no new `IMDE` code.

A selector diagnostic MUST include:

- the supplied selector, if any;
- expected semantic kind;
- actual resolution result or failure reason;
- root Package Revision identity;
- actual owning Package Revision when resolved; and
- invocation or metadata origin.

An invalid selector suppresses expansion diagnostics that require a selected Assembly.

## 7. Determinism and Ordering

Given identical complete build inputs and the same selector, the implementation MUST produce identical:

- selected Assembly Declaration Identity;
- root declaration order and identities;
- expanded occurrence graph;
- application-level Connection resolution;
- diagnostic facts and ordering; and
- snapshot provenance.

Candidate enumeration order MUST NOT influence selection. If candidate identities are displayed in a diagnostic, they are sorted by canonical structured identity.

The Assembly selector itself is identity-bearing build input, not semantic source syntax.

## 8. Compatibility and Migration

Renaming or moving an Application Assembly changes its Declaration Identity under RFC-0001B and RFC-0001C and therefore requires updating selectors.

Changing root Instance Declaration Identity, referenced Definition, or application-level Connections changes the structural graph and snapshot.

Adding a second Assembly MUST NOT change an invocation that still selects the original complete identity.

This Draft establishes no stable CLI, manifest, wire, snapshot, or deployment compatibility. Experimental selector and snapshot encodings may change incompatibly.

## 9. Safety and Security Considerations

- Explicit selection prevents accidental execution or analysis of an unintended Assembly.
- The root-Package restriction prevents a dependency from becoming an entry point through name collision or discovery order.
- Target neutrality prevents physical mappings from hiding inside the logical graph.
- Multiple-root support avoids a synthetic privileged Instance whose semantics were never declared.
- Treating the selector as a complete build input supports reproducibility and cache isolation.

Structural selection does not establish authorization to deploy, execute, or control equipment. Deployment approval, target qualification, hazard analysis, and commissioning remain outside this subset.

## 10. Tooling and Incremental Compilation

Tooling MUST be able to:

- list Application Assembly Declaration Identities deterministically;
- distinguish root-Package and dependency-Package Assemblies;
- navigate the selected Assembly to roots and application-level Connections;
- report selector origins separately from source origins;
- invalidate expansion when the selected identity or selected Assembly changes; and
- avoid invalidating the selected graph solely because an unrelated unselected Assembly changes, except where shared dependencies require it.

An IDE MAY offer candidate completion. It MUST NOT write an implicit selection or reinterpret ordinary visibility as entry authorization.

## 11. Examples

All selector and source-like examples are conceptual and do not establish grammar or CLI spelling.

### 11.1 Positive: Multiple Roots

```text
application WaterTreatment {
    instance process : ProcessArea;
    instance utilities : UtilityArea;
    connection utility_status {
        source utilities.available;
        destination process.utility_available;
    }
}
```

The Assembly owns two root Instances and one application-level Connection. It is not represented as one wrapper Instance.

### 11.2 Positive: Complete Selector

```json
{
  "package_identity": ["example.org", "water-treatment"],
  "namespace_path": ["applications"],
  "declaration_path": ["WaterTreatment"],
  "declaration_kind": "application-assembly"
}
```

This shape is illustrative fixture metadata. It does not define a Project Manifest field.

### 11.3 Positive: Private Root-Package Assembly

A dedicated entry lookup resolves a complete private Assembly identity in the root Package Revision. The same declaration remains unavailable to ordinary dependency consumers unless RFC-0001C exports it.

### 11.4 Negative: Missing Selector

The Project contains two Assemblies and the invocation supplies none. Spike A reports `SPIKEA003`; it does not choose either Assembly.

### 11.5 Negative: Dependency Entry

The selector resolves to an exported example Assembly in a direct dependency. Spike A rejects it because the Package Revision is not the Project root.

### 11.6 Negative: Implicit `main`

An Assembly named `main` receives no special treatment. Without its complete explicit selector, expansion does not begin.

### 11.7 Boundary: Empty Assembly

An explicitly selected empty Assembly publishes a valid empty experimental snapshot after the normal publication gate.

## 12. Alternatives Considered

### 12.1 Select the Only Assembly

Rejected because adding another declaration would silently change build validity and because enumeration order is not an entry contract.

### 12.2 Reserved `main` Grammar

Rejected for Spike A because entry selection belongs to the build boundary and final grammar is not authorized.

### 12.3 One Synthetic Root Instance

Rejected because RFC-0001A permits multiple root Instance Declarations and makes the Application Assembly itself the semantic graph root.

### 12.4 Deployment Model as Entry

Rejected because it would make structural identity and validation depend on target selection before the Deployment contract exists.

### 12.5 Dependency Assemblies as Entry Points

Rejected for version `0.1` because it complicates project ownership, visibility, security, and reproducibility without helping the first structural slice.

## 13. Unresolved Questions

The following are delegated and do not block the structural slice:

- final selector CLI or build API;
- whether a future RFC-0001D schema adds an Assembly selector field;
- coordinated multi-Assembly deployment;
- deployment selection and Target Profile semantics;
- public distribution of runnable Assembly templates; and
- production authorization and deployment lifecycle.

No unresolved question in this slice requires expression parsing, state execution, or target mapping.

## 14. Conformance Requirements

A Structural Layer implementation satisfies this Draft subset only if it:

- models Application Assembly as a distinct target-neutral owner;
- supports zero-to-many root Instance Declarations;
- supports application-level Connections between immediate roots;
- selects exactly one Assembly by complete resolved Declaration Identity;
- prohibits every implicit and discovery-based fallback;
- restricts entry selection to the root Package Revision;
- permits dedicated lookup of a private root-Package Assembly;
- treats the selector as an extralinguistic complete build input;
- accepts an explicitly selected empty Assembly;
- creates no synthetic root Instance; and
- includes no deployment or target facts in the structural graph.

Planned fixtures include empty, single-root, and multiple-root Assemblies; root-to-root Connections; missing, multiple, wrong-kind, unresolved, and dependency selectors; private root entry; duplicate display names with distinct complete identities; randomized source enumeration; and target-independent output.

## 15. Non-Normative Implementation Notes

An experimental compiler API may accept a typed Assembly selector object rather than a string. Test fixtures should record the selector separately from `.plant` source.

The resolver should establish all candidate Declaration Identities before entry selection. The expander should receive one resolved Assembly handle and must not perform discovery.

## 16. Change Log

| Date | Change |
| --- | --- |
| 2026-07-23 | Initial Draft defining explicit target-neutral Application Assembly selection and multiple-root expansion for Spike A |
