# Spike A: Experimental Structural Input

| Field | Value |
| --- | --- |
| Contract identifier | `experimental-structural-input/0` |
| Status | Experimental |
| Language version | `0.1` |
| JSON Schema dialect | Draft 2020-12 |
| Intended consumer | Structural Reference Spike A |
| Normative scope | This experimental contract only |
| Public compatibility | None |

## 1. Purpose and Lifecycle

This document defines the expression-free fixture contract that supplies the two immutable inputs required by [`Spike_A_Experimental_Snapshot.md`](Spike_A_Experimental_Snapshot.md):

1. a fixture representation of **Resolved Project Context**; and
2. **Collected Structural Input** containing declaration candidates, unresolved references, one unresolved Application Assembly selector request, origins, and typed unsupported-feature markers.

The contract exists only to unblock deterministic testing of Structural Reference Spike A. It is:

- **Experimental**;
- **Non-normative**;
- **Non-conforming**;
- **Non-interoperable**;
- **not** `.plant` grammar;
- **not** the public Project, Package, or Dependency Lock serialization owned by RFC-0001D;
- **not** a public compiler API;
- **not** Canonical IR; and
- **not** a compatibility promise.

Schema `0` may be deleted and replaced by schema `1` without migration or backward compatibility. A fixture consumer MUST compare the complete `schema` value and MUST reject every unknown identifier.

This document does not authorize a production parser, compiler implementation, production `.plant` fixture, RFC status promotion, or treatment of the experimental input as a stable serialization.

## 2. Pipeline Boundary

The loader consumes one UTF-8 JSON document and, on complete success, publishes two immutable build-local artifacts:

```text
project_context
+ compilation_units[*] ownership and source-identity fields
    -> Resolved Project Context fixture artifact

selector_request
+ compilation_units[*] collected language, namespace, import,
  declaration, reference, marker, and origin fields
    -> Collected Structural Input fixture artifact
```

The loader MUST NOT publish either artifact when framing, parsing, closed-schema validation, loader-resource validation, or cross-record input-integrity validation fails.

Collected Structural Input deliberately stops before semantic resolution. It MUST NOT contain:

- a resolved Declaration Identity or build-local declaration handle;
- a resolved Type Identity;
- a prevalidated or resolved Assembly selector;
- a Structural Validation Closure or Expansion Closure;
- an Instance, Endpoint, or Connection Occurrence Identity;
- an expanded occurrence graph;
- snapshot provenance;
- a snapshot record; or
- a diagnostic preassigned to a later pipeline step.

Pipeline step 1 owns ordinary-symbol collision handling, Declaration Identity construction, reference resolution, and RFC-0002 intrinsic type recognition. Pipeline step 2b alone owns Assembly selector resolution and root-Package-Revision validation.

## 3. Top-Level Document

The top-level JSON object contains exactly:

| Field | Meaning |
| --- | --- |
| `schema` | Exact contract identifier `experimental-structural-input/0` |
| `project_context` | Closed resolved package, dependency, Module, fingerprint, and limit facts |
| `selector_request` | One selector-submission envelope containing a bounded candidate list |
| `compilation_units` | Logical Compilation Units carrying imports and collected declaration candidates |

JSON object member order has no semantic meaning. Arrays whose order is semantically a set are normalized as specified in section 11. Only Definition and Application Assembly `members` arrays carry semantic declaration order.

## 4. Resolved Project Context Fixture

`project_context` carries the minimum already-resolved RFC-0001C facts needed by the spike:

- exact language version;
- exact root Package Revision;
- every resolved immutable dependency Package Revision;
- direct package dependency edges and aliases;
- Module identities, exposure, source roots, and direct Module dependency edges;
- Project Manifest and Dependency Lock origins;
- the experimental Project Resolution Fingerprint; and
- active structural and diagnostic limits.

Compilation Unit ownership and Canonical Source Identity records are carried once in `compilation_units` and joined with `project_context` while the loader constructs the Resolved Project Context fixture artifact. Their collected language, namespace, import, declaration, reference, marker, and origin fields are projected into Collected Structural Input. This avoids two copies of one unit identity while preserving the phase boundary.

The root Package Revision is separate from `dependency_package_revisions`. The latter MUST NOT repeat the root Package Identity. Exactly one Package Revision may occur for one Package Identity.

Every dependency revision MUST be reachable from the root through `dependency_edges`. Every dependency edge target MUST name exactly one entry in `dependency_package_revisions`. Package and Module graphs MUST be acyclic. Aliases and Module relationships remain subject to RFC-0001C collision, visibility, and direct-dependency rules.

The fixture does not rerun manifest or lock resolution and does not claim to serialize those public documents. `project_manifest_origin` and `dependency_lock_origin` identify the exact fixture metadata records from which the already-resolved context was constructed.

Package Content Identity remains a structured tuple in this input contract:

```text
(kind, digest_algorithm, digest)
```

The only schema-`0` digest algorithm is `sha256`. The digest uses 64 lowercase hexadecimal characters.

## 5. Compilation Units and Collected Declarations

One `compilation_units` entry represents one RFC-0001C logical Compilation Unit. It contains:

- a structured Compilation Unit Identity;
- Canonical Source Identity components;
- exact source length in UTF-8 bytes;
- the collected language-version directive and its origin;
- one Namespace Path and its origin;
- zero or more explicit imports; and
- zero or more top-level declaration candidates or unsupported-feature markers.

Schema `0` supports the following top-level declarations:

- `definition`;
- `application-assembly`; and
- `unsupported-marker`.

A top-level Definition or Application Assembly appears in exactly one Compilation Unit. Schema `0` does not support partial declarations or owner-member merging across units.

Every Definition has one ordered `members` array containing:

- `endpoint`;
- `instance`;
- `connection`; or
- `unsupported-marker`.

Every `instance` contains exactly one `definition_reference`. Schema `0` has no cardinality field because every admitted Instance Declaration has cardinality exactly one; the closed schema rejects attempts to add replication or a count. A recognized replication construct uses an `unsupported-marker`.

Every Application Assembly has one ordered `members` array containing:

- `instance`;
- `connection`; or
- `unsupported-marker`.

An Endpoint directly owned by an Application Assembly is a closed-schema error. An unknown member `kind` is a closed-schema error, not an unsupported-feature marker.

The zero-based array index in the complete owner `members` array is the member's `declaration_ordinal`. The ordinal is derived; it MUST NOT be supplied as an input field. Unsupported markers consume their positions and therefore leave observable gaps between occurrence-producing members.

