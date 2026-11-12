# Project Templates

Modernized [cookiecutter](https://cookiecutter.readthedocs.io/) templates for
new projects, set up for [uv](https://docs.astral.sh/uv/) and following the
conventions of the sibling projects (hatchling + hatch-vcs, ruff/black/mypy/
vulture via `./checks`, and GitHub Actions for publishing).

## Usage

Run `./install.sh` to register the templates in your user's cookiecutter store,
or `./install.sh --remove` to unregister them. Each template is installed with
a `sevaht-` prefix. List installed templates with:

```bash
cookiecutter -l
```

Create a new project from the python or rust template:

```bash
cookiecutter sevaht-python-project
cookiecutter sevaht-rust-project
```

## The `python-project` template

Prompts for the usual project metadata plus three shaping choices:

- **`project_type`** — `application` (gets a console-script entry point) or
  `library` (gets a Sphinx docs scaffold + a GitHub Pages workflow).
- **`gui`** — `yes`/`no`; only meaningful for applications. A GUI application
  depends on `sevaht-gui` (and Pillow) and starts from a `TkApp` skeleton; a
  non-GUI application starts from an argparse CLI.
- **`versioning`** — `dynamic` (version derived from git tags via hatch-vcs) or
  `standard` (a static `version` in `pyproject.toml`).

Every generated project depends on the PyPI-published `sevaht-utility`.

## The `rust-project` template

Generates a Cargo package that follows the Rust coding standards: edition
2024, a pinned stable toolchain, the full clippy configuration, rustfmt,
cargo-deny, optimized release builds for applications, and a `./checks` script
(`./checks --docs` runs the documentation checks, which never block the
regular run, and `./checks --coverage` reports test coverage). Prompts for the
same metadata as the python template, plus:

- **`project_type`**: `application` or `library`. An application is a library
  plus a thin `main.rs`. It starts from a clap command line with the standard
  logging options (`--log-file`, and one of `-v`, `-q`, `--debug`) wired to
  `tracing`, and integration tests that run the executable. A library starts
  from a documented, empty `lib.rs`.
- **`crate_name`**: the name used in Rust code, derived from `binary_name`.
- **`keywords`** and **`categories`**: crates.io metadata, which clippy
  requires of any publishable package.
- **`rust_version`**: the minimum supported Rust version (1.85 or newer, the
  first with the 2024 edition).

The checks need `cargo-nextest`, `cargo-deny`, and `cargo-machete`, and
`./checks --coverage` also needs `cargo-llvm-cov` (on Arch:
`pacman -S cargo-nextest cargo-deny cargo-machete cargo-llvm-cov`).

## Recommendations

Python's `pyproject.toml`, Rust's `Cargo.toml`, and the MIT/BSD license texts
want an author name and email. Those fields are prompted first so you can fill
in this typically-identical information and then focus on the project-specific
fields.
To avoid retyping it every time, set defaults in `~/.cookiecutterrc`:

```yaml
default_context:
    author: "First Last"
    email: "somebody@website.com"
    github_owner: "your-github-username"
```
