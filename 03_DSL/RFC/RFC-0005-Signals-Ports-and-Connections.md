# RFC-0005: Signals, Ports, and Connections

**Status:** Draft

**Authors:** IndustrialMDE Project

**Created:** 2026-07-23

**Last Updated:** 2026-07-23

**Target Language Version:** Pre-1.0; experimental language version `0.1` structural subset

**Dependencies (Structural Layer):** RFC-0000, RFC-0001, RFC-0001A, RFC-0001B, RFC-0002

**Dependencies (Runtime Layer):** RFC-0003 and RFC-0004

**Supersedes:** None

**Superseded By:** None

**Implementation Status:** Not Started

**Review:** Draft review artifact for Structural Reference Spike A

## 1. Summary

This RFC drafts the minimum target-neutral Endpoint and Connection contract required by Structural Reference Spike A.

The contract is deliberately split into two layers:

1. the **Structural Layer** owns Endpoint identity and direction, Connection identity and locality, exact type compatibility, and duplicate-driver validation; and
2. the **Runtime Layer** owns values, evaluation, transfer timing, sampling, quality, execution order, state interaction, and behavioral cycle semantics.

Only the Structural Layer is defined by this revision. It can be reviewed and exercised without parsing expressions or executing state. The Runtime Layer remains deferred until RFC-0003 and RFC-0004 provide compatible expression and execution contracts.

This Draft is non-normative. It does not make the Spike A snapshot Canonical IR, does not authorize production implementation, and does not establish final source grammar.

## 2. Motivation

RFC-0001A establishes Endpoint Declaration and Connection Declaration as distinct, first-class semantic entities. RFC-0002 establishes exact Type Equality as the minimum Type Compatibility relation. Neither RFC defines the complete contextual rule that answers:

- which Endpoint occurrence may act as a Connection source or destination;
- which composition boundaries a Connection may cross;
- how a Connection Declaration becomes a Connection occurrence;
- whether unequal Endpoint types may connect;
- how fan-out and multiple drivers are represented; or
- which facts may enter a structural snapshot before runtime semantics exist.

Leaving those questions to parser shape, AST traversal, or target lowering would make structural validity implementation-dependent. Defining runtime transfer semantics at the same time would instead pull RFC-0003 and RFC-0004 into the first compiler bootstrap slice. This RFC separates those concerns.

## 3. Goals

- Define the minimum `input` and `output` Endpoint directions.
- Define contextual source and destination capability at a composition boundary.
- Define named, first-class Connection Declarations and expanded Connection occurrences.
- Restrict each Endpoint reference to the owning boundary or one immediate child boundary.
- Invoke exact RFC-0002 Type Equality for structural Connection compatibility.
- Define explicit fan-out and a single-driver structural rule.
- Preserve deterministic identity, ordering, diagnostics, and source traceability.
- Keep Structural Reference Spike A independent of expressions, values, execution, state updates, target mapping, and generated behavior.

## 4. Non-Goals

This structural revision does not define:

- final Endpoint, Port, Signal, or Connection source syntax;
- `inout`, bidirectional ports, buses, channels, events, or message queues;
- values, initializers, defaults, expressions, conversions, or transformations;
- units, scaling, calibration, quality, timestamps, sampling, or freshness;
- scan cycles, transfer timing, scheduling, execution order, or state updates;
- behavioral cycle rejection, algebraic-loop semantics, delays, or buffering;
- target addresses, physical networks, memory, tasks, or vendor mappings;
- interface substitution or public member visibility;
- Canonical IR, Target IR, or an interoperable snapshot encoding; or
- implicit broadcast, hyperedges, or multiple-driver conflict resolution.

If any of these facts is required by an implementation experiment, the feature is unsupported in Spike A and must return to its owning RFC.

## 5. Terminology

