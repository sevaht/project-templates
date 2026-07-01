"""Sphinx configuration for the {{ cookiecutter.binary_name }} documentation."""

from __future__ import annotations

import importlib.metadata
import sys
from pathlib import Path

# Allow autodoc to import the package directly from the source tree even when
# it has not been installed into the build environment.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

# -- Project information ------------------------------------------------------
project = "{{ cookiecutter.binary_name }}"
author = "{{ cookiecutter.author }}"
copyright = f"{{ cookiecutter.copyright_year }}, {author}"  # noqa: A001

try:
    release = importlib.metadata.version("{{ cookiecutter.binary_name }}")
except importlib.metadata.PackageNotFoundError:
    release = "0.0.0"
version = release

# -- General configuration ----------------------------------------------------
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "myst_parser",
]

source_suffix = {".rst": "restructuredtext", ".md": "markdown"}
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Autodoc / Napoleon -------------------------------------------------------
autodoc_member_order = "bysource"
autodoc_typehints = "signature"
autodoc_default_options = {"members": True, "show-inheritance": True}
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = False

# -- MyST (Markdown) ----------------------------------------------------------
myst_enable_extensions = ["colon_fence", "deflist"]
myst_heading_anchors = 3

# -- Cross references ---------------------------------------------------------
intersphinx_mapping = {"python": ("https://docs.python.org/3", None)}

# -- HTML output --------------------------------------------------------------
html_theme = "furo"
html_title = f"{{ cookiecutter.binary_name }} {version}"
html_static_path = ["_static"]
