# RFC-0006: Composition and Interfaces

**Status:** Draft

**Authors:** IndustrialMDE Project

**Created:** 2026-07-23

**Last Updated:** 2026-07-23

**Target Language Version:** Pre-1.0; experimental language version `0.1` structural subset

**Dependencies:** RFC-0000, RFC-0001, RFC-0001A, RFC-0001B, RFC-0002, RFC-0005 Structural Layer

**Supersedes:** None

**Superseded By:** None

**Implementation Status:** Not Started

**Review:** Draft review artifact for Structural Reference Spike A

## 1. Summary

This RFC drafts the minimum static composition contract required to expand named Definitions and Instance Declarations into a finite structural graph for Structural Reference Spike A.

The subset defines:

- cardinality-one Instance Declarations;
- acyclic Definition containment;
- direct parent-child composition boundaries;
- deterministic expansion;
- separate declaration and occurrence identity;
- tuple-based Instance, Endpoint, and Connection occurrence identities; and
- mandatory expansion resource limits.

Interfaces, substitution, inheritance, generics, bounded replication, configuration expressions, and runtime behavior remain deferred.

This Draft is non-normative. It does not establish final source grammar, authorize production compiler implementation, or define Canonical IR.

## 2. Motivation

RFC-0001A distinguishes a reusable Definition, an Instance Declaration, and an expanded Instance. It establishes acyclic static expansion and baseline resource capacity. RFC-0005 Structural Layer needs concrete Endpoint occurrences and owner contexts before it can validate Connection locality, direction, type, and drivers.

The initial structural spike therefore needs one deterministic answer for:

- which member categories participate in the experiment;
- how an Instance Declaration selects a Definition;
- how repeated use of one Definition produces distinct occurrences;
- which containment cycles are rejected and when;
- how identities are represented without parser paths or concatenated strings;
- how the expansion forest and Connection overlay remain separate; and
- when an invalid or resource-exhausted model may publish output.

Interface substitution and configuration would add type, visibility, expression, and compatibility obligations that are not needed to test these structural hypotheses.

## 3. Goals

- Define the smallest Definition member subset needed by Spike A.
- Require named, resolved, cardinality-one Instance Declarations.
- Preserve Definition reuse while creating distinct Instance occurrences.
- Reject direct and indirect Definition containment cycles before materialization.
- Restrict structural references to owner and immediate-child boundaries.
- Define structured occurrence identities as mathematical tuples.
- Separate semantic identity from source ordinal and serialization order.
- Bound expansion by depth `64` and `262,144` total expanded semantic entities per selected Application Assembly.
- Prevent invalid or partial expansion from entering the experimental snapshot.
- Keep expansion independent of expressions, runtime execution, state, and targets.

## 4. Non-Goals

This structural revision does not define:

- final Definition, Instance, or member grammar;
- interface declarations, implementation, conformance, substitution, or variance;
- inheritance, traits, mixins, generics, templates, or conditional members;
- anonymous or inline Definitions;
- arrays, collections, dynamic cardinality, or bounded replication;
- instance-specific structural mutation;
- Parameter, Constant, State, Behavior, annotation, or profile execution semantics;
- configuration bindings, initializers, default values, or expressions;
- public member visibility or Export Surface closure;
- runtime object creation or destruction;
- execution order, scheduling, state updates, or Connection transfer behavior;
- target mapping, physical layout, generated names, or deployment; or
- Canonical IR or Target IR schemas.

Unsupported member categories may remain valid language concepts under their owning RFCs. They are not silently erased when the Spike A subset encounters them.

## 5. Terminology

