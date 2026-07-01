"""Post-generation cleanup for the python-project template.

Writes the chosen LICENSE from the shared license texts and prunes the files
that do not apply to the selected project type:

* libraries drop the application entry points (``__main__.py`` / the entry
  module);
* applications drop the Sphinx docs scaffold and its Pages workflow.
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path
from string import Template


def remove_path(path: Path) -> None:
    if path.is_dir():
        shutil.rmtree(path)
    elif path.exists():
        path.unlink()


def write_license() -> None:
    license_id = r"{{ cookiecutter.license }}"
    if license_id == "None":
        return
    source_file = (
        Path(r"{{ cookiecutter._repo_dir }}").resolve().parent
        / ".shared"
        / "licenses"
        / f"{license_id}.txt"
    )
    license_template = Template(source_file.read_text())
    (Path.cwd() / "LICENSE").write_text(
        license_template.substitute(
            copyright_year=r"{{ cookiecutter.copyright_year }}",
            author=r"{{ cookiecutter.author }}",
        )
    )


def main() -> int:
    write_license()
    package_path = Path("src") / r"{{ cookiecutter.project_slug }}"
    if r"{{ cookiecutter.project_type }}" == "library":
        remove_path(package_path / "__main__.py")
        remove_path(package_path / "application.py")
    else:
        remove_path(Path("docs"))
        remove_path(Path(".github") / "workflows" / "docs.yml")
    return 0


if __name__ == "__main__":
    sys.exit(main())
