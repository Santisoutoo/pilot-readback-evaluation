# pilot-readback-evaluation

A judge module that evaluates, response by response, what ATC agents (DEL / GND / TWR)
produce against the [pilot-readback-corpus](https://github.com/Santisoutoo/pilot-readback-corpus).
The judge is **hybrid**: everything structurally verifiable (callsign, identity, squawk, altitude,
runway, SID, QNH, frequencies) is checked **outside the model** with deterministic code, while the
**qualitative judgement** (natural phraseology, semantic completeness) is left **to the model** — a
Google ADK agent backed by LiteLLM, so the underlying model is swappable (`gemini/...`,
`gpt-4o-mini`, `claude-...`, `ollama/...`).

> ⚠️ **Scaffolding only.** This repo currently contains just the folder structure; the modules below
> are placeholders (`.gitkeep`) to be filled in the next phases.

## Planned layout

```
pilot-readback-evaluation/
├── corpus/                      # git submodule -> Santisoutoo/pilot-readback-corpus
├── pilot_eval/
│   ├── schema.py                # Pydantic Turn, TurnEvaluation, Finding + score composition
│   ├── rubric.py                # per-turn ICAO rubric / prompt builder
│   ├── corpus.py                # load corpus/DEL|GND|TWR/*.jsonl -> list[Turn]
│   ├── extractors.py            # deterministic phonetic decoders (squawk, runway, SID, ...)
│   ├── features.py              # deterministic layer: verified_facts per turn
│   ├── judges/
│   │   ├── base.py              # BaseJudge.evaluate(turn) -> TurnEvaluation
│   │   ├── adk_judge.py         # ADK Agent(model=LiteLlm(...), output_schema=TurnEvaluation)
│   │   └── deterministic_judge.py  # LLM-free baseline (verified_facts only)
│   ├── data_gen/
│   │   ├── perturb.py           # corrupt gold readbacks -> labelled turns (deterministic label)
│   │   └── distill.py           # label pairs with a strong judge (distillation)
│   ├── train/
│   │   ├── build_dataset.py     # SFT JSONL: (rubric + turn + verified_facts) -> evaluation JSON
│   │   ├── train_lora.py        # TRL SFTTrainer + PEFT QLoRA, model-parameterised (cloud)
│   │   └── config.example.yaml
│   ├── run_judge.py             # CLI: run a judge over a set -> output/*.jsonl + *.csv
│   └── evaluate_judge.py        # meta-eval: judge vs deterministic agreement; compare judges
├── output/                      # results (gitignored)
└── tests/
```

## Quickstart: the readback judge

The judge agent under `agents/readback_judge/` evaluates a controller instruction + pilot readback
and returns a structured `TurnEvaluation` (JSON). Deterministic checks (callsign, structure) run in
its `before_agent_callback`, outside the model; the model judges phraseology and completeness. It
loads in the ADK web UI.

```powershell
# 1. Environment (Python 3.11 via uv)
python -m pip install uv
uv sync

# 2. Pull a model into the running Ollama daemon
ollama pull qwen2.5:0.5b-instruct

# 3. Launch the ADK web UI from the repo root; it discovers agents/readback_judge
uv run adk web agents
#   open http://localhost:8000, select "readback_judge", paste a CONTROLLER + READBACK pair
```

One-shot CLI alternative (no UI): `uv run adk run agents/readback_judge`

The model is set by `OLLAMA_MODEL` in `agents/readback_judge/.env` (copy from `.env.example`). Swap
it for a hosted string (`gemini/...`, `gpt-4o-mini`, `claude-...`) to judge with an API model.

The model is set by `OLLAMA_MODEL` in `agents/ollama_smoke/.env` (copy from `.env.example`).
Swap it for a hosted string (`gemini/...`, `gpt-4o-mini`, `claude-...`) to talk to an API model
through the same agent.

## Corpus submodule

The corpus is consumed as a git submodule under `corpus/`:

```bash
git submodule update --init --recursive      # first checkout
git submodule update --remote                 # pull corpus updates as it grows
```

## Configuration

Copy `.env.example` to `.env` and set `JUDGE_MODEL` plus the matching provider key.