- **Endpoint Declaration** — a named, typed interaction boundary owned by one Definition.
- **Endpoint Occurrence** — the per-Instance occurrence of an Endpoint Declaration after structural expansion.
- **Endpoint Reference** — a typed semantic reference that resolves to one Endpoint occurrence in the active composition context.
- **Connection Declaration** — a named, first-class relationship with one explicit source reference and one explicit destination reference.
- **Connection Occurrence** — the relationship produced from a Connection Declaration in one expanded owner context.
- **Owner Endpoint** — an Endpoint occurrence on the current `self` Instance whose Definition owns the Connection Declaration.
- **Child Endpoint** — an Endpoint occurrence on an immediate child Instance of the current owner.
- **Root Endpoint** — an Endpoint occurrence on an immediate root Instance of an Application Assembly.
- **Driver** — a structurally valid Connection source for one destination Endpoint occurrence. This term establishes no scheduling or runtime write behavior.
- **Structural Layer** — the identity, locality, direction, type, and driver-count contract defined by this revision.
- **Runtime Layer** — deferred data-flow and execution behavior owned with RFC-0003 and RFC-0004.

## 6. Normative Specification

### 6.1 Layer Boundary

The Structural Layer MUST answer only whether a resolved, expanded Connection edge is structurally well formed.

A Structural Layer implementation MUST NOT:

- construct or evaluate a runtime value;
- parse or evaluate an initializer or expression for Connection validation;
- infer an Endpoint type from another Endpoint;
- choose a conversion or transformation;
- determine execution or transfer order;
- reject a graph solely because the Connection overlay contains a directed cycle; or
- introduce target-specific data.

A structurally valid Connection is not evidence that the eventual runtime behavior is safe, schedulable, causally well founded, or deployable.

### 6.2 Endpoint Declaration

Every Endpoint Declaration admitted by the structural subset MUST preserve:

- one stable Declaration Identity;
- the Declaration Identity of its owning Definition;
- exactly one direction, `input` or `output`;
- exactly one resolved RFC-0002 Type Identity;
- a primary declaration origin; and
- the Type Reference origin.

Every Endpoint Declaration MUST be named under RFC-0001B. Anonymous Endpoints are unsupported.

An Endpoint Declaration MUST NOT contain a runtime value, initializer, default, conversion, transformation, sampling rule, quality rule, target address, or execution policy in the Structural Layer.

`input` means that a value conceptually enters an Instance through that Instance boundary. `output` means that a value conceptually leaves an Instance through that boundary. These directions establish structural capability only; they do not establish when or how a value moves.

### 6.3 Endpoint Occurrence

Expansion of one Instance MUST create one distinct Endpoint occurrence for each Endpoint Declaration owned by the Instance's resolved Definition.

An Endpoint occurrence MUST retain:

- its structured Endpoint Occurrence Identity from RFC-0006;
- its owning Instance Occurrence Identity;
- its creating Endpoint Declaration Identity;
- direction;
- resolved Type Identity; and
- declaration and type-reference traceability.

Two Instances of the same Definition produce distinct Endpoint occurrences even when they share one Endpoint Declaration.

### 6.4 Composition Context and Direction

Direction capability is interpreted relative to the enclosing Connection owner:

| Connection owner | Endpoint reference | `input` capability | `output` capability |
| --- | --- | --- | --- |
| Definition body expanded for `self` | `self` | Source | Destination |
| Definition body expanded for `self` | Immediate child Instance | Destination | Source |
| Application Assembly | Immediate root Instance | Destination | Source |

The inversion at a child or root boundary follows the boundary viewpoint. A child's `input` receives from its enclosing composition, while a child's `output` supplies that composition. An owner's `input` supplies the interior of that owner, while its `output` receives from the interior.

A source reference MUST resolve to an Endpoint occurrence marked Source in this table. A destination reference MUST resolve to an Endpoint occurrence marked Destination.

An Application Assembly has no implicit `self` Endpoint in this subset.

### 6.5 Connection Declaration

Every Connection Declaration in the structural subset MUST preserve:

- one stable Declaration Identity;
- one enclosing Definition or Application Assembly identity;
- one explicit source Endpoint reference;
- one explicit destination Endpoint reference;
- the declaration origin;
- distinct source-reference and destination-reference origins; and
- deterministic declaration order within its owner.

Every Connection Declaration MUST be explicitly named. Source order alone MUST NOT create Connection Declaration Identity.

A Connection Declaration MUST NOT contain an implicit or explicit transformation in this subset. It MUST NOT encode a value, initializer, execution order, sampling rule, target route, or physical transport.

### 6.6 Reference Locality

A Definition-owned Connection Declaration MAY reference only:

