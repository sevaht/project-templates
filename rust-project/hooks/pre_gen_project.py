"""Validate inputs before generation.

Cookiecutter does no escaping: every value is substituted verbatim into the
generated files *and into these hooks*. A stray quote or backslash in a
free-text field would therefore produce broken TOML (or break this script).
Values are pulled in below through the ``tojson`` filter -- which emits a valid
literal even when the value contains quotes or backslashes -- so they can be
checked here and a bad value fails fast with a clear message instead of
silently generating something that will not compile.
"""

from __future__ import annotations

import re
import sys

# Rendered via tojson so the embedded literals are injection-safe regardless of
# what the value contains.
BINARY_NAME = {{ cookiecutter.binary_name | tojson }}
CRATE_NAME = {{ cookiecutter.crate_name | tojson }}
GITHUB_OWNER = {{ cookiecutter.github_owner | tojson }}
AUTHOR = {{ cookiecutter.author | tojson }}
EMAIL = {{ cookiecutter.email | tojson }}
DESCRIPTION = {{ cookiecutter.project_description | tojson }}
COPYRIGHT_YEAR = {{ cookiecutter.copyright_year | tojson }}
RUST_VERSION = {{ cookiecutter.rust_version | tojson }}
KEYWORDS = {{ cookiecutter.keywords | tojson }}
CATEGORIES = {{ cookiecutter.categories | tojson }}

# binary_name becomes the Cargo package and executable name, crate_name the
# identifier used in Rust code, and github_owner part of the project URLs, so
# each has to satisfy the rules for what it becomes. Cargo also accepts
# underscores in package names, but the convention is kebab-case.
PACKAGE_RE = re.compile(r"^[a-z][a-z0-9]*(-[a-z0-9]+)*$")
CRATE_RE = re.compile(r"^[a-z][a-z0-9]*(_[a-z0-9]+)*$")
OWNER_RE = re.compile(r"^[a-z0-9](-?[a-z0-9])*$", re.IGNORECASE)
RUST_VERSION_RE = re.compile(r"^1\.[0-9]+(\.[0-9]+)?$")
MINIMUM_RUST_MINOR_VERSION = 85  # the 2024 edition's first release

# crates.io's rules: at most five of each; a keyword is ASCII, starts with a
# letter, and is at most 20 characters; a category is a slug such as
# "command-line-utilities" or "parsing::text".
MAXIMUM_LIST_LENGTH = 5
KEYWORD_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_+-]{0,19}$")
CATEGORY_RE = re.compile(r"^[a-z0-9-]+(::[a-z0-9-]+)*$")

# Words that cannot name a crate, because the crate name is a Rust identifier.
RUST_KEYWORDS = frozenset(
    "as async await break const continue crate dyn else enum extern false fn "
    "for gen if impl in let loop match mod move mut pub ref return self Self "
    "static struct super trait true type unsafe use where while".split()
)

# These characters terminate the double-quoted TOML string literals the
# free-text values are substituted into, which would break the generated files.
UNSAFE_CHARACTERS = ('"', "\\")


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def split_list(text: str) -> list[str]:
    return [item.strip() for item in text.split(",") if item.strip()]


def validate_list(label: str, text: str, item_re: re.Pattern[str]) -> None:
    items = split_list(text)
    if len(items) > MAXIMUM_LIST_LENGTH:
        fail(f"{label} may list at most {MAXIMUM_LIST_LENGTH}: {text!r}")
    invalid = [item for item in items if not item_re.fullmatch(item)]
    if invalid:
        fail(f"{label} contains invalid entries: {invalid!r}")


def main() -> None:
    if not PACKAGE_RE.fullmatch(BINARY_NAME):
        fail(
            f"binary_name {BINARY_NAME!r} is not a valid package name "
            "(lowercase letters and digits, separated by single hyphens)."
        )
    if not CRATE_RE.fullmatch(CRATE_NAME) or CRATE_NAME in RUST_KEYWORDS:
        fail(
            f"crate_name {CRATE_NAME!r} is not a valid crate name "
            "(lowercase letters and digits, separated by single underscores, "
            "and not a Rust keyword)."
        )
    if not OWNER_RE.fullmatch(GITHUB_OWNER):
        fail(f"github_owner {GITHUB_OWNER!r} is not a valid GitHub owner.")
    if not RUST_VERSION_RE.fullmatch(RUST_VERSION) or (
        int(RUST_VERSION.split(".")[1]) < MINIMUM_RUST_MINOR_VERSION
    ):
        fail(
            f"rust_version {RUST_VERSION!r} must be 1.{MINIMUM_RUST_MINOR_VERSION}"
            " or newer, written as 1.MINOR or 1.MINOR.PATCH."
        )
    validate_list("keywords", KEYWORDS, KEYWORD_RE)
    validate_list("categories", CATEGORIES, CATEGORY_RE)
    for label, value in (
        ("author", AUTHOR),
        ("email", EMAIL),
        ("project_description", DESCRIPTION),
        ("copyright_year", COPYRIGHT_YEAR),
    ):
        present = [char for char in UNSAFE_CHARACTERS if char in value]
        if present:
            quoted = " or ".join(repr(char) for char in present)
            fail(f"{label} may not contain {quoted}: {value!r}")


if __name__ == "__main__":
    main()
