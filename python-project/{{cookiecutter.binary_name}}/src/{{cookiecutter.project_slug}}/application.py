{%- if cookiecutter.gui == "yes" -%}
"""Graphical entry point for {{ cookiecutter.binary_name }}."""

from __future__ import annotations

import argparse
import importlib.metadata
import logging
import tkinter as tk
from tkinter import ttk
from typing import TYPE_CHECKING

from PIL import Image
from sevaht_gui import TkApp
from sevaht_utility.log_utility import add_log_arguments, configure_logging

if TYPE_CHECKING:
    from collections.abc import Sequence

logger = logging.getLogger(__name__)

APP_NAME = "{{ cookiecutter.binary_name }}"


def render_icon(size: int) -> Image.Image:
    """Render the tray/window icon (any PIL image, path, or renderer works)."""
    return Image.new("RGBA", (size, size), (0, 128, 255, 255))


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=importlib.metadata.metadata(__package__).get("summary")
    )
    add_log_arguments(parser)
    args = parser.parse_args(args=argv)
    configure_logging(args)

    # TkApp owns the main thread and runs the tray icon on a worker thread; it
    # handles theming, centering, close-to-tray, and quit confirmation.
    app = TkApp(quit_confirm=f"Quit {APP_NAME}?")
    app.root.title(APP_NAME)

    content = ttk.Frame(app.root, padding=24)
    content.pack(fill=tk.BOTH, expand=True)
    ttk.Label(content, text="application code goes here!").pack(pady=(0, 12))
    ttk.Button(
        content,
        text="Send a notification",
        command=lambda: app.notify(APP_NAME, "This is a notification."),
    ).pack(pady=(0, 8))
    # app.quit() is thread-safe and honors the quit_confirm prompt above.
    ttk.Button(content, text="Quit", command=app.quit).pack()

    # None when no system tray is available; the app then runs window-only.
    tray_icon = app.create_tray_icon(APP_NAME, APP_NAME, render_icon)
    app.run(tray_icon)
    return 0
{%- else -%}
"""Command-line entry point for {{ cookiecutter.binary_name }}."""

from __future__ import annotations

import argparse
import importlib.metadata
import logging
from typing import TYPE_CHECKING

from sevaht_utility.log_utility import add_log_arguments, configure_logging

if TYPE_CHECKING:
    from collections.abc import Sequence

logger = logging.getLogger(__name__)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=importlib.metadata.metadata(__package__).get("summary")
    )
    add_log_arguments(parser)
    args = parser.parse_args(args=argv)
    configure_logging(args)

    logger.warning("application code goes here!")
    return 0
{%- endif %}