- **Definition Containment Graph** — the directed graph whose nodes are resolved Definition Identities and whose edges are Instance Declarations from an owning Definition to a referenced Definition.
- **Expansion Forest** — the parent-child Instance occurrence forest owned by one selected Application Assembly.
- **Graph Overlay** — Connection occurrences over Endpoint occurrences; it does not change containment ownership.
- **Owner Context Identity** — either an Instance Occurrence Identity for a Definition-owned Connection or an Application Assembly Identity for an application-level Connection.
- **Declaration Path** — the ordered sequence of Instance Declaration Identities from one root declaration through the declaration that creates an occurrence.
- **Occurrence** — one expanded semantic entity associated with a declaration in one owner context.
- **Declaration Ordinal** — deterministic position retained for traceability and traversal; it is not a semantic identity component unless an owning RFC explicitly says otherwise.
- **Reach-Through** — a reference from a composition owner directly to a grandchild or deeper descendant member.

## 6. Normative Specification

### 6.1 Structural Spike Member Subset

For Spike A, a Definition is structurally interpreted only through:

- Endpoint Declarations;
- Instance Declarations; and
- Connection Declarations.

Every admitted declaration MUST remain a distinct semantic kind. A parser or semantic builder MUST NOT coerce an unsupported member into one of these kinds.

If the experimental input contains a Constant, Parameter, State, Behavior, Interface, configuration expression, replication construct, deployment mapping, or another member outside this subset, Spike A MUST produce the experimental unsupported-feature diagnostic and MUST NOT silently ignore the declaration.

This restriction is an experimental implementation boundary, not a claim that RFC-0001A removes those member categories.

### 6.2 Definition

Every Definition admitted by this subset MUST:

- be explicitly named;
- have one resolved Declaration Identity;
- own a statically fixed ordered member collection;
- retain source origins for itself and every member;
- remain independent of any expanded occurrence; and
- participate in containment-cycle analysis.

Anonymous and inline Definitions are prohibited by RFC-0001A and remain prohibited here.

A Definition MAY have no members. A Definition MAY be referenced by zero, one, or many Instance Declarations.

### 6.3 Instance Declaration

Every Instance Declaration MUST:

- be explicitly named;
- have one stable Declaration Identity;
- identify exactly one enclosing Definition or Application Assembly;
- contain exactly one semantic reference that resolves to a named Definition;
- have cardinality exactly one;
- preserve the declaration origin and referenced Definition origin;
- participate in deterministic declaration order; and
- participate in Definition containment-cycle analysis when Definition-owned.

An Instance Declaration MUST NOT:

- resolve to an Interface, Instance, Endpoint, value, target, or another non-Definition kind;
- contain an anonymous or inline Definition;
- add, remove, replace, or mutate members of the referenced Definition;
- choose a Definition through an expression, runtime dispatch, target selection, or profile callback;
- create a variable number of Instances; or
- contain a nested structural member that is absent from its referenced Definition.

Configuration bindings and contextual roles remain outside Spike A even where RFC-0001A reserves them for later contracts.

### 6.4 Definition Containment Graph

For every Definition-owned Instance Declaration `i`:

```text
containment_edge(i) =
    (i.owner_definition_identity,
     i.referenced_definition_identity,
     i.declaration_identity)
```

The Definition containment graph MUST be acyclic.

Cycle detection MUST complete before expansion materializes Instance or Endpoint occurrences. If a direct or indirect cycle exists:

- compilation MUST fail with RFC-0001A `IMDE2001`;
- the diagnostic MUST preserve the deterministic cycle path and participating Instance Declaration origins;
- no depth-limited partial expansion may be used as semantic recovery; and
- no experimental structural snapshot may be published.

The graph algorithm MUST operate on resolved Definition Identity, not source spelling, parser-object identity, or file path.

### 6.5 Composition Boundary

Within one expanded Definition context, structural relationships MAY address only:

- the current owner Instance (`self`); and
- immediate child Instances produced by Instance Declarations owned directly by that Definition.

Within an Application Assembly, structural relationships MAY address only immediate root Instances declared directly by that Assembly.

Reach-through to a grandchild or deeper descendant is prohibited. A nested Definition must expose an Endpoint on each boundary crossed, and each owner must declare the corresponding Connection.

This rule establishes a Spike A boundary-visible subset. It does not settle the complete public/private member-visibility model, which remains delegated to RFC-0001C and the full RFC-0006 contract.

### 6.6 Application Expansion Root

Expansion operates on exactly one explicitly selected Application Assembly under RFC-0007.

