"""
The Ofrenda — Memento (p.283).

Each ofrenda remembers a dead open-source project.
Mementos capture: name, last commit, cause of death.
"""

from __future__ import annotations

from dataclasses import dataclass

from rich.panel import Panel
from rich.table import Table

from .base import Exhibit


@dataclass(frozen=True)
class RepoMemento:
    """A snapshot of a dead project. Immutable — like a photograph."""
    name: str
    last_commit: str
    cause_of_death: str


class OfrendaExhibit(Exhibit):
    name = "The Ofrenda"

    # The memorial shelf — you can add more mementos anytime.
    MEMENTOS: list[RepoMemento] = [
        RepoMemento(
            "youtube-dl",
            "2021-06-06",
            "Ripped from the internet like a ghost from a shell.",
        ),
        RepoMemento(
            "Fabric",
            "2021-04-14",
            "Deprecated by its author; survived as a fork named 'invoke'.",
        ),
        RepoMemento(
            "AngularJS",
            "2022-01-01",
            "End-of-life. Survived by tourists in old StackOverflow answers.",
        ),
    ]

    def describe(self) -> None:
        self.console.print(
            Panel(
                "[bold white]An ofrenda, lit by marigolds and candlelight.[/]\n"
                "[dim]Each photo is a project that once lived.[/]",
                title="🕯️  Exhibit: The Ofrenda",
                border_style="yellow",
            )
        )

    def perform(self) -> None:
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("Project")
        table.add_column("Last commit")
        table.add_column("Cause of death", max_width=48)
        for m in self.MEMENTOS:
            table.add_row(m.name, m.last_commit, m.cause_of_death)
        self.console.print(table)

        for m in self.MEMENTOS:
            whisper = self.model.whisper(
                f"Write a one-line remembrance for the open-source project "
                f"{m.name}, whose last commit was {m.last_commit}. "
                f"Account of its passing: {m.cause_of_death}.",
                kind="ofrenda",
            )
            self.console.print(
                f"  [bold]{m.name}[/] — [italic magenta]{whisper}[/]"
            )
