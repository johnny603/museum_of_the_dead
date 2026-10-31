"""
Exhibit — Template Method (p.325) base class.

Concrete exhibits override describe() and perform().
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from rich.console import Console

from llm_engine import LocalModel


class Exhibit(ABC):
    name: str = "Untitled Exhibit"

    def __init__(self, model: LocalModel, console: Console) -> None:
        self.model = model
        self.console = console

    @abstractmethod
    def describe(self) -> None:  # primitive operation
        ...

    @abstractmethod
    def perform(self) -> None:  # primitive operation
        ...
