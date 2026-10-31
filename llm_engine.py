"""
LocalModel — Strategy (p.315) for swapping open-weight LLMs.

Tries, in order:
  1. llama-cpp-python (local .gguf file in ~/.cache/museum_of_the_dead/)
  2. ollama (if the daemon is running)
  3. canned offline fallback (deterministic, no deps)

The point: no internet required for the fallback path. Truly offline.
"""

from __future__ import annotations

import hashlib
import os
from pathlib import Path
from typing import Optional


CANNED = {
    "zombie": (
        "I was a child process once. My parent forgot to wait() for me. "
        "I stand here, hollow, until someone reaps my exit status."
    ),
    "daemon": (
        "I forked away from my parent and closed the doors behind me. "
        "No terminal, no signal, no goodbye. I am the eternal watcher."
    ),
    "ofrenda": (
        "A project's last commit is not its death. Its README is not its eulogy. "
        "As long as someone still remembers it, it walks."
    ),
    "seance": (
        "I speak in a language that compilers forgot. Ask, and I will answer "
        "in dialects that only make sense to machines."
    ),
}


class LocalModel:
    def __init__(self, model_name: str = "phi-3-mini", offline: bool = False) -> None:
        self.model_name = model_name
        self.offline = offline
        self._impl = None

        if not offline:
            self._impl = self._try_llama_cpp() or self._try_ollama()
            if self._impl is None:
                # graceful fallback
                self.offline = True

    # --- backend probing ------------------------------------------------
    def _try_llama_cpp(self) -> Optional[object]:
        try:
            from llama_cpp import Llama  # type: ignore

            cache = Path.home() / ".cache" / "museum_of_the_dead"
            cache.mkdir(parents=True, exist_ok=True)
            for f in cache.glob("*.gguf"):
                return Llama(model_path=str(f), n_ctx=1024, verbose=False)
            return None
        except Exception:
            return None

    def _try_ollama(self) -> Optional[object]:
        try:
            import ollama  # type: ignore

            ollama.list()  # probes daemon
            return ollama
        except Exception:
            return None

    # --- public API -----------------------------------------------------
    def whisper(self, prompt: str, kind: str = "ofrenda") -> str:
        if self._impl is not None:
            try:
                if hasattr(self._impl, "chat"):
                    resp = self._impl.chat(
                        model=self.model_name,
                        messages=[{"role": "user", "content": prompt}],
                    )
                    return resp["message"]["content"].strip()
                out = self._impl(
                    prompt, max_tokens=80, temperature=0.8, echo=False
                )
                return out["choices"][0]["text"].strip()
            except Exception:
                pass  # fall through to canned

        # Offline / canned fallback — deterministic, themed
        seed = int(hashlib.sha1(prompt.encode()).hexdigest(), 16)
        return CANNED.get(kind, CANNED["ofrenda"]) + f"  (whisper #{seed % 1000:03d})"
