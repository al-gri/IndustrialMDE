# Spike A: Experimental Structural Snapshot

**Status:** Experimental, Non-normative, Non-conforming, Non-interoperable

**Applicability:** Structural Reference Spike A only

**Created:** 2026-07-23

**Last Updated:** 2026-07-23

**Schema Identifier:** `experimental-structural-snapshot/0`

**Semantic Inputs:** RFC-0001A, RFC-0001B, RFC-0001C, RFC-0002, Draft RFC-0005 Structural Layer, Draft RFC-0006 Structural Layer, Draft RFC-0007 Structural Layer

**Canonical IR Owner:** RFC-0012, not this document

## 1. Purpose

This document defines the experimental output and validation contract for Structural Reference Spike A.

The snapshot is an immutable, versioned, flat representation of one explicitly selected and fully validated Application Assembly. It exists only to test structural compiler hypotheses:

- resolved declaration and occurrence identity;
- deterministic static Instance expansion;
- Endpoint occurrence construction;
- Connection occurrence resolution;
- direction and exact type validation;
- duplicate-driver validation;
- source traceability; and
- phase-boundary publication.

The snapshot is:

- **not Canonical IR**;
- **not Target IR**;
- **not a generated target artifact**;
- **not a public interchange format**;
- **not evidence of language conformance**; and
- **not compatible across schema identifiers unless an explicit experimental migration says so**.

No consumer may bypass a future RFC-0012 Canonical IR by treating this snapshot as a production generation input.

## 2. Scope

### 2.1 Included Structural Facts

The snapshot contains only:

- the selected Application Assembly Declaration Identity;
- ordered root Instance Occurrence Identities;
- expanded Instance occurrence records;
- Endpoint occurrence records with direction and resolved Type Identity;
- Connection occurrence records with resolved source and destination identities;
- owner and declaration identities;
- deterministic declaration ordinals;
- complete experimental build provenance; and
- semantic-identity-to-source-or-metadata-origin traceability.

### 2.2 Excluded Facts

The snapshot MUST NOT contain:

```text
value
initializer
default value
expression
constant evaluation
parameter binding
state
behavior
execution order
scan cycle
schedule
operation
runtime cycle classification
conversion
transformation
sampling
quality
target
target profile
deployment mapping
address
memory area
task
generated target name
```

Within the Structural Validation Closure, a feature already classified by the versioned experimental input contract as requiring one of these facts produces `SPIKEA001`. The marker retains its category and origin while its payload remains opaque. The implementation MUST NOT invent a placeholder field, evaluate the feature, import RFC-0003 expression grammar, or silently discard it.

Input bytes that the experimental input contract cannot classify as a supported declaration or typed unsupported-feature marker fail under that contract's experimental syntax diagnostic before the Structural Spike pipeline. They do not receive a fabricated `SPIKEA001`.

## 3. Input, Phase, Scope, and Publication Contract

### 3.1 Upstream and Experimental Inputs

Spike A is not handed a fully resolved language Semantic Model. It receives two immutable inputs:

1. **Resolved Project Context.** RFC-0001C provides the exact root Package Revision, resolved dependency and lock context, effective language version, logical compilation units, and Canonical Source Identities required to build the symbol universe. It does not pre-resolve language Declaration Identities, Endpoint Type References, Connection references, or the Assembly selector for Spike A.
2. **Collected Structural Input.** A future explicitly versioned experimental input or fixture contract provides collected declaration candidates, unresolved references, source origins, one Assembly selector request with its metadata origin, and typed unsupported-feature markers whose payloads are opaque. It may contain bounded invalid or recovery records, but it contains no occurrence identity or expanded graph.

The exact experimental input-contract identifier is a required provenance field. Until that contract exists and assigns an identifier, the implementation gate remains closed.

`SPIKEA001` applies only to a typed unsupported-feature marker produced by the input contract. Unclassifiable bytes are owned by that contract's experimental syntax diagnostic and prevent creation of Collected Structural Input.

### 3.2 Immutable Phase Artifacts

Each successful boundary publishes a new immutable build-local artifact. A later phase MUST NOT mutate an earlier artifact.

| Artifact | Producer | Required facts | Invalid or recovery content | Failure owner and transition rule |
| --- | --- | --- | --- | --- |
| Resolved Project Context | RFC-0001C project/package resolution | Root Package Revision, locked dependency context, language version, logical units, source identities | None in a successfully published context | RFC-0001C failures prevent Collected Structural Input from entering Spike A |
| Collected Structural Input | Versioned experimental input/fixture loader | Declaration candidates, unresolved references, selector request, origins, typed unsupported markers | Bounded syntax recovery and typed unsupported markers are permitted | Input-contract diagnostics; a blocking syntax failure prevents step 1 |
| Resolved Structural Model | Pipeline step 1 | Project Resolution Universe, stable Declaration Identities, and each reference resolved or represented by an explicit invalid record | Invalid records may exist only for bounded diagnostic recovery | RFC-0001B/RFC-0001C resolution diagnostics; a blocking record cannot cross a boundary requiring that fact |
| Selected Structural Model | Pipeline step 2 | Valid semantic kinds, exactly one resolved root-Package Assembly, and the four validation scopes | Non-blocking invalid records outside the Structural Validation Closure may remain in the Diagnostic Universe | Owning kind diagnostic or `SPIKEA003`; selector failure prevents step 3 |
| Acyclic Expansion Plan | Pipeline step 3 | Closure-local Definition containment graph and deterministic traversal plan | None in the Structural Validation Closure | `IMDE2001`; a closure cycle prevents occurrence materialization |
| Validated Occurrence Graph | Pipeline steps 4–8 | Complete bounded Instance forest, Endpoint records, Connection overlay, traceability, and successful structural validation | No invalid placeholder is publishable | `IMDE2011`, owning `IMDE`, or `SPIKEA002`; any blocking failure prevents step 9 |
| Snapshot Publication Candidate | Pipeline step 9 before freeze | Validated graph plus complete provenance in closed schema shape | No placeholder or diagnostic node | `SPIKEA002(snapshot-schema)` or `SPIKEA002(snapshot-referential-integrity)` |
| Published Snapshot | Pipeline step 9 after freeze | Exactly one immutable `experimental-structural-snapshot/0` | None | No in-place mutation; a changed input creates another artifact |