The Application Assembly is a virtual owning root over an Instance forest. It is not an Instance and does not require one synthetic root Instance.

The selected Assembly MAY contain zero or more root Instance Declarations. Each root declaration creates one root Instance occurrence with no parent Instance.

### 6.7 Deterministic Expansion

After successful cycle validation, expansion MUST:

1. enter the selected Application Assembly owner context;
2. visit root Instance Declarations in deterministic declaration order;
3. create one root Instance occurrence for each declaration;
4. create Endpoint occurrences from the referenced Definition's Endpoint Declarations;
5. visit child Instance Declarations in deterministic member order;
6. create one distinct child Instance occurrence per declaration and parent context;
7. recursively repeat steps 4 through 6;
8. create Definition-owned Connection occurrences in each applicable Instance context;
9. create Application Assembly-owned Connection occurrences; and
10. pass the complete graph to RFC-0005 structural validation.

Two different Instance Declarations that reference the same Definition MUST create distinct Instance occurrences. The same member Instance Declaration expanded under two different parent occurrences MUST also create distinct child occurrences.

Expansion MUST NOT:

- mutate the resolved Definition graph;
- use source-object addresses as occurrence identity;
- share one mutable Endpoint occurrence between different Instances;
- infer a child from a Connection reference;
- publish an occurrence before the whole selected Assembly has passed the publication gate; or
- depend on parser traversal, filesystem discovery, hash-map order, or concurrency timing.

### 6.8 Structured Occurrence Identities

Occurrence identities are strict mathematical tuples.

```text
InstanceOccurrenceIdentity =
    (ApplicationAssemblyIdentity,
     OrderedPath<InstanceDeclarationIdentity>)

EndpointOccurrenceIdentity =
    (InstanceOccurrenceIdentity,
     EndpointDeclarationIdentity)

ConnectionOccurrenceIdentity =
    (OwnerContextIdentity,
     ConnectionDeclarationIdentity)

OwnerContextIdentity =
    ApplicationAssemblyIdentity
    | InstanceOccurrenceIdentity
```

The ordered path in an Instance Occurrence Identity includes the root Instance Declaration Identity followed by every member Instance Declaration Identity leading to the occurrence.

The tuple elements MUST retain their own structured identity types. An implementation MUST NOT establish semantic equality by concatenating display spellings such as:

```text
"WaterTreatment.station_1.main_pump"
```

Delimiter-concatenated strings MAY be produced only as non-authoritative display text when every identity consumer retains the structured tuple.

Declaration ordinal, source span, target-generated name, external tag, memory address, random UUID, allocation order, and object identity MUST NOT be tuple components.

### 6.9 Occurrence Records

Every Instance occurrence MUST retain:

- Instance Occurrence Identity;
- parent Instance Occurrence Identity, absent for roots;
- resolved Definition Identity;
- creating Instance Declaration Identity;
- deterministic declaration ordinal;
- child occurrence identities; and
- complete declaration-path traceability.

Every Endpoint occurrence MUST retain:

- Endpoint Occurrence Identity;
- owner Instance Occurrence Identity;
- creating Endpoint Declaration Identity;
- direction and Type Identity from RFC-0005; and
- declaration and type-reference origins.

Every Connection occurrence MUST retain:

- Connection Occurrence Identity;
- Owner Context Identity;
- creating Connection Declaration Identity;
- source and destination Endpoint Occurrence Identities;
- declaration ordinal; and
- declaration and reference origins.

Containment ownership and the Connection overlay MUST remain distinguishable. A Connection does not become a containment parent or child.

### 6.10 Resource Limits

The structural contract fixes the Spike A limits at:

```text
maximum expansion depth:              64
maximum expanded semantic entities:   262,144
```

Both limits apply per selected Application Assembly.

Depth counts root Instance occurrences at depth `1`. The empty Assembly has depth `0`.

The expanded-entity counter MUST include every materialized Instance occurrence, Endpoint occurrence, and Connection occurrence admitted to the experimental snapshot. An implementation MAY count additional internal candidate entities conservatively, but it MUST document that choice and MUST NOT claim a higher externally observable capacity.

