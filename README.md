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

Create a new project from the python template:

```bash
cookiecutter sevaht-python-project
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

## Recommendations

Python's `pyproject.toml`, and the MIT/BSD license texts, want an author name
and email. Those fields are prompted first so you can fill in this
typically-identical information and then focus on the project-specific fields.
To avoid retyping it every time, set defaults in `~/.cookiecutterrc`:

```yaml
default_context:
    author: "First Last"
    email: "somebody@website.com"
    github_owner: "your-github-username"
```
