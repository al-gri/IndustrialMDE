# RFC-0001: Core Language and Lexical Structure

**Status:** Proposed

**Authors:** IndustrialMDE Project

**Created:** 2026-07-19

**Last Updated:** 2026-07-19

**Target Language Version:** Pre-1.0

**Dependencies:** RFC-0000

**Supersedes:** None

**Superseded By:** None

**Implementation Status:** Not Started

**Review:** [Foundational RFC Review Decisions](../../00_Project_Brain/06_Foundational_RFC_Review_Decisions.md)

## 1. Summary

This RFC defines the source-file and lexical foundation of the IndustrialMDE language. It establishes source encoding, line endings, trivia, identifiers, reserved words, scalar literals, punctuation, the language-version directive, metadata syntax, source coordinates, and deterministic lexical diagnostics.

This RFC deliberately does not define the semantic meaning of industrial declarations. Semantic entities, scopes, compilation units, types, expressions, and attributes are owned by later RFCs.

RFC-0000 is currently Proposed. This RFC may be reviewed as Proposed while its dependency is at a compatible review status. It cannot become Accepted until RFC-0000 and every other normative dependency required by its final scope are Accepted.

## 2. Motivation

Every later language feature depends on a stable lexical contract. If encoding, token boundaries, version selection, or source coordinates vary between implementations, then parsing, diagnostics, caching, source maps, and compatibility become nondeterministic.

The lexical layer must also protect the vendor-neutral language from accidental constraints. Internal identifiers are programming-language symbols; P&ID tags, HMI names, asset identifiers, and vendor symbols are external engineering data and must not redefine the identifier grammar.

## 3. Goals

This RFC is intended to provide:

- deterministic tokenization for a declared language version;
- a UTF-8 source format with an ASCII identifier space;
- stable rules for comments, whitespace, and source coordinates;
- an explicit language-version directive in every source file;
- a non-semantic metadata container;
- unambiguous string and numeric literal forms;
- a lexical contract independent of any parser framework;
- stable diagnostic expectations for invalid source text;
- a compatibility boundary for future lexical changes.

## 4. Non-Goals

This RFC does not define:

- the project manifest or source-file discovery algorithm;
- modules, packages, libraries, or dependency resolution;
- namespace ownership, merging, or import resolution;
- scopes, shadowing, aliases, or fully qualified symbol identity;
- industrial definitions, instances, signals, or connections;
- type names, type inference, or numeric ranges;
- expression precedence or runtime evaluation;
- duration, time-of-day, date, unit, or engineering literals;
- attribute registration or attribute semantics;
- naming-style conventions such as `PascalCase` or `snake_case`;
- the final grammar or parser implementation;
- target-specific symbol restrictions or name mangling.

## 5. Terminology

This RFC uses terms from the [IndustrialMDE Glossary](../Glossary.md).

- **Source File** — a sequence of bytes presented to the language frontend.
- **Source Text** — the Unicode scalar sequence obtained after valid UTF-8 decoding.
- **Trivia** — source text that separates tokens but is not a semantic token, including whitespace and ordinary comments.
- **Token** — a lexical unit consumed by syntax analysis.
- **Identifier** — an internal language symbol spelling that conforms to the grammar in this RFC.
- **External Tag** — engineering identity stored as data, not as an internal identifier.
- **Effective Language Version** — the version selected by the required `dsl` directive.
- **Raw Span** — a half-open byte range in the original source file.

## 6. Source File Contract

### 6.1 File Extension

IndustrialMDE language source files MUST use the `.plant` extension.

Project manifests, dependency locks, generated artifacts, and serialized intermediate representations are not language source files and MUST use formats defined by their governing specifications.

File-extension matching by project tooling MUST be case-sensitive. A file named `Model.PLANT` is not a canonical IndustrialMDE source file.

### 6.2 Encoding

Source files MUST be valid UTF-8.

An optional UTF-8 byte-order mark is permitted only as the first three bytes of a source file. The byte-order mark is ignored for tokenization but remains part of the raw file and raw byte offsets.

Other byte-order marks and malformed UTF-8 MUST produce an error. A compiler MUST NOT silently replace invalid byte sequences.

