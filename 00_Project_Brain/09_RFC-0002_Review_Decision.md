# RFC-0002 Review Decision

**Status:** Approved

**Decision Date:** 2026-07-21

**Decision Owner:** IndustrialMDE Project Owner

**Scope:** RFC-0002 Proposed transition, binary64 `REAL` value-domain closure, Canonical Value Identity, and deterministic evaluation ownership

## 1. Decision Effect

The architectural review authorizes RFC-0002 to advance from Draft to Proposed after the amendments recorded here are incorporated in [Pull Request #11](https://github.com/al-gri/IndustrialMDE/pull/11).

The transition closes the Draft-to-Proposed gates for `REAL` infinities, NaN identity, signaling NaN, and signed zero. It also records the minimum deterministic contract that RFC-0003 must satisfy when it defines `REAL` literal conversion and compile-time expression evaluation.

Proposed remains a non-normative review status. This decision does not make RFC-0002 Accepted, Implemented, or Stabilized. It does not authorize a production compiler, execution runtime, Canonical IR, target implementation, or vendor emitter.

## 2. Confirmed Minimum Type-System Direction

The review confirms that RFC-0002 remains consistent with Approved Project Constitution version 2.1 and the Proposed RFC-0000 through RFC-0001C direction. It approves the following Proposed architecture:

- language version `0.1` has the closed intrinsic set `BOOL`, `INT`, `REAL`, and `TIME`;
- intrinsic designators remain RFC-0001 Identifier tokens and are recognized only by an explicit Type Reference context rule;
- intrinsic types create no hidden Package, Namespace, import, ordinary Binding, or implicit prelude;
- Intrinsic Type Identity includes the effective Language Version, while build-local handles also retain Project resolution context;
- `BOOL`, `INT`, `REAL`, and `TIME` remain distinct nominal identities;
- `INT` and `TIME` have exact signed 64-bit-range semantic domains, while `TIME` denotes integer nanoseconds;
- minimum Type Compatibility is exact Type Equality;
- declaration type inference, subtyping, variance, and every cross-type conversion are unsupported in the minimum subset;
- semantic value domains are distinct from physical target representations; and
- a target that cannot preserve a required domain must reject deployment rather than silently narrow or reinterpret the source type.

## 3. `REAL` Semantic Domain and Identity

### 3.1 Complete Domain

`REAL` uses IEEE 754 binary64 as its target-neutral abstract semantic numeric format. Its domain contains:

- every finite binary64 value, including subnormal and normal values;
- positive and negative zero;
- positive and negative infinity; and
- exactly one canonical semantic quiet NaN.

This decision establishes semantic values, not target register layout or mandatory native instructions.

### 3.2 Canonical Value Identity

Canonical Value Identity is separate from Type Identity and from future numeric operator equality.

- positive and negative zero have distinct Canonical Value Identities;
- positive and negative infinity have distinct Canonical Value Identities;
- all admitted quiet-NaN encodings normalize to one `canonical-quiet-nan` identity; and
- NaN sign and payload are not observable semantic facts.

The identity relation remains reflexive for the canonical NaN value. RFC-0003 may later define numeric equality so that signed zeros compare equal and NaN compares unequal to every operand, including itself. Such operator behavior does not alter Canonical Value Identity.

### 3.3 Signaling NaN

A signaling NaN is not a language value and cannot enter the immutable Semantic Model. A future target, deployment, external-data, or interoperability contract that can encounter a signaling NaN must explicitly define rejection or conversion to the canonical quiet NaN, including diagnostics, faults, and traceability. Host-language quieting or trapping behavior is not an implicit language contract.

## 4. Deterministic Evaluation Boundary

RFC-0002 owns the `REAL` domain and Canonical Value Identity. RFC-0003 owns literal conversion, expression typing, operators, numeric equality, and compile-time evaluation, subject to these minimum constraints:

- decimal conversion has a unique binary64 result under `roundTiesToEven`;
- every separately specified semantic operation produces a binary64 result rounded under `roundTiesToEven` at that operation boundary;
- separately specified operations are not implicitly contracted into a fused operation;
- excess intermediate precision cannot change an observable result;
- quiet-NaN results normalize to the canonical semantic NaN; and
- results are bit-exact across hosts, clean and incremental builds, compiler configurations, and targets.

The specification constrains observable results rather than requiring platform-specific x87 or FMA switches. An implementation may use verified software arithmetic, suitable hardware arithmetic, or a mixed strategy.

If a compiler or reference spike cannot guarantee the required result for an admitted compile-time `REAL` expression, it must fail deterministically or reject the expression as a documented non-conforming spike limitation. It cannot publish a host-dependent approximation and cannot defer a compile-time Constant to Target IR.

## 5. Correction to the Verification Recommendation

The review accepts canonical quiet NaN, signed-zero identity, and bit-exact cross-compilation determinism, with one material correction.

The proposed fallback that would disable `REAL` constant folding and delegate a compile-time Constant expression to Target IR is rejected. A Constant is a compile-time semantic fact established before target lowering. Deferral would make source semantics depend on target selection and would violate vendor neutrality, deterministic public signatures, and clean/incremental equivalence.

This correction does not require RFC-0002 to define arithmetic operators. It establishes a binding boundary for the future RFC-0003 evaluator.

## 6. Cross-RFC Ownership

| Concern | Owner |
| --- | --- |
| Intrinsic type set, domains, Type Identity, Type Equality, minimum compatibility | RFC-0002 |
| `REAL` Canonical Value Identity and signaling-NaN exclusion from the Semantic Model | RFC-0002 |
| Literal conversion, operators, numeric equality, constant-expression evaluation | RFC-0003 |
| Runtime arithmetic, exceptional propagation, and observable faults | RFC-0004 |
| Endpoint and Connection constraints | RFC-0005 |
| Target capability, deployment validation, and external-value boundaries | RFC-0007 |
| Public byte encoding of values in signatures, fingerprints, or IR | Applicable future public contract |

A downstream RFC may define behavior within the RFC-0002 domain. It cannot silently change the domain or Canonical Value Identity.

## 7. Remaining Acceptance and Conformance Gates

RFC-0002 remains Proposed until explicit acceptance review. Before it can become Accepted:

- every normative rule must have a testable conformance mapping;
- material review objections must be resolved;
- terminology and ownership boundaries must remain consistent with its dependencies;
- the intrinsic recognition, identity, equality, domain, diagnostic, signature, and target-capability fixtures must be reviewed; and
- project-owner acceptance must be recorded explicitly.

Complete language claims additionally require compatible Accepted downstream contracts. In particular, RFC-0003 and RFC-0004 must define expression and execution semantics; RFC-0005 must define Endpoint and Connection behavior; RFC-0007 must define deployment and target boundaries; and public fingerprint or IR owners must define interoperable encodings.

No implementation may fill those gates with undocumented host or target behavior.

## 8. Next Authorized Work

After the Proposed transition is published for review:

1. review the RFC-0002 conformance matrix and diagnostic precedence before acceptance;
2. review Draft RFC-0001D independently as a public serialization contract;
3. define the minimum RFC-0005, RFC-0006, and RFC-0007 structural slices required for the Structural Reference Spike;
4. draft RFC-0003 before admitting numeric initializer or compile-time arithmetic behavior; and
5. keep any Structural Reference Spike explicitly non-conforming until its applicable semantic contracts are Accepted.

Production compiler, runtime, target, and vendor-specific implementation remain unauthorized by this decision.
