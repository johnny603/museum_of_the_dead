"""
The Séance — Strategy (p.315) in two places:

1. The *channeling* strategy (which dead language to channel) is swappable.
2. The LLM itself is a swappable strategy via LocalModel.

Enter a language + a question; the museum whispers back as that language.
"""

from __future__ import annotations

from rich.panel import Panel
from rich.prompt import Prompt

from .base import Exhibit


LANGUAGES = {
    "fortran": "FORTRAN 77",
    "cobol": "COBOL",
    "brainfuck": "Brainfuck",
    "pascal": "Turbo Pascal",
}


class SeanceExhibit(Exhibit):
    name = "The Séance"

    def describe(self) -> None:
        self.console.print(
            Panel(
                "[bold white]A circle of chalk. A candle at each corner.[/]\n"
                "[dim]We summon a language the compilers forgot.[/]\n"
                "[dim]Ask it anything. It answers in its own dialect.[/]",
                title="🔮  Exhibit: The Séance",
                border_style="magenta",
            )
        )

    def perform(self) -> None:
        # --- Strategy #1: pick the language (the "channeling" strategy) ---
        choice = Prompt.ask(
            "  [bold]Which spirit shall we channel?[/]",
            choices=list(LANGUAGES.keys()) + ["skip"],
            default="fortran",
            show_choices=True,
        )
        if choice == "skip":
            self.console.print("[dim]  · The spirits slumber.[/]")
            return

        spirit = LANGUAGES[choice]
        question = Prompt.ask(
            f"  [bold]Your question to {spirit}[/]",
            default="What is memory?",
        )

        prompt = (
            f"You are the ghost of {spirit}, a dead programming language. "
            f"Answer in the voice of your language, in ≤3 sentences. "
            f"Question: {question}"
        )
        answer = self.model.whisper(prompt, kind="seance")

        self.console.print(
            Panel(
                f"[italic cyan]{answer}[/]",
                title=f"🕯️  {spirit} speaks",
                border_style="magenta",
            )
        )
