# RFC-0002: Type System

**Status:** Draft

**Authors:** IndustrialMDE Project

**Created:** 2026-07-21

**Last Updated:** 2026-07-21

**Target Language Version:** Pre-1.0; minimal language version `0.1` subset

**Dependencies:** RFC-0000, RFC-0001, RFC-0001A, RFC-0001B, RFC-0001C

**Supersedes:** None

**Superseded By:** None

**Implementation Status:** Not Started

**Review:** [Pull Request #11](https://github.com/al-gri/IndustrialMDE/pull/11)

## 1. Summary

This RFC proposes the minimum target-neutral type system needed to review the first structural reference spike. It defines four intrinsic scalar types:

- `BOOL`;
- `INT`;
- `REAL`; and
- `TIME`.

The proposal defines their type identities, semantic value domains, equality and compatibility relation, type-context resolution, public-signature participation, deterministic diagnostics, and target-capability boundary.

Language version `0.1` has no implicit package, namespace, ordinary-symbol, or standard-library prelude. The four intrinsic spellings remain RFC-0001 `Identifier` tokens. They are recognized by an explicit type-context rule and do not become lexical keywords, hidden imports, namespace contributions, or ordinary bindings.

The minimal subset deliberately has:

- no user-defined value types;
- no declaration type inference;
- no subtyping or variance;
- no cross-type implicit conversion;
- no cross-type explicit conversion;
- no compound or collection types; and
- no target-dependent reinterpretation of a core type.

This RFC defines semantic value domains, not physical target storage. A target may use any representation that preserves the complete observable domain under later Accepted execution and lowering contracts. A target that cannot preserve a required domain must reject the deployment deterministically rather than silently narrow the type.

This document is a non-normative Draft. In particular, the complete language treatment of `REAL` exceptional values remains unresolved and blocks transition to Proposed.

## 2. Motivation

RFC-0001A defines typed semantic categories such as Constant, Parameter, Endpoint, and State without defining their value types. RFC-0001B and RFC-0001C close the foundational name-resolution and build boundaries while explicitly allowing a later type RFC to introduce language-owned intrinsic type entities without an implicit prelude.

A structural reference spike cannot check typed declarations or produce stable semantic snapshots until the following questions have one public answer:

- which minimum scalar types exist;
- how an intrinsic type is recognized without a hidden namespace;
- whether its identity changes across language versions;
- which values belong to each type;
- whether two types are equal or compatible;
- whether a target may narrow a source type silently;
- which type facts participate in public signatures and invalidation; and
- which RFC owns literals, conversions, operations, execution faults, connections, and physical storage.

Leaving those questions to implementation defaults would make observable behavior depend on a parser framework, host integer size, host floating-point behavior, target vendor, or cache representation. That would violate the deterministic and vendor-neutral requirements of the Approved Project Constitution and RFC-0000.

The minimum type system must nevertheless remain smaller than a production language. Its purpose is to establish a coherent scalar foundation and make subsequent RFC boundaries testable, not to anticipate every numeric, aggregate, unit, interface, or target-specific type.

## 3. Goals

This RFC proposes to:

- define one closed intrinsic scalar type set for the language version `0.1` minimum subset;
- define a stable, structured Intrinsic Type Identity that includes the effective language version;
- recognize intrinsic type designators without an implicit prelude or ordinary-symbol lookup;
- define exact `BOOL`, `INT`, and `TIME` value domains;
- propose IEEE 754 binary64 as the `REAL` semantic numeric format while exposing remaining exceptional-value gates;
- define deterministic type equality and minimum compatibility;
- prohibit declaration type inference and cross-type conversions in the minimum subset;
- separate semantic value domains from physical target memory representation;
- prevent silent target-dependent narrowing;
- define type-system diagnostic ownership and precedence;
- define the type facts contributed to public semantic signatures; and
- provide conformance-ready semantic examples without claiming final source grammar.

## 4. Non-Goals

This RFC does not define:

- final declaration or type-reference grammar;
- a parser, syntax-tree, AST, binder, or semantic-model class hierarchy;
- user-defined aliases, distinct types, records, tuples, variants, enumerations, or subranges;
- arrays, lists, sets, maps, optional values, references, or nullability;
- generic types, type parameters, traits, interfaces, inheritance, or overload resolution;
- engineering units, dimensions, quantities, scaling, or calibration semantics;
- date, wall-clock, time-zone, calendar, timestamp, or scheduling types;
- string or byte-sequence value types;
- literal evaluation, operators, constant folding, or expression typing beyond the representability predicates defined here;
- a source syntax or runtime semantics for casts;
- arithmetic overflow, division, rounding, comparison, NaN propagation, or runtime fault behavior;
- Endpoint direction, Connection compatibility, transformation, quality, sampling, or timing;
- runtime initialization, state update, scan-cycle, retention, or persistence semantics;
- Canonical IR or Target IR schemas;
- public fingerprint byte encoding;
- physical storage width, byte order, alignment, register selection, or memory layout; or
- vendor-specific numeric types or implicit compatibility with them.

## 5. Terminology

This RFC uses terms from the [IndustrialMDE Glossary](../Glossary.md), RFC-0001A, RFC-0001B, and RFC-0001C.

- **Type** — a language-defined classification with a stable Type Identity and a semantic value domain.
- **Intrinsic Type** — a language-owned type whose identity and semantics are defined directly by an RFC rather than by a Package declaration.
- **Intrinsic Type Designator** — an exact source spelling recognized as an Intrinsic Type only in a type-reference context.
- **Intrinsic Kind** — one of the closed tags `BOOL`, `INT`, `REAL`, or `TIME` in this minimum subset.
- **Intrinsic Type Identity** — the structured, language-versioned identity of one Intrinsic Kind.
- **Type Reference** — a source or semantic reference whose context requires a Type.
- **Type Equality** — the relation determining whether two Type Identities denote the same Type.
- **Type Compatibility** — a relation that an owning semantic rule may use when it requires values of one type to be acceptable as another type. In this minimum subset it is identical to Type Equality.
- **Semantic Value Domain** — the complete set of values a Type can denote before target lowering.
- **Representability** — membership of a mathematical or semantic value in a Type's Semantic Value Domain.
- **Physical Representation** — a target- or implementation-specific storage and operation encoding. It is not Type Identity.
- **Invalid Type Placeholder** — a build-local recovery value used after a type diagnostic. It is not a valid Type and cannot enter published semantic or generated artifacts.

The phrase **structured identity** describes an identity encoded as named fields. It does not mean that language version `0.1` supports structural typing of user-defined types.

## 6. Normative Specification

### 6.1 Ownership and Cross-RFC Boundary

This RFC owns:

- the intrinsic type set;
- Intrinsic Type Identity;
- intrinsic type-context recognition and spelling reservation;
- scalar Semantic Value Domains;
- Type Equality and the minimum Type Compatibility relation;
- representability predicates;
- the absence of type inference and cross-type conversions in the minimum subset;
- type facts contributed to public semantic signatures; and
- type-system diagnostics defined in section 6.15.

RFC-0001 owns tokenization and literal token forms. The exact spellings `BOOL`, `INT`, `REAL`, and `TIME` remain `Identifier` tokens under language version `0.1`.

RFC-0001B owns ordinary name resolution. It does not add the Intrinsic Types to an ordinary-symbol environment. This RFC defines a separate, explicit rule that applies only in a Type Reference context.

RFC-0003 owns expression grammar, operator typing, conversion syntax, literal evaluation, constant-expression evaluation, and the application of representability to evaluated expressions.

RFC-0004 owns target-neutral observable execution behavior, including runtime arithmetic results, faults, and propagation rules. Observable behavior cannot vary silently by target.

RFC-0005 owns Endpoint direction and Connection compatibility. It may invoke the Type Equality or Type Compatibility relation from this RFC but must define the complete Connection rule and its contextual diagnostic.

RFC-0006 owns composition, interfaces, member visibility, and the complete public structural signature of Definitions.

RFC-0007 and later target contracts own target capability declaration, deployment validation, target lowering, and physical target representation. Target-specific memory planning occurs only after target lowering has established the target memory model.

RFC-0012 owns any future Canonical IR schema. This RFC does not prescribe an IR encoding.

### 6.2 Closed Minimum Type Set

The minimum language version `0.1` type set defined by this RFC is exactly:

```text
BOOL
INT
REAL
TIME
```

Each item is an Intrinsic Type. No Package, Module, Namespace, import, dependency, user declaration, standard-library declaration, or plugin registration creates it.

A compiler MUST NOT add an implementation-defined intrinsic type to this set. A target profile MUST NOT redefine one of these types or add a target type to the vendor-neutral type set under an unqualified spelling.

User-defined value types and every type constructor are unsupported by this minimum subset. A later RFC revision may add them only after defining identity, resolution, compatibility, public-signature, migration, and boundedness rules.

### 6.3 Lexical Form and Type-Context Recognition

The intrinsic spellings are not RFC-0001 reserved keywords. The lexer MUST emit the same `Identifier` token kind for `BOOL`, `INT`, `REAL`, and `TIME` that it emits for other valid uppercase identifiers.

When a syntactic or normalized semantic context requires a Type Reference, the compiler applies this rule before ordinary name resolution:

1. compare the complete raw Identifier spelling against the four exact intrinsic spellings;
2. if exactly equal, construct the corresponding Intrinsic Type Identity;
3. do not search a Namespace, owner scope, Import Environment, Package, or dependency for that reference; and
4. otherwise continue with the explicit ordinary resolution rules applicable to that Type Reference.

The comparison is ASCII, exact, and case-sensitive. `INT` is intrinsic. `Int`, `int`, and `iNt` are not intrinsic designators.

This recognition rule does not create a Binding. It does not create a hidden lexical scope, initial Type Environment, language Package, or standard-library prelude.

The exact intrinsic spellings are semantically reserved for language-owned types. A source or build input MUST NOT introduce any of those exact spellings as:

- an ordinary declaration identifier;
- a Namespace segment;
- an import alias; or
- another source-visible alias that may begin name traversal.

An exact reserved-spelling violation produces `IMDE5001`. Case variants are not reserved by this RFC and remain subject to RFC-0001B ordinary collision rules and any later target-profile validation.

### 6.4 Intrinsic Type Identity

An Intrinsic Type Identity is structured data with these fields:

```text
domain:           industrialmde.language.intrinsic-type
language_version: exact effective Language Version
kind:             BOOL | INT | REAL | TIME
```

The fields MUST NOT be represented for semantic equality by delimiter-concatenating strings. The implementation representation may be an enum, tagged record, or another immutable form, but observable equality and ordering must follow this RFC.

Package Identity, Package Revision, Module Identity, Namespace Path, source path, source span, import alias, target name, physical representation, process identifier, timestamp, object address, and random UUID are not fields of Intrinsic Type Identity.

The Language Version is identity-significant. For example:

```text
(intrinsic-type, 0.1, INT)
```

is not equal to an `INT` identity from a future language version unless a future cross-version contract explicitly defines an identity-preserving relationship. Language version `0.1` does not support mixed-version Projects under RFC-0001C.

An Intrinsic Type has no Package Revision. A build-local resolved handle for an Intrinsic Type MUST nevertheless include the Project Resolution Fingerprint or equivalent complete build context required by RFC-0001C:

```text
(Intrinsic Type Identity, Project Resolution Fingerprint)
```

Intrinsic Type Identity alone MUST NOT authorize cross-build cache reuse or dereference after the effective language version, compiler semantic version, Project resolution, or relevant configuration changes.

### 6.5 `BOOL`

`BOOL` has exactly two semantic values:

```text
false
true
```

The RFC-0001 literal tokens `false` and `true` denote `BOOL` values when an owning expression or declaration grammar admits them.

`BOOL` is not numeric. It has no implicit or explicit conversion to or from `INT`, `REAL`, or `TIME` in the minimum subset.

This RFC does not define a physical bit width, target storage unit, truthy value, numeric encoding, or target register representation for `BOOL`.

### 6.6 `INT`

`INT` denotes mathematical integers in the exact inclusive range:

```text
[-2^63, 2^63 - 1]
```

Equivalently:

```text
[-9223372036854775808, 9223372036854775807]
```

For a mathematical integer `n`:

```text
representable(INT, n) iff -2^63 <= n <= 2^63 - 1
```

The range is a semantic domain. This RFC does not prescribe two's-complement physical storage, byte order, alignment, register count, or instruction selection.

RFC-0001 tokenizes a leading sign separately from a numeric literal. Therefore the source expression that may eventually denote `-2^63` requires RFC-0003 expression semantics. The representability predicate applies to the evaluated mathematical value, not independently to the unsigned magnitude token.

Binary and hexadecimal literal interpretation, contextual typing, unary signs, operator results, overflow, wrapping, saturation, and bitwise behavior remain owned by RFC-0003 and RFC-0004.

### 6.7 `REAL`

`REAL` is proposed to use the IEEE 754 binary64 interchange format as its target-neutral semantic numeric format.

At minimum, its finite numeric domain includes:

- both binary64 zero encodings;
- every binary64 subnormal finite value;
- every binary64 normal finite value; and
- both signs where the format provides them.

This RFC does not define a physical target register layout or require native binary64 instructions. A target may emulate the required semantics if a later Accepted execution and lowering contract permits it.

RFC-0001 does not define `NaN` or infinity source literals. The following questions remain unresolved in this Draft:

- whether positive and negative infinity are language values;
- whether NaN is one semantic value or a family distinguished by sign, quiet/signaling state, or payload;
- whether signaling NaNs may enter the Semantic Model;
- whether positive and negative zero have distinct canonical value identities;
- how exceptional values participate in equality, ordering, constant evaluation, public signatures, and deterministic serialization; and
- which rounding rule converts a decimal real literal to a binary64 value.

Until those questions are resolved by compatible RFC revisions, an implementation MUST NOT claim full RFC-0002 conformance for `REAL` exceptional values. A reference spike that excludes them must declare that restriction and identify itself as non-conforming.

Arithmetic, comparison, rounding mode, fused operations, overflow, underflow, NaN propagation, and runtime fault behavior are not established by this RFC.

### 6.8 `TIME`

`TIME` denotes signed durations measured in exact integer nanoseconds.

Its semantic value domain is:

```text
[-2^63, 2^63 - 1] nanoseconds
```

For a mathematical integer nanosecond count `n`:

```text
representable(TIME, n ns) iff -2^63 <= n <= 2^63 - 1
```

Negative durations are valid `TIME` values. A later timer, scheduling, profile, or API contract may require a non-negative duration in a particular context, but that constraint does not change the Type's domain.

`TIME` is not an absolute timestamp, wall-clock value, calendar value, time-zone value, scan-cycle identifier, or target timer instance.

RFC-0001 does not define a `TIME` literal form. RFC-0003 must define any future duration literal or expression syntax. This RFC defines only the value domain and identity.

`TIME` is distinct from `INT` even though both domains use the same integer bounds. Equal mathematical payload ranges do not imply equal Type Identities or compatibility.

### 6.9 Type Equality

Type Equality is exact equality of Type Identity.

For Intrinsic Types `A` and `B`:

```text
type_equal(A, B) iff
    A.domain == B.domain and
    A.language_version == B.language_version and
    A.kind == B.kind
```

Type Equality is reflexive, symmetric, and transitive.

Within one valid language version `0.1` Project:

| Left | Right | Equal |
| --- | --- | --- |
| `BOOL` | `BOOL` | Yes |
| `INT` | `INT` | Yes |
| `REAL` | `REAL` | Yes |
| `TIME` | `TIME` | Yes |
| any distinct pair | any distinct pair | No |

Package Revision, source origin, import spelling, and target representation cannot make two unequal Intrinsic Type Identities equal or make equal identities unequal.

### 6.10 Type Compatibility and Assignability

The minimum compatibility relation is exact Type Equality:

```text
type_compatible(source, destination) iff type_equal(source, destination)
```

The relation is symmetric in this minimum subset. It defines no subtyping, widening, narrowing, covariance, contravariance, unit conversion, or representation conversion.

An owning semantic RFC may require Type Compatibility for a specific relationship. That RFC must define:

- which source and destination entities participate;
- direction and occurrence rules;
- whether a more specific contextual diagnostic replaces `IMDE5003`;
- any transformation entity permitted between unequal types; and
- the public-signature and compatibility effects.

RFC-0005, not this RFC, owns the rule for Endpoint Connections.

### 6.11 No Cross-Type Conversions

The minimum subset supports no cross-type conversion.

In particular, the following are unsupported in both implicit and explicit form:

- `BOOL` to or from any other Intrinsic Type;
- `INT` to or from `REAL`;
- `INT` to or from `TIME`;
- `REAL` to or from `TIME`; and
- any target-specific reinterpretation presented as a core conversion.

RFC-0003 may propose conversion syntax only together with a compatible RFC-0002 amendment that defines the allowed source and destination identities, total or partial value mapping, rounding, exceptional cases, diagnostics, and compatibility consequences.

The absence of a conversion is not permission for a target to reinterpret bits or narrow values silently.

### 6.12 No Declaration Type Inference

Every typed declaration in the minimum subset MUST contain an explicit Type Reference once its owning declaration grammar is defined.

The compiler MUST NOT infer a declaration type from:

- an initializer token or expression;
- a connected Endpoint;
- a target address or register;
- a configured value;
- a neighboring declaration;
- a naming convention;
- a profile role; or
- a host-language value used by an implementation API.

The fact that the RFC-0001 tokens `true` and `false` denote `BOOL` values is literal typing, not permission to omit a declaration Type Reference.

Numeric literal contextual typing and expression result typing remain owned by RFC-0003. Until that RFC defines them, a reference spike may model typed structure without accepting numeric initializers.

### 6.13 Kernel Object Integration

RFC-0001A defines Constant, Parameter, Endpoint, and State as distinct semantic categories. This RFC supplies Type Identity and representability facts without changing those categories.

For every typed declaration admitted by its owning semantic RFC, the immutable resolved Semantic Model MUST retain:

- the resolved Type Identity;
- the Type Reference source span or equivalent traceability origin;
- resolution status; and
- any invalid recovery state without replacing it by a valid Type.

This RFC does not determine:

- how a Constant expression is evaluated;
- how a Parameter receives an effective value;
- whether an Endpoint may connect to another Endpoint;
- how State is initialized or updated; or
- whether a member is public.

Those rules must invoke this RFC's Type Equality, Type Compatibility, or representability predicates explicitly rather than inventing another undocumented type relation.

### 6.14 Public Semantic Signature Participation

When another Accepted RFC includes a typed declaration in an Export Surface or public structural surface, its semantic signature MUST include the complete Type Identity of every externally observable typed position.

At minimum, later public-signature contracts must account for:

- declared member Type Identity;
- ordered parameter or field positions when such constructs exist;
- result Type Identity when such constructs exist; and
- type constraints or bounds introduced by later RFCs.

Constant values, default values, units, array bounds, field ordering, enum members, conversion behavior, and interface substitution are included only when their owning RFC defines them as public semantic facts.

Changing a public typed position from one Intrinsic Type Identity to another changes the public semantic signature input and requires downstream invalidation under RFC-0001C. It is compatibility-significant. This RFC does not claim that every public-signature change has the same migration policy.

The exact public fingerprint byte encoding remains outside this RFC. Until a compatible fingerprint specification registers an encoding, a reference spike may emit only an explicitly experimental, non-interoperable snapshot.

### 6.15 Target Capability and Lowering Boundary

A selected target profile must be capable of preserving every observable value and operation required by the source model and Accepted semantic RFCs.

For the types in this minimum subset:

- a target MUST NOT redefine the `INT` range;
- a target MUST NOT reinterpret `TIME` as a different duration unit;
- a target MUST NOT silently collapse distinct `BOOL` values;
- a target MUST NOT silently reduce required `REAL` precision or exponent range; and
- a target MUST NOT treat an unsupported value as an unrelated target value.

If the selected target cannot preserve a required semantic domain, compilation for that target fails with `IMDE5005` or a more specific diagnostic registered by the Accepted target contract.

Observing that current constants happen to fit a narrower representation is not sufficient to narrow a Parameter, Endpoint, State, or other runtime-capable value. A semantics-preserving internal optimization may be considered only under an Accepted execution model and optimization contract with complete proof obligations and unchanged observable behavior.

This RFC does not require a native physical width. Emulation is permitted only when it satisfies later execution, timing, resource, and target-conformance requirements.

### 6.16 Invalid Types and Recovery

After a type diagnostic, an implementation may create an Invalid Type Placeholder to continue bounded analysis.

An Invalid Type Placeholder:

- has no valid Type Identity;
- is unequal and incompatible with every valid Type and every other placeholder unless a diagnostic-recovery algorithm explicitly groups occurrences;
- must not suppress an independently provable diagnostic outside deterministic suppression rules;
- must not enter an Export Surface, public semantic fingerprint, Canonical IR, Target IR, or generated artifact; and
- must not be persisted as though it were a source-defined or intrinsic type.

Recovery order, suppression, and diagnostic limits must be deterministic.

### 6.17 Validation and Diagnostics

This RFC reserves diagnostics `IMDE5001` through `IMDE5005` for the minimum Type System:

| Code | Severity | Condition | Required diagnostic facts |
| --- | --- | --- | --- |
| `IMDE5001` | Error | Exact intrinsic spelling introduced as an ordinary declaration, Namespace segment, import alias, or other source-visible alias | Spelling, binding category, applicable Intrinsic Type Identity, and source or build-document introduction span |
| `IMDE5002` | Error | Successfully resolved Type entity or type form is unsupported by the effective minimum Type System | Resolved identity or form, effective language version, and supported type set |
| `IMDE5003` | Error | A context owned by this or a later RFC requires compatible types and no more-specific contextual diagnostic applies | Source and destination Type Identities, owning relationship, and both type-reference spans |
| `IMDE5004` | Error | A deterministic mathematical or semantic value supplied by an owning expression or declaration rule is outside the declared Type's representability predicate | Target Type Identity, normalized value fact, applicable bound, and value/type spans |
| `IMDE5005` | Error | Selected target lowering cannot preserve a required Intrinsic Type domain | Type Identity, required domain or capability, target-profile identity, and target-selection or mapping origin |

This RFC reuses, rather than duplicates:

- `IMDE3004` from RFC-0001B when an ordinary Type Reference remains unresolved after intrinsic recognition;
- `IMDE2009` from RFC-0001A when a uniquely resolved reference has the wrong semantic kind; and
- future RFC-0005 or RFC-0007 diagnostics when their contextual rule is more specific.

One invalid fact MUST NOT produce both the general and more-specific diagnostic. Validation precedence is:

1. lexical validity under RFC-0001;
2. intrinsic spelling reservation and recognition under this RFC;
3. ordinary name resolution under RFC-0001B when required;
4. semantic-kind validation under RFC-0001A;
5. Type Equality, Type Compatibility, or representability validation; and
6. contextual connection, execution, deployment, or target validation under its owning RFC.

Diagnostics follow the deterministic ordering rules in section 7. A fix suggestion is optional and must not silently rename a declaration, change a Type Reference, insert a conversion, change a value, or select a different target.

## 7. Determinism and Ordering

Given identical complete build inputs, a conforming implementation must produce identical:

- Intrinsic Type Identities;
- Type Equality and Type Compatibility results;
- representability results;
- type-resolution outcomes;
- invalid-placeholder publication decisions;
- public semantic signature inputs; and
- diagnostic codes, severities, facts, spans, and ordering.

Locale, host integer width, host floating-point mode, object identity, hash-map order, filesystem order, target vendor defaults, current time, process state, and concurrency schedule must not change those results.

When Intrinsic Kinds require deterministic ordering, they are ordered by the unsigned UTF-8 byte sequence of their exact spelling:

```text
BOOL
INT
REAL
TIME
```

Type-system diagnostics with source origins are ordered by:

1. Canonical Source Identity or normalized logical source path under RFC-0001C;
2. primary raw start offset;
3. primary raw end offset;
4. diagnostic code;
5. involved Type Identity fields in canonical field order; and
6. a stable rule-specific secondary key.

A target-capability diagnostic without a source Type Reference uses the stable target-selection or Deployment Mapping origin defined by its owning target contract. Absolute checkout, cache, or extraction paths must not establish order.

An `IMDE5001` diagnostic originating in a manifest follows the RFC-0001C stable build-document origin and, when a compatible serialization contract applies, its field-path ordering rather than source-file ordering.

## 8. Compatibility and Migration

### 8.1 Language-Version Significance

Intrinsic Type Identity includes the exact effective Language Version. Changing the language-version component changes the identity unless a future cross-version RFC defines an explicit compatible bridge.

Language version `0.1` permits only one effective version per Project, so no implicit cross-version type equality exists.

### 8.2 Type-System Changes

The following changes are compatibility-significant and require explicit RFC revision and language-version analysis:

- adding, removing, or renaming an Intrinsic Kind;
- changing an intrinsic spelling reservation rule;
- changing a Semantic Value Domain;
- changing Type Equality or Type Compatibility;
- adding an implicit or explicit conversion;
- changing representability at a boundary;
- changing `TIME` unit or signedness;
- changing `REAL` format or exceptional-value identity; and
- changing which type facts participate in public signatures.

Adding an intrinsic designator can invalidate a previously legal ordinary identifier. For a Stabilized language version it is a breaking change unless the spelling was already reserved for that purpose.

### 8.3 Public API Evolution

Changing the Type Identity of a public typed position changes its public semantic signature input and invalidates semantic consumers.

Migration tooling should report:

- the declaration identity;
- old and new Type Identities;
- affected public consumers;
- configuration values requiring review;
- Connections or interfaces requiring later owning-RFC review; and
- target mappings whose representability may change.

Physical source relocation does not change Intrinsic Type Identity. It may change Compilation Unit fingerprints and source traceability under RFC-0001C.

### 8.4 Pre-1.0 Status

This Draft may change incompatibly during review while history remains available. It creates no Stabilized guarantee and no production compatibility claim.

## 9. Safety and Security Considerations

- Exact domains prevent host or target integer widths from silently changing accepted values.
- No implicit conversion prevents unreviewed precision loss, unit confusion, or boolean/numeric reinterpretation.
- Distinct `INT` and `TIME` identities prevent an equal payload range from erasing duration meaning.
- Target rejection prevents unsupported hardware from silently narrowing core values.
- Type-context intrinsic recognition avoids dependency confusion through a hidden standard-library Package.
- Semantic spelling reservation prevents an ordinary binding from impersonating an Intrinsic Type in another context.
- Invalid placeholders cannot reach generated artifacts.
- The closed four-type set bounds intrinsic lookup and prevents attacker-controlled type-registry growth.

`REAL` exceptional-value, comparison, and execution semantics remain unresolved. No safety claim may rely on unspecified NaN, infinity, signed-zero, rounding, overflow, or target-fault behavior.

Successful type checking does not establish process safety, numerical stability, target timing adequacy, SIL or PL compliance, or physical equipment correctness.

## 10. Tooling and Incremental Compilation

### 10.1 Required Semantic Records

Tooling must retain, for every successfully resolved typed position:

- complete Type Identity;
- source Type Reference and raw span;
- owning semantic declaration identity;
- effective Language Version;
- build-local resolved handle context; and
- public-signature participation when established by the owning RFC.

### 10.2 Syntax and Semantic Representation

A lossless syntax tree should preserve `BOOL`, `INT`, `REAL`, and `TIME` as their original Identifier tokens. The resolved Semantic Model should represent the resulting Intrinsic Type Identity explicitly.

This RFC does not require an `IntrinsicTypeNode`, a particular AST layer, an enum class, or parser-level keyword token. An implementation may omit a normalized AST when it adds no value beyond the syntax tree and immutable Semantic Model.

### 10.3 Incremental Invalidation

At minimum, the following changes invalidate affected type results:

| Change | Required invalidation |
| --- | --- |
| effective Language Version | all Intrinsic Type Identities and typed semantic consumers |
| Type Reference spelling | owning declaration and semantic dependents |
| declaration identity or visibility | affected ordinary type lookup and consumers |
| public typed position | public semantic signature and downstream consumers |
| target-profile capability | target validation and lowering, not source Type Identity |
| compiler semantic version affecting type rules | Project Resolution Fingerprint and affected caches |

A cached type-equality result cannot be reused from Intrinsic Type Identity alone. Its cache key must include the applicable build context required by RFC-0001C.

### 10.4 IDE Behavior

An IDE should expose:

- the Intrinsic Kind and exact Semantic Value Domain;
- the effective Language Version in identity details;
- the distinction between semantic domain and target physical representation;
- unresolved or wrong-kind references without inventing fallback types;
- the owner of a contextual compatibility rule; and
- target capability failures separately from source type errors.

An IDE must not auto-insert a conversion or replace a type solely because a selected target has a narrower native representation.

## 11. Examples

The examples in this section are semantic conformance fixtures. They do not establish final `.plant` declaration grammar. A future grammar fixture must map its source spans to the same observable semantic results.

### 11.1 Positive: Intrinsic Recognition

```text
effective language version: 0.1
context: type reference
identifier token: INT
```

Expected result:

```text
Intrinsic Type Identity
  domain: industrialmde.language.intrinsic-type
  language_version: 0.1
  kind: INT
```

No ordinary-symbol lookup, import, Package declaration, or prelude binding is created.

### 11.2 Positive: Exact Equality

```text
left:  (intrinsic-type, 0.1, TIME)
right: (intrinsic-type, 0.1, TIME)
```

Expected result: Type Equality and Type Compatibility are both true.

### 11.3 Positive: Equal Payload Range Does Not Imply Equal Type

```text
left:  (intrinsic-type, 0.1, INT)
right: (intrinsic-type, 0.1, TIME)
```

Expected result: Type Equality and Type Compatibility are false even though both use the same integer bounds.

### 11.4 Negative: Reserved Intrinsic Spelling

```text
declaration category: Definition
declaration identifier token: REAL
```

Expected result: `IMDE5001`. The lexer still emitted an Identifier token; semantic declaration validation rejects the exact intrinsic spelling.

### 11.5 Negative: Case Variant Is Not Intrinsic

```text
effective language version: 0.1
context: type reference
identifier token: Int
ordinary environments contain no binding named Int
```

Expected result: intrinsic recognition does not match. Ordinary resolution produces RFC-0001B `IMDE3004`.

### 11.6 Negative: Wrong Semantic Kind

```text
context: type reference
identifier token: Motor
ordinary resolution result: Definition Motor
```

Expected result: RFC-0001A `IMDE2009`. The compiler does not reinterpret the Definition as a Type and does not perform a second lookup.

### 11.7 Boundary: `INT`

| Mathematical value supplied by an owning rule | Representable as `INT` |
| --- | --- |
| `-9223372036854775809` | No — `IMDE5004` |
| `-9223372036854775808` | Yes |
| `0` | Yes |
| `9223372036854775807` | Yes |
| `9223372036854775808` | No — `IMDE5004` |

These are mathematical-value fixtures. They do not imply that a leading sign is part of an RFC-0001 numeric literal token.

### 11.8 Boundary: `TIME`

| Duration | Representable as `TIME` |
| --- | --- |
| `-9223372036854775809 ns` | No — `IMDE5004` |
| `-9223372036854775808 ns` | Yes |
| `0 ns` | Yes |
| `9223372036854775807 ns` | Yes |
| `9223372036854775808 ns` | No — `IMDE5004` |

### 11.9 Negative: Cross-Type Compatibility

```text
required destination type: REAL
provided source type: INT
owning context has no more-specific mismatch diagnostic
```

Expected result: `IMDE5003`. The compiler does not insert an `INT`-to-`REAL` conversion.

### 11.10 Negative: Unsupported Target Domain

```text
required type: INT with [-2^63, 2^63 - 1]
selected target capability: native signed 32-bit only, no conforming emulation
```

Expected result: `IMDE5005`. The compiler does not narrow `INT` based on current initializer values.

### 11.11 Boundary: Cross-Version Identity

```text
left:  (intrinsic-type, 0.1, BOOL)
right: (intrinsic-type, future-version, BOOL)
```

Expected result: the identities are unequal in the absence of a future explicit cross-version contract. RFC-0001C independently rejects a mixed-version language version `0.1` Project.

### 11.12 Draft Gate: `REAL` Exceptional Values

```text
candidate semantic value: NaN with payload 0x1
```

Expected result for this Draft: no conformance result is defined. A reference spike must reject or exclude the case under a documented non-conforming limitation rather than select host-language behavior implicitly.

## 12. Alternatives Considered

### 12.1 Hidden Standard-Library Package

Rejected for language version `0.1`. It would introduce an implicit dependency, Package Identity, namespace contribution, visibility policy, and resolution path contrary to RFC-0001B and RFC-0001C.

### 12.2 Lexically Reserved Uppercase Keywords

Rejected. RFC-0001 defines the language version `0.1` keyword table and tokenizes these spellings as Identifiers. Converting them to keywords would require a lexical compatibility change and would unnecessarily couple the parser to semantic Type Identity.

### 12.3 Undocumented Initial Type Environment

Rejected. An ambient environment would be indistinguishable from an implicit prelude and could create hidden lookup priority. This RFC instead defines one closed type-context recognition rule.

### 12.4 Absolute Global Singleton Identity

Rejected because it would conflate types across language versions and invite invalid cross-build cache reuse. Intrinsic identity is language-versioned, and resolved handles retain Project resolution context.

### 12.5 Target-Sized `INT` or `TIME`

Rejected because identical source would acquire different value domains on different targets. Target capability validation must reject an unsupported domain rather than redefine it.

### 12.6 Mandatory Physical 64-Bit Layout

Rejected. The semantic range is fixed, but native storage width, alignment, byte order, registers, and emulation are target-lowering concerns.

### 12.7 Implicit Numeric Widening

Rejected for the minimum subset. Even apparently widening `INT` to binary64 `REAL` cannot represent every 64-bit integer exactly and would create hidden precision changes.

### 12.8 Explicit Casts Without Complete Semantics

Rejected. Syntax alone cannot define rounding, exceptional cases, partiality, diagnostics, or execution behavior. Cross-type casts remain unsupported until a compatible amendment defines the complete mapping.

### 12.9 Type Inference from Initializers or Connections

Rejected for the minimum subset because it would require expression and connection rules that belong to RFC-0003 and RFC-0005 and could make declaration meaning depend on distant context.

### 12.10 Compound and Unit Types in the First Slice

Deferred. They require identity, bounds, compatibility, layout intent, public-signature, and migration rules that are unnecessary for the initial structural hypothesis.

## 13. Unresolved Questions

The following questions change the `REAL` Semantic Value Domain or canonical value identity and block transition of this RFC from Draft to Proposed:

1. Does the `REAL` Semantic Value Domain include positive and negative infinity?
2. What semantic identities, if any, distinguish NaN sign, quiet/signaling state, and payload?
3. Are positive and negative zero distinct for canonical value identity, equality, public constants, and serialization?

Resolution must preserve vendor neutrality and deterministic clean/incremental equivalence. Delegation is valid only when the owning RFC and the boundary are explicit; an implementation default is not a resolution.

The following are explicit downstream gates rather than blockers to RFC-0002 Proposed consideration once the value domain and ownership boundary above are complete:

- RFC-0003 must define deterministic decimal-literal conversion, expression typing, constant evaluation, and application of representability predicates;
- RFC-0003 and RFC-0004 must define operator equality, ordering, rounding, exceptional results, and runtime fault or propagation behavior; and
- RFC-0005 and RFC-0007 must define whether and how exceptional values may cross Endpoint, deployment, and target boundaries.

The following features are resolved as unsupported in the minimum subset rather than left open:

- user-defined value types;
- compound and collection types;
- type inference;
- subtyping and variance;
- all cross-type conversions;
- implicit prelude bindings; and
- target-dependent core type domains.

## 14. Conformance Requirements

An implementation may claim conformance to a future Accepted revision of this RFC only if it:

- recognizes exactly the registered intrinsic spellings in Type Reference contexts;
- keeps those spellings as RFC-0001 Identifier tokens;
- creates no hidden Package, Namespace, import, or ordinary Binding;
- constructs complete language-versioned Intrinsic Type Identities;
- distinguishes identity from build-local resolved handles;
- implements exact Type Equality and minimum Type Compatibility;
- enforces the `BOOL`, `INT`, and `TIME` domains exactly;
- implements the finally accepted `REAL` domain and exceptional-value rules;
- rejects unsupported type forms, inference, and cross-type conversions;
- prevents invalid placeholders from reaching published artifacts;
- contributes type facts to public signatures as required;
- rejects target lowering that cannot preserve the required domain;
- produces required deterministic diagnostics and ordering; and
- passes the positive, negative, boundary, compatibility, randomized-order, and target-capability fixtures registered for this RFC.

At minimum, planned fixtures include:

- each exact intrinsic spelling and multiple case variants;
- every pair in the four-by-four Type Equality matrix;
- exact `INT` and `TIME` minima, maxima, and one value beyond each bound;
- declaration and alias collisions with every intrinsic spelling;
- unresolved and wrong-kind Type References with diagnostic precedence;
- invalid-placeholder publication rejection;
- public signature change after a Type Identity change;
- target capability failure without silent narrowing;
- cross-version identity inequality; and
- randomized internal map and file orders producing identical semantic results and diagnostics.

Until section 13 is resolved, no implementation can claim complete RFC-0002 conformance. A deliberately limited reference spike may implement a declared subset only when it identifies itself as non-conforming and records architecture feedback.

## 15. Implementation Notes

This section is non-normative.

A compiler can implement intrinsic recognition as a closed comparison table in the type binder while leaving the lexer and lossless syntax tree unchanged. The resolved Semantic Model can use an immutable enum-tagged record for Intrinsic Type Identity.

An implementation should not use:

- a host-language class or object identity as Type Identity;
- the host integer width as the `INT` range;
- the host float parser without a specified deterministic conversion contract;
- a target register type as the source Type;
- raw strings interchangeably for Type Identity and display names; or
- a valid Type as the error-recovery placeholder.

The reference spike should test whether a dedicated resolved intrinsic record simplifies semantic checking. It should not require a parser-specific `IntrinsicTypeNode` or treat that internal choice as evidence for source-language grammar.

Experimental semantic or structural snapshots must be labeled non-conforming and non-interoperable until the Canonical IR and fingerprint encodings are governed by compatible specifications.

## 16. Change Log

| Date | Change |
| --- | --- |
| 2026-07-21 | Created the initial minimal Type System Draft with four language-versioned Intrinsic Types, exact equality, no conversions or inference, and explicit target-preservation boundaries |