Top-level declarations carry normalized `public` or `private` visibility. Private is the source-language default, but the collector resolves that default before publishing Collected Structural Input. Visibility is not used to bypass RFC-0001C access checks.

## 6. Unresolved References

An unresolved ordinary or type reference contains only:

```text
segments: ordered raw Identifier spellings
origin:   exact reference origin
```

The loader validates Identifier shape but does not resolve, qualify, rewrite, case-fold, or classify the reference.

Pipeline step 1 interprets:

- an Instance `definition_reference` under RFC-0001B and RFC-0001C;
- an Endpoint `type_reference` under RFC-0002's type-context rule before ordinary name resolution;
- an Import `target_reference` under RFC-0001B and RFC-0001C; and
- Connection Endpoint references as unresolved member paths.

The only Type References that can produce a valid schema-`0` Endpoint are the exact intrinsic spellings `BOOL`, `INT`, `REAL`, and `TIME`. Other Identifier paths remain representable only so negative fixtures can reach the owning unresolved-reference or wrong-kind diagnostics; they cannot enter a published structural snapshot as a supported user-defined type.

A Connection Endpoint reference contains at least two segments. The contract intentionally permits a longer path so that a syntactically collected grandchild reach-through reaches semantic locality validation and receives the owning diagnostic. The first segment may be `self` in a Definition-owned Connection; an Application Assembly has no implicit `self`.

The input contract MUST NOT attach an expected or resolved semantic kind to a reference. Semantic-kind checking remains pipeline step 2a.

## 7. Assembly Selector Request

Every document contains exactly one `selector_request` submission envelope. Its `candidates` array deliberately admits zero, one, or multiple candidates so step 2b can own the RFC-0007 missing- and multiple-selector diagnostics.

Each candidate may carry a partial `target`. A complete target supplies the unresolved Canonical Declaration Identity components required for lookup:

- Package Identity;
- Namespace Path;
- owning declaration path;
- declaration identifier.

Application Assembly kind is the expected kind of the selector operation and is not an input-controlled discriminator. A candidate missing one or more target components is a bounded invalid selector record, not a schema-recovery node. Step 2b reports `SPIKEA003(incomplete)`.

Candidate `raw_spelling` is a bounded, printable-ASCII diagnostic rendering. It is trace-only: the resolver MUST use the structured `target`, MUST NOT parse `raw_spelling`, and MUST NOT allow a mismatch to select another declaration.

The submission envelope and candidates are still unresolved because they contain no resolved declaration handle, owning Package Revision, source owner, or proof of existence. Step 2b MUST:

1. require exactly one candidate;
2. require that candidate's structured target to be complete;
3. match the complete target against the step-1 candidate universe;
4. require exactly one Application Assembly;
5. require ownership by the exact root Package Revision; and
6. preserve the candidate's non-source origin, or the submission-envelope origin when no unique candidate exists.

No source-order, only-Assembly, `main`, filename, target, or cached-selector fallback is permitted.

## 8. Origins and Byte Ranges

A source origin contains:

- `kind: "source"`;
- non-empty `source_identity_components`;
- `raw_start`;
- `raw_end`.

Offsets are zero-based UTF-8 byte offsets into the exact source artifact identified by `source_identity_components`. `raw_start` is inclusive and `raw_end` is exclusive.

For every source origin:

```text
0 <= raw_start <= raw_end <= source_length_bytes
```

Every source origin nested in a Compilation Unit MUST use exactly that unit's `source_identity_components`. The input-integrity pass validates this relation before step 1.

Non-source origins identify one of:

- `project-manifest`;
- `fixture-metadata`;
- `build-metadata`; or
- `invocation`.

A non-source origin has no fabricated source offsets.

## 9. Typed Unsupported-Feature Markers

A recognized construct outside the supported structural subset is represented only as:

```text
kind
category
owning_future_rfc
owner_context
origin
opaque_payload_range
```

The payload bytes remain in the named source artifact. The fixture contains no payload text, parsed expression, normalized expression tree, executable value, callback, or placeholder structural member.

`opaque_payload_range` uses source-byte offsets and MUST lie within the marker origin and the owning Compilation Unit. The loader does not inspect or execute those bytes.

Schema `0` categories and diagnostic ownership are:

| Category | Owning future layer | Closure-local diagnostic |
| --- | --- | --- |
| `expression` | RFC-0003 | `SPIKEA001` |
| `constant` | RFC-0003 | `SPIKEA001` |
| `parameter` | RFC-0003 | `SPIKEA001` |
| `configuration-expression` | RFC-0003 | `SPIKEA001` |
| `state` | RFC-0004 | `SPIKEA001` |
| `behavior` | RFC-0004 | `SPIKEA001` |
| `interface` | RFC-0006 | `SPIKEA001` |
| `replication` | RFC-0006 | `SPIKEA001` |
| `deployment` | RFC-0007 | `SPIKEA001` |
| `target` | RFC-0007 | `SPIKEA001` |
| `deployment-mapping` | RFC-0007 / RFC-0001A | `IMDE2004` |

`owning_future_rfc` MUST agree with the fixed category table. `owner_context` records only an unresolved container kind and source identifier spelling; it is not a Declaration Identity. It MUST match the marker's actual Compilation Unit, Definition, or Application Assembly placement.

The marker is successfully classified input. If it belongs to the Structural Validation Closure, the pipeline emits the single owner shown above and blocks publication. Outside that closure it may produce a separate non-blocking diagnostic under the snapshot scope rules.

Unknown `kind` or `category` values fail this input contract. Unclassifiable source bytes fail before Collected Structural Input is created. Neither case receives a fabricated `SPIKEA001`.

## 10. Closed Draft 2020-12 JSON Schema