### 3.3 Validation Scopes

Each invocation establishes four explicit scopes:

1. **Project Resolution Universe** — every Project, Package Revision, compilation unit, source identity, and declaration candidate required to establish deterministic identities and resolve the selected closure.
2. **Structural Validation Closure** — the selected Application Assembly, its root Instance Declarations, every transitively referenced Definition, every admitted or recognized-unsupported member owned by those Definitions, and every reference, type, origin, and shared declaration required to validate them.
3. **Expansion Closure** — the selected Application Assembly and exactly the transitively reachable Definitions and admitted structural members that can create Instance, Endpoint, or Connection occurrences.
4. **Diagnostic Universe** — the complete Project Resolution Universe from which both blocking closure diagnostics and separate non-blocking diagnostics may be reported.

A Project or Package resolution failure that prevents construction of the universe, a valid selector, or a shared identity is blocking. Every error in the Structural Validation Closure is blocking. An error wholly outside that closure is non-blocking unless it changes a shared dependency, makes an identity or selector ambiguous, or otherwise affects a closure fact.

Unselected Assemblies and unreachable Definitions produce no occurrence. Their diagnostics, if requested, are returned separately and MUST NOT be serialized into the snapshot. A previously unreachable declaration becomes blocking as soon as a selected or shared reference brings it into the Structural Validation Closure.

### 3.4 Publication Result

Spike A returns exactly one of:

```text
successful selected closure
    -> one complete immutable snapshot
       plus zero or more separate non-blocking diagnostics

any blocking failure
    -> blocking diagnostics
       plus optional independent diagnostics
       and no snapshot
```

Publication is all-or-nothing for the selected Application Assembly and its Structural Validation Closure. There is no valid partial snapshot, recovery snapshot, invalid-node placeholder, or per-branch publication mode.

The snapshot MUST be immutable after publication. A later diagnostic, provenance change, or transformation creates another artifact rather than mutating the published object.

## 4. Nine-Step Validation Pipeline

Spike A MUST execute the following pipeline in order:

1. **Ordinary-symbol collision and declaration/reference resolution.**
   Consume Resolved Project Context and Collected Structural Input. Establish the Project Resolution Universe and complete candidate Declaration Identities; resolve each admitted reference under RFC-0001B and RFC-0001C, or retain an explicit invalid record for bounded diagnostics. Publish Resolved Structural Model.
2. **Semantic-kind checking and Assembly selection.**
   **2a** verifies every resolved reference has the required semantic kind. **2b** resolves exactly one complete Assembly selector, verifies Application Assembly kind and root Package Revision ownership, confirms the inherited Project Resolution Universe, and establishes Structural Validation Closure, Expansion Closure, and Diagnostic Universe. Publish Selected Structural Model.
3. **Closure-local Definition containment-cycle validation.**
   Validate the resolved Definition containment graph in the Structural Validation Closure before occurrence materialization. Publish Acyclic Expansion Plan.
4. **Static expansion with exact resource accounting.**
   Expand the selected Assembly with depth limit `64` and `published_entity_count` limit `262,144`, counting only Instance, Endpoint, and Connection occurrence records as defined by RFC-0006.
5. **Endpoint reference locality.**
   Resolve each Endpoint occurrence within `self`, immediate-child, or immediate-root boundaries only.
6. **Source/destination direction validation.**
   Apply the RFC-0005 contextual direction table.
7. **Exact RFC-0002 type compatibility.**
   Require exact Type Equality for every otherwise valid Connection.
8. **Duplicate-driver validation.**
   Require at most one otherwise valid driver for each destination Endpoint occurrence. Publish Validated Occurrence Graph only if steps 4–8 have no blocking failure.
9. **Provenance, integrity, and immutable snapshot publication.**
   Construct complete provenance; validate the closed schema and every semantic graph invariant; sort collections canonically; freeze the publication candidate; and publish exactly one snapshot.

### 4.1 Failure and Suppression

A blocking error at steps 1 through 8 prevents step 9. An input-contract syntax failure prevents step 1.

An earlier failure suppresses a later diagnostic only when the later rule requires the missing or invalid fact. In particular:

- an unresolved reference does not also receive wrong-kind, locality, direction, type, or driver diagnostics;
- a wrong-kind Connection reference does not also receive Endpoint locality, direction, or type diagnostics;
- an invalid-direction or type-incompatible Connection is excluded from duplicate-driver analysis;
- a containment cycle in the Structural Validation Closure prevents expansion and suppresses occurrence-derived diagnostics;
- an invalid Assembly selector prevents closure construction and every expansion-derived diagnostic; and
- a schema failure and a semantic referential-integrity failure use their distinct `SPIKEA002` reasons when both can be evaluated independently.

