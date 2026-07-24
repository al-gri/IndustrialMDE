"""Small reviewable byte fixtures for lexical loader behavior."""

INVALID_UTF8 = b'{"value":"\xff"}'
UTF8_BOM = b"\xef\xbb\xbf{}"
EMPTY = b" \t\r\n"
MULTIPLE_DOCUMENTS = b"{} {}"
TRAILING_CONTENT = b"{} trailing"
DUPLICATE_DIRECT_KEY = b'{"name":0,"name":1}'
DUPLICATE_ESCAPE_EQUIVALENT_KEY = b'{"name":0,"n\\u0061me":1}'

CANONICAL_ZERO = b"0"
LEADING_ZERO = b"01"
NEGATIVE_ZERO = b"-0"
NEGATIVE_INTEGER = b"-1"
FRACTIONAL = b"1.0"
EXPONENT = b"1e2"
MAXIMUM_INTEGER = b"2147483647"
OVERFLOW_INTEGER = b"2147483648"

VALID_SURROGATE_PAIR = b'"\\ud83d\\ude80"'
UNPAIRED_HIGH_SURROGATE = b'"\\ud83d"'
UNPAIRED_LOW_SURROGATE = b'"\\ude80"'
INVALID_ESCAPE = b'"\\x"'
