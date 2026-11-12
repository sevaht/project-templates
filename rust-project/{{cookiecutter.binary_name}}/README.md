# {{ cookiecutter.project_name }}

{{ cookiecutter.project_description }}

## Development

The toolchain is pinned in `rust-toolchain.toml`; rustup installs it on first
use. The checks need four cargo extensions:

```console
$ cargo install --locked cargo-nextest cargo-deny cargo-machete cargo-llvm-cov
```

Run every check (formatting, lints, tests, dependency audit), only the
documentation checks, or the tests with a coverage report:

```console
$ ./checks
$ ./checks --docs
$ ./checks --coverage
```

Browse the generated documentation, private items included:

```console
$ cargo doc --document-private-items --open
```
{%- if cookiecutter.project_type == "application" %}

## Usage

```console
$ cargo run -- --help
```
{%- endif %}