Independent errors remain reportable within the active deterministic diagnostic limit. A diagnostic wholly outside the Structural Validation Closure does not prevent step 9 and is returned separately from the snapshot.

### 4.2 Diagnostic Ordering

Diagnostics are ordered by:

1. validation step;
2. primary origin-kind rank: `source`, `project-manifest`, `fixture-metadata`, `build-metadata`, `invocation`, then `no-origin`;
3. Canonical Source Identity components for a source origin, or the non-source origin identity for metadata and invocation origins;
4. zero-based raw start offset and then raw end offset for source origins, with `0` used for both fields for a non-source origin;
5. diagnostic code;
6. canonical structured semantic identity, or the empty tuple when no valid identity exists; and
7. a stable reason-specific secondary key.

The diagnostic owner selects one primary origin. Related origins are sorted by the traceability-origin order in section 9. Source-less selector diagnostics therefore order by their structured metadata or invocation origin rather than filesystem discovery.

No filesystem discovery order, hash-map order, concurrency schedule, locale, target selection, or current time may change diagnostic output.

## 5. Structured Identities

Every semantic identity in the snapshot is a JSON object representing a typed mathematical tuple. No semantic identity is a delimiter-concatenated string.

### 5.1 Declaration Identity

The experimental representation follows the RFC-0001B identity components:

```json
{
  "package_identity": {
    "authority": "example.org",
    "name": "water-treatment"
  },
  "namespace_path": ["Applications"],
  "owner_path": [],
  "identifier": "WaterTreatment",
  "entity_kind": "application-assembly"
}
```

Every segment remains a separate JSON value. This encoding is experimental and does not bind RFC-0001B, RFC-0001C, RFC-0012, or a future fingerprint contract to these field names.

### 5.2 Instance Occurrence Identity

```json
{
  "assembly_identity": {
    "package_identity": {
      "authority": "example.org",
      "name": "water-treatment"
    },
    "namespace_path": ["Applications"],
    "owner_path": [],
    "identifier": "WaterTreatment",
    "entity_kind": "application-assembly"
  },
  "declaration_path": [
    {
      "package_identity": {
        "authority": "example.org",
        "name": "water-treatment"
      },
      "namespace_path": ["Applications"],
      "owner_path": ["WaterTreatment"],
      "identifier": "station_1",
      "entity_kind": "instance-declaration"
    }
  ]
}
```

The root Instance Declaration Identity is the first path element.

### 5.3 Endpoint Occurrence Identity

```json
{
  "instance_identity": {
    "assembly_identity": {
      "package_identity": {
        "authority": "example.org",
        "name": "water-treatment"
      },
      "namespace_path": ["Applications"],
      "owner_path": [],
      "identifier": "WaterTreatment",
      "entity_kind": "application-assembly"
    },
    "declaration_path": [
      {
        "package_identity": {
          "authority": "example.org",
          "name": "water-treatment"
        },
        "namespace_path": ["Applications"],
        "owner_path": ["WaterTreatment"],
        "identifier": "station_1",
        "entity_kind": "instance-declaration"
      }
    ]
  },
  "endpoint_declaration_identity": {
    "package_identity": {
      "authority": "example.org",
      "name": "water-treatment"
    },
    "namespace_path": ["Domain"],
    "owner_path": ["PumpStation"],
    "identifier": "running",
    "entity_kind": "endpoint-declaration"
  }
}
```

### 5.4 Connection Occurrence Identity

```json
{
  "owner_context": {
    "kind": "application-assembly",
    "assembly_identity": {
      "package_identity": {
        "authority": "example.org",
        "name": "water-treatment"
      },
      "namespace_path": ["Applications"],
      "owner_path": [],
      "identifier": "WaterTreatment",
      "entity_kind": "application-assembly"
    }
  },
  "connection_declaration_identity": {
    "package_identity": {
      "authority": "example.org",
      "name": "water-treatment"
    },
    "namespace_path": ["Applications"],
    "owner_path": ["WaterTreatment"],
    "identifier": "publish_running",
    "entity_kind": "connection-declaration"
  }
}
```

An Instance-owned Connection uses `kind: "instance"` and an `instance_identity` field.

## 6. Snapshot Records

### 6.1 Provenance

The mandatory top-level provenance record contains:

- the experimental snapshot contract identifier;
- the exact versioned experimental input-contract identifier;
- effective language version;
- exact root Package Revision, including Package Identity, version, and content identity;
- an explicitly experimental Project Resolution Fingerprint with algorithm identifier;
- the effective resolved Assembly selector and its structured invocation or metadata origin;
- compiler semantic version;
- versioned semantic-algorithm identifier;
- an explicitly experimental complete-build fingerprint with algorithm identifier; and
- active maximum expansion depth, maximum expanded semantic entities, and maximum diagnostics.

The Project Resolution Fingerprint covers the dependency/lock and source-content facts used to establish the selected Structural Validation Closure. The complete-build fingerprint covers every provenance field and every input byte or typed fixture fact designated by the input contract. Both encodings are experimental, non-interoperable, and MUST NOT be presented as the future public fingerprint contract.

### 6.2 Assembly

The Assembly record contains:

- selected Application Assembly Declaration Identity; and
- root Instance Occurrence Identities in deterministic declaration order.

