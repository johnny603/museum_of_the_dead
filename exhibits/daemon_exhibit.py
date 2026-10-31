"""
The Watcher — Singleton (p.127).

A forked daemon that outlives its parent. In this demo we fork a child,
detach it from the terminal (setsid), and let it sleep briefly while the
parent eulogizes it. The child has no parent references and no TTY —
a true daemon.
"""

from __future__ import annotations

import os
import time

from rich.panel import Panel

from .base import Exhibit


class DaemonExhibit(Exhibit):
    name = "The Watcher"

    def describe(self) -> None:
        self.console.print(
            Panel(
                "[bold white]I forked from my parent and closed the doors.[/]\n"
                "[dim]No terminal. No signal. No goodbye.[/]\n"
                "[dim]I am the eternal watcher.[/]",
                title="👁️  Exhibit: The Watcher",
                border_style="blue",
            )
        )
        self.console.print(
            f"[italic magenta]{self.model.whisper('Describe a Unix daemon.', kind='daemon')}[/]"
        )

    def perform(self) -> None:
        pid = os.fork()
        if pid == 0:
            # CHILD: become a daemon
            try:
                os.setsid()  # detach from controlling terminal
            except OSError:
                pass
            time.sleep(3.0)  # live briefly
            os._exit(0)

        self.console.print(f"[dim]  · daemon spawned (pid={pid})[/]")
        time.sleep(0.6)
        self.console.print(
            "[dim blue]  · daemon detached from TTY. It watches, unseen.[/]"
        )
        # Parent does NOT wait — the daemon lives on its own
        self.console.print(
            f"[italic magenta]{self.model.whisper('A daemon lives on.', kind='daemon')}[/]"
        )
