"""
Curator — the museum guide.

Facade (p.185): unifies all exhibits behind a single visit() call.
Builder (p.97) : the tour is assembled step-by-step in __init__.
Iterator (p.257): the visit loop iterates exhibits sequentially.
"""

from __future__ import annotations

from rich.console import Console
from rich.panel import Panel

from exhibits.zombie_exhibit import ZombieExhibit
from exhibits.daemon_exhibit import DaemonExhibit
from exhibits.ofrenda_exhibit import OfrendaExhibit
from exhibits.seance_exhibit import SeanceExhibit
from llm_engine import LocalModel


class Curator:
    def __init__(self, model: LocalModel, console: Console) -> None:
        self.model = model
        self.console = console

        # --- Builder: assemble the tour step-by-step ---
        self.exhibits = [
            OfrendaExhibit(model, console),
            ZombieExhibit(model, console),
            DaemonExhibit(model, console),
            SeanceExhibit(model, console),
        ]

    def visit(self) -> None:
        self.console.print(
            Panel.fit(
                "[bold yellow]The Curator welcomes you.[/]\n"
                "Walk slowly. Listen. The machine remembers.",
                border_style="yellow",
            )
        )

        for i, exhibit in enumerate(self.exhibits, start=1):
            self.console.rule(
                f"[bold cyan]Exhibit {i} of {len(self.exhibits)} — {exhibit.name}[/]"
            )
            exhibit.describe()
            exhibit.perform()
            self.console.print()

        self.console.print(
            Panel.fit(
                "[bold green]You exit the museum. The dead rest again.[/]\n"
                "[dim italic]Their stories are yours now.[/]",
                border_style="green",
            )
        )
