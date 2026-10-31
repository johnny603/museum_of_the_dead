
# 🕯️ Museum of the Dead

> *A memorial for the ghosts in the machine — built with open-weight AI, offline.*

The **Museum of the Dead** is a terminal-based museum of Unix spirits. Each exhibit is a real running process — a zombie, a daemon, a memorial — narrated by a locally-running open-weight language model. No internet. No API keys. Your data never leaves your machine.

Built for the [Hacktoberfest Open-Source AI Challenge: Week 4 — Ghost in the Machine](https://dev.to/).

```
   __  ___           __                __   ____         __     _
  /  |/  /_ __ ___  / /_  ____  __ __ / /_ / __/__  ___ / /_   (_)__  ___
 / /|_/ / // (_-< / __/ / __/ / // // __// _// _ \/ -_) __/  / / _ \/ _ \
/_/  /_/\_,_/___/ \__/  \___/ \_,_/ \__//_/  \___/\__/\__/  /_/\___/_//_/
```

## Why open innovation matters

- **Runs with the lights off.** The full tour works with `--offline` — no model, no network, no API. A museum that requires an internet connection isn't a memorial, it's a subscription.
- **Data stays home.** Family stories, project epitaphs, and whispered eulogies never touch a server you don't control.
- **Models are swappable.** Phi-3, TinyLlama, Qwen — pick whichever ghost you trust. The `LocalModel` strategy makes swapping a one-line change.
- **Costs nothing to run.** No token bills at a funeral.

## Design Patterns used (Gamma et al., 1994)

| Pattern | Book page | Where |
|---|---|---|
| **Facade** | 185 | `curator.py` — one `visit()` over four exhibits |
| **Builder** | 97 | `curator.py` — tour is assembled step-by-step |
| **Iterator** | 257 | `curator.py` — `for exhibit in self.exhibits` |
| **Observer** | 293 | `exhibits/zombie_exhibit.py` — parent waits on child exit |
| **Singleton** | 127 | `exhibits/daemon_exhibit.py` — one Watcher per system |
| **Memento** | 283 | `exhibits/ofrenda_exhibit.py` — snapshots of dead repos |
| **Strategy** | 315 | `llm_engine.py` + `exhibits/seance_exhibit.py` — swap models & channeling styles |
| **Template Method** | 325 | `exhibits/base.py` — `Exhibit.describe()` hook |

## Exhibits

1. **🕯️ The Ofrenda** — a memorial for dead open-source projects. Provide a name, last commit, and cause of death; the local model writes a remembrance.
2. **🧟 The Zombie** — a real Unix zombie is created, observed, and reaped on screen (`os.fork()` → `waitpid()`).
3. **👁️ The Watcher** — a forked daemon that outlives its parent (`os.fork()` + `os.setsid()`); the model eulogizes it.
4. **🔮 The Séance** — a chatbot that channels a long-dead programming language (FORTRAN 77, COBOL, Brainfuck, Turbo Pascal).

## Stack

- **Python 3.10+**
- [`rich`](https://github.com/Textualize/rich) — terminal rendering
- [`ollama`](https://ollama.com/) *or* [`llama-cpp-python`](https://github.com/abetlen/llama-cpp-python) — local open-weight inference *(optional — offline mode works without them)*
- `os`, `multiprocessing`, `dataclasses` — stdlib only

## Quickstart

> **Requires Python 3.10+. On macOS use `python3` — the bare `python` command is not installed by default.**

```bash
git clone https://github.com/johnny603/museum_of_the_dead.git
cd museum_of_the_dead

# 1. Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

# 2. Install the only required dependency
pip install rich

# 3. Run the offline museum — no model, no network needed
python main.py --offline
```

You should see the banner, the Curator's welcome, four exhibits, and a closing panel:

```
╭───────────────────────────────────────────╮
│ You exit the museum. The dead rest again. │
│ Their stories are yours now.              │
╰───────────────────────────────────────────╯
```

That's the whole thing. It runs in under a second and needs **zero** network access.

## Optional: run with a real open-weight model

The offline mode uses deterministic canned whispers (great for demos, CI, and screenshots). To let the model actually *speak* on each run, install Ollama and pull a small open-weight model:

```bash
# macOS
brew install ollama
ollama serve &                     # start the daemon
ollama pull phi3:mini              # ~2.2 GB, one-time download

# in the project venv
pip install ollama

# run the museum with the live model
python main.py --model phi3:mini
```

Every ofrenda gets a fresh, personalized eulogy. Every séance gets a real ghost voice. The model runs entirely on your machine — no API key, no outbound traffic.

> **Prefer `llama-cpp-python`?** Drop a `.gguf` file into `~/.cache/museum_of_the_dead/` and `llm_engine.py` will auto-detect it.

## Command reference

```bash
python main.py                        # offline tour (auto-falls-back if no model)
python main.py --offline              # force offline; skip all model probes
python main.py --model phi3:mini      # use a specific Ollama model
python main.py --model qwen2.5:3b     # any Ollama-tagged model works
```

## Project layout

```
museum_of_the_dead/
├── main.py                       # entry point — argparse + banner
├── curator.py                    # Facade (185) + Builder (97) + Iterator (257)
├── llm_engine.py                 # Strategy (315) — swap LLM backends
├── exhibits/
│   ├── __init__.py               # re-exports Exhibit
│   ├── base.py                   # Template Method (325) base class
│   ├── ofrenda_exhibit.py        # Memento (283) — dead-repo snapshots
│   ├── zombie_exhibit.py         # Observer (293) — real fork + waitpid
│   ├── daemon_exhibit.py         # Singleton (127) — real fork + setsid
│   └── seance_exhibit.py         # Strategy (315) — swappable channeling
├── README.md
└── LICENSE
```

## Troubleshooting

| Symptom | Fix |
|---|---|
| `zsh: command not found: python` | Use `python3` — macOS no longer ships the `python` alias. Or activate the venv first. |
| `ModuleNotFoundError: No module named 'rich'` | You forgot to `source .venv/bin/activate` (or `pip install rich`). |
| `ModuleNotFoundError: No module named 'llm_engine'` | Run `python main.py` from the repo root, not from inside `exhibits/`. |
| Séance prompt exits with `EOFError` | `rich.Prompt.ask()` needs a TTY. Run interactively — don't pipe into `tee`/`grep`. |
| Daemon exhibit leaves a stray Python process | That's the point — `os.setsid()` detaches it. It exits within 3 seconds. |
| Zombie exhibit doesn't show `Z` in `ps` | The window is ~200 ms. Run `watch -n 0.1 'ps -o pid,stat,cmd \| grep "[p]ython"'` in a second terminal. |

## License

MIT — see `LICENSE`.

> *"It is possible to make buildings by stringing together patterns, in a rather loose way."* — Christopher Alexander
```
