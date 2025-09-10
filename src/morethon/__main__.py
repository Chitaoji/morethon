"""Execute morethon."""

from pathlib import Path

import click

from .grammar import MoInterpreter


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.argument("filename", default="")
def run(filename: str) -> None:
    """
    Run the morethon interpreter.

    If FILENAME is specified, read from script file;
    otherwise read from std input.

    """
    MoInterpreter().exec(Path(filename).read_text("utf-8"))
