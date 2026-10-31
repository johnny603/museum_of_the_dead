"""
Museum of the Dead — entry point.

The Curator (Facade pattern, p.185) hides everything behind visit().
"""

from __future__ import annotations

import argparse
import sys

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from curator import Curator
from llm_engine import LocalModel


BANNER = r"""
   __  ___           __                __   ____         __     _
  /  |/  /_ __ ___  / /_  ____  __ __ / /_ / __/__  ___ / /_   (_)__  ___
 / /|_/ / // (_-< / __/ / __/ / // // __// _// _ \/ -_) __/  / / _ \/ _ \
/_/  /_/\_,_/___/ \__/  \___/ \_,_/ \__//_/  \___/\__/\__/  /_/\___/_//_/
"""


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Museum of the Dead")
    p.add_argument(
        "--model",
        default="phi-3-mini",
        help="Local open-weight model to load (default: phi-3-mini)",
    )
    p.add_argument(
        "--offline",
        action="store_true",
        help="Run without an LLM (canned whispers — for demos & CI)",
    )
    return p.parse_args()


def main() -> int:
    args = parse_args()
    console = Console()

    console.print(Text(BANNER, style="bold magenta"))
    console.print(
        Panel.fit(
            "[bold white]A memorial for the ghosts in the machine.[/]\n"
            "[dim italic]Open-weight AI. Offline. Yours.[/]",
            border_style="magenta",
        )
    )

    model = LocalModel(args.model, offline=args.offline)
    console.print(
        f"[dim]Model:[/] [cyan]{model.model_name}[/]"
        f"  [dim]Offline:[/] [cyan]{args.offline}[/]\n"
    )

    museum = Curator(model, console)
    museum.visit()
    return 0


if __name__ == "__main__":
    sys.exit(main())