The implementation MUST check limits before allocating or publishing the next entity. Exceeding either limit produces RFC-0001A `IMDE2011` and MUST NOT publish a partial snapshot.

These fixed Spike A limits satisfy the baseline capacity stated by RFC-0001A. Lower implicit defaults are prohibited.

### 6.11 Invalid and Partial Models

An unresolved, wrong-kind, cyclic, over-limit, or structurally invalid model MUST NOT produce `experimental-structural-snapshot/0`.

An implementation MAY retain build-local invalid placeholders for bounded diagnostic recovery, but:

- placeholders have no valid occurrence identity;
- placeholders MUST NOT enter the published graph;
- a valid-looking node MUST NOT stand in for an unresolved declaration; and
- diagnostics MUST NOT be serialized as graph nodes.

Publication is all-or-nothing for the selected Application Assembly.

### 6.12 Interfaces Deferred

The title retains Interfaces because the complete RFC-0006 roadmap owns them. This Draft does not define an Interface Declaration or substitution relation.

Spike A MUST reject, rather than approximate:

- Interface declarations;
- `implements` or conformance claims;
- structural subtyping;
- member projection;
- substitutable Instance target Definitions; and
- interface-driven Connection binding.

No result from this structural subset may be cited as an Interface compatibility guarantee.

## 7. Determinism and Ordering

Given identical complete build inputs and the same RFC-0007 Assembly selector, expansion MUST produce identical:

- Definition containment-cycle results;
- Instance, Endpoint, and Connection occurrence identities;
- parent-child ownership;
- declaration ordinals;
- source-to-occurrence traceability;
- resource-limit decisions;
- RFC-0005 validation inputs; and
- diagnostics and snapshot publication decisions.

Traversal uses deterministic declaration order. Flat snapshot collections use canonical structured-identity order. These orders are distinct and both are retained.

Canonical comparison of a structured identity MUST compare typed tuple components in their owning canonical order. It MUST NOT compare locale-dependent display strings.

## 8. Compatibility and Migration

Changing any identity-bearing Definition, Instance Declaration, Endpoint Declaration, Connection Declaration, owner, or declaration path changes affected occurrence identities.

Physical file relocation preserves identity only under the RFC-0001B and RFC-0001C rules for unchanged Package, Namespace, owner, and declaration identity. A serialized source path is traceability, not occurrence identity.

This Draft creates no stable public serialization. `experimental-structural-snapshot/0` may change or be discarded and is not a migration format.

## 9. Safety and Security Considerations

- Pre-expansion cycle detection prevents recursive resource amplification.
- Fixed depth and entity limits bound memory and traversal work for the selected Assembly.
- Direct-boundary locality prevents hidden dependencies on arbitrary descendant internals.
- Tuple identities prevent delimiter collision and parser-order dependence.
- All-or-nothing publication prevents partially validated graphs from reaching later consumers.

These guarantees do not validate execution behavior, physical process safety, target capacity, or timing.

## 10. Tooling and Incremental Compilation

Tooling MUST be able to navigate:

- Definition to every Instance Declaration that references it;
- Instance Declaration to every expanded occurrence;
- occurrence to its complete Declaration Path and source origins;
- parent occurrence to deterministic children;
- Endpoint and Connection occurrence to creating declarations; and
- cycle or resource-limit diagnostic to the responsible path.

A structural change to a Definition MUST invalidate expansion for every transitively dependent root Instance Declaration. A change to one Instance Declaration Identity invalidates the identity of that occurrence and every descendant occurrence. A source-only relocation that preserves semantic identity may update origins without changing occurrence identity.

## 11. Examples

All source-like examples are conceptual and do not establish grammar.

### 11.1 Positive: Reused Definition

```text
definition PumpStation {
    instance main_pump : MotorVfd;
}

application WaterTreatment {
    instance station_1 : PumpStation;
    instance station_2 : PumpStation;
}
```