### 6.3 Instances

Each Instance record contains:

- Instance Occurrence Identity;
- optional parent Instance Occurrence Identity;
- referenced Definition Declaration Identity;
- creating Instance Declaration Identity;
- declaration ordinal; and
- child Instance Occurrence Identities in deterministic declaration order.

### 6.4 Endpoints

Each Endpoint record contains:

- Endpoint Occurrence Identity;
- owner Instance Occurrence Identity;
- creating Endpoint Declaration Identity;
- direction, exactly `input` or `output`;
- complete RFC-0002 Type Identity; and
- declaration ordinal.

### 6.5 Connections

Each Connection record contains:

- Connection Occurrence Identity;
- Owner Context Identity;
- creating Connection Declaration Identity;
- resolved source Endpoint Occurrence Identity;
- resolved destination Endpoint Occurrence Identity; and
- declaration ordinal.

Connections contain no values, transformations, execution order, or runtime status.

### 6.6 Declaration Ordinals

`declaration_ordinal` is the zero-based position in the owner's complete deterministic semantic member order after applicable declaration merging and name resolution, and before filtering by semantic kind. Instance, Endpoint, and Connection records use the same rule. Root Instance records use the complete deterministic Application Assembly member order.

Gaps are retained when intervening members do not create the same occurrence kind. The ordinal is traceability and ordering metadata, never an identity component. If the applicable owning RFC does not produce a complete deterministic merged-member order, the publication candidate fails integrity rather than using parser or file order.

### 6.7 Traceability

Traceability is stored separately from graph records. Each trace entry maps one typed semantic identity and one precise origin role to one or more normalized origins.

The allowed roles are:

```text
declaration
instance-definition-reference
endpoint-type-reference
connection-source-reference
connection-destination-reference
assembly-selector
```

A source origin uses zero-based UTF-8 byte offsets into the exact source artifact named by its Canonical Source Identity. `raw_start` is inclusive, `raw_end` is exclusive, and `raw_end >= raw_start`. A non-source origin identifies one invocation or metadata channel without pretending it is a source span.

There is at most one trace entry for each `(semantic_identity, origin_role)` pair. Multiple origins for merged or related declarations are stored in that entry and sorted canonically. The `assembly-selector` entry for the selected Assembly MUST match the selector origin in provenance.

Source and metadata origins are not semantic identity. Relocating a physical checkout does not change a semantic identity when RFC-0001B and RFC-0001C identity components remain unchanged.

## 7. Experimental JSON Schema