Implementations MUST interpret source text as Unicode scalar values. They MUST NOT apply Unicode normalization, case folding, locale-dependent conversion, or replacement-character recovery before tokenization.

### 6.3 Line Endings

The lexical layer MUST recognize both:

- line feed (`U+000A`); and
- carriage return followed by line feed (`U+000D U+000A`)

as one logical newline.

A lone carriage return is invalid source text and MUST produce an error.

Line-ending style MUST NOT change tokenization or language semantics. Implementations MAY retain the original bytes for source mapping and exact source reproduction.

### 6.4 Control Characters

Outside comments and string literals, the only permitted control characters are horizontal tab, line feed, and carriage return when it is part of a valid carriage-return/line-feed pair.

`U+0000` is prohibited everywhere in a source file, including comments and string literals.

Other control characters outside comments and string literals MUST produce an error. String escape sequences are governed by Section 11.

### 6.5 Source Size and Resource Limits

A compiler MUST apply declared resource limits to source size, token count, comment size, and literal size so that untrusted input cannot require unbounded resources.

The active limits MUST be deterministic build configuration. Exceeding a limit MUST produce a diagnostic rather than a partial semantic result.

Required minimum supported limits and compiler configuration keys are deferred to the compiler specification.

## 7. Source Coordinates

### 7.1 Raw Spans

Every token and lexical diagnostic MUST be representable by a half-open raw byte span `[start, end)` in the original source file.

Raw byte offset zero identifies the first byte of the file, including an optional UTF-8 byte-order mark. A zero-width span is permitted for a missing token or end-of-file diagnostic.

### 7.2 Human-Readable Positions

Human-readable lines and columns are one-based.

Logical line counting treats line feed and carriage-return/line-feed as one newline. Columns count Unicode scalar values from the start of the logical line. A horizontal tab advances to the next one-based tab stop in columns 1, 5, 9, and so on.

The canonical tab width for reported source columns is four. Editors MAY display another tab width, but compiler diagnostics and golden tests MUST use the canonical rule.

### 7.3 Protocol Adapters

An LSP or IDE adapter MAY convert canonical spans to the coordinate representation required by its protocol. Such conversion MUST NOT change the canonical diagnostic identity or stored raw span.

## 8. Whitespace

Outside comments and string literals, lexical whitespace consists only of:

- space (`U+0020`);
- horizontal tab (`U+0009`);
- line feed (`U+000A`); and
- a valid carriage-return/line-feed pair.

Other Unicode whitespace characters are not lexical whitespace and MUST produce an error outside comments and string literals. This rule prevents visually indistinguishable source from tokenizing differently across tools.

Whitespace separates tokens when required but is otherwise not semantically significant. No whitespace sequence may synthesize a token or statement terminator.

## 9. Comments and Documentation Comments

### 9.1 Ordinary Comments

The language supports line comments:

```plant
// This comment ends at the logical newline.
```

and block comments:

```plant
/* This comment may span logical lines. */
```

Block comments MUST NOT nest. The first `*/` after the opening delimiter closes the comment. An unclosed block comment is an error.

Comment delimiters inside a string literal are string contents. String delimiters inside a comment do not begin a string literal.

### 9.2 Documentation Comments

The lexical layer recognizes line documentation comments:

```plant
/// Public documentation text.
```

and block documentation comments:

```plant
/** Public documentation text. */
```

Documentation comment tokens MUST retain their source spans and text for later syntax and tooling phases. Attachment to declarations, whitespace trimming, Markdown interpretation, and public API behavior are deferred to a later RFC.

An implementation MUST NOT infer language semantics from the prose inside a documentation comment.

### 9.3 Unicode in Comments

Comments MAY contain Unicode text after valid UTF-8 decoding, subject to the prohibition on `U+0000`.

Tools SHOULD visibly surface bidirectional formatting controls and other invisible security-sensitive characters in comments. A future diagnostics specification may strengthen this recommendation.

## 10. Identifiers and Reserved Words

### 10.1 Identifier Grammar

An identifier token MUST match:

