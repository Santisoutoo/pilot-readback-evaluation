import os

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

MODEL = os.getenv("OLLAMA_MODEL", "ollama_chat/qwen2.5:0.5b-instruct")

INSTRUCTION = (
    "You are a test assistant for an ATC pilot-readback evaluation project. "
    "Answer briefly in standard ICAO English. If asked to read back a clearance, "
    "produce a concise, correct pilot readback."
)

root_agent = Agent(
    name="ollama_smoke",
    model=LiteLlm(model=MODEL),
    description="Smoke test: ADK agent talking to a local Ollama model via LiteLLM.",
    instruction=INSTRUCTION,
    tools=[],
)