The two `main_pump` occurrences share one member Instance Declaration Identity but have different ordered declaration paths because their root declaration identities differ.

### 11.2 Positive: Structured Identity

```json
{
  "assembly": {
    "declaration_identity": ["package", "namespace", "WaterTreatment"]
  },
  "declaration_path": [
    ["member", "station_1"],
    ["member", "main_pump"]
  ]
}
```

The JSON shape is illustrative. RFC-0012 does not inherit it.

### 11.3 Negative: Direct Cycle

```text
definition A {
    instance again : A;
}
```

Expected result: `IMDE2001` before occurrence materialization.

### 11.4 Negative: Indirect Cycle

```text
definition A { instance b : B; }
definition B { instance c : C; }
definition C { instance a : A; }
```

Expected result: one deterministic cycle path and no snapshot.

### 11.5 Negative: Reach-Through

```text
connection invalid {
    source child.grandchild.output;
    destination self.output;
}
```

The reference crosses more than one child boundary and is rejected under RFC-0005 locality.

### 11.6 Boundary: Empty Assembly

An explicitly selected Application Assembly with zero root Instance Declarations expands to an empty forest and may publish an empty valid snapshot.

### 11.7 Boundary: Expansion Limits

Depth `64` and exactly `262,144` expanded semantic entities are admitted. The next depth level or entity is rejected with `IMDE2011`; no partial snapshot is published.

## 12. Alternatives Considered

### 12.1 One Mutable Definition/Instance Object

Rejected because reuse, per-occurrence identity, traceability, and deterministic invalidation require declarations and occurrences to remain distinct.

### 12.2 Concatenated String Paths

Rejected because delimiters may collide with display forms and strings erase the types of identity components.

### 12.3 Descendant Reach-Through

Rejected because it breaks boundaries and couples an owner to arbitrary nested implementation detail.

### 12.4 Depth-Limited Recovery for Cycles

Rejected because a semantic containment cycle is invalid, not a large finite composition.

### 12.5 Include Interfaces in Spike A

Rejected because substitution requires visibility, public-signature, variance, and compatibility rules not needed for static expansion.

## 13. Unresolved Questions

The following questions are delegated and do not block the defined structural slice:

- final Interface declaration and conformance semantics;
- public and private member visibility;
- bounded static replication and replication-index identity;
- generic specialization and configuration;
- profile-driven structural requirements;
- configuration binding and override rules; and
- final public serialization of occurrence identity.

No unresolved question in this slice requires expression parsing or state execution.

## 14. Conformance Requirements

A Structural Layer implementation satisfies this Draft subset only if it:

- keeps Definition, Instance Declaration, and occurrence records distinct;
- rejects anonymous or inline Definitions and instance-specific structural mutation;
- rejects direct and indirect Definition containment cycles before expansion;
- expands repeated Definitions into distinct occurrences;
- enforces direct-boundary locality;
- constructs the three tuple identity forms exactly;
- never uses delimiter-concatenated strings as semantic identity;
- enforces depth `64` and entity limit `262,144`;
- retains source ordinal separately from identity;
- distinguishes containment from the Connection overlay; and
- publishes no invalid or partial snapshot.

Planned fixtures include empty and nested Definitions, repeated Instance Declarations, multiple roots, direct and indirect cycles, wrong-kind targets, mutation attempts, reach-through, exact limits, limit overflow, tuple delimiter collisions, randomized ordering, and invalid-publication attempts.

## 15. Non-Normative Implementation Notes

A reference implementation may:

1. build an immutable resolved Definition graph;
2. validate containment cycles;
3. expand immutable occurrence records;
4. resolve Connection endpoints within owner contexts;
5. validate RFC-0005 structural rules; and
6. publish the experimental snapshot only after global success.

Cycle detection should operate on Definition Identity before materialization. Expansion may use depth-first traversal over deterministic member order while snapshot serialization later sorts flat records by canonical structured identity.

## 16. Change Log

| Date | Change |
| --- | --- |
| 2026-07-23 | Initial Draft defining the minimal static composition and occurrence-identity subset for Spike A |
