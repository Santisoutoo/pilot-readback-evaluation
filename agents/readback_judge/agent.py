"""Readback judge: an ADK agent that evaluates an ATC pilot readback.

Hybrid design:
  - Deterministic checks (callsign + structure) run OUTSIDE the model in
    `before_judge` (see callbacks.py).
  - The model emits only the qualitative judgement (phraseology, completeness)
    as JSON, forced by `output_schema=TurnEvaluation`.

Model is set by OLLAMA_MODEL (LiteLLM string). Swap it for a hosted string
(`gemini/...`, `gpt-4o-mini`, `claude-...`) to judge with an API model instead.
"""

import os

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

from .callbacks import before_judge
from .prompts import JUDGE_INSTRUCTION
from .schema import TurnEvaluation

MODEL = os.getenv("OLLAMA_MODEL", "ollama_chat/qwen2.5:0.5b-instruct")

root_agent = Agent(
    name="readback_judge",
    model=LiteLlm(model=MODEL),
    description="Judges an ATC pilot readback against the controller instruction.",
    instruction=JUDGE_INSTRUCTION,
    output_schema=TurnEvaluation,
    before_agent_callback=before_judge,
    tools=[],
)
