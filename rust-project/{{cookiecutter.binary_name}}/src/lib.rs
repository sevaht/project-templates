//! {{ cookiecutter.project_description }}
{%- if cookiecutter.project_type == "application" %}
//!
//! Everything the `{{ cookiecutter.binary_name }}` binary does lives in this
//! library; `src/main.rs` only connects it to the process. That keeps all of
//! it reachable from tests and from the generated documentation.

pub mod arguments;
pub mod logging;

pub use arguments::Arguments;

/// Runs the application with the parsed command line.
///
/// # Errors
///
/// Returns an error describing why the application could not finish.
pub fn run(arguments: &Arguments) -> anyhow::Result<()> {
    tracing::debug!(?arguments, "starting");
    tracing::warn!("application code goes here!");
    Ok(())
}
{%- else %}
//!
//! Describe the concepts this library models, name its primary types, and show
//! a short example of typical use. This text is the front page of the
//! generated documentation (`cargo doc --open`).
{%- endif %}
