"""Post-generation cleanup for the rust-project template.

Writes the chosen LICENSE from the shared license texts and prunes the files
that do not apply to the selected project type: libraries drop the binary entry
point, its command-line and logging modules, and the command-line tests (the
only tests the template provides). For the workspace layout it then moves the
crate (its manifest, sources and tests) under ``crates/``; the single-crate
layout drops that member manifest instead.
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


def arrange_layout() -> None:
    member_manifest = Path("crate-Cargo.toml")
    if r"{{ cookiecutter.layout }}" != "workspace":
        remove_path(member_manifest)
        return
    crate_path = Path("crates") / r"{{ cookiecutter.binary_name }}"
    crate_path.mkdir(parents=True)
    member_manifest.rename(crate_path / "Cargo.toml")
    for name in ("src", "tests"):
        if Path(name).exists():
            Path(name).rename(crate_path / name)


def main() -> int:
    write_license()
    if r"{{ cookiecutter.project_type }}" == "library":
        source_path = Path("src")
        remove_path(source_path / "main.rs")
        remove_path(source_path / "arguments.rs")
        remove_path(source_path / "logging.rs")
        remove_path(Path("tests"))
    arrange_layout()
    return 0


if __name__ == "__main__":
    sys.exit(main())
