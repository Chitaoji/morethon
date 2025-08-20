"""Execute uquant."""

import argparse
from pathlib import Path

from .grammer import UqParser


class StartAction(argparse.Action):
    """Start Action."""

    def __call__(self, *args): ...


parser = argparse.ArgumentParser(description="uquant")
parser.add_argument("file", nargs="?", help="read from script file")
parser.add_argument(".", nargs=0, action=StartAction, help="read from std input")

namespace = vars(parser.parse_args())
if namespace["file"]:
    UqParser().parse_code(Path(namespace["file"]).read_text("utf-8"))
else:
    print("not implemented yet")
