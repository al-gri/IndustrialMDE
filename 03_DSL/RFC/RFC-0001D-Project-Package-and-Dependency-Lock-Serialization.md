# RFC-0001D: Project, Package, and Dependency-Lock Serialization

**Status:** Draft

**Authors:** IndustrialMDE Project

**Created:** 2026-07-20

**Last Updated:** 2026-07-20

**Target Language Version:** Pre-1.0; manifest schema `0.1`

**Dependencies:** RFC-0000, RFC-0001, RFC-0001C

**Supersedes:** None

**Superseded By:** None

**Implementation Status:** Not Started

**Review:** [Pull Request #10](https://github.com/al-gri/IndustrialMDE/pull/10); [RFC-0001C Review Decision](../../00_Project_Brain/08_RFC-0001C_Review_Decision.md)

## 1. Summary

This RFC defines the public serialization contract for the Project Manifest, Package Manifest, and Dependency Lock introduced by RFC-0001C.

Manifest schema `0.1` is a closed, strict profile of JSON. It defines:

- canonical filenames and document roles;
- UTF-8 encoding and newline handling;
- exact object members and JSON value kinds;
- duplicate-member rejection before map construction;
- Package Identity, version, path, and digest encodings;
- deterministic document spans and diagnostic ordering;
- closed-schema handling for unknown members;
- a canonical serialization for deterministic tool output; and
- explicit compatibility and migration rules.

This RFC owns a public build-input format. A parser library, internal parsed representation, and reference-spike codec architecture remain implementation choices and MAY be recorded in an ADR. An ADR MUST NOT redefine the observable document contract in this RFC.

This document is a non-normative Draft. It makes the complete schema available for architectural review but does not establish an Accepted compatibility contract.

## 2. Motivation

RFC-0001C deliberately defined the semantic document model before selecting a public encoding. That separation prevented an implementation convenience from becoming a format by accident, but a concrete format is required before manifests and locks can become interoperable build inputs.

Using JSON without a stricter profile is insufficient. General-purpose JSON parsers can disagree about duplicate object members, malformed Unicode escapes, numeric precision, byte-order marks, and extensions accepted beyond the standard grammar. A build graph cannot depend on whichever behavior a selected library happens to expose.

The serialization contract must also preserve the separation between:

- source bytes and parsed values;
- user-facing document formatting and semantic ordering;
- immutable dependency artifact identity and mutable root-workspace state;
- a public format and an internal compiler data structure; and
- validation diagnostics and automatic document mutation.

## 3. Goals

This RFC provides:

- one strict public JSON profile for all foundational build documents;
- exact schema `0.1` structures for Project, Package, and lock data;
- deterministic rejection of malformed, duplicate, unknown, or mistyped input;
- source spans suitable for command-line, IDE, and conformance diagnostics;
- explicit path, identity, version, and digest representations;
- deterministic canonical serialization for package-manager output and fixtures;
- a closed extension policy that prevents hidden build semantics; and
- migration behavior that never runs implicitly during compilation.

## 4. Non-Goals

This RFC does not define:

- dependency selection, name resolution, visibility, or package graph semantics beyond their serialized representation;
- a package registry, publication protocol, archive layout, signature, or provenance trust policy;
- the internal compiler object model or cache serialization;
- a JSON parser library or programming-language binding;
- comments, trailing commas, YAML tags, environment interpolation, or executable manifest expressions;
- user-defined semantic extensions to schema `0.1`;
- a general configuration-file format for target or plugin settings;
- the Package Public Semantic API fingerprint encoding; or
- the Project Resolution Fingerprint encoding.

## 5. Terminology

This RFC uses terms from the [IndustrialMDE Glossary](../Glossary.md) and RFC-0001C.

- **Document Role** — one of Project Manifest, Package Manifest, or Dependency Lock.
- **Strict JSON Profile** — the RFC 8259 subset and additional restrictions defined by section 6.1.
- **Document Path** — the explicit path from which a build document was read.
- **Field Path** — an RFC 6901 JSON Pointer identifying a value or member within a parsed document; the empty pointer identifies the document root.
- **Raw Document Span** — a half-open byte range `[start, end)` in the original document bytes.
- **Canonical Data Model** — a validated schema value after uniqueness of RFC-0001C canonical collection keys has been established and semantically unordered collections have been sorted by those keys.
- **Canonical Serialization** — the RFC 8785 JSON Canonicalization Scheme output of the Canonical Data Model.
- **Content Digest** — an algorithm-qualified digest record containing an exact lowercase hexadecimal value.

## 6. Normative Specification

### 6.1 Strict JSON Profile

Each schema `0.1` document MUST be one JSON object conforming to [RFC 8259](https://www.rfc-editor.org/rfc/rfc8259).

The following additional rules apply:

- the input MUST be valid UTF-8 without a byte-order mark;
- the top-level value MUST be an object;
- every object member name MUST be unique within that object;
- an unpaired UTF-16 surrogate escape is invalid;
- comments and trailing commas are invalid;
- object member order has no semantic meaning;
- every member and value MUST be recognized by the applicable closed schema;
- JSON numbers, booleans, and `null` are not used by schema `0.1`; and
- a parser MUST NOT accept a non-standard token, escape, numeric spelling, or preprocessing extension.

A duplicate member MUST be diagnosed from the token stream before an implementation converts the object to a map that could discard an occurrence.

Strings are compared after JSON escape decoding as sequences of Unicode scalar values. An implementation MUST NOT normalize, case-fold, trim, interpolate, or otherwise rewrite a decoded string unless the field-specific rule explicitly requires a validation projection such as the RFC-0001C ASCII Case-Folded Key.

All schema `0.1` field names and all permitted field values are ASCII. JSON Unicode escapes MAY spell an ASCII scalar, but canonical output uses the RFC 8785 string representation.

### 6.2 Encoding, Whitespace, and Newlines

Documents MUST be valid UTF-8. A UTF-8 byte-order mark, UTF-16, UTF-32, invalid UTF-8, and replacement-character recovery are prohibited.

Outside JSON strings, the profile permits:

- space (`U+0020`);
- horizontal tab (`U+0009`);
- line feed (`U+000A`); and
- carriage return only when immediately followed by line feed.

A lone carriage return is invalid. Line-feed and carriage-return/line-feed presentations have identical parsed meaning but different raw bytes and raw spans.

Whitespace before or after the top-level object is permitted. It has no semantic meaning. Canonical Serialization contains no insignificant whitespace.

### 6.3 Canonical Filenames and Selection

Schema `0.1` defines these exact lowercase filenames:

| Document role | Canonical filename |
| --- | --- |
| Project Manifest | `industrialmde.project.json` |
| Package Manifest | `industrialmde.package.json` |
| Dependency Lock | `industrialmde.lock.json` |

Compilation still begins from an explicitly supplied Project Manifest path as required by RFC-0001C. The canonical filename MUST NOT authorize current-directory or parent-directory discovery.

The supplied Project Manifest path MUST end in `industrialmde.project.json`. Its `root_package_manifest` field MUST identify a portable Project-relative path whose final segment is `industrialmde.package.json`. When present, its `dependency_lock` field MUST identify a portable Project-relative path whose final segment is `industrialmde.lock.json`.

A portable Project-relative path uses the exact segment grammar, separators, reserved-name restrictions, and lexical non-escape rules of an RFC-0001C Portable Package Path, but its resolution base is the Project root rather than a package root. Filesystem containment, link, and cross-path collision validation remains governed by RFC-0001C. The path does not become a Compilation Unit or semantic identity component.

An immutable dependency package artifact MUST place its one Package Manifest at exact artifact-root path `industrialmde.package.json`.

RFC-0001C requires each selected build document to be a regular non-link file and governs link-free resolution below the applicable Project, package, or artifact root. This RFC validates the serialized path before that filesystem or artifact check.

Alternate filenames require a later schema version. A compiler MUST NOT guess a document role from object members or accept a renamed document as schema `0.1`.

### 6.4 Document Spans and Field Paths

Every syntax or schema diagnostic MUST be representable by:

- Document Role;
- Document Path or explicit non-file origin;
- a half-open Raw Document Span `[start, end)` in original UTF-8 bytes; and
- a Field Path when parsing reached a unique structural location.

For a document inside an immutable package artifact, the non-file origin is the structured tuple `(locked Package Content Identity, artifact-relative Document Path)`. Its display rendering is not an identity component. A host cache path, extraction directory, process identifier, or download timestamp MUST NOT be used as the stable origin.

Raw byte offset zero identifies the first byte of the document. Human-readable lines and columns follow RFC-0001 rules: they are one-based, line feed and carriage-return/line-feed each count as one logical newline, Unicode scalar values count as columns, and a horizontal tab advances to the next one-based tab stop in columns 1, 5, 9, and so on.

For a duplicate object member:

- the second and later member-name token is the primary span;
- the first member-name token is related information; and
- the decoded member name is included in the diagnostic facts.

For a missing required member, the primary span is the closing brace of the containing object and the Field Path identifies the missing member.

For an unknown member, the primary span is its member-name token, the containing object is related information, and the Field Path identifies the unknown member.

### 6.5 Common Value Records

#### 6.5.1 Schema Version

Every top-level document MUST contain:

```text
"schema_version": "0.1"
```

`schema_version` is a required top-level string. Its position among object members has no semantic meaning. A schema `0.1` reader MUST reject every other value without fallback.

#### 6.5.2 Package Identity

A Package Identity is encoded as:

```json
{
  "authority": "com.acme.automation",
  "name": "water-treatment"
}
```

The object contains exactly `authority` and `name`. Their decoded values MUST satisfy RFC-0001C Package Authority and Package Name grammar.

The two strings remain structured components. A tool MUST NOT treat `authority + "/" + name` or another concatenation as the canonical in-memory identity.

#### 6.5.3 Package Version

A Package Version is encoded as one JSON string using the exact RFC-0001C three-component form:

```json
"1.2.3"
```

It MUST NOT be encoded as a JSON number, array, or object. Parsing each decimal component uses exact integer arithmetic and RFC-0001C range and leading-zero rules.

#### 6.5.4 Language Version

One Language Version is encoded as a JSON string using the RFC-0001 source-directive grammar. For example:

```json
"0.1"
```

The decoded value contains exactly two ASCII decimal components separated by one dot. Each component has no leading zero unless it is exactly `0`. A patch component, range, wildcard, prerelease label, and build label are invalid.

Schema `0.1` does not accept a list or range of language versions. RFC-0001C requires one exact effective language version throughout one foundational Project and separately validates compiler support. Manifest schema version `0.1` and language version `0.1` are independent coordinates; an unsupported but well-formed Language Version is not an unsupported manifest schema.

#### 6.5.5 Content Digest

A Content Digest is encoded as:

```json
{
  "algorithm": "sha256",
  "value": "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"
}
```

The object contains exactly `algorithm` and `value`.

For algorithm `sha256`:

- `value` MUST contain exactly 64 lowercase ASCII hexadecimal digits;
- uppercase hexadecimal digits are invalid rather than normalized; and
- the digest represents the exact bytes named by the owning field.

A later schema may register another algorithm. Schema `0.1` accepts only `sha256`.

#### 6.5.6 Package Content Identity

An immutable dependency Package Content Identity is encoded as:

```json
{
  "kind": "immutable-artifact",
  "algorithm": "sha256",
  "value": "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"
}
```

The object contains exactly `kind`, `algorithm`, and `value`. Schema `0.1` accepts only fixed kind `immutable-artifact` in a Dependency Lock. The root `workspace-snapshot` identity is computed from the compilation snapshot and is not serialized into that lock.

`algorithm` and `value` satisfy the Content Digest rules in section 6.5.5.

#### 6.5.7 Portable Package Path

A Portable Package Path is encoded as one JSON string and MUST satisfy the RFC-0001C lexical path rules before host-path conversion. Filesystem containment, link, existence, directory, and cross-path collision checks occur later under RFC-0001C.

The JSON spelling uses `/` separators. Backslashes, URI decoding, percent decoding, Unicode normalization, and host-native separator replacement MUST NOT occur while validating the serialized value.

### 6.6 Project Manifest Schema

The Project Manifest contains exactly these members:

| Member | JSON kind | Requirement |
| --- | --- | --- |
| `schema_version` | string | Required; exact `0.1` |
| `root_package_manifest` | string | Required portable Project-relative path ending in `industrialmde.package.json` |
| `dependency_lock` | string | Optional portable Project-relative path ending in `industrialmde.lock.json` |
| `language_version` | string | Required Language Version |
| `project_configuration_identity` | Content Digest object | Optional; required by RFC-0001C when external project configuration changes semantic or generated results |

No other member is permitted.

`dependency_lock` MAY be absent only for a build mode that RFC-0001C permits to be unlocked and non-reproducible. Its absence MUST NOT cause implicit lock discovery.

`project_configuration_identity` identifies external configuration bytes declared through a later owning contract. It does not embed configuration, authorize an undeclared configuration source, or make a missing configuration available.

### 6.7 Package Manifest Schema

The Package Manifest contains exactly these members:

| Member | JSON kind | Requirement |
| --- | --- | --- |
| `schema_version` | string | Required; exact `0.1` |
| `package` | Package Identity object | Required |
| `version` | string | Required Package Version |
| `language_version` | string | Required Language Version |
| `modules` | array of Module objects | Required and non-empty |
| `dependencies` | array of Dependency Declaration objects | Required; may be empty |

No other member is permitted.

#### 6.7.1 Module Object

A Module object contains exactly:

| Member | JSON kind | Requirement |
| --- | --- | --- |
| `name` | string | Required RFC-0001 Identifier |
| `exposure` | string | Required; `exported` or `internal` |
| `source_roots` | array of strings | Required, non-empty set of Portable Package Paths |
| `dependencies` | array of strings | Required, possibly empty set of direct Module names |

Duplicate Module names, ASCII case-only Module-name collisions, duplicate Source Roots, duplicate module-dependency names, self-dependencies, overlapping Source Roots, and unknown dependency targets are semantic errors governed by RFC-0001C.

#### 6.7.2 Dependency Declaration Object

A Dependency Declaration object contains exactly:

| Member | JSON kind | Requirement |
| --- | --- | --- |
| `alias` | string | Required RFC-0001 Identifier |
| `package` | Package Identity object | Required |
| `version` | string | Required exact Package Version |

Duplicate aliases, ASCII case-only alias collisions, duplicate target Package Identities, self-dependencies, and non-exact requirements are semantic errors governed by RFC-0001C.

### 6.8 Dependency Lock Schema

The Dependency Lock contains exactly these members:

| Member | JSON kind | Requirement |
| --- | --- | --- |
| `schema_version` | string | Required; exact `0.1` |
| `root` | Root Package object | Required |
| `packages` | array of Locked Package objects | Required; may be empty |
| `edges` | array of Locked Edge objects | Required; may be empty |

No other member is permitted.

The root workspace package is represented only by `root`; it MUST NOT also appear in `packages`. Its Workspace Content Fingerprint is computed from the immutable compilation snapshot and is not stored in the lock that participates in the Project Resolution Fingerprint.

#### 6.8.1 Root Package Object

The Root Package object contains exactly:

| Member | JSON kind | Requirement |
| --- | --- | --- |
| `package` | Package Identity object | Required |
| `version` | string | Required Package Version |

#### 6.8.2 Locked Package Object

A Locked Package object contains exactly:

| Member | JSON kind | Requirement |
| --- | --- | --- |
| `package` | Package Identity object | Required |
| `version` | string | Required Package Version |
| `content_identity` | Package Content Identity object | Required tagged digest of exact immutable artifact bytes |
| `manifest_digest` | Content Digest object | Required digest of exact `industrialmde.package.json` bytes within that artifact |
| `origin` | string | Required opaque retrieval locator and provenance value |

`origin` MUST be a non-empty sequence of printable ASCII characters from `U+0021` through `U+007E`. It is not parsed into Package Identity and does not prove publisher ownership. A Package Distribution RFC MAY define retrieval behavior for registered origin prefixes without changing schema `0.1` acceptance. Restricting or otherwise changing the accepted `origin` grammar requires a new manifest schema version.

The `packages` array MUST contain exactly one entry for every immutable dependency Package Identity reachable from `root` and MUST NOT contain another revision of the same identity.

#### 6.8.3 Locked Edge Object

A Locked Edge object contains exactly:

| Member | JSON kind | Requirement |
| --- | --- | --- |
| `consumer` | Package Identity object | Required root or locked consuming Package |
| `alias` | string | Required Dependency Alias from the consumer Package Manifest |
| `target` | Package Identity object | Required identity present in `packages` |

The exact target version and content identity are obtained from the unique `packages` entry for `target`. An edge MUST NOT repeat version or digest fields that could disagree with that entry.

### 6.9 Cross-Document Validation

Parsing a valid JSON document does not make the document graph valid. Before publishing a Resolved Project Graph, validation MUST establish at least:

- Project `language_version` equals the root Package `language_version`;
- the compiler explicitly supports that exact Project Language Version;
- every participating source-file `dsl` version equals the Project language version;
- every dependency Package language version equals the Project language version in foundational version `0.1`;
- the root Package Identity and Package Version equal the lock `root` values;
- every Package Manifest Dependency Declaration has exactly one matching edge whose consumer, alias, and target identity agree and whose target Locked Package has the exact required version;
- every edge has exactly one matching Dependency Declaration under the same rule;
- every edge target has exactly one Locked Package entry;
- each locked artifact and embedded manifest matches its recorded digest;
- every locked Package Manifest identity and version matches its Locked Package entry;
- every Locked Package is reachable from `root`; and
- no root package or extra revision is present in `packages`.

Serialization diagnostics from this RFC are emitted before the RFC-0001C semantic diagnostics that require a successfully parsed field. An implementation MAY continue within deterministic diagnostic limits when recovery cannot change which original byte span is reported.

### 6.10 Closed Schemas and Extensions

Every schema `0.1` object is closed. An unknown member is an Error even when its name begins with `x-`, `_`, a vendor prefix, or a reverse-domain prefix.

There is no `extensions`, `metadata`, include, profile, condition, or plugin-owned member in schema `0.1`.

A later schema version may define extension points only when it also defines:

- ownership and collision rules;
- whether extension data can affect build meaning;
- ordering and fingerprint participation;
- compatibility behavior for implementations that do not support the extension; and
- security and resource limits.

An implementation MUST NOT preserve an unknown member while silently ignoring it during compilation and later re-emit it as if the document were valid.

### 6.11 Canonical Serialization

Canonical Serialization is used for deterministic tool output, conformance fixtures, and any public operation that explicitly requests canonical bytes. A valid input document is not required to arrive in canonical form.

Schema `0.1` uses only objects, arrays, and ASCII strings and rejects duplicate names and invalid Unicode, so its validated data model remains within the [I-JSON](https://www.rfc-editor.org/rfc/rfc7493) constraints required by RFC 8785.

Canonicalization proceeds as follows:

1. parse and validate the complete document under this RFC;
2. establish under RFC-0001C that every semantically unordered array in that document has unique canonical keys;
3. construct the typed validated document value;
4. sort every semantically unordered array by its canonical key to form the Canonical Data Model;
5. serialize the resulting JSON value using [RFC 8785 JSON Canonicalization Scheme](https://www.rfc-editor.org/rfc/rfc8785); and
6. emit exactly the RFC 8785 bytes with no byte-order mark, prefix, suffix, or trailing newline.

A document with a duplicate canonical collection key has no Canonical Serialization. The applicable RFC-0001C diagnostic is emitted; input order MUST NOT be used as a tie-breaker. An ASCII-case collision whose exact canonical keys differ may still be ordered deterministically, but remains an RFC-0001C semantic error. Canonicalizing one document does not by itself claim full semantic or unavailable cross-document validation.

The canonical array keys are:

| Array | Canonical key |
| --- | --- |
| `modules` | Module Name by exact ASCII bytes |
| Module `source_roots` | Portable Package Path by exact ASCII bytes |
| Module `dependencies` | target Module Name by exact ASCII bytes |
| Package `dependencies` | Dependency Alias, then target Package Identity |
| Lock `packages` | Package Identity |
| Lock `edges` | consumer Package Identity, Dependency Alias, target Package Identity |

Sorting is performed on validated decoded values before JSON serialization. JSON member order in a non-canonical input MUST NOT affect the result.

The exact source document bytes remain the input to raw-document digests such as `manifest_digest`. Canonical Serialization MUST NOT silently replace those bytes while verifying a lock.

### 6.12 Validation and Diagnostics

This RFC reserves diagnostics `IMDE4101` through `IMDE4107`:

| Code | Severity | Condition | Required facts |
| --- | --- | --- | --- |
| `IMDE4101` | Error | Invalid encoding, prohibited BOM, or prohibited newline form | Document role, origin, byte span, and failure kind |
| `IMDE4102` | Error | Malformed JSON, prohibited Unicode escape, or non-standard JSON extension | Document role, byte span, and expected JSON token or scalar class |
| `IMDE4103` | Error | Duplicate object member | Decoded member name and first and repeated spans |
| `IMDE4104` | Error | Missing or unknown object member | Document role, Field Path, member name, and containing-object span |
| `IMDE4105` | Error | Wrong JSON value kind or invalid field value | Field Path, expected kind or grammar, and observed value kind |
| `IMDE4106` | Error | Wrong document filename or invalid serialized Portable Package Path | Document role, path value, and required filename or path rule |
| `IMDE4107` | Error | Unsupported manifest or lock schema version | Document role, declared version, and supported versions |

Semantic graph, identity, lock consistency, digest, cycle, visibility, language-version, and resource-limit errors retain the applicable RFC-0001C `IMDE4xxx` codes.

Duplicate or colliding keys inside semantically unordered arrays are semantic collection errors governed by RFC-0001C. They are not duplicate JSON object members and MUST NOT be reported as `IMDE4103`.

A fix-it MAY suggest a missing canonical filename or a safely removable unknown member. A compiler MUST NOT apply the fix, rewrite the document, sort an array, regenerate a digest, or update the lock during compilation.

## 7. Determinism and Ordering

Document diagnostics are ordered by:

1. validation layer in order RFC-0001D encoding, JSON, and schema diagnostics, then RFC-0001C semantic document-graph diagnostics;
2. Document Role in order Project Manifest, root Package Manifest, dependency Package Manifest, Dependency Lock;
3. for a dependency Package Manifest, the expected Package Identity from the lock and then its locked Package Content Identity;
4. stable Document Path by exact bytes or structured non-file origin by its canonical component keys;
5. primary Raw Document Span start, then end;
6. diagnostic code; and
7. Field Path by exact UTF-8 bytes.

When an expected Package Identity or locked Content Identity is unavailable because earlier validation failed, its position is represented by an explicit absent marker that sorts before a present value, and the stable Document Path or non-file origin determines the remaining order. Host cache and extraction paths are never ordering inputs.

Canonical Serialization MUST produce identical bytes for semantically identical validated schema values regardless of:

- input object-member order;
- input whitespace and permitted newline presentation;
- input ordering of semantically unordered arrays;
- JSON escape choice for the same scalar sequence;
- host locale;
- filesystem enumeration;
- map iteration;
- concurrency; or
- parser-library object ordering.

Raw document hashes and raw spans MAY differ when presentation bytes differ. Parsed meaning and Canonical Serialization MUST remain equal.

## 8. Compatibility and Migration

Schema version `0.1` is exact. A reader MUST NOT interpret an unknown schema using best effort, a nearest supported version, or the language version.

A well-formed but unsupported `language_version` does not select another manifest schema and is not `IMDE4107`. It reaches RFC-0001C language-version validation and produces `IMDE4014` when the Project, Package, source, or compiler constraints do not permit it.

The following changes do not change schema `0.1` meaning:

- object-member reordering;
- permitted whitespace or newline presentation changes;
- equivalent JSON escapes for the same permitted ASCII value; and
- reordering an array declared semantically unordered by this RFC; and
- a compiler adding support for another well-formed Language Version without changing the serialized field grammar.

The following require a new schema version:

- adding, removing, or renaming a member;
- changing whether a member is required;
- changing a JSON value kind;
- changing a field grammar or identity interpretation;
- adding an extension point;
- changing a canonical array key; or
- changing cross-document meaning.

Changing only Canonical Serialization while preserving the data model also requires a new schema version or an independently versioned canonicalization contract because it changes public bytes.

Migration MUST be an explicit user-selected operation. Compilation MUST NOT update a schema, rename a member, insert a default, rewrite presentation, or mutate a lock.

A migration tool MUST:

- name the source and target schema versions;
- validate the complete source document before migration unless a documented recovery mode is selected;
- report every semantic change and dropped field;
- write the target to a distinct output or require explicit replacement approval; and
- produce deterministic output for the same input and migration configuration.

## 9. Safety and Security Considerations

All document bytes are untrusted input.

Implementations MUST enforce deterministic limits for:

- total document bytes;
- JSON nesting depth;
- object member count;
- array element count;
- decoded string length;
- diagnostics per document; and
- total parsed document memory.

Limits and failure behavior follow RFC-0001C. A limit failure MUST NOT publish a partial Project Graph.

The strict profile reduces ambiguity by rejecting duplicate members, malformed Unicode, unknown fields, comments, interpolation, and implementation-specific JSON extensions.

Paths MUST be validated as serialized Portable Package Paths before any filesystem access. Filesystem resolution must then apply RFC-0001C containment and link rules.

An `origin` value is untrusted provenance data. A compiler MUST NOT execute it, interpolate credentials into it, fetch it during semantic interpretation, or treat its authority spelling as proof of publisher ownership.

Digest comparison SHOULD use a constant-time primitive where the selected security library provides one, but digest equality alone remains content-integrity evidence rather than publisher authentication.

## 10. Tooling and Incremental Compilation

A parser intended for diagnostics or IDE use MUST retain:

- original document bytes;
- every object-member occurrence before duplicate rejection;
- Raw Document Spans for names and values;
- decoded scalar values;
- Field Paths;
- document role and origin; and
- schema-validation state.

An internal typed representation MAY discard JSON presentation only after required diagnostics and traceability records have been published immutably.

At minimum, independent fingerprints are needed for:

- raw document bytes;
- validated typed document meaning;
- Canonical Serialization bytes; and
- the RFC-0001C Project Resolution inputs that consume the documents.

A formatting-only edit changes the raw-document fingerprint. It need not change the typed-meaning or Canonical Serialization fingerprint. A manifest whose exact raw bytes are locked by `manifest_digest` still requires an explicit lock update after a formatting-only byte change.

## 11. Examples

Examples use presentation whitespace for readability. They are valid inputs but are not RFC 8785 canonical bytes.

### 11.1 Positive Project Manifest

```json
{
  "schema_version": "0.1",
  "root_package_manifest": "industrialmde.package.json",
  "dependency_lock": "industrialmde.lock.json",
  "language_version": "0.1"
}
```

### 11.2 Positive Package Manifest

```json
{
  "schema_version": "0.1",
  "package": {
    "authority": "com.acme.automation",
    "name": "water-treatment"
  },
  "version": "0.1.0",
  "language_version": "0.1",
  "modules": [
    {
      "name": "Application",
      "exposure": "internal",
      "source_roots": ["src/application"],
      "dependencies": ["Domain"]
    },
    {
      "name": "Domain",
      "exposure": "exported",
      "source_roots": ["src/domain"],
      "dependencies": []
    }
  ],
  "dependencies": [
    {
      "alias": "Motors",
      "package": {
        "authority": "org.industrialmde",
        "name": "motor-library"
      },
      "version": "1.2.3"
    }
  ]
}
```

### 11.3 Positive Dependency Lock

```json
{
  "schema_version": "0.1",
  "root": {
    "package": {
      "authority": "com.acme.automation",
      "name": "water-treatment"
    },
    "version": "0.1.0"
  },
  "packages": [
    {
      "package": {
        "authority": "org.industrialmde",
        "name": "motor-library"
      },
      "version": "1.2.3",
      "content_identity": {
        "kind": "immutable-artifact",
        "algorithm": "sha256",
        "value": "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"
      },
      "manifest_digest": {
        "algorithm": "sha256",
        "value": "abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789"
      },
      "origin": "https://packages.example.invalid/org.industrialmde/motor-library/1.2.3"
    }
  ],
  "edges": [
    {
      "consumer": {
        "authority": "com.acme.automation",
        "name": "water-treatment"
      },
      "alias": "Motors",
      "target": {
        "authority": "org.industrialmde",
        "name": "motor-library"
      }
    }
  ]
}
```

### 11.4 Negative Duplicate Member

```json
{
  "schema_version": "0.1",
  "schema_version": "0.2",
  "root_package_manifest": "industrialmde.package.json",
  "language_version": "0.1"
}
```

Expected result: `IMDE4103` on the second `schema_version`, with the first occurrence as related information. No last-wins or first-wins map is constructed.

### 11.5 Negative Unknown Member

```json
{
  "schema_version": "0.1",
  "root_package_manifest": "industrialmde.package.json",
  "language_version": "0.1",
  "extensions": {}
}
```

Expected result: `IMDE4104` for unknown member `/extensions`.

### 11.6 Negative Numeric Version

```json
{
  "schema_version": "0.1",
  "package": {
    "authority": "com.acme.automation",
    "name": "water-treatment"
  },
  "version": 1.2,
  "language_version": "0.1",
  "modules": [
    {
      "name": "Domain",
      "exposure": "internal",
      "source_roots": ["src/domain"],
      "dependencies": []
    }
  ],
  "dependencies": []
}
```

Expected result: `IMDE4105` at `/version`. Version components are never derived from a floating-point JSON number.

### 11.7 Negative Root Repeated as Locked Package

A lock whose `packages` array contains the same Package Identity as `root` is structurally parseable but semantically invalid.

Expected result: RFC-0001C `IMDE4004`. The root workspace snapshot is not an immutable dependency artifact entry.

### 11.8 Boundary and Conformance Fixtures

Fixtures MUST include:

- empty, one-byte, malformed UTF-8, and BOM-prefixed documents;
- line-feed, carriage-return/line-feed, and rejected lone-carriage-return input;
- every JSON value kind at each required field;
- duplicate members at the top level and in every nested object kind;
- equal decoded member names written with different JSON escapes;
- missing and unknown members for every object kind;
- unpaired high and low surrogate escapes;
- maximum active byte, depth, member, array, string, and diagnostic limits and one above each;
- versions at `0.0.0` and `2147483647.2147483647.2147483647`;
- well-formed Language Versions such as `0.1` and `1.0`, malformed leading-zero or extra-component forms, and a well-formed unsupported version producing `IMDE4014` rather than `IMDE4107`;
- digests with 63, 64, and 65 digits and uppercase hexadecimal;
- shuffled object members and semantically unordered arrays producing identical Canonical Serialization;
- duplicate and ASCII case-only Module and alias keys;
- a Project Manifest with and without each optional member, including explicit unlocked-mode and production-mode handling when `dependency_lock` is absent;
- canonical and rejected Project-relative manifest and lock paths, including wrong final filenames;
- a zero-dependency lock;
- unreachable, missing, duplicate, and extra lock entries and edges; and
- randomized parser-map and filesystem iteration producing identical diagnostics.

## 12. Alternatives Considered

### 12.1 YAML

Rejected for schema `0.1` because aliases, tags, implicit scalar typing, duplicate-key behavior, and implementation profiles create more observable parser choices than the foundational documents require.

### 12.2 TOML

Rejected for schema `0.1` because nested graph records and canonical serialization would require additional project-specific rules, while strict JSON already provides the necessary structured values and mature interchange specifications.

### 12.3 Custom IndustrialMDE Manifest Syntax

Rejected because it would require a second lexer, parser, formatter, source-span contract, and security surface before the DSL reference spike provides evidence that a custom syntax adds value.

### 12.4 General JSON Without a Profile

Rejected because duplicate members, non-standard extensions, malformed Unicode handling, and numeric conversion would vary across libraries.

### 12.5 Comments and Trailing Commas

Rejected for schema `0.1` because neither is part of RFC 8259 and accepting them would create another public dialect. A later schema may select a different public format through explicit migration.

### 12.6 Store the Root Workspace Fingerprint in the Lock

Rejected because the lock participates in the complete Project Resolution inputs. Recording a fingerprint whose input includes the lock would create a self-referential digest. The root Workspace Content Fingerprint and the complete Project Resolution Fingerprint remain separate RFC-0001C concepts.

### 12.7 Use Canonicalized Manifest Bytes for `manifest_digest`

Rejected because the lock is intended to detect exact published bytes. Canonical meaning fingerprints may coexist, but they do not replace exact artifact and manifest integrity checks.

## 13. Unresolved Questions and Delegated Decisions

Schema `0.1` has no unresolved serialization behavior required for Proposed review.

The following adjacent decisions remain delegated:

| Topic | Current rule | Owner |
| --- | --- | --- |
| Package origin schemes and retrieval | `origin` is opaque printable ASCII provenance | Package Distribution RFC |
| Canonical package archive | Lock hashes exact artifact bytes | Package Distribution RFC |
| Signatures and authority ownership | Not established by JSON or SHA-256 | Security and Package Distribution RFCs |
| Project configuration document format | Only an optional identity is represented here | Owning target/plugin/configuration RFC |
| Numeric production resource minima | Deterministic limits required; exact minima unset | Compiler Conformance Specification |
| Internal parsed representation and parser library | Must preserve observable behavior | ADR or implementation |

No delegated owner may silently change schema `0.1` bytes or meaning.

## 14. Conformance Requirements

An implementation conforms to an Accepted version of this RFC only if it:

- accepts only the defined UTF-8 Strict JSON Profile;
- rejects a byte-order mark, malformed UTF-8, lone carriage return, comments, and trailing commas;
- detects every duplicate object member before map construction;
- rejects unpaired surrogate escapes;
- validates exact filenames and document roles without discovery;
- enforces every required, optional, and prohibited member;
- rejects every unknown member;
- validates exact value kinds and field grammars;
- preserves Raw Document Spans and Field Paths for required diagnostics;
- distinguishes the root workspace from immutable locked package entries;
- performs the required cross-document checks with RFC-0001C;
- produces deterministic diagnostics and Canonical Serialization;
- does not mutate a document or lock during compilation;
- enforces deterministic resource limits; and
- passes all positive, negative, boundary, compatibility, canonicalization, and randomized-order fixtures.

Conformance to this RFC does not establish conformance to dependency resolution, name resolution, Type System, execution, package distribution, or target generation beyond the serialized fields governed here.

## 15. Non-Normative Implementation Notes

A conforming parser commonly requires a token-preserving object representation because a normal dictionary cannot report duplicate members after they have been overwritten.

A useful internal pipeline is:

```text
raw bytes
→ strict UTF-8 and newline validation
→ JSON tokens with raw spans
→ duplicate-preserving JSON value
→ closed-schema validation
→ typed immutable document
→ RFC-0001C semantic validation
```

The parser library, typed classes, JSON Pointer library, digest library, and RFC 8785 implementation are replaceable choices. Tests should include differential parsing against more than one independent JSON implementation, but only this RFC determines acceptance.

An experimental reference spike MAY initially support only a declared subset of document-size limits. It must identify itself as non-conforming and must not alter the public schema.

## 16. References and Change Log

### 16.1 External References

- [RFC 6901: JavaScript Object Notation (JSON) Pointer](https://www.rfc-editor.org/rfc/rfc6901)
- [RFC 7493: The I-JSON Message Format](https://www.rfc-editor.org/rfc/rfc7493)
- [RFC 8259: The JavaScript Object Notation (JSON) Data Interchange Format](https://www.rfc-editor.org/rfc/rfc8259)
- [RFC 8785: JSON Canonicalization Scheme](https://www.rfc-editor.org/rfc/rfc8785)

### 16.2 Change Log

#### Draft — 2026-07-20

- Defined strict JSON schema `0.1` for Project Manifests, Package Manifests, and Dependency Locks.
- Defined canonical filenames, UTF-8 handling, closed schemas, duplicate detection, spans, diagnostics, and migration.
- Defined exact Package Identity, Package Version, language-version, path, digest, Module, dependency, lock-package, and lock-edge encodings.
- Defined stable artifact-based diagnostic origins independent of host cache paths.
- Defined RFC 8785 Canonical Serialization after semantic array ordering and canonical-key uniqueness validation.
- Kept root Workspace Content Fingerprint outside the lock to avoid self-referential hashing.
