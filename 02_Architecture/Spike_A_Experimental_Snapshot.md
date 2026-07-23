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
- deterministic declaration ordinals; and
- semantic-identity-to-source-origin traceability.

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

Encountering a source or semantic feature that requires one of these facts produces `SPIKEA001`. The implementation MUST NOT invent a placeholder field, evaluate the feature, or silently discard it.

## 3. Input and Publication Contract

Spike A consumes:

1. a complete resolved Project and Package graph under RFC-0001C;
2. resolved Declaration Identities and typed references;
3. exactly one valid RFC-0007 Assembly selector;
4. Definitions containing only the admitted RFC-0006 structural member subset; and
5. Endpoint Type Identities already resolved under RFC-0002.

Spike A publishes either:

- one complete immutable `experimental-structural-snapshot/0`; or
- diagnostics and no snapshot.

Publication is all-or-nothing for the selected Application Assembly. There is no valid partial snapshot, recovery snapshot, invalid-node placeholder, or per-branch publication mode.

The snapshot MUST be immutable after publication. A later diagnostic or transformation MUST create another artifact rather than mutate the published object.

## 4. Nine-Step Validation Pipeline

Spike A MUST execute the following pipeline in order:

1. **Ordinary-symbol collision and name resolution.**
   Establish complete candidate Declaration Identities and resolved references under RFC-0001B and RFC-0001C.
2. **Semantic-kind checking.**
   Verify every resolved reference has the kind required by RFC-0001A and the owning structural rule.
3. **Definition containment-cycle validation.**
   Validate the resolved Definition containment graph before occurrence materialization.
4. **Static expansion with resource limits.**
   Expand the selected Assembly with depth limit `64` and total expanded-entity limit `262,144`.
5. **Endpoint reference locality.**
   Resolve each Endpoint occurrence within `self`, immediate-child, or immediate-root boundaries only.
6. **Source/destination direction validation.**
   Apply the RFC-0005 contextual direction table.
7. **Exact RFC-0002 type compatibility.**
   Require exact Type Equality for every otherwise valid Connection.
8. **Duplicate-driver validation.**
   Require at most one otherwise valid driver for each destination Endpoint occurrence.
9. **Immutable snapshot publication.**
   Verify schema and referential integrity, sort flat collections canonically, freeze the artifact, and publish it.

### 4.1 Failure and Suppression

An error at steps 1 through 8 prevents step 9.

An earlier failure suppresses a later diagnostic only when the later rule requires the missing or invalid fact. In particular:

- an unresolved reference does not also receive wrong-kind, locality, direction, type, or driver diagnostics;
- a wrong-kind reference does not also receive Endpoint direction or type diagnostics;
- an invalid-direction or type-incompatible Connection is excluded from duplicate-driver analysis;
- a containment cycle prevents expansion and therefore suppresses occurrence-derived diagnostics; and
- an invalid Assembly selector prevents every expansion-derived diagnostic.

Independent errors remain reportable within the configured deterministic diagnostic limit.

### 4.2 Diagnostic Ordering

Diagnostics are ordered by:

1. validation step;
2. normalized logical source path or Canonical Source Identity;
3. primary raw start offset;
4. diagnostic code;
5. canonical structured semantic identity; and
6. a stable reason-specific secondary key.

No filesystem discovery order, hash-map order, concurrency schedule, or target selection may change diagnostic output.

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

### 6.1 Assembly

The Assembly record contains:

- selected Assembly Declaration Identity; and
- root Instance Occurrence Identities in deterministic declaration order.

### 6.2 Instances

Each Instance record contains:

- Instance Occurrence Identity;
- optional parent Instance Occurrence Identity;
- referenced Definition Declaration Identity;
- creating Instance Declaration Identity;
- declaration ordinal; and
- child Instance Occurrence Identities in deterministic declaration order.

### 6.3 Endpoints

Each Endpoint record contains:

- Endpoint Occurrence Identity;
- owner Instance Occurrence Identity;
- creating Endpoint Declaration Identity;
- direction, exactly `input` or `output`;
- complete RFC-0002 Type Identity; and
- declaration ordinal.

### 6.4 Connections

Each Connection record contains:

- Connection Occurrence Identity;
- Owner Context Identity;
- creating Connection Declaration Identity;
- resolved source Endpoint Occurrence Identity;
- resolved destination Endpoint Occurrence Identity; and
- declaration ordinal.

Connections contain no values, transformations, execution order, or runtime status.