```regex
^[A-Za-z_][A-Za-z0-9_]*$
```

Consequently:

- identifiers use only ASCII letters, ASCII digits, and underscore;
- the first character is an ASCII letter or underscore;
- hyphens, spaces, dots, and Unicode letters are not identifier characters;
- source files remain UTF-8 even though identifiers are ASCII-only.

An identifier beginning with two underscores is reserved for implementation and generated-symbol use. User source MUST NOT declare such an identifier.

### 10.2 Identifier Length

A source identifier MUST contain no more than 255 ASCII characters.

The core limit is intentionally not derived from a legacy target. A target profile MAY impose a stricter representable-symbol limit during target validation and MAY define deterministic name mangling with traceability. A target-specific restriction MUST NOT retroactively make the source text lexically malformed.

The 255-character limit is the Proposed vendor-neutral core contract. Stricter target limits remain target-validation concerns.

### 10.3 Case

Identifier spelling is case-sensitive. `Pump`, `pump`, and `PUMP` are different token spellings.

Case-only collision rules within semantic scopes and case-insensitive target profiles are deferred to RFC-0001B and RFC-0007. Case sensitivity does not imply that every pair of case-only spellings will be legal in the same scope or deployment.

### 10.4 External Engineering Identity

An external engineering tag such as `PUMP-01` is data, not an identifier. It MUST be represented by a string-valued language facility defined by an attribute, annotation, mapping, or domain-profile RFC.

This RFC does not authorize a particular attribute spelling. Examples such as `@tag("PUMP-01")` remain non-normative until the attribute system is defined.

### 10.5 Reserved Keywords

For language version `0.1`, the following lowercase spellings are reserved keywords:

```text
as
dsl
false
import
metadata
namespace
private
public
true
```

Reserved keywords MUST NOT be used as identifiers in that language version. Keyword matching is case-sensitive; for example, `Dsl` is an identifier token, not the `dsl` keyword.

Declaration keywords not yet established by an Accepted semantic RFC are not made normative by this list. A change to the keyword table requires an explicit RFC revision and compatibility analysis.

Adding a reserved keyword to a Stabilized language version is a breaking lexical change unless the spelling was already reserved or the grammar uses a specified contextual-keyword rule.

## 11. String Literals

### 11.1 Form

A string literal begins and ends with an ASCII double quote:

```plant
"Pump station"
```

Single-quoted, raw, interpolated, and multiline string literals are not supported by this RFC.

A physical newline, carriage return, or unescaped control character MUST NOT occur inside a string literal.

### 11.2 Escape Sequences

The following escape sequences are permitted:

| Escape | Value |
| --- | --- |
| `\"` | Double quote |
| `\\` | Backslash |
| `\n` | Line feed |
| `\r` | Carriage return |
| `\t` | Horizontal tab |
| `\u{H...}` | Unicode scalar value expressed by one to six hexadecimal digits |

A Unicode escape MUST encode a valid Unicode scalar value, MUST NOT encode a surrogate code point, and MUST NOT encode `U+0000`.

Unknown escapes, empty Unicode escapes, more than six hexadecimal digits, missing closing braces, and invalid scalar values are errors.

### 11.3 String Identity

String value identity is the exact decoded Unicode scalar sequence after escape processing. The compiler MUST NOT normalize, case-fold, or apply locale-specific transformations to string values.

Target profiles MAY validate whether a string can be represented in a target encoding. Such validation occurs after source parsing.

## 12. Boolean Literals

The lowercase keywords `true` and `false` are boolean literal tokens.

Uppercase or mixed-case variants are identifiers unless a later name-resolution rule resolves them otherwise. They are not boolean literals.

Boolean type semantics are deferred to RFC-0002.

## 13. Numeric Literals

### 13.1 Decimal Integer Literals

A decimal integer literal is either `0` or a nonzero ASCII digit followed by zero or more ASCII digits. Leading zeroes are prohibited in a multi-digit decimal integer.

Examples:

```plant
0
7
1200
1_000_000
```

Underscores MAY separate digits for readability. An underscore MUST have a valid digit on both sides. Consecutive, leading, and trailing underscores are prohibited.