The following JSON Schema defines the closed top-level and record shapes for schema `0`. It is an experimental golden-test contract, not a public compatibility schema.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "urn:industrialmde:experimental-structural-snapshot:0",
  "title": "IndustrialMDE Experimental Structural Snapshot 0",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "schema",
    "provenance",
    "assembly",
    "instances",
    "endpoints",
    "connections",
    "traceability"
  ],
  "properties": {
    "schema": {
      "const": "experimental-structural-snapshot/0"
    },
    "provenance": {
      "$ref": "#/$defs/provenance"
    },
    "assembly": {
      "$ref": "#/$defs/assembly"
    },
    "instances": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/instance"
      },
      "uniqueItems": true
    },
    "endpoints": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/endpoint"
      },
      "uniqueItems": true
    },
    "connections": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/connection"
      },
      "uniqueItems": true
    },
    "traceability": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/trace-entry"
      },
      "uniqueItems": true
    }
  },
  "$defs": {
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
          "minLength": 1
        },
        "name": {
          "type": "string",
          "minLength": 1
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
          "minLength": 1
        },
        "content_identity": {
          "type": "string",
          "minLength": 1
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
          "type": "string",
          "minLength": 1
        },
        "value": {
          "type": "string",
          "minLength": 1
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
          "minLength": 1
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
          "minimum": 1
        }
      }
    },
    "provenance": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "experimental_contract_identifier",
        "input_contract_identifier",
        "language_version",
        "root_package_revision",
        "project_resolution_fingerprint",
        "assembly_selector",
        "compiler_semantic_version",
        "semantic_algorithm_identifier",
        "build_fingerprint",
        "active_limits"
      ],
      "properties": {
        "experimental_contract_identifier": {
          "const": "experimental-structural-snapshot/0"
        },
        "input_contract_identifier": {
          "type": "string",
          "minLength": 1
        },
        "language_version": {
          "const": "0.1"
        },
        "root_package_revision": {
          "$ref": "#/$defs/package-revision"
        },
        "project_resolution_fingerprint": {
          "$ref": "#/$defs/experimental-fingerprint"
        },
        "assembly_selector": {
          "type": "object",
          "additionalProperties": false,
          "required": [
            "identity",
            "origin"
          ],
          "properties": {
            "identity": {
              "$ref": "#/$defs/application-assembly-identity"
            },
            "origin": {
              "$ref": "#/$defs/non-source-origin"
            }
          }
        },
        "compiler_semantic_version": {
          "type": "string",
          "minLength": 1
        },
        "semantic_algorithm_identifier": {
          "type": "string",
          "minLength": 1
        },
        "build_fingerprint": {
          "$ref": "#/$defs/experimental-fingerprint"
        },
        "active_limits": {
          "$ref": "#/$defs/active-limits"
        }
      }
    },
    "declaration-identity": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "package_identity",
        "namespace_path",
        "owner_path",
        "identifier",
        "entity_kind"
      ],
      "properties": {
        "package_identity": {
          "$ref": "#/$defs/package-identity"
        },
        "namespace_path": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "owner_path": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "identifier": {
          "type": "string",
          "minLength": 1
        },
        "entity_kind": {
          "type": "string",
          "minLength": 1
        }
      }
    },
    "application-assembly-identity": {
      "allOf": [
        {
          "$ref": "#/$defs/declaration-identity"
        },
        {
          "properties": {
            "entity_kind": {
              "const": "application-assembly"
            }
          }
        }
      ]
    },
    "definition-identity": {
      "allOf": [
        {
          "$ref": "#/$defs/declaration-identity"
        },
        {
          "properties": {
            "entity_kind": {
              "const": "definition"
            }
          }
        }
      ]
    },
    "instance-declaration-identity": {
      "allOf": [
        {
          "$ref": "#/$defs/declaration-identity"
        },
        {
          "properties": {
            "entity_kind": {
              "const": "instance-declaration"
            }
          }
        }
      ]
    },
    "endpoint-declaration-identity": {
      "allOf": [
        {
          "$ref": "#/$defs/declaration-identity"
        },
        {
          "properties": {
            "entity_kind": {
              "const": "endpoint-declaration"
            }
          }
        }
      ]
    },
    "connection-declaration-identity": {
      "allOf": [
        {
          "$ref": "#/$defs/declaration-identity"
        },
        {
          "properties": {
            "entity_kind": {
              "const": "connection-declaration"
            }
          }
        }
      ]
    },
    "intrinsic-type-identity": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "domain",
        "language_version",
        "kind"
      ],
      "properties": {
        "domain": {
          "const": "industrialmde.language.intrinsic-type"
        },
        "language_version": {
          "const": "0.1"
        },
        "kind": {
          "enum": [
            "BOOL",
            "INT",
            "REAL",
            "TIME"
          ]
        }
      }
    },
    "instance-occurrence-identity": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "assembly_identity",
        "declaration_path"
      ],
      "properties": {
        "assembly_identity": {
          "$ref": "#/$defs/application-assembly-identity"
        },
        "declaration_path": {
          "type": "array",
          "minItems": 1,
          "items": {
            "$ref": "#/$defs/instance-declaration-identity"
          }
        }
      }
    },
    "endpoint-occurrence-identity": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "instance_identity",
        "endpoint_declaration_identity"
      ],
      "properties": {
        "instance_identity": {
          "$ref": "#/$defs/instance-occurrence-identity"
        },
        "endpoint_declaration_identity": {
          "$ref": "#/$defs/endpoint-declaration-identity"
        }
      }
    },
    "owner-context": {
      "oneOf": [
        {
          "type": "object",
          "additionalProperties": false,
          "required": [
            "kind",
            "assembly_identity"
          ],
          "properties": {
            "kind": {
              "const": "application-assembly"
            },
            "assembly_identity": {
              "$ref": "#/$defs/application-assembly-identity"
            }
          }
        },
        {
          "type": "object",
          "additionalProperties": false,
          "required": [
            "kind",
            "instance_identity"
          ],
          "properties": {
            "kind": {
              "const": "instance"
            },
            "instance_identity": {
              "$ref": "#/$defs/instance-occurrence-identity"
            }
          }
        }
      ]
    },
    "connection-occurrence-identity": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "owner_context",
        "connection_declaration_identity"
      ],
      "properties": {
        "owner_context": {
          "$ref": "#/$defs/owner-context"
        },
        "connection_declaration_identity": {
          "$ref": "#/$defs/connection-declaration-identity"
        }
      }
    },
    "assembly": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "identity",
        "root_instance_identities"
      ],
      "properties": {
        "identity": {
          "$ref": "#/$defs/application-assembly-identity"
        },
        "root_instance_identities": {
          "type": "array",
          "items": {
            "$ref": "#/$defs/instance-occurrence-identity"
          },
          "uniqueItems": true
        }
      }
    },
    "instance": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "identity",
        "parent_identity",
        "definition_identity",
        "creating_declaration_identity",
        "declaration_ordinal",
        "child_identities"
      ],
      "properties": {
        "identity": {
          "$ref": "#/$defs/instance-occurrence-identity"
        },
        "parent_identity": {
          "oneOf": [
            {
              "$ref": "#/$defs/instance-occurrence-identity"
            },
            {
              "type": "null"
            }
          ]
        },
        "definition_identity": {
          "$ref": "#/$defs/definition-identity"
        },
        "creating_declaration_identity": {
          "$ref": "#/$defs/instance-declaration-identity"
        },
        "declaration_ordinal": {
          "type": "integer",
          "minimum": 0
        },
        "child_identities": {
          "type": "array",
          "items": {
            "$ref": "#/$defs/instance-occurrence-identity"
          },
          "uniqueItems": true
        }
      }
    },
    "endpoint": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "identity",
        "owner_instance_identity",
        "creating_declaration_identity",
        "direction",
        "type_identity",
        "declaration_ordinal"
      ],
      "properties": {
        "identity": {
          "$ref": "#/$defs/endpoint-occurrence-identity"
        },
        "owner_instance_identity": {
          "$ref": "#/$defs/instance-occurrence-identity"
        },
        "creating_declaration_identity": {
          "$ref": "#/$defs/endpoint-declaration-identity"
        },
        "direction": {
          "enum": [
            "input",
            "output"
          ]
        },
        "type_identity": {
          "$ref": "#/$defs/intrinsic-type-identity"
        },
        "declaration_ordinal": {
          "type": "integer",
          "minimum": 0
        }
      }
    },
    "connection": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "identity",
        "owner_context",
        "creating_declaration_identity",
        "source_identity",
        "destination_identity",
        "declaration_ordinal"
      ],
      "properties": {
        "identity": {
          "$ref": "#/$defs/connection-occurrence-identity"
        },
        "owner_context": {
          "$ref": "#/$defs/owner-context"
        },
        "creating_declaration_identity": {
          "$ref": "#/$defs/connection-declaration-identity"
        },
        "source_identity": {
          "$ref": "#/$defs/endpoint-occurrence-identity"
        },
        "destination_identity": {
          "$ref": "#/$defs/endpoint-occurrence-identity"
        },
        "declaration_ordinal": {
          "type": "integer",
          "minimum": 0
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
          "items": {
            "type": "string"
          }
        },
        "raw_start": {
          "type": "integer",
          "minimum": 0
        },
        "raw_end": {
          "type": "integer",
          "minimum": 0
        }
      }
    },
    "origin": {
      "oneOf": [
        {
          "$ref": "#/$defs/source-origin"
        },
        {
          "$ref": "#/$defs/non-source-origin"
        }
      ]
    },
    "trace-entry": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "semantic_identity",
        "origin_role",
        "origins"
      ],
      "properties": {
        "semantic_identity": {
          "oneOf": [
            {
              "$ref": "#/$defs/declaration-identity"
            },
            {
              "$ref": "#/$defs/instance-occurrence-identity"
            },
            {
              "$ref": "#/$defs/endpoint-occurrence-identity"
            },
            {
              "$ref": "#/$defs/connection-occurrence-identity"
            }
          ]
        },
        "origin_role": {
          "enum": [
            "declaration",
            "instance-definition-reference",
            "endpoint-type-reference",
            "connection-source-reference",
            "connection-destination-reference",
            "assembly-selector"
          ]
        },
        "origins": {
          "type": "array",
          "minItems": 1,
          "items": {
            "$ref": "#/$defs/origin"
          },
          "uniqueItems": true
        }
      }
    }
  }
}
```

## 8. Referential, Provenance, and Schema Invariants

JSON Schema validates closed record shape. A separate deterministic semantic integrity validator MUST enforce every cross-record rule below before publication.

### 8.1 Provenance

- the schema identifier and `provenance.experimental_contract_identifier` are exact and equal;
- the provenance selector identity equals `assembly.identity`;
- the selected Assembly Package Identity equals the root Package Revision Package Identity;
- every Intrinsic Type Identity language version equals `provenance.language_version`;
- the input-contract, compiler, semantic-algorithm, Project Resolution Fingerprint, and build-fingerprint identifiers are non-empty and belong to the effective invocation;
- active depth and entity limits are exactly `64` and `262,144`, and the active diagnostic limit is positive; and
- the build fingerprint is recomputed by its recorded experimental algorithm over the complete inputs designated in section 6.1.

### 8.2 Identity Kinds and Internal Equality

- every Application Assembly identity has `entity_kind: application-assembly`;
- every Definition identity has `entity_kind: definition`;
- every element of an Instance declaration path and every creating Instance declaration has `entity_kind: instance-declaration`;
- every Endpoint declaration identity has `entity_kind: endpoint-declaration`;
- every Connection declaration identity has `entity_kind: connection-declaration`;
- every occurrence embeds the same Assembly identity as the top-level Assembly;
- every Instance creating declaration equals the last declaration-path element;
- every Endpoint owner equals `identity.instance_identity`; and
- every Endpoint and Connection creating declaration equals the corresponding declaration identity embedded in its occurrence identity.

### 8.3 Instance Forest

- every root identity names exactly one Instance record with `parent_identity: null` and a declaration path of length one;
- all and only Instances with `parent_identity: null` occur exactly once in `assembly.root_instance_identities`;
- every non-root parent identity names exactly one Instance record and its declaration path is the exact proper prefix obtained by removing the child's final path element;
- every child identity names exactly one Instance whose parent points back to the owner;
- root and child arrays contain no duplicates;
- every Instance is reachable from exactly one root;
- no disconnected Instance component or parent cycle exists; and
- root and child arrays follow declaration order and agree with each record's zero-based complete-member ordinal.

### 8.4 Endpoint and Connection Graph

- every Endpoint owner names exactly one Instance in the selected graph;
- every Connection source and destination names exactly one Endpoint in that graph;
- every Connection `owner_context` equals the Owner Context embedded in its Connection Occurrence Identity;
- an Application Assembly owner context names exactly the selected Assembly;
- an Instance owner context names exactly one selected-graph Instance;
- source and destination occurrences embed the selected Assembly identity;
- every typed identity is unique within its flat collection; and
- `published_entity_count = instances.length + endpoints.length + connections.length` is at most `262,144`.

### 8.5 Traceability and Publication

- every trace entry names a published semantic identity;
- each `(semantic_identity, origin_role)` pair is unique;
- each origin collection is non-empty, duplicate-free, and canonically ordered;
- source origins use zero-based UTF-8 byte offsets with inclusive start, exclusive end, and `raw_end >= raw_start`;
- the selected Assembly has an `assembly-selector` trace entry equal to the provenance selector origin;
- Connection source and destination references use their distinct origin roles;
- no invalid placeholder or diagnostic appears as a graph node; and
- every excluded runtime or target field is absent.

Any failure is a publication-integrity error. No snapshot is emitted.

## 9. Ordering and Serialization

The snapshot uses explicit deterministic orders:

- Assembly root and Instance child arrays retain deterministic declaration order;
- flat `instances`, `endpoints`, and `connections` arrays sort by canonical structured identity;
- `traceability` sorts by canonical structured semantic identity and then by the following origin-role rank: `declaration`, `instance-definition-reference`, `endpoint-type-reference`, `connection-source-reference`, `connection-destination-reference`, `assembly-selector`; and
- origins inside one trace entry sort by origin-kind rank `source`, `project-manifest`, `fixture-metadata`, `build-metadata`, `invocation`; then by Canonical Source Identity components or non-source origin identity; then by raw start and raw end for a source origin.

Declaration ordinal is stored separately and MUST NOT be reconstructed from flat-array position. It is zero-based in the owner's complete deterministic semantic member order as defined in section 6.6.

Canonical identity and origin comparison operates on typed tuple fields and UTF-8 byte ordering where an owning RFC defines string ordering. It MUST NOT compare locale-dependent rendered display names. `raw_start` is inclusive and `raw_end` is exclusive over the exact UTF-8 source bytes.

JSON object member order is not semantic. Golden tests MUST parse the JSON and compare the complete normalized data model or use one documented experimental canonical encoder. Neither procedure creates a public byte-compatibility promise.

The serialized document MUST be UTF-8. Writers SHOULD use LF line endings and a final newline for repository fixtures.

## 10. Temporary Diagnostics

Spike A uses the `SPIKEA` diagnostic domain only for experimental limitations or structural rules that do not yet own an exact public `IMDE` code.

These codes:

- are not language-version diagnostics;
- do not reserve the `IMDE` namespace;
- may change or disappear with the experimental schema;
- MUST NOT be cited as production compatibility guarantees; and
- MUST still carry stable facts and deterministic ordering within one Spike A revision.

| Code | Severity | Condition | Required facts |
| --- | --- | --- | --- |
| `SPIKEA001` | Error | Feature lies in the Structural Validation Closure and was classified by the versioned input contract as outside its supported subset | Feature category, owning future RFC, declaration or construct origin, opaque marker range, and supported subset |
| `SPIKEA002` | Error | Structural Connection or snapshot-publication rule fails without a more-specific registered `IMDE` code | Reason, owning identity, related Endpoint or record identities, relevant Type Identities, and all applicable origins |
| `SPIKEA003` | Error | Application Assembly selector is missing, multiple, unresolved, wrong-kind, incomplete, or outside the root Package Revision | Reason, supplied selector, expected kind, resolution result, root Package Revision, and invocation or metadata origin |

`SPIKEA002.reason` is one of:

```text
endpoint-locality
endpoint-direction
connection-type-mismatch
duplicate-driver
snapshot-schema
snapshot-referential-integrity
```

The single-owner precedence matrix is:

| Condition | Single diagnostic owner |
| --- | --- |
| Input cannot classify syntax as a declaration or typed unsupported marker | Versioned experimental input-contract syntax diagnostic |
| Recognized unsupported feature in the Structural Validation Closure | `SPIKEA001` |
| Unresolved reference spelling | Applicable RFC-0001B resolution diagnostic |
| Connection reference resolves to a non-Endpoint kind | `IMDE2007` |
| Other applicable semantic-kind mismatch | `IMDE2009` or a more-specific owning `IMDE` |
| Resolved Endpoint crosses the direct boundary | `SPIKEA002(endpoint-locality)` |
| Wrong contextual direction | `SPIKEA002(endpoint-direction)` |
| Unequal Connection Type Identities | `SPIKEA002(connection-type-mismatch)` |
| More than one otherwise-valid driver | `SPIKEA002(duplicate-driver)` |
| Prohibited Deployment Mapping matching RFC-0001A | `IMDE2004` |
| Other recognized unsupported deployment or target construct in the closure | `SPIKEA001` |
| Containment cycle | `IMDE2001` |
| Expansion depth or exact published-entity limit exceeded | `IMDE2011` |
| Invalid Assembly selector | `SPIKEA003` |
| Closed-schema violation | `SPIKEA002(snapshot-schema)` |
| Cross-record semantic integrity violation | `SPIKEA002(snapshot-referential-integrity)` |

One invalid fact produces one most-specific diagnostic. A Connection type mismatch therefore produces `SPIKEA002(connection-type-mismatch)` and not `IMDE5003`. A reach-through that resolves to an Endpoint produces `SPIKEA002(endpoint-locality)`; a spelling that resolves to a non-Endpoint produces `IMDE2007`. A construct matching `IMDE2004` does not also produce `SPIKEA001`.

## 11. Dependency Matrix

| Artifact | Hard inputs for the structural slice | Provides to Spike A | Explicitly deferred |
| --- | --- | --- | --- |
| RFC-0005 Structural Layer | RFC-0001A, RFC-0001B, RFC-0002 | Endpoint direction, Connection edge, locality, type and driver validation | Values, timing, quality, transformations, behavioral cycles |
| RFC-0006 Structural Layer | RFC-0001A, RFC-0001B, RFC-0002, RFC-0005 Structural Layer | Definition composition, deterministic expansion, occurrence identities and limits | Interfaces, substitution, replication, configuration |
| RFC-0007 Structural Layer | RFC-0001A, RFC-0001B, RFC-0001C, RFC-0005/0006 Structural Layers | Explicit Assembly entry, multiple roots, application Connections | Deployment, target profiles, mapping, physical resources |
| Snapshot schema `0` | All three Draft structural layers and Constitution phase boundaries | Immutable experimental expanded graph and traceability | Canonical IR, Target IR, production compatibility |

The dependency direction is:

```text
RFC-0002
    -> RFC-0005 Structural Layer
    -> RFC-0006 Structural Layer
    -> RFC-0007 Structural Layer
    -> experimental-structural-snapshot/0
