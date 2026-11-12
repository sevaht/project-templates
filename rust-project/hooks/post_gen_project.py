"""Post-generation cleanup for the rust-project template.

Writes the chosen LICENSE from the shared license texts and prunes the files
that do not apply to the selected project type: libraries drop the binary entry
point, its command-line and logging modules, and the command-line tests (the
only tests the template provides).
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
    source_file = (
        Path(r"{{ shared_directory }}") / "licenses" / f"{license_id}.txt"
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
    if r"{{ cookiecutter.project_type }}" == "library":
        source_path = Path("src")
        remove_path(source_path / "main.rs")
        remove_path(source_path / "arguments.rs")
        remove_path(source_path / "logging.rs")
        remove_path(Path("tests"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