### 13.2 Binary and Hexadecimal Integer Literals

A binary integer literal begins with `0b` or `0B` and contains one or more binary digits.

A hexadecimal integer literal begins with `0x` or `0X` and contains one or more hexadecimal digits. Hexadecimal digits are case-insensitive.

Digit separators follow the same rule as decimal integer literals.

Octal integer literals are not defined.

Examples:

```plant
0b1010_0011
0x2A
0xFF_00
```

### 13.3 Real Literals

A real literal contains:

1. a valid decimal integer part;
2. an ASCII dot;
3. one or more fractional ASCII digits; and
4. an optional decimal exponent.

The exponent begins with `e` or `E`, may contain `+` or `-`, and must contain at least one decimal digit. Digit separators MAY appear between exponent digits.

Examples:

```plant
0.0
10.25
1_000.125
6.022e23
1.0E-6
```

Forms such as `.5`, `1.`, and `1e3` are not valid real literals in this language version.

### 13.4 Sign, Range, and Special Values

A leading `+` or `-` is a separate punctuation or operator token and is not part of a numeric literal.

Literal range, inferred type, overflow behavior, and conversion semantics are deferred to RFC-0002 and RFC-0003.

`NaN`, infinity, locale-specific decimal separators, and implementation-specific numeric suffixes are not numeric literals.

### 13.5 Other Industrial Literals

Time, duration, date, engineering-unit, address, and enumeration literals require later RFCs. Their familiar vendor spellings MUST NOT be accepted as undocumented lexical special cases.

## 14. Punctuation and Token Boundaries

### 14.1 Reserved Punctuation Characters

The following ASCII characters are reserved for language punctuation and operators:

```text
{ } ( ) [ ] ; : , . @ = + - * / % < > ! & | ? #
```

Reservation does not make every spelling a valid construct. A grammar rule or later RFC must authorize each use.

`@` is reserved for a future attribute or annotation system. `#` is reserved for possible versioned literal forms. Neither character acquires semantics from this RFC alone.

Backticks, single quotes, dollar signs, and backslashes outside string literals are invalid source characters unless a later language version explicitly assigns them syntax.

### 14.2 Longest Valid Token

When more than one token can begin at the same source position, the lexer MUST select the longest token valid for the effective language version.

Comment openers take precedence over the division punctuation token. A digit sequence followed by a dot and a decimal digit is tokenized as a real literal; otherwise the dot is a separate punctuation token.

Composite operator tokens, if introduced, MUST be listed by the RFC that defines their syntax.

### 14.3 Statement Terminators

There is no automatic semicolon insertion.

The version directive and metadata entries defined by this RFC use explicit semicolons. Later RFCs must state where a terminator is required after each additional declaration form.

### 14.4 No Preprocessor or Shebang

Source files MUST NOT contain a shebang, textual include directive, macro preprocessor, conditional-compilation directive, or line-remapping directive unless a future RFC explicitly introduces one.

Dependencies are represented through the module and package model rather than textual inclusion.

## 15. Language-Version Directive

### 15.1 Required Form

Every `.plant` source file MUST declare its language version with:

```plant
dsl "0.1";
```

The version string MUST contain one or more ASCII decimal digits, one ASCII dot, and one or more ASCII decimal digits. Leading zeroes are prohibited in each component except for the component `0`.

A patch component, range, wildcard, prerelease label, or build label is not permitted in the source directive.

### 15.2 Placement

The `dsl` directive MUST be the first non-trivia construct in the file. An optional UTF-8 byte-order mark, whitespace, ordinary comments, and documentation comments MAY precede it.

A file MUST contain exactly one `dsl` directive.

### 15.3 Version Selection

The declared version selects the lexical and syntactic contract used for the entire source file.

A compiler that does not support the declared version MUST report that fact and MUST NOT silently parse the file as another version.

RFC-0001C may constrain the set of language versions permitted within one Project. The explicit per-file directive remains authoritative for that file and MUST NOT be silently overridden by a manifest.

## 16. Metadata Block

### 16.1 Form

A source file MAY contain one metadata block immediately after the version directive and intervening trivia:

```plant
metadata {
    author: "Jane Doe";
    company: "Industrial Automation Inc";
    revision: "0.1.0";
}
```

A metadata entry consists of an identifier key, a colon, a scalar literal, and a semicolon.

This RFC permits string, boolean, decimal integer, binary integer, hexadecimal integer, and real literals as metadata values. Expressions, references, collections, and nested metadata objects are prohibited.

### 16.2 Uniqueness and Ordering

A metadata key MUST appear at most once in a metadata block. A source file MUST contain at most one metadata block.

Source order is retained for source formatting and traceability. Consumers that serialize metadata into a canonical artifact MUST use the deterministic ordering defined by that artifact format.

### 16.3 Semantic Boundary

Metadata MUST NOT alter name resolution, type checking, execution behavior, connection semantics, validation severity, or target selection.

An Accepted specification MAY define how particular metadata keys are copied into documentation, provenance, or artifact manifests. Unknown metadata keys MUST be preserved by lossless tooling but MUST NOT acquire implementation-defined semantics.

This RFC standardizes no metadata keys. A later provenance or documentation contract may register keys without making metadata executable.

Required project configuration and compiler options belong in the project manifest, not in source metadata.

## 17. Post-Metadata Syntax Boundary

The source prefix owned by this RFC is:

```text
language-version directive
optional metadata block
remaining token stream defined by later syntax RFCs
```

The following is a complete source file under the syntax owned by this RFC:

```plant
dsl "0.1";

metadata {
    author: "Jane Doe";
    revision: "0.1.0";
}
```

The `namespace` and `import` spellings are reserved keywords, but this RFC defines no namespace or import directive grammar. RFC-0001B owns namespace, scope, qualification, and import syntax. RFC-0001C owns module, package, dependency, and compilation-unit semantics.

## 18. Deterministic Lexical Behavior

For identical source bytes, effective language version, and declared lexical resource limits, conforming implementations MUST produce the same:

- token kinds;
- token spellings and decoded literal values;
- token raw spans;
- logical line and column positions;
- trivia classification;
- lexical diagnostic codes, severities, primary spans, and ordering.

Locale, operating system, default platform encoding, filesystem ordering, hash iteration, or parser framework MUST NOT affect these results.

Lexical diagnostics MUST be ordered by raw start offset, then raw end offset, then diagnostic code, then a stable implementation-independent secondary key defined by the diagnostics specification.

## 19. Diagnostic Expectations

The following diagnostic codes are defined by this Proposed revision. A code change requires an explicit RFC revision and diagnostic compatibility analysis.

| Code | Severity | Condition | Required primary span |
| --- | --- | --- | --- |
| `IMDE1001` | Error | Invalid UTF-8 or unsupported byte-order mark | Invalid byte sequence or mark |
| `IMDE1002` | Error | Invalid source, control, or Unicode whitespace character | Offending bytes |
| `IMDE1003` | Error | Unterminated block comment | Opening delimiter through end of file |
| `IMDE1004` | Error | Unterminated string literal | Opening quote through failure point |
| `IMDE1005` | Error | Invalid string escape or Unicode scalar | Escape sequence |
| `IMDE1006` | Error | Malformed numeric literal | Maximal malformed numeric-like sequence |
| `IMDE1007` | Error | Identifier exceeds the core limit or uses a reserved implementation prefix | Identifier spelling |
| `IMDE1101` | Error | Missing, duplicate, or misplaced language-version directive | Failure point or duplicate directive |
| `IMDE1102` | Error | Unsupported or malformed language version | Version string or directive |
| `IMDE1103` | Error | Duplicate metadata key | Later key, with the first key as related information |
| `IMDE1104` | Error | Duplicate or misplaced metadata block | Later or misplaced `metadata` keyword |

Every diagnostic MUST follow the diagnostic contract in RFC-0000. A fix-it is optional and MUST NOT be applied without user confirmation.

Syntax diagnostics for otherwise valid token sequences are owned by the grammar specification.

## 20. Examples

### 20.1 Positive Example

