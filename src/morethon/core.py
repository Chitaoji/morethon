"""
Contains the core of morethon: ... , etc.

NOTE: this module is private. All functions and objects are available in the main
`morethon` namespace - use that instead.

"""

__all__ = ["runfile"]

from pathlib import Path

from .grammar import MoParser


def runfile(filename: str) -> None:
    """Read from script file and run the morethon interpreter."""
    MoParser().exec(Path(filename).read_text("utf-8"))