### 6.5 Traceability

Traceability is stored separately from graph records. Each trace entry maps:

- one typed semantic identity;
- one origin role such as `declaration`, `reference`, or `type-reference`; and
- one or more normalized source origins.

Source origins are not semantic identity. Relocating a physical checkout does not change a semantic identity when RFC-0001B and RFC-0001C identity components remain unchanged.

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
    "assembly": {
      "$ref": "#/$defs/assembly"
    },
    "instances": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/instance"
      }
    },
    "endpoints": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/endpoint"
      }
    },
    "connections": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/connection"
      }
    },
    "traceability": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/trace-entry"
      }
    }
  },
  "$defs": {
    "package-identity": {
      "type": "object",
      "additionalProperties": false,
      "required": ["authority", "name"],
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
    "intrinsic-type-identity": {
      "type": "object",
      "additionalProperties": false,
      "required": ["domain", "language_version", "kind"],
      "properties": {
        "domain": {
          "const": "industrialmde.language.intrinsic-type"
        },
        "language_version": {
          "const": "0.1"
        },
        "kind": {
          "enum": ["BOOL", "INT", "REAL", "TIME"]
        }
      }
    },
    "instance-occurrence-identity": {
      "type": "object",
      "additionalProperties": false,
      "required": ["assembly_identity", "declaration_path"],
      "properties": {
        "assembly_identity": {
          "$ref": "#/$defs/declaration-identity"
        },
        "declaration_path": {
          "type": "array",
          "minItems": 1,
          "items": {
            "$ref": "#/$defs/declaration-identity"
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
          "$ref": "#/$defs/declaration-identity"
        }
      }
    },
    "owner-context": {
      "oneOf": [
        {
          "type": "object",
          "additionalProperties": false,
          "required": ["kind", "assembly_identity"],
          "properties": {
            "kind": {
              "const": "application-assembly"
            },
            "assembly_identity": {
              "$ref": "#/$defs/declaration-identity"
            }
          }
        },
        {
          "type": "object",
          "additionalProperties": false,
          "required": ["kind", "instance_identity"],
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
          "$ref": "#/$defs/declaration-identity"
        }
      }
    },
    "assembly": {
      "type": "object",
      "additionalProperties": false,
      "required": ["identity", "root_instance_identities"],
      "properties": {
        "identity": {
          "$ref": "#/$defs/declaration-identity"
        },
        "root_instance_identities": {
          "type": "array",
          "items": {
            "$ref": "#/$defs/instance-occurrence-identity"
          }
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
          "$ref": "#/$defs/declaration-identity"
        },
        "creating_declaration_identity": {
          "$ref": "#/$defs/declaration-identity"
        },
        "declaration_ordinal": {
          "type": "integer",
          "minimum": 0
        },
        "child_identities": {
          "type": "array",
          "items": {
            "$ref": "#/$defs/instance-occurrence-identity"
          }
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
          "$ref": "#/$defs/declaration-identity"
        },
        "direction": {
          "enum": ["input", "output"]
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
          "$ref": "#/$defs/declaration-identity"
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
        "source_identity_components",
        "raw_start",
        "raw_end"
      ],
      "properties": {
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
    "trace-entry": {
      "type": "object",
      "additionalProperties": false,
      "required": ["semantic_identity", "origin_role", "origins"],
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
            "reference",
            "type-reference"
          ]
        },
        "origins": {
          "type": "array",
          "minItems": 1,
          "items": {
            "$ref": "#/$defs/source-origin"
          }
        }
      }
    }
  }
}
```

## 8. Referential and Schema Invariants

Before publication, Spike A MUST verify:

- the schema identifier is exact;
- every record satisfies the closed schema;
- every root identity names exactly one Instance record with `parent_identity: null`;
- every non-root parent identity names exactly one Instance record;
- every child identity names exactly one Instance record whose parent points back to the owner;
- every Endpoint owner identity names exactly one Instance;
- every Endpoint Declaration and Type Identity is resolved;
- every Connection source and destination identity names exactly one Endpoint;
- every Connection owner context exists;
- every identity is unique within its typed collection;
- every trace entry names a published semantic identity;
- no invalid placeholder or diagnostic appears as a graph node; and
- excluded runtime or target fields are absent.

A failure is a publication-integrity error. No snapshot is emitted.

## 9. Ordering and Serialization

The snapshot uses two explicit orders:

- owner child and root arrays retain deterministic declaration order; and
- flat `instances`, `endpoints`, `connections`, and `traceability` arrays are sorted by canonical structured identity.

Declaration ordinal is stored separately and MUST NOT be reconstructed from flat-array position.

Canonical identity comparison operates on typed tuple fields and UTF-8 byte ordering where an owning RFC defines string ordering. It MUST NOT compare locale-dependent rendered display names.

JSON object member order is not semantic. Golden tests MUST parse the JSON and compare the complete normalized data model or use one documented experimental canonical encoder. Neither procedure creates a public byte-compatibility promise.

The serialized document MUST be UTF-8. Writers SHOULD use LF line endings and a final newline for repository fixtures.

## 10. Temporary Diagnostics

Spike A uses the `SPIKEA` diagnostic domain only for experimental limitations or structural rules that do not yet own an accepted public `IMDE` code.

These codes:

- are not language-version diagnostics;
- do not reserve the `IMDE` namespace;
- may change or disappear with the experimental schema;
- MUST NOT be cited as production compatibility guarantees; and
- MUST still carry stable facts and deterministic ordering within one Spike A revision.

| Code | Severity | Condition | Required facts |
| --- | --- | --- | --- |
| `SPIKEA001` | Error | Unsupported feature outside the structural subset | Feature category, owning future RFC, declaration or construct origin, and supported subset |
| `SPIKEA002` | Error | Structural Connection or snapshot-publication rule fails without a more-specific registered `IMDE` code | Reason, owning identity, related Endpoint or record identities, relevant Type Identities, and all applicable origins |
| `SPIKEA003` | Error | Application Assembly selector is missing, multiple, unresolved, wrong-kind, incomplete, or outside the root Package Revision | Reason, supplied selector, expected kind, resolution result, root Package Revision, and invocation origin |

`SPIKEA002.reason` is one of:

```text
endpoint-locality
endpoint-direction
connection-type-mismatch
duplicate-driver
snapshot-schema
snapshot-referential-integrity
```

Existing diagnostics from Proposed owning RFCs remain usable where their condition is exact, including `IMDE2001`, `IMDE2002`, `IMDE2007`, `IMDE2009`, `IMDE2011`, and the RFC-0001B and RFC-0002 resolution diagnostics. Spike A MUST NOT invent a new `IMDE` code.

One invalid fact produces one most-specific diagnostic. For example, a Connection type mismatch produces `SPIKEA002` with reason `connection-type-mismatch` and not an additional `IMDE5003`.

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
- entity count exactly `262,144` and entity-count overflow;
- identity components containing punctuation that would collide under string joining;
- randomized file, map, and internal traversal order;
- schema and referential-integrity corruption;
- unsupported expression, State, Interface, replication, and deployment features; and
- proof that invalid input publishes no snapshot.

## 14. Documentation Readiness and Implementation Gate

Documentation requirements established by TE-STRUCTURAL-RFC-01:

- [x] Draft RFC-0005 separates Structural and Runtime layers.
- [x] Draft RFC-0006 fixes direct-boundary composition and tuple occurrence identities.
- [x] Draft RFC-0007 fixes explicit, root-Package Assembly selection without language grammar.
- [x] Snapshot schema is versioned, closed, experimental, non-conforming, and non-interoperable.
- [x] Validation pipeline has exactly nine ordered steps.
- [x] Expansion limits are `64` and `262,144`.
- [x] Invalid and partial models cannot publish a snapshot.
- [x] Temporary diagnostics use `SPIKEA`, not an unregistered `IMDE` code.
- [x] Expression, execution, State, and target facts are explicitly excluded.

Implementation remains gated on:

- [ ] review of the three Draft structural RFCs and this contract;
- [ ] an explicit experimental input grammar or fixture contract that excludes expressions;
- [ ] approved positive, negative, boundary, randomized-order, and integrity fixtures;
- [ ] a bounded implementation Task Envelope; and
- [ ] confirmation that the reference spike remains disposable and non-conforming.

## 15. Change and Disposal Policy

Schema `0` may change incompatibly or be deleted while review history remains available.

If a future revision changes any record, identity, ordering, diagnostic, or publication rule, it MUST use another experimental schema identifier or explicitly declare that existing fixtures are replaced.

RFC-0012 is free to adopt, change, or reject every representation in this document. No production consumer may depend on schema `0`.

## 16. Change Log

| Date | Change |
| --- | --- |
| 2026-07-23 | Initial experimental contract for the Structural Reference Spike A validation pipeline and snapshot schema |
