"""{{ cookiecutter.project_description }}

Attributes:
    __version__: The installed distribution version.
"""

import importlib.metadata

__version__ = importlib.metadata.version(__package__)