- an Endpoint owned by the current `self` Instance; or
- an Endpoint owned by one immediate child Instance declared directly by that Definition.

An Application Assembly-owned Connection Declaration MAY reference only an Endpoint owned by one immediate root Instance declared directly by that Assembly.

A reference to a grandchild or deeper descendant is prohibited. The descendant's Definition must expose the required interaction through its own boundary Endpoint and explicit intermediate Connections.

Locality is checked after name resolution and semantic-kind checking. A source spelling that resolves to a Definition, Instance Declaration, non-Endpoint member, or unresolved placeholder is not an Endpoint occurrence.

### 6.7 Connection Occurrence

Expansion MUST create:

- one Connection occurrence for each Definition-owned Connection Declaration in every expanded Instance context of that Definition; and
- one Connection occurrence for each Application Assembly-owned Connection Declaration in the selected Assembly context.

Every Connection occurrence MUST preserve:

- the structured Connection Occurrence Identity from RFC-0006;
- the owner context identity;
- the creating Connection Declaration Identity;
- one resolved source Endpoint Occurrence Identity;
- one resolved destination Endpoint Occurrence Identity;
- declaration and reference traceability; and
- a declaration ordinal retained separately from semantic identity.

A Connection occurrence is an immutable graph edge. It is not a mutable pointer stored only on either Endpoint.

### 6.8 Type Compatibility

For source Endpoint occurrence `S` and destination Endpoint occurrence `D`, the structural type rule is:

```text
connection_type_compatible(S, D) iff
    type_equal(S.type_identity, D.type_identity)
```

`type_equal` is the exact RFC-0002 Type Equality relation. The Structural Layer defines no widening, narrowing, subtyping, variance, unit conversion, representation conversion, or target-specific reinterpretation.

An unequal source and destination Type Identity is a Connection-context error. The owning RFC-0005 diagnostic category takes precedence over the general RFC-0002 `IMDE5003`; Spike A uses the experimental diagnostic contract in `Spike_A_Experimental_Snapshot.md` and MUST NOT register a new `IMDE` code.

### 6.9 Fan-Out, Drivers, and Unconnected Endpoints

Fan-out MUST be represented by multiple named Connection Declarations that share a source Endpoint occurrence and have distinct destination Endpoint occurrences.

A destination Endpoint occurrence MUST have at most one structurally valid driver in the expanded graph.

Duplicate-driver validation MUST consider only Connections that have already passed:

1. reference resolution;
2. semantic-kind validation;
3. locality validation;
4. direction validation; and
5. type compatibility.

An invalid Connection MUST NOT suppress an otherwise valid driver or create a second derived diagnostic for the same invalid fact.

An Endpoint occurrence MAY remain unconnected in this subset. Required connectivity, default behavior, environmental bindings, and profile-specific completeness are deferred.

### 6.10 Cycles

The Structural Layer MAY represent a directed cycle in the Connection overlay. It MUST NOT reject a cycle solely from graph topology.

Runtime causality, delay, state interaction, scheduling, and algebraic-loop validity belong to the Runtime Layer and RFC-0004. This rule does not permit Definition containment cycles; RFC-0001A and RFC-0006 reject those before expansion.

### 6.11 Validation Precedence

For each Connection Declaration, validation MUST proceed in this order:

1. ordinary name resolution;
2. semantic-kind checking;
3. Endpoint occurrence resolution in the active owner context;
4. reference-locality checking;
5. source and destination direction checking;
6. exact type compatibility; and
7. duplicate-driver checking across otherwise valid Connections.

An earlier failure suppresses diagnostics that require the missing or invalid fact. One invalid fact produces exactly one most-specific diagnostic under the following precedence matrix:

| Condition | Single diagnostic owner |
| --- | --- |
| Unresolved reference spelling | Applicable RFC-0001B resolution diagnostic |
| Connection reference resolves to a non-Endpoint kind | `IMDE2007` |
| Resolved Endpoint crosses the permitted direct composition boundary | `SPIKEA002(endpoint-locality)` |
| Source or destination has the wrong contextual direction | `SPIKEA002(endpoint-direction)` |
| Resolved Endpoint Type Identities are unequal | `SPIKEA002(connection-type-mismatch)` |
| Otherwise-valid Connections provide more than one driver | `SPIKEA002(duplicate-driver)` |
| Prohibited Deployment Mapping matching the RFC-0001A condition | `IMDE2004` |
| Other recognized unsupported deployment or target construct | `SPIKEA001` |
| Structural expansion exceeds a fixed RFC-0006 limit | `IMDE2011` |
| Publication candidate violates schema or graph integrity | `SPIKEA002(snapshot-schema)` or `SPIKEA002(snapshot-referential-integrity)`, according to the failed rule |