```

RFC-0004 gates the deferred RFC-0005 Runtime Layer. It is not a dependency of RFC-0005 Structural Layer or this snapshot.

## 12. Validation Against Deferred Semantics

| Fact | RFC-0003 needed | RFC-0004 needed | Spike A |
| --- | --- | --- | --- |
| Endpoint Type Identity | No | No | Included |
| Connection identity edge | No | No | Included |
| Direction compatibility | No | No | Included |
| Exact type compatibility | No | No | Included |
| Single-driver structural rule | No | No | Included |
| Instance expansion | No | No | Included |
| Values and defaults | Yes | Possibly | Excluded |
| Conversion or transformation | Yes | Possibly | Excluded |
| State update or execution order | No | Yes | Excluded |
| Behavioral cycle rejection | No | Yes | Excluded |
| Target mapping | No | No, but deployment contract required | Excluded |

No included fact requires parsing an expression or executing state.

## 13. Required Golden Fixtures

The eventual Spike A test plan MUST include:

- an empty selected Assembly;
- multiple root Instances and application-level Connections;
- nested and repeated Instances of the same Definition;
- owner-to-child, child-to-owner, and sibling Connections;
- valid fan-out;
- direct and indirect Definition containment cycles;
- wrong-kind Endpoint references;
- invalid direction;
- exact type mismatch;
- duplicate driver;
- descendant reach-through;
- unconnected Endpoint;
- depth exactly `64` and depth overflow;
- entity count exactly `262,144` under `instances + endpoints + connections`, and overflow at `262,145`;
- proof that internal candidate or work-item counts do not consume the semantic entity limit;
- identity components containing punctuation that would collide under string joining;
- randomized file, map, and internal traversal order;
- schema, provenance, identity-kind, parent-prefix, reachability, embedded-owner, and traceability corruption;
- stable ordering of source and non-source origins;
- root Package Revision, selector-origin, compiler-version, input-contract, algorithm, and fingerprint provenance changes;
- an unreachable invalid Assembly or Definition that remains non-blocking, and the same declaration becoming blocking when referenced;
- a typed opaque unsupported-expression marker and unclassifiable syntax owned by the input contract;
- unsupported State, Interface, replication, and deployment features; and
- proof that blocking invalid input publishes no snapshot while unrelated diagnostics remain separate.

## 14. Documentation Readiness and Implementation Gate

Current Draft requirements:

- [x] Draft RFC-0005 separates Structural and Runtime layers and defines single-owner diagnostic precedence.
- [x] Draft RFC-0006 fixes direct-boundary composition, tuple occurrence identities, exact resource accounting, and declaration ordinals.
- [x] Draft RFC-0007 fixes explicit root-Package Assembly selection, selector phase ownership, validation closure, and provenance obligations.
- [x] Snapshot schema is versioned, closed, experimental, non-conforming, and non-interoperable.
- [x] Validation pipeline has exactly nine ordered steps with named immutable phase artifacts.
- [x] Project Resolution Universe, Structural Validation Closure, Expansion Closure, and Diagnostic Universe are explicit.
- [x] Provenance records the exact build context without claiming a public fingerprint contract.
- [x] Semantic integrity rules cover identity kinds, forest reachability, embedded identities, graph ownership, and traceability.
- [x] Expansion limits are exactly `64` and `262,144` published entities.
- [x] Blocking invalid and partial models cannot publish a snapshot.
- [x] Temporary diagnostics use `SPIKEA`, not an unregistered `IMDE` code.
- [x] Expression, execution, State, and target facts remain explicitly excluded.

Implementation remains gated on:

- [ ] independent re-review and recorded approval of these amendments;
- [ ] an explicit versioned experimental input or fixture contract implementing typed opaque unsupported-feature markers;
- [ ] approved positive, negative, boundary, randomized-order, provenance, and integrity fixtures;
- [ ] a bounded implementation Task Envelope; and
- [ ] confirmation that the reference spike remains disposable and non-conforming.

## 15. Change and Disposal Policy

Schema `0` may change incompatibly or be deleted while review history remains available.

This review amendment replaces the initial pre-implementation schema `0` draft in full. No implementation, fixture, or consumer existed, so all earlier illustrative schema `0` shapes are declared obsolete rather than migrated.

If a future revision changes any record, identity, ordering, diagnostic, or publication rule, it MUST use another experimental schema identifier or explicitly declare that existing fixtures are replaced.

RFC-0012 is free to adopt, change, or reject every representation in this document. No production consumer may depend on schema `0`.

## 16. Change Log

| Date | Change |
| --- | --- |
| 2026-07-23 | Resolved review findings for phase contracts, validation scope, provenance, graph integrity, resource accounting, unsupported input, diagnostics, traceability, and ordinals; replaced the pre-implementation schema `0` draft |
| 2026-07-23 | Initial experimental contract for the Structural Reference Spike A validation pipeline and snapshot schema |