```plant
// UTF-8 comments and strings are permitted: ciśnienie, давление.
dsl "0.1";

metadata {
    author: "Controls Team";
    revision: "0.1.0";
    reviewed: false;
    source_number: 1_024;
}
```

Expected result: the lexical layer produces a version directive, one metadata block, no diagnostics, and stable raw spans.

### 20.2 Invalid Internal Tag Spelling

```plant
dsl "0.1";
PUMP-01
```

Expected result: `PUMP-01` cannot form one identifier. It is tokenized as separate identifier, punctuation, and malformed numeric-like input and is rejected. Tooling SHOULD explain that a hyphenated engineering tag belongs in an external string-valued facility.

### 20.3 Invalid Unicode Identifier

```plant
dsl "0.1";
Насос
```

Expected result: the first non-ASCII identifier character produces `IMDE1002`.

### 20.4 Invalid Numeric Separators

```plant
dsl "0.1";

metadata {
    first: _10;
    second: 10_;
    third: 1__0;
}
```

Expected result: each malformed numeric-like spelling is rejected. `_10` tokenizes as an identifier and is rejected by metadata syntax; `10_` and `1__0` produce `IMDE1006`.

### 20.5 Invalid Nested Comment Assumption

```plant
dsl "0.1";
/* outer /* inner */ still_source */
```

Expected result: the first `*/` closes the only block comment. The remaining source is tokenized normally and rejected by syntax analysis; the lexer must not treat comments as nested.

### 20.6 Unsupported Version

```plant
dsl "99.0";
```

Expected result: a compiler without language version `99.0` support emits `IMDE1102` and does not reinterpret the file as its newest supported version.

### 20.7 Boundary Cases

Conformance fixtures for this RFC MUST include:

- identifiers containing exactly 255 and 256 ASCII characters;
- files with no byte-order mark and with one valid UTF-8 byte-order mark;
- line feed and carriage-return/line-feed variants of the same source;
- tabs at columns before and on canonical tab stops;
- Unicode scalar escapes at `U+0001`, `U+D7FF`, `U+E000`, and `U+10FFFF`;
- rejected escapes for `U+0000`, surrogate code points, and values above `U+10FFFF`;
- maximum permitted source and literal sizes for the active resource profile.

## 21. Compatibility

### 21.1 Versioned Lexical Contract

Tokenization is part of the declared language-version contract. A compiler supporting an older version MUST use that version's keyword table and token rules rather than applying the newest rules.

A lexical change that causes valid Stabilized source to tokenize differently is breaking unless the old spelling was explicitly reserved for that purpose.

### 21.2 Managed Evolution

Future lexical features SHOULD prefer:

- previously reserved punctuation;
- contextual keywords with unambiguous grammar positions;
- explicit version boundaries;
- diagnostics and migration guidance before removal.

An Accepted compatibility policy may require a stronger transition process. This RFC does not promise that every pre-1.0 Draft spelling will remain supported.

### 21.3 Newline and Encoding Portability

Line-feed and carriage-return/line-feed source variants have the same tokens and semantic meaning but are not byte-identical source inputs. Raw hashes and raw spans MAY differ. Canonical content identity and cache normalization are deferred to RFC-0001C.

## 22. Safety and Security Considerations

- ASCII-only identifiers reduce mixed-script and confusable-symbol risk.
- Prohibiting silent UTF-8 repair prevents tools from compiling text different from the text reviewed.
- Explicit decimal syntax avoids locale-dependent numeric interpretation.
- Non-nesting comments and bounded literals simplify resource control.
- A required version directive prevents silent parsing under a different language contract.
- Prohibiting textual includes and preprocessors preserves explicit dependency analysis.
- Exact string identity avoids hidden normalization changes to external tags and asset identifiers.
- Tooling should make invisible and bidirectional Unicode controls visible during review.

These rules do not make source trustworthy. Compilers must still treat source files, packages, manifests, and plugins as untrusted input.

## 23. Relationship to Later RFCs

RFC-0001A will define the Core Semantic Kernel and industrial-profile relationship.

RFC-0001B will define identifier categories, naming conventions, scopes, namespaces, qualification, collisions, shadowing, and import-name exposure.