`IMDE2009` remains available for an applicable non-Connection semantic-kind mismatch, but MUST NOT duplicate `IMDE2007`. `IMDE5003` MUST NOT accompany the Connection-specific type-mismatch diagnostic. A construct matching `IMDE2004` MUST NOT also receive `SPIKEA001`.

Diagnostic publication, scope, and global ordering are defined by the Spike A snapshot contract.

## 7. Determinism and Ordering

Given identical complete build inputs and the same selected Application Assembly, the Structural Layer MUST produce identical:

- Endpoint and Connection identities;
- source and destination resolution;
- direction and type-compatibility results;
- driver sets;
- diagnostics and suppression decisions; and
- declaration ordinals and canonical output ordering.

Identity MUST NOT depend on delimiter-concatenated strings, parser-object identity, allocation order, filesystem order, hash-map order, concurrency, target selection, or current time.

Connection occurrences retain declaration order as a traceability ordinal. A serialized structural snapshot orders flat collections by canonical structured identity, not by parser traversal order.

## 8. Compatibility and Migration

Changing any of the following is structurally compatibility-significant:

- Endpoint Declaration Identity, owner, direction, or Type Identity;
- Connection Declaration Identity or owner;
- source or destination Endpoint reference;
- a composition boundary that changes Endpoint Occurrence Identity; or
- any public structural fact later included in an Export Surface.

This Draft defines no public wire or IR compatibility. The experimental Spike A snapshot is explicitly non-interoperable and may change incompatibly.

## 9. Safety and Security Considerations

- Exact type matching prevents target or host defaults from silently connecting unlike intrinsic domains.
- Direct-boundary locality bounds reference traversal and preserves encapsulation.
- The single-driver rule exposes ambiguous structural ownership before runtime lowering.
- Explicit named Connections preserve reviewable traceability.
- Deterministic limits and diagnostic suppression prevent malformed graphs from amplifying work without bound.

Structural validity does not prove process safety, control stability, fail-safe behavior, timing adequacy, or target suitability. Those properties remain external engineering responsibilities unless an Accepted contract defines and verifies them.

## 10. Tooling and Incremental Compilation

Tooling MUST be able to navigate:

- Connection Declaration to source and destination Endpoint Declarations;
- Connection occurrence to both Endpoint occurrences and its owner context;
- Endpoint Declaration to all expanded occurrences;
- Endpoint occurrence to its owning Instance and Type Identity; and
- a structural diagnostic to the Connection and both relevant declarations.

A change to an Endpoint direction or Type Identity MUST invalidate Connections that reference its occurrences. A change to a Connection endpoint reference MUST invalidate the corresponding occurrences and driver analysis. Runtime-only facts MUST NOT be invented as structural cache inputs.

## 11. Examples

All source-like examples are conceptual and do not establish grammar.

### 11.1 Positive: Owner Input to Child Input

```text
definition ControllerCell {
    endpoint enable : input BOOL;
    instance controller : Controller;
    connection enable_controller {
        source self.enable;
        destination controller.enable;
    }
}
```

`self.enable` is source-capable inside `ControllerCell`; `controller.enable` is destination-capable at the child boundary. Both types are `BOOL`.

### 11.2 Positive: Child Output to Owner Output

```text
connection publish_running {
    source controller.running;
    destination self.running;
}
```

The child `output` is source-capable and the owner `output` is destination-capable.

### 11.3 Positive: Explicit Fan-Out

```text
connection distribute_1 { source sensor.value; destination controller_1.value; }
connection distribute_2 { source sensor.value; destination controller_2.value; }
```

The two named Connections share one source and have distinct destinations.

### 11.4 Negative: Direction

```text
connection reversed {
    source child.command;
    destination self.command;
}
```

