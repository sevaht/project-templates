"""Validate inputs before generation.

Cookiecutter does no escaping: every value is substituted verbatim into the
generated files *and into these hooks*. A stray quote or backslash in a
free-text field would therefore produce broken Python/TOML (or break this
script). Values are pulled in below through the ``tojson`` filter -- which
emits a valid literal even when the value contains quotes or backslashes -- so
they can be checked here and a bad value fails fast with a clear message
instead of silently generating something that will not compile.
"""

from __future__ import annotations

import re
import sys

# Rendered via tojson so the embedded literals are injection-safe regardless of
# what the value contains.
PROJECT_SLUG = {{ cookiecutter.project_slug | tojson }}
BINARY_NAME = {{ cookiecutter.binary_name | tojson }}
GITHUB_OWNER = {{ cookiecutter.github_owner | tojson }}
AUTHOR = {{ cookiecutter.author | tojson }}
EMAIL = {{ cookiecutter.email | tojson }}
DESCRIPTION = {{ cookiecutter.project_description | tojson }}
COPYRIGHT_YEAR = {{ cookiecutter.copyright_year | tojson }}

# project_slug becomes the importable package name, binary_name the published
# distribution name, and github_owner part of the project URLs, so each has to
# satisfy the rules for what it becomes.
SLUG_RE = re.compile(r"^[a-z_][a-z0-9_]*$")
DIST_RE = re.compile(r"^[a-z0-9]+([._-][a-z0-9]+)*$")
OWNER_RE = re.compile(r"^[a-z0-9](-?[a-z0-9])*$", re.IGNORECASE)

# These characters terminate the double-quoted Python/TOML string literals the
# free-text values are substituted into, which would break the generated files.
UNSAFE_CHARACTERS = ('"', "\\")


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    if not SLUG_RE.fullmatch(PROJECT_SLUG):
        fail(
            f"project_slug {PROJECT_SLUG!r} is not a valid Python package "
            "name; choose a project_name of letters, digits, and spaces "
            "(e.g. 'My Project')."
        )
    if not DIST_RE.fullmatch(BINARY_NAME):
        fail(
            f"binary_name {BINARY_NAME!r} is not a valid distribution name "
            "(lowercase letters, digits, and single . _ - separators)."
        )
    if not OWNER_RE.fullmatch(GITHUB_OWNER):
        fail(f"github_owner {GITHUB_OWNER!r} is not a valid GitHub owner.")
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