RFC-0001C will define compilation units, project manifests, source discovery, module and package identity, dependency graphs, language-version coordination, and content identity.

RFC-0002 and RFC-0003 will define literal typing, ranges, expressions, operators, and conversions.

A future attribute RFC or an explicitly scoped section of another RFC will define `@` syntax and attribute registration.

RFC-0014 will consolidate the Accepted syntax into a complete grammar. It MUST conform to this RFC rather than redefine its lexical semantics silently.

## 24. Alternatives Considered

### 24.1 Unicode Identifiers

Unicode identifiers would improve native-language naming but introduce normalization, confusable, target-encoding, and mixed-script concerns. UTF-8 comments, documentation, strings, and external display data provide localization without making symbol identity dependent on those concerns.

### 24.2 Hyphenated Identifiers

Allowing `PUMP-01` as one identifier would conflict with subtraction and make internal symbol rules depend on engineering-tag syntax. External tags remain strings.

### 24.3 Project-Only Language Version

A version only in the manifest would reduce repetition but make an isolated source file ambiguous and complicate tooling. This Proposed RFC requires an explicit per-file directive. RFC-0001C may define coordinated project constraints without silently changing a file's effective version.

### 24.4 A 64-Character Core Identifier Limit

A 64-character core limit would embed constraints from some legacy targets in the vendor-neutral lexical layer. This Proposed RFC instead defines a generous core limit and target-profile validation or deterministic mangling.

### 24.5 Multiline and Interpolated Strings

These forms add lexer complexity and can blur the boundary between data and executable templates. They are excluded until a concrete modeling use case justifies them.

## 25. Resolved and Delegated Decisions

| Topic | Resolution | Owning contract |
| --- | --- | --- |
| Identifier length | 255 ASCII characters in the core | This RFC |
| UTF-8 BOM | Permitted only at byte offset zero; ignored for tokens and retained in raw offsets | This RFC |
| Canonical source span | Half-open raw UTF-8 byte span | This RFC |
| Bidirectional controls | Tooling SHOULD expose security-sensitive invisible characters; no mandatory warning is added here | This RFC and future diagnostics policy |
| Documentation before `dsl` | Permitted as trivia; attachment remains undefined | This RFC and documentation contract |
| Standard metadata keys | None | Future provenance or documentation contract |
| Binary and hexadecimal integers | Included | This RFC |
| Reserved punctuation | Retained as reserved syntax space without implicit semantics | This RFC |
| Namespace and import syntax | Fully delegated | RFC-0001B |
| Project language-version constraints | May restrict the permitted set but cannot override a file directive | RFC-0001C |

## 26. Conformance Requirements

An implementation conforms to this RFC revision only if it:

- accepts every valid lexical example and required boundary case;
- rejects every invalid lexical example with the required diagnostic facts;
- produces deterministic tokens, spans, decoded values, and diagnostics;
- preserves documentation-comment information for later phases;
- does not apply implementation-specific normalization or recovery;
- does not infer unstandardized semantics from metadata or reserved punctuation;
- reports its supported language versions explicitly.

Conformance to this Proposed RFC alone does not make the implementation conformant to an IndustrialMDE language release.

## 27. Non-Normative Implementation Notes

A frontend may use a generated lexer, scannerless parser, parser combinators, or a hand-written tokenizer. The implementation strategy is an ADR concern.

It is often useful to retain:

- original source bytes;
- decoded source text;
- raw byte spans;
- logical line-start indexes;
- trivia and documentation-comment tokens;
- decoded literal values alongside original spellings.

These notes do not require a separate concrete syntax tree and AST. Phase-representation choices must demonstrate the value added by each layer.

## 28. Change Log

### Draft — 2026-07-19

- Created the canonical RFC-0001 file.
- Defined the initial source, lexical, version, metadata, and diagnostic contracts.
- Recorded unresolved design questions without claiming acceptance.

### Proposed — 2026-07-19

- Incorporated project-owner audit decisions.
- Confirmed the 255-character identifier limit, BOM handling, raw-byte spans, literals, and reserved punctuation.
- Delegated all namespace and import grammar to RFC-0001B.
