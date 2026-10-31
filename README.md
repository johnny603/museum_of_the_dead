# 🕯️ Museum of the Dead

> *A memorial for the ghosts in the machine — built with open-weight AI, offline.*

The **Museum of the Dead** is a terminal-based museum of Unix spirits. Each exhibit is a real running process — a zombie, a daemon, a memorial — narrated in real time by a locally-running open-weight language model. No internet. No API keys. Your data never leaves your machine.

Built for the [Hacktoberfest Open-Source AI Challenge: Week 4 — Ghost in the Machine](https://dev.to/).

## Why open innovation matters

- **Runs with the lights off.** The museum works with `--offline`. A museum that requires an internet connection isn't a memorial — it's a subscription.
- **Data stays home.** Family stories, project epitaphs, and whispered eulogies never touch a server you don't control.
- **Models are swappable.** Phi-3, TinyLlama, Qwen — pick whichever ghost you trust. The `LocalModel` strategy makes swapping a one-liner.
- **Costs nothing to run.** No token bills at a funeral.

## Design Patterns used (Gamma et al., 1994)

| Pattern | Book page | Where |
|---|---|---|
| **Facade** | 185 | `curator.py` — one `visit()` over four exhibits |
| **Builder** | 97 | `curator.py` — tour is assembled step-by-step |
| **Iterator** | 257 | `curator.py` — `for exhibit in self.exhibits` |
| **Observer** | 293 | `zombie_exhibit.py` — parent waits on child exit |
| **Singleton** | 127 | `daemon_exhibit.py` — one Watcher per system |
| **Memento** | 283 | `ofrenda_exhibit.py` — snapshots of dead repos |
| **Strategy** | 315 | `llm_engine.py` + `seance_exhibit.py` — swap models & channeling styles |
| **Template Method** | 325 | `Exhibit.describe()` base hook |

## Exhibits

1. **🕯️ The Ofrenda** — a memorial for dead open-source projects. Provide a name, last commit, and cause of death; the local model writes a remembrance.
2. **🧟 The Zombie** — a real Unix zombie is created, observed, and reaped on screen.
3. **👁️ The Watcher** — a forked daemon that outlives its parent; the model eulogizes it.
4. **🔮 The Séance** — a chatbot that channels a long-dead programming language (choose from FORTRAN 77, COBOL, Brainfuck, Turbo Pascal).

## Stack

- Python 3.11+
- [`rich`](https://github.com/Textualize/rich) — terminal rendering
- [`llama-cpp-python`](https://github.com/abetlen/llama-cpp-python) *or* [`ollama`](https://ollama.com/) — local open-weight inference
- `os`, `multiprocessing`, `dataclasses` — stdlib only

## Install & Run

```bash
git clone https://github.com/johnny603/museum_of_the_dead.git
cd museum_of_the_dead

# pick ONE:
pip install llama-cpp-python rich
#   OR
ollama pull phi3:mini && pip install ollama rich

python main.py            # full museum (with LLM)
python main.py --offline  # no model required — canned whispers
