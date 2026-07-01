# {{ cookiecutter.project_name }}

{{ cookiecutter.project_description }}

## Development

This project uses [uv](https://docs.astral.sh/uv/). Sync the environment
(including the dev dependency group) and run the linters and tests:

```console
$ uv sync
$ ./checks
```
{% if cookiecutter.project_type == "application" %}
## Usage

```console
$ uv run {{ cookiecutter.binary_name }} --help
```
{% else %}
## Installation

```console
$ pip install {{ cookiecutter.binary_name }}
```

## Documentation

The docs are built with Sphinx and published to GitHub Pages. Build them
locally with:

```console
$ uv run --group docs sphinx-build -b html docs docs/_build/html
```
{% endif %}