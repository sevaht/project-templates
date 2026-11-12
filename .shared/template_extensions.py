"""Jinja extensions shared by every template in this repository.

Each template directory links to this module, and its ``cookiecutter.json``
lists ``template_extensions.SharedDirectoryExtension`` under ``_extensions``.
Cookiecutter imports the module from the template directory before anything
is rendered, so ``__file__`` resolves (through the link) to this directory no
matter how the template was named on the command line.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from jinja2.ext import Extension

if TYPE_CHECKING:
    from jinja2 import Environment

SHARED_DIRECTORY = Path(__file__).resolve().parent


class SharedDirectoryExtension(Extension):
    """Exposes ``shared_directory``: the absolute path of this directory.

    Hooks use it to find shared files. ``cookiecutter._repo_dir`` cannot be
    used for that: it is the template path exactly as given, so a relative
    path breaks once the hook runs inside the generated project.
    """

    def __init__(self, environment: Environment) -> None:
        super().__init__(environment)
        environment.globals["shared_directory"] = str(SHARED_DIRECTORY)
