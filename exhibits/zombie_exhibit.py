"""
The Zombie — Observer (p.293) + real Unix fork/exit demo.

The parent process *observes* the child's exit status via waitpid().
While the child is unreaped, it is a zombie — visible in `ps`.
"""

from __future__ import annotations

import os
import time

from rich.panel import Panel

from .base import Exhibit


class ZombieExhibit(Exhibit):
    name = "The Zombie"

    def describe(self) -> None:
        self.console.print(
            Panel(
                "[bold white]A child is born. The parent forgets to wait().[/]\n"
                "[dim]The child exits, but its exit status is never reaped.[/]\n"
                "[dim]For a little while, the child still walks — a zombie.[/]",
                title="🕯️  Exhibit: The Zombie",
                border_style="red",
            )
        )
        self.console.print(
            f"[italic magenta]{self.model.whisper('Describe a zombie process.', kind='zombie')}[/]"
        )

    def perform(self) -> None:
        pid = os.fork()
        if pid == 0:
            # CHILD: live briefly, then exit — becoming a zombie until reaped
            self.console.print("[dim cyan]  · child process breathing…[/]")
            time.sleep(0.4)
            os._exit(7)  # exit status 7 = "the seventh seal"

        # PARENT: observe the child
        self.console.print(f"[dim]  · parent pid={os.getpid()}, child pid={pid}[/]")
        time.sleep(0.6)
        self.console.print("[dim yellow]  · child is now a zombie (DEFUNCT in ps)…[/]")
        time.sleep(0.6)

        # Reap — the Observer is notified
        _, status = os.waitpid(pid, 0)
        exit_code = os.waitstatus_to_exitcode(status)
        self.console.print(
            f"[bold green]  · parent reaps child (exit={exit_code}). Peace returns.[/]"
        )
        self.console.print(
            f"[italic magenta]{self.model.whisper('The child has been reaped.', kind='zombie')}[/]"
        )