If both Endpoints are `input`, the child Endpoint cannot be a source and the owner Endpoint cannot be a destination in this context.

### 11.5 Negative: Type Mismatch

```text
source type:      (intrinsic-type, 0.1, INT)
destination type: (intrinsic-type, 0.1, REAL)
```

The Connection is structurally invalid. Spike A reports its Connection-context diagnostic and does not also report `IMDE5003` for the same fact.

### 11.6 Negative: Descendant Reach-Through

```text
source station_1.main_pump.running;
```

From an Application Assembly, `main_pump` is below the immediate root `station_1`. The reference is invalid even when every declaration can otherwise be named.

### 11.7 Boundary: Unconnected Endpoint and Connection Cycle

An unconnected destination is accepted by this subset. A structurally valid directed cycle is retained in the graph and is not classified as runtime-safe or runtime-invalid.

## 12. Alternatives Considered

### 12.1 Define Runtime Data Flow in the First Slice

Rejected because values, transformations, timing, scheduling, and behavioral cycles require RFC-0003 and RFC-0004.

### 12.2 Infer Direction from Source and Destination Position

Rejected because Endpoint direction is an explicit declaration fact and must remain independently reviewable.

### 12.3 Permit Arbitrary Descendant References

Rejected because it breaks composition boundaries, expands invalidation scope, and makes reusable Definitions depend on internal descendant structure.

### 12.4 Permit Implicit Conversion

Rejected for the minimum subset. RFC-0002 defines exact Type Equality and no cross-type conversions.

### 12.5 Store Only Pointers on Endpoints

Rejected by RFC-0001A because Connection identity, ordering, traceability, and diagnostics require a first-class relationship.

## 13. Unresolved Runtime Questions

The Structural Layer has no unresolved question that requires expression parsing or state execution.

The following questions are delegated to the Runtime Layer and MUST NOT be answered by Spike A:

- runtime transfer and update timing;
- sampling, quality, freshness, and event semantics;
- buffering and delayed edges;
- runtime treatment of disconnected Endpoints;
- behavioral cycle and algebraic-loop validity;
- transformations and conversions;
- environmental and target bindings; and
- `inout`, bus, channel, and message semantics.

While RFC-0005 remains one umbrella document, the Structural Layer has no lifecycle status independent of the RFC as a whole. It may be reviewed as an explicit subset, but that review is not a Proposed or Accepted transition.

Before any RFC-0005 transition beyond Draft, the project MUST either split Structural and Runtime contracts into separately governed RFCs or adopt one lifecycle whose gates include the unresolved Runtime Layer. The transition decision MUST state which strategy applies.

## 14. Conformance Requirements

A Structural Layer implementation satisfies this Draft subset only if it:

- represents Endpoint and Connection Declarations separately from occurrences;
- implements the contextual direction table exactly;
- rejects references outside the direct composition boundary;
- applies exact RFC-0002 Type Equality;
- performs no conversion or transformation;
- represents fan-out with explicit named Connections;
- rejects more than one valid driver per destination;
- permits unconnected Endpoints;
- does not reject Connection cycles as runtime cycles;
- preserves structured identity and role-specific source traceability;
- applies the single-owner diagnostic precedence matrix; and
- can complete validation without expressions, values, execution, state updates, or target mapping.

Planned fixtures include valid owner-child and sibling Connections, application-level Connections, repeated Instance expansion, wrong-kind references, invalid directions, type mismatch, duplicate drivers, descendant reach-through, unconnected Endpoints, structural cycles, and randomized internal ordering.

## 15. Non-Normative Implementation Notes

A compiler may represent Endpoints and Connections with immutable records after resolution. The Structural Layer should consume resolved Type Identities rather than type spellings and should publish no graph after a fatal expansion or validation error.

The reference spike may use the temporary `SPIKEA` diagnostic domain. Those codes are experimental and do not reserve the public `IMDE` namespace.

## 16. Change Log

| Date | Change |
| --- | --- |
| 2026-07-23 | Clarified diagnostic ownership, role-specific Connection origins, and the umbrella-RFC lifecycle gate after independent review |
| 2026-07-23 | Initial Draft separating the Structural Layer required by Spike A from the deferred Runtime Layer |