The following schema is complete for contract `experimental-structural-input/0`.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "urn:industrialmde:experimental:structural-input:0",
  "title": "IndustrialMDE Experimental Structural Input 0",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "schema",
    "project_context",
    "selector_request",
    "compilation_units"
  ],
  "properties": {
    "schema": {
      "const": "experimental-structural-input/0"
    },
    "project_context": {
      "$ref": "#/$defs/project-context"
    },
    "selector_request": {
      "$ref": "#/$defs/selector-request"
    },
    "compilation_units": {
      "type": "array",
      "maxItems": 1000000,
      "items": {
        "$ref": "#/$defs/compilation-unit"
      }
    }
  },
  "$defs": {
    "identifier": {
      "type": "string",
      "minLength": 1,
      "maxLength": 255,
      "pattern": "^[A-Za-z_][A-Za-z0-9_]*$",
      "not": {
        "pattern": "^__"
      }
    },
    "portable-package-path": {
      "type": "string",
      "minLength": 1,
      "maxLength": 4096,
      "pattern": "^[A-Za-z0-9_](?:[A-Za-z0-9._/-]*[A-Za-z0-9_])?$"
    },
    "namespace-path": {
      "type": "array",
      "minItems": 1,
      "maxItems": 64,
      "items": {
        "$ref": "#/$defs/identifier"
      }
    },
    "owner-path": {
      "type": "array",
      "maxItems": 64,
      "items": {
        "$ref": "#/$defs/identifier"
      }
    },
    "reference-segments": {
      "type": "array",
      "minItems": 1,
      "maxItems": 64,
      "items": {
        "$ref": "#/$defs/identifier"
      }
    },
    "endpoint-reference-segments": {
      "type": "array",
      "minItems": 2,
      "maxItems": 64,
      "items": {
        "$ref": "#/$defs/identifier"
      }
    },
    "package-identity": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "authority",
        "name"
      ],
      "properties": {
        "authority": {
          "type": "string",
          "minLength": 1,
          "maxLength": 255,
          "pattern": "^[a-z][a-z0-9]*(?:-[a-z0-9]+)*(?:\\.[a-z][a-z0-9]*(?:-[a-z0-9]+)*)*$"
        },
        "name": {
          "type": "string",
          "minLength": 1,
          "maxLength": 255,
          "pattern": "^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$"
        }
      }
    },
    "package-content-identity": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "kind",
        "digest_algorithm",
        "digest"
      ],
      "properties": {
        "kind": {
          "enum": [
            "immutable-artifact",
            "workspace-snapshot"
          ]
        },
        "digest_algorithm": {
          "const": "sha256"
        },
        "digest": {
          "type": "string",
          "pattern": "^[0-9a-f]{64}$"
        }
      }
    },
    "package-revision": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "package_identity",
        "version",
        "content_identity"
      ],
      "properties": {
        "package_identity": {
          "$ref": "#/$defs/package-identity"
        },
        "version": {
          "type": "string",
          "pattern": "^(?:0|[1-9][0-9]*)\\.(?:0|[1-9][0-9]*)\\.(?:0|[1-9][0-9]*)$"
        },
        "content_identity": {
          "$ref": "#/$defs/package-content-identity"
        }
      }
    },
    "experimental-fingerprint": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "algorithm",
        "value"
      ],
      "properties": {
        "algorithm": {
          "const": "sha256"
        },
        "value": {
          "type": "string",
          "pattern": "^[0-9a-f]{64}$"
        }
      }
    },
    "source-origin": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "kind",
        "source_identity_components",
        "raw_start",
        "raw_end"
      ],
      "properties": {
        "kind": {
          "const": "source"
        },
        "source_identity_components": {
          "type": "array",
          "minItems": 1,
          "maxItems": 16,
          "items": {
            "type": "string",
            "minLength": 1,
            "maxLength": 4096
          }
        },
        "raw_start": {
          "type": "integer",
          "minimum": 0,
          "maximum": 2147483647
        },
        "raw_end": {
          "type": "integer",
          "minimum": 0,
          "maximum": 2147483647
        }
      }
    },
    "non-source-origin": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "kind",
        "identity"
      ],
      "properties": {
        "kind": {
          "enum": [
            "project-manifest",
            "fixture-metadata",
            "build-metadata",
            "invocation"
          ]
        },
        "identity": {
          "type": "string",
          "minLength": 1,
          "maxLength": 4096
        }
      }
    },
    "active-limits": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "maximum_expansion_depth",
        "maximum_expanded_semantic_entities",
        "maximum_diagnostics"
      ],
      "properties": {
        "maximum_expansion_depth": {
          "const": 64
        },
        "maximum_expanded_semantic_entities": {
          "const": 262144
        },
        "maximum_diagnostics": {
          "type": "integer",
          "minimum": 1,
          "maximum": 1000000
        }
      }
    },
    "module-identity": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "package_identity",
        "module_name"
      ],
      "properties": {
        "package_identity": {
          "$ref": "#/$defs/package-identity"
        },
        "module_name": {
          "$ref": "#/$defs/identifier"
        }
      }
    },
    "module": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "identity",
        "exposure",
        "source_roots",
        "origin"
      ],
      "properties": {
        "identity": {
          "$ref": "#/$defs/module-identity"
        },
        "exposure": {
          "enum": [
            "exported",
            "internal"
          ]
        },
        "source_roots": {
          "type": "array",
          "minItems": 1,
          "maxItems": 1024,
          "uniqueItems": true,
          "items": {
            "$ref": "#/$defs/portable-package-path"
          }
        },
        "origin": {
          "$ref": "#/$defs/non-source-origin"
        }
      }
    },
    "dependency-edge": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "consumer",
        "alias",
        "dependency",
        "origin"
      ],
      "properties": {
        "consumer": {
          "$ref": "#/$defs/package-identity"
        },
        "alias": {
          "$ref": "#/$defs/identifier"
        },
        "dependency": {
          "$ref": "#/$defs/package-identity"
        },
        "origin": {
          "$ref": "#/$defs/non-source-origin"
        }
      }
    },
    "module-edge": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "consumer",
        "dependency",
        "origin"
      ],
      "properties": {
        "consumer": {
          "$ref": "#/$defs/module-identity"
        },
        "dependency": {
          "$ref": "#/$defs/module-identity"
        },
        "origin": {
          "$ref": "#/$defs/non-source-origin"
        }
      }
    },
    "project-context": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "language_version",
        "root_package_revision",
        "dependency_package_revisions",
        "dependency_edges",
        "modules",
        "module_edges",
        "project_manifest_origin",
        "dependency_lock_origin",
        "project_resolution_fingerprint",
        "active_limits"
      ],
      "properties": {
        "language_version": {
          "const": "0.1"
        },
        "root_package_revision": {
          "$ref": "#/$defs/package-revision"
        },
        "dependency_package_revisions": {
          "type": "array",
          "maxItems": 4096,
          "uniqueItems": true,
          "items": {
            "$ref": "#/$defs/package-revision"
          }
        },
        "dependency_edges": {
          "type": "array",
          "maxItems": 16384,
          "items": {
            "$ref": "#/$defs/dependency-edge"
          }
        },
        "modules": {
          "type": "array",
          "minItems": 1,
          "maxItems": 65536,
          "items": {
            "$ref": "#/$defs/module"
          }
        },
        "module_edges": {
          "type": "array",
          "maxItems": 262144,
          "items": {
            "$ref": "#/$defs/module-edge"
          }
        },
        "project_manifest_origin": {
          "$ref": "#/$defs/non-source-origin"
        },
        "dependency_lock_origin": {
          "$ref": "#/$defs/non-source-origin"
        },
        "project_resolution_fingerprint": {
          "$ref": "#/$defs/experimental-fingerprint"
        },
        "active_limits": {
          "$ref": "#/$defs/active-limits"
        }
      }
    },
    "selector-target-request": {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "package_identity": {
          "$ref": "#/$defs/package-identity"
        },
        "namespace_path": {
          "$ref": "#/$defs/namespace-path"
        },
        "owner_path": {
          "$ref": "#/$defs/owner-path"
        },
        "identifier": {
          "$ref": "#/$defs/identifier"
        }
      }
    },
    "selector-candidate": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "raw_spelling",
        "origin"
      ],
      "properties": {
        "target": {
          "$ref": "#/$defs/selector-target-request"
        },
        "raw_spelling": {
          "type": "string",
          "minLength": 1,
          "maxLength": 2048,
          "pattern": "^[ -~]+$"
        },
        "origin": {
          "$ref": "#/$defs/non-source-origin"
        }
      }
    },
    "selector-request": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "origin",
        "candidates"
      ],
      "properties": {
        "origin": {
          "$ref": "#/$defs/non-source-origin"
        },
        "candidates": {
          "type": "array",
          "maxItems": 16,
          "items": {
            "$ref": "#/$defs/selector-candidate"
          }
        }
      }
    },
    "compilation-unit-identity": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "package_identity",
        "module_name",
        "portable_package_path"
      ],
      "properties": {
        "package_identity": {
          "$ref": "#/$defs/package-identity"
        },
        "module_name": {
          "$ref": "#/$defs/identifier"
        },
        "portable_package_path": {
          "$ref": "#/$defs/portable-package-path"
        }
      }
    },
    "namespace": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "segments",
        "origin"
      ],
      "properties": {
        "segments": {
          "$ref": "#/$defs/namespace-path"
        },
        "origin": {
          "$ref": "#/$defs/source-origin"
        }
      }
    },
    "name-reference": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "segments",
        "origin"
      ],
      "properties": {
        "segments": {
          "$ref": "#/$defs/reference-segments"
        },
        "origin": {
          "$ref": "#/$defs/source-origin"
        }
      }
    },
    "endpoint-reference": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "segments",
        "origin"
      ],
      "properties": {
        "segments": {
          "$ref": "#/$defs/endpoint-reference-segments"
        },
        "origin": {
          "$ref": "#/$defs/source-origin"
        }
      }
    },
    "import": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "kind",
        "target_reference",
        "alias",
        "origin"
      ],
      "properties": {
        "kind": {
          "const": "import"
        },
        "target_reference": {
          "$ref": "#/$defs/name-reference"
        },
        "alias": {
          "oneOf": [
            {
              "$ref": "#/$defs/identifier"
            },
            {
              "type": "null"
            }
          ]
        },
        "origin": {
          "$ref": "#/$defs/source-origin"
        }
      }
    },
    "payload-range": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "raw_start",
        "raw_end"
      ],
      "properties": {
        "raw_start": {
          "type": "integer",
          "minimum": 0,
          "maximum": 2147483647
        },
        "raw_end": {
          "type": "integer",
          "minimum": 0,
          "maximum": 2147483647
        }
      }
    },
    "unsupported-owner-context": {
      "oneOf": [
        {
          "type": "object",
          "additionalProperties": false,
          "required": [
            "kind",
            "identifier"
          ],
          "properties": {
            "kind": {
              "const": "compilation-unit"
            },
            "identifier": {
              "type": "null"
            }
          }
        },
        {
          "type": "object",
          "additionalProperties": false,
          "required": [
            "kind",
            "identifier"
          ],
          "properties": {
            "kind": {
              "const": "definition"
            },
            "identifier": {
              "$ref": "#/$defs/identifier"
            }
          }
        },
        {
          "type": "object",
          "additionalProperties": false,
          "required": [
            "kind",
            "identifier"
          ],
          "properties": {
            "kind": {
              "const": "application-assembly"
            },
            "identifier": {
              "$ref": "#/$defs/identifier"
            }
          }
        }
      ]
    },
    "unsupported-marker": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "kind",
        "category",
        "owning_future_rfc",
        "owner_context",
        "origin",
        "opaque_payload_range"
      ],
      "properties": {
        "kind": {
          "const": "unsupported-marker"
        },
        "category": {
          "enum": [
            "expression",
            "constant",
            "parameter",
            "configuration-expression",
            "state",
            "behavior",
            "interface",
            "replication",
            "deployment",
            "target",
            "deployment-mapping"
          ]
        },
        "owning_future_rfc": {
          "enum": [
            "RFC-0003",
            "RFC-0004",
            "RFC-0006",
            "RFC-0007"
          ]
        },
        "owner_context": {
          "$ref": "#/$defs/unsupported-owner-context"
        },
        "origin": {
          "$ref": "#/$defs/source-origin"
        },
        "opaque_payload_range": {
          "$ref": "#/$defs/payload-range"
        }
      }
    },
    "endpoint-declaration": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "kind",
        "name",
        "direction",
        "type_reference",
        "origin"
      ],
      "properties": {
        "kind": {
          "const": "endpoint"
        },
        "name": {
          "$ref": "#/$defs/identifier"
        },
        "direction": {
          "enum": [
            "input",
            "output"
          ]
        },
        "type_reference": {
          "$ref": "#/$defs/name-reference"
        },
        "origin": {
          "$ref": "#/$defs/source-origin"
        }
      }
    },
    "instance-declaration": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "kind",
        "name",
        "definition_reference",
        "origin"
      ],
      "properties": {
        "kind": {
          "const": "instance"
        },
        "name": {
          "$ref": "#/$defs/identifier"
        },
        "definition_reference": {
          "$ref": "#/$defs/name-reference"
        },
        "origin": {
          "$ref": "#/$defs/source-origin"
        }
      }
    },
    "connection-declaration": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "kind",
        "name",
        "source_reference",
        "destination_reference",
        "origin"
      ],
      "properties": {
        "kind": {
          "const": "connection"
        },
        "name": {
          "$ref": "#/$defs/identifier"
        },
        "source_reference": {
          "$ref": "#/$defs/endpoint-reference"
        },
        "destination_reference": {
          "$ref": "#/$defs/endpoint-reference"
        },
        "origin": {
          "$ref": "#/$defs/source-origin"
        }
      }
    },
    "definition-member": {
      "oneOf": [
        {
          "$ref": "#/$defs/endpoint-declaration"
        },
        {
          "$ref": "#/$defs/instance-declaration"
        },
        {
          "$ref": "#/$defs/connection-declaration"
        },
        {
          "$ref": "#/$defs/unsupported-marker"
        }
      ]
    },
    "assembly-member": {
      "oneOf": [
        {
          "$ref": "#/$defs/instance-declaration"
        },
        {
          "$ref": "#/$defs/connection-declaration"
        },
        {
          "$ref": "#/$defs/unsupported-marker"
        }
      ]
    },
    "definition": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "kind",
        "name",
        "visibility",
        "members",
        "origin"
      ],
      "properties": {
        "kind": {
          "const": "definition"
        },
        "name": {
          "$ref": "#/$defs/identifier"
        },
        "visibility": {
          "enum": [
            "public",
            "private"
          ]
        },
        "members": {
          "type": "array",
          "maxItems": 1000000,
          "items": {
            "$ref": "#/$defs/definition-member"
          }
        },
        "origin": {
          "$ref": "#/$defs/source-origin"
        }
      }
    },
    "application-assembly": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "kind",
        "name",
        "visibility",
        "members",
        "origin"
      ],
      "properties": {
        "kind": {
          "const": "application-assembly"
        },
        "name": {
          "$ref": "#/$defs/identifier"
        },
        "visibility": {
          "enum": [
            "public",
            "private"
          ]
        },
        "members": {
          "type": "array",
          "maxItems": 1000000,
          "items": {
            "$ref": "#/$defs/assembly-member"
          }
        },
        "origin": {
          "$ref": "#/$defs/source-origin"
        }
      }
    },
    "top-level-declaration": {
      "oneOf": [
        {
          "$ref": "#/$defs/definition"
        },
        {
          "$ref": "#/$defs/application-assembly"
        },
        {
          "$ref": "#/$defs/unsupported-marker"
        }
      ]
    },
    "compilation-unit": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "unit_identity",
        "source_identity_components",
        "source_length_bytes",
        "language_version",
        "language_version_origin",
        "namespace",
        "imports",
        "declarations"
      ],
      "properties": {
        "unit_identity": {
          "$ref": "#/$defs/compilation-unit-identity"
        },
        "source_identity_components": {
          "type": "array",
          "minItems": 1,
          "maxItems": 16,
          "items": {
            "type": "string",
            "minLength": 1,
            "maxLength": 4096
          }
        },
        "source_length_bytes": {
          "type": "integer",
          "minimum": 0,
          "maximum": 2147483647
        },
        "language_version": {
          "const": "0.1"
        },
        "language_version_origin": {
          "$ref": "#/$defs/source-origin"
        },
        "namespace": {
          "$ref": "#/$defs/namespace"
        },
        "imports": {
          "type": "array",
          "maxItems": 65536,
          "items": {
            "$ref": "#/$defs/import"
          }
        },
        "declarations": {
          "type": "array",
          "maxItems": 1000000,
          "items": {
            "$ref": "#/$defs/top-level-declaration"
          }
        }
      }
    }
  }
}
```

JSON Schema cannot express every cross-record semantic invariant. Passing the schema is necessary but not sufficient for publishing the two input artifacts.

## 11. Input-Integrity and Deterministic Normalization

After closed-schema validation and before step 1, the loader MUST validate all of the following:

1. Package Version components are each at most `2147483647`.
2. Portable Package Paths satisfy all RFC-0001C segment, traversal, separator, case-collision, and reserved-device rules.
3. Package Revision identities are unique by Package Identity; dependency revisions do not repeat the root Package Identity.
4. Every package dependency target exists, all dependency revisions are reachable, aliases are unique in their consuming Package, and the package graph is acyclic.
5. Module identities are unique, every Module belongs to a participating Package Revision, every Module edge remains in one Package, and each Module graph is acyclic.
6. Every Compilation Unit Identity is unique and names an existing Module in the same Package.
7. Every Compilation Unit source identity is unique.
8. Every unit's `language_version` equals the Project language version.
9. Every source origin uses its owning unit's source identity and satisfies the byte-range relation in section 8.
10. Every marker payload range is ordered, lies within its marker origin, lies within the owning source, and does not exceed the fixed opaque-payload-span limit.
11. Every marker's `owning_future_rfc` agrees with its category, and `owner_context` agrees with its actual container and unresolved owner spelling.
12. Declaration and import collisions are reported under the owning RFC rules, not repaired by source order.
13. `members` index is the only source of `declaration_ordinal`; an input-provided ordinal is impossible under the closed schema.
14. No field contains a resolved identity, occurrence, expanded node, expression payload, runtime fact, or snapshot fact under an alias.

Failure of items 1 through 11 or 14 is an input-contract integrity failure and prevents step 1. Item 12 is intentionally passed to pipeline step 1 so the owning RFC diagnostic and precedence remain intact. Selector candidate cardinality, target completeness, resolution, kind, and root-Package ownership are intentionally not input-integrity conditions; they belong to step 2b.

The loader normalizes set-like collections by these keys:

| Collection | Canonical key |
| --- | --- |
| Dependency Package Revisions | RFC-0001C Package Revision key |
| Package dependency edges | consumer Package Identity, alias, dependency Package Identity |
| Modules | Package Identity, Module Name |
| Module edges | consumer Module Identity, dependency Module Identity |
| Compilation Units | Package Identity, Module Name, Portable Package Path |
| Selector candidates | target-completeness rank, present structured target components, origin, raw spelling |
| Imports in one Compilation Unit | target segments, alias or empty value, origin |
| Top-level declarations in one Compilation Unit | kind rank, identifier or empty value, origin |

Origin comparison uses the snapshot contract's origin-kind rank, then Canonical Source Identity components or non-source origin identity, then source raw start and raw end. Unsupported top-level markers use the same origin key. Unsupported member markers retain their semantic `members` positions.

Reordering any set-like input array MUST produce the same two input artifacts, diagnostics, fingerprints, and downstream snapshot. Definition and Application Assembly `members` arrays MUST NOT be reordered.

JSON object member order, filesystem discovery order, hash-map iteration, locale, concurrency, host path rules, current time, and random values MUST NOT influence normalization or diagnostics.

## 12. Mapping into Spike A

| Input fact | Consumer | Result |
| --- | --- | --- |
| `project_context` plus each unit's ownership and source identity | Boundary before step 1 | Immutable Resolved Project Context fixture artifact |
| Unit identity, namespace, imports, top-level declarations | Step 1 | Project Resolution Universe and candidate Declaration Identities |
| `definition_reference` | Step 1, then step 2a | Resolved Definition candidate, then required-kind validation |
| `type_reference` | Step 1, then step 2a | RFC-0002 intrinsic recognition or ordinary resolution, then required-kind validation |
| Connection Endpoint references | Step 1, then steps 2a and 5 | Resolved member path, required Endpoint kind, then direct-boundary locality |
| `selector_request` envelope and candidates | Carried unchanged through step 1; consumed by step 2b | Exactly one complete candidate and one selected root-Package Application Assembly, or `SPIKEA003` |
| `members` index | Steps 1 and 4 | Stable zero-based declaration ordinal retained through expansion |
| `unsupported-marker` | Carried through step 1; classified after closure construction | Closure-local `SPIKEA001` or the more-specific owner in section 9 |
| Source and non-source origins | All diagnostic steps and publication | Deterministic diagnostics and snapshot traceability |

The loader MUST NOT emit `SPIKEA001`, `SPIKEA002`, or `SPIKEA003`. Those codes require facts established by the structural pipeline.

The four scope projections are:

1. all participating project-context records and Compilation Units establish the **Project Resolution Universe**;
2. the unique selected Assembly, every transitively referenced Definition, their admitted or unsupported members, and required shared facts establish the **Structural Validation Closure**;
3. only the selected Assembly and transitively reachable occurrence-producing structural members establish the **Expansion Closure**; and
4. the complete Project Resolution Universe, including unselected and unreachable records, remains the **Diagnostic Universe**.

The top-level `schema` value is copied exactly into snapshot provenance as `input_contract_identifier`. No filename, branch name, or inferred loader version may replace it.

## 13. Loader Diagnostics and Recovery

The input contract uses an internal experimental diagnostic domain. These identifiers are not `IMDE` codes and reserve no public namespace.

| Code | Condition | Result |
| --- | --- | --- |
| `INPUT_SYNTAX_001` | Invalid UTF-8, invalid JSON, duplicate object key, or forbidden framing | Fatal; no artifacts |
| `INPUT_SCHEMA_001` | Draft 2020-12 closed-schema violation | Fatal; no artifacts |
| `INPUT_LIMIT_001` | Input byte, JSON depth, input-record, or loader-diagnostic limit exceeded | Fatal; no artifacts |
| `INPUT_INTEGRITY_001` | Cross-record invariant in section 11 fails before semantic resolution | Fatal; no artifacts |

Precedence is:

1. byte limit;
2. UTF-8 and framing;
3. JSON depth and duplicate-key-aware parsing;
4. input-record limit;
5. closed-schema validation;
6. pre-step-1 input integrity;
7. Spike A pipeline diagnostics.

Every numeric field uses an unsigned canonical decimal JSON integer token: `0` or a non-zero digit followed by decimal digits. Fractional notation, exponent notation, negative zero, and values greater than `2147483647` are rejected before artifact publication. The loader MUST NOT round through binary64.

Schema `0` performs no syntax recovery and publishes no syntax-recovery node. Validation is all-or-nothing for the complete fixture. Schema-valid unresolved references, typed unsupported markers, and zero, partial, or multiple selector candidates are intentional bounded semantic-invalidity records owned by later pipeline steps; they are not loader recovery.

A deterministic bounded set of independent loader diagnostics MAY be returned, ordered by RFC 6901 JSON Pointer with `~0` and `~1` token escaping and exact UTF-8 byte comparison, then diagnostic code, then reason. The active diagnostic limit and the fixed loader ceiling in section 14 both bound loader diagnostics.

An unknown declaration or member `kind`, an unknown marker `category`, or an unknown field is `INPUT_SCHEMA_001`. It is never rewritten into an unsupported marker.

## 14. Loader Limits and Semantic Limits

The contract fixes independent loader limits:

```text
maximum input document bytes:  10,485,760
maximum JSON depth:             32
maximum input records:          1,000,000
maximum source origins directly attached to one record: 3
maximum opaque marker payload span bytes:                1,048,576
maximum loader diagnostics:                              min(active maximum_diagnostics, 4,096)
```

`maximum input document bytes` counts the exact input bytes before UTF-8 decoding.

JSON depth counts the root value at depth `1` and increments for each nested object or array. A scalar does not add depth beyond its containing slot.

An input record is one value occurrence occupying an array slot or object-member value, including containers and scalars. The top-level root is one record. This definition prevents a very large scalar or container collection from evading the record budget. The byte limit remains independently binding.

A source origin is directly attached when it is the record's own `origin` or the origin of one of its direct reference fields. A Connection therefore has the maximum three: declaration, source reference, and destination reference. Origins nested in child member records are counted against those child records, not recursively against the owner container.

An opaque payload span is `opaque_payload_range.raw_end - opaque_payload_range.raw_start`. It is bounded even though the payload bytes are absent.

The loader MUST check a limit before admitting the next byte, nesting level, record, origin, payload span, or diagnostic. It MUST NOT first materialize an over-limit tree.

These limits are implementation-work budgets. They do not consume or weaken the RFC-0006 semantic limits:

```text
maximum expansion depth:             64
maximum published semantic entities: 262,144
```

The semantic entity count remains exactly:

```text
instances.length + endpoints.length + connections.length
```

Parser nodes, JSON values, Compilation Units, declarations, markers, symbol-table entries, diagnostics, and temporary graph nodes do not consume that semantic count. An otherwise valid selected closure at exactly `262,144` published entities remains admissible.

## 15. Security

The fixture is untrusted input.

- The loader MUST reject duplicate JSON keys before object construction.
- `additionalProperties: false` prevents unknown fields from silently changing meaning; it is not a substitute for ordinary parser hardening.
- JSON entity expansion is unavailable, but depth, byte, record, string, and array bounds remain mandatory.
- No fixture string is executed, interpolated, treated as a shell command, fetched as a URL, or loaded as a host path.
- `raw_spelling` is diagnostic-only and MUST be escaped by every terminal, log, HTML, or structured-output renderer.
- Portable Package Paths and origin identities are data. The fixture loader MUST NOT open a file merely because one of those values names it.
- Unsupported payload bytes are absent from the fixture and therefore cannot be evaluated by the loader.
- Fingerprints and digests are equality and provenance facts, not proof of trust or code safety.
- A fatal loader diagnostic MUST NOT expose unrelated host paths, environment variables, cache locations, credentials, or memory contents.

## 16. Required Fixture Matrix

The follow-up implementation task MUST create fixtures covering at least:

| Fixture | Required fact | Expected result |
| --- | --- | --- |
| `input_01_valid_flat` | One Definition, one root Instance, intrinsic Endpoint types | Loader success; step 1 begins |
| `input_02_valid_nested` | Reused Definition under distinct parents | Distinct occurrence paths |
| `input_03_empty_assembly` | Selected Assembly has no members | Empty valid snapshot |
| `input_04_schema_unknown_kind` | Misspelled member `kind` | `INPUT_SCHEMA_001`; no step 1 |
| `input_05_duplicate_key` | Duplicate JSON object key | `INPUT_SYNTAX_001`; no artifacts |
| `input_06_marker_hit` | Unsupported marker in selected closure | Loader success; closure-local `SPIKEA001` |
| `input_07_marker_miss` | Unsupported marker wholly outside selected closure | Snapshot may publish; separate non-blocking diagnostic |
| `input_08_deployment_mapping` | Exact deployment-mapping marker in closure | `IMDE2004`, not `SPIKEA001` |
| `input_09_selector_missing` | Submission has zero candidates | `SPIKEA003(missing)` at step 2b |
| `input_10_selector_multiple` | Submission has two complete candidates | `SPIKEA003(multiple)` at step 2b |
| `input_11_selector_incomplete` | One candidate omits target components | `SPIKEA003(incomplete)` at step 2b |
| `input_12_selector_unresolved` | Complete request matches no declaration | `SPIKEA003(unresolved)` at step 2b |
| `input_13_selector_wrong_kind` | Complete request matches a Definition | `SPIKEA003(wrong-kind)` at step 2b |
| `input_14_selector_dependency` | Request matches dependency-Package Assembly | `SPIKEA003(non-root-package)` at step 2b |
| `input_15_selector_private_root` | Request matches a private root-Package Assembly | Successful selection |
| `input_16_multiple_roots` | Selected Assembly declares independent roots | Ordered root forest; no synthetic root |
| `input_17_containment_direct_cycle` | Closure-local Definition self-cycle | `IMDE2001`; no expansion |
| `input_18_containment_indirect_cycle` | Multi-Definition closure cycle | `IMDE2001`; deterministic cycle path |
| `input_19_connection_contexts` | Owner-to-child, child-to-owner, sibling, and Assembly-level edges | Contextual direction table applied |
| `input_20_reach_through` | Connection path addresses a grandchild Endpoint | `SPIKEA002(endpoint-locality)` |
| `input_21_unresolved_references` | Independent unresolved Definition, Endpoint, and Type references | Owning RFC resolution diagnostics |
| `input_22_wrong_kinds` | Resolved references have wrong semantic kinds | `IMDE2007`, `IMDE2009`, or more-specific owner |
| `input_23_direction` | Resolved Endpoint has wrong contextual direction | `SPIKEA002(endpoint-direction)` |
| `input_24_type_mismatch` | Resolved Endpoint Type Identities differ | `SPIKEA002(connection-type-mismatch)`, not `IMDE5003` |
| `input_25_fan_out` | Named Connections share one source and distinct destinations | Valid fan-out |
| `input_26_duplicate_driver` | Two otherwise-valid drivers share a destination | `SPIKEA002(duplicate-driver)` |
| `input_27_unconnected_endpoint` | Endpoint has no Connection | Valid structural graph |
| `input_28_marker_categories` | Expression, State, Interface, replication, deployment, and target markers | Category-to-owner mapping in section 9 |
| `input_29_randomized_sets` | Reordered units, Modules, revisions, edges, and object fields | Byte-equivalent normalized artifacts and downstream result |
| `input_30_origin_order` | Source and all non-source origin kinds | Snapshot diagnostic and trace order |
| `input_31_ordinal_gap` | Unsupported member lies between structural members | Later structural member retains gapped ordinal |
| `input_32_delimiter_components` | Identity segments contain spellings that collide if concatenated | Structured identities remain distinct |
| `input_33_source_relocation` | Physical source location changes but semantic identity components do not | Semantic identities remain unchanged |
| `input_34_depth_exact` | Expansion depth exactly `64` | Accepted with respect to depth |
| `input_35_depth_overflow` | Expansion would create depth `65` | `IMDE2011`; no snapshot |
| `input_36_entity_exact` | Published entity count exactly `262,144` | Accepted with respect to entity count |
| `input_37_entity_overflow` | Next entity would make `262,145` | `IMDE2011`; no partial snapshot |
| `input_38_loader_byte_limit` | Input exceeds `10,485,760` bytes | `INPUT_LIMIT_001` before full materialization |
| `input_39_loader_depth_limit` | JSON depth exceeds `32` | `INPUT_LIMIT_001` |
| `input_40_loader_record_limit` | Next JSON value would exceed `1,000,000` records | `INPUT_LIMIT_001` before admission |
| `input_41_marker_span_limit` | Opaque payload span exceeds `1,048,576` bytes | `INPUT_LIMIT_001` |
| `input_42_loader_diagnostic_limit` | Independent loader errors exceed the active/fixed cap | Deterministic bounded prefix plus omitted count |
| `input_43_origin_integrity` | Span exceeds owning source or uses another unit identity | `INPUT_INTEGRITY_001` |
| `input_44_project_graph_integrity` | Duplicate revision, unreachable dependency, or graph cycle | `INPUT_INTEGRITY_001` |

Positive, negative, boundary, randomized-order, limit, and referential-integrity fixtures require independent review before compiler implementation is authorized.

## 17. Minimal Valid Example

This example demonstrates schema shape only. It does not replace the required fixture matrix.

```json
{
  "schema": "experimental-structural-input/0",
  "project_context": {
    "language_version": "0.1",
    "root_package_revision": {
      "package_identity": {
        "authority": "org.example",
        "name": "control"
      },
      "version": "0.1.0",
      "content_identity": {
        "kind": "workspace-snapshot",
        "digest_algorithm": "sha256",
        "digest": "0000000000000000000000000000000000000000000000000000000000000000"
      }
    },
    "dependency_package_revisions": [],
    "dependency_edges": [],
    "modules": [
      {
        "identity": {
          "package_identity": {
            "authority": "org.example",
            "name": "control"
          },
          "module_name": "Core"
        },
        "exposure": "internal",
        "source_roots": [
          "src"
        ],
        "origin": {
          "kind": "project-manifest",
          "identity": "fixture/project.json#/root-module"
        }
      }
    ],
    "module_edges": [],
    "project_manifest_origin": {
      "kind": "project-manifest",
      "identity": "fixture/project.json"
    },
    "dependency_lock_origin": {
      "kind": "build-metadata",
      "identity": "fixture/dependency-lock.json"
    },
    "project_resolution_fingerprint": {
      "algorithm": "sha256",
      "value": "1111111111111111111111111111111111111111111111111111111111111111"
    },
    "active_limits": {
      "maximum_expansion_depth": 64,
      "maximum_expanded_semantic_entities": 262144,
      "maximum_diagnostics": 1024
    }
  },
  "selector_request": {
    "origin": {
      "kind": "fixture-metadata",
      "identity": "fixture/input.json#/selector_request"
    },
    "candidates": [
      {
        "target": {
          "package_identity": {
            "authority": "org.example",
            "name": "control"
          },
          "namespace_path": [
            "Process"
          ],
          "owner_path": [],
          "identifier": "Main"
        },
        "raw_spelling": "org.example/control::Process.Main",
        "origin": {
          "kind": "fixture-metadata",
          "identity": "fixture/input.json#/selector_request/candidates/0"
        }
      }
    ]
  },
  "compilation_units": [
    {
      "unit_identity": {
        "package_identity": {
          "authority": "org.example",
          "name": "control"
        },
        "module_name": "Core",
        "portable_package_path": "src/main.plant"
      },
      "source_identity_components": [
        "org.example",
        "control",
        "Core",
        "src/main.plant",
        "sha256:2222222222222222222222222222222222222222222222222222222222222222"
      ],
      "source_length_bytes": 512,
      "language_version": "0.1",
      "language_version_origin": {
        "kind": "source",
        "source_identity_components": [
          "org.example",
          "control",
          "Core",
          "src/main.plant",
          "sha256:2222222222222222222222222222222222222222222222222222222222222222"
        ],
        "raw_start": 0,
        "raw_end": 8
      },
      "namespace": {
        "segments": [
          "Process"
        ],
        "origin": {
          "kind": "source",
          "source_identity_components": [
            "org.example",
            "control",
            "Core",
            "src/main.plant",
            "sha256:2222222222222222222222222222222222222222222222222222222222222222"
          ],
          "raw_start": 9,
          "raw_end": 27
        }
      },
      "imports": [],
      "declarations": [
        {
          "kind": "definition",
          "name": "Pump",
          "visibility": "private",
          "members": [
            {
              "kind": "endpoint",
              "name": "command",
              "direction": "input",
              "type_reference": {
                "segments": [
                  "BOOL"
                ],
                "origin": {
                  "kind": "source",
                  "source_identity_components": [
                    "org.example",
                    "control",
                    "Core",
                    "src/main.plant",
                    "sha256:2222222222222222222222222222222222222222222222222222222222222222"
                  ],
                  "raw_start": 80,
                  "raw_end": 84
                }
              },
              "origin": {
                "kind": "source",
                "source_identity_components": [
                  "org.example",
                  "control",
                  "Core",
                  "src/main.plant",
                  "sha256:2222222222222222222222222222222222222222222222222222222222222222"
                ],
                "raw_start": 60,
                "raw_end": 86
              }
            }
          ],
          "origin": {
            "kind": "source",
            "source_identity_components": [
              "org.example",
              "control",
              "Core",
              "src/main.plant",
              "sha256:2222222222222222222222222222222222222222222222222222222222222222"
            ],
            "raw_start": 30,
            "raw_end": 120
          }
        },
        {
          "kind": "application-assembly",
          "name": "Main",
          "visibility": "private",
          "members": [
            {
              "kind": "instance",
              "name": "pump_1",
              "definition_reference": {
                "segments": [
                  "Pump"
                ],
                "origin": {
                  "kind": "source",
                  "source_identity_components": [
                    "org.example",
                    "control",
                    "Core",
                    "src/main.plant",
                    "sha256:2222222222222222222222222222222222222222222222222222222222222222"
                  ],
                  "raw_start": 240,
                  "raw_end": 244
                }
              },
              "origin": {
                "kind": "source",
                "source_identity_components": [
                  "org.example",
                  "control",
                  "Core",
                  "src/main.plant",
                  "sha256:2222222222222222222222222222222222222222222222222222222222222222"
                ],
                "raw_start": 220,
                "raw_end": 250
              }
            }
          ],
          "origin": {
            "kind": "source",
            "source_identity_components": [
              "org.example",
              "control",
              "Core",
              "src/main.plant",
              "sha256:2222222222222222222222222222222222222222222222222222222222222222"
            ],
            "raw_start": 180,
            "raw_end": 280
          }
        }
      ]
    }
  ]
}
```

## 18. Explicit Unresolved Questions

The following questions remain deliberately outside schema `0` and do not block its fixture role:

1. RFC-0001D or a compatible future owner must define any public Project, Package, Dependency Lock, or Canonical Source Identity byte serialization. Schema `0` uses only its explicitly non-interoperable fixture records.
2. The owning fingerprint specification must define any public canonical fingerprint encoding. Schema `0` fixes only an experimental `sha256` carrier and does not claim public fingerprint compatibility.
3. A future fixture contract may embed immutable source bytes or a content-addressed source bundle. Schema `0` carries source identity components, length, and spans only; those values never authorize host filesystem access.
4. A later schema may permit bounded parser recovery records. Schema `0` permits only schema-valid unresolved references, typed unsupported markers, and invalid selector cardinality or completeness; every loader failure remains all-or-nothing.

Any answer that changes these choices requires a new contract identifier.

## 19. Review and Implementation Gates

The Experimental Input Contract design is complete only when review confirms:

- the schema parses as Draft 2020-12;
- every `$ref` resolves;
- the minimal example validates;
- negative schema fixtures fail for the intended reason;
- the project-context carrier is sufficient for RFC-0001B/RFC-0001C resolution without becoming a public manifest format;
- selector resolution remains exclusively in step 2b;
- unsupported input cannot be silently discarded or mislabeled;
- loader and semantic limits remain separate;
- ordering and origin invariants are deterministic; and
- the fixture matrix covers all required positive, negative, boundary, randomized-order, limit, and referential-integrity cases.

After this document is reviewed, a separate implementation Task Envelope may authorize:

1. a duplicate-key-aware, bounded JSON fixture loader;
2. executable schema validation;
3. input-integrity validation;
4. the approved fixture corpus; and
5. only then the bounded Structural Reference Spike A compiler.

Until that authorization, parser and compiler implementation remains on hold.

## 20. Change Log

### Experimental — 2026-07-24

- Registered `experimental-structural-input/0`.
- Defined the closed expression-free top-level record and full Draft 2020-12 JSON Schema.
- Defined fixture Resolved Project Context, Collected Structural Input, unresolved references, selector requests, origins, typed unsupported markers, deterministic normalization, diagnostics, and loader limits.
- Kept loader work budgets separate from RFC-0006 expansion depth and published-entity limits.
- Added the required fixture and review gates without authorizing implementation.
