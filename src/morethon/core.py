"""
Contains the core of morethon: ... , etc.

NOTE: this module is private. All functions and objects are available in the main
`morethon` namespace - use that instead.

"""

__all__ = ["execfile"]

from pathlib import Path

from .grammar import MoInterpreter


def execfile(filename: str) -> None:
    """Execute a script file."""
    MoInterpreter().exec(Path(filename).read_text("utf-8"))
