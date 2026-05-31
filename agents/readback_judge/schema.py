"""Structured output schema for the readback judge.

`TurnEvaluation` is wired as the ADK agent's `output_schema`, so the model is
forced to return JSON matching this shape. `verified_facts` echoes what the
deterministic layer (the before_agent_callback) checked outside the model —
callsign and structure — so the LLM's qualitative judgement and the
deterministic facts travel together in one object.
"""

from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, Field


class Finding(BaseModel):
    """A single observation about one element of the readback."""

    element: str = Field(description="Element judged, e.g. 'callsign', 'squawk', 'phraseology'.")
    expected: Optional[str] = Field(default=None, description="Expected value, if applicable.")
    got: Optional[str] = Field(default=None, description="Value found in the readback, if applicable.")
    verdict: Literal["good", "bad"] = Field(description="Whether this element was correct.")
    note: str = Field(description="One short sentence explaining the verdict.")


class CategoryScore(BaseModel):
    """Score for one qualitative category judged by the model."""

    name: Literal["phraseology", "completeness"]
    score: int = Field(ge=0, le=10, description="0-10 integer score for this category.")
    summary: str = Field(description="1-2 sentence justification.")


class TurnEvaluation(BaseModel):
    """Full evaluation of one controller-instruction / pilot-readback turn."""

    verdict: Literal["correct", "partial", "incorrect"]
    overall_score: int = Field(ge=0, le=100, description="0-100 integer overall score.")
    categories: list[CategoryScore] = Field(
        description="Qualitative category scores (phraseology, completeness)."
    )
    error_tags: list[str] = Field(
        default_factory=list,
        description="Machine-readable error tags, e.g. 'missing_callsign', 'wrong_squawk'.",
    )
    findings: list[Finding] = Field(
        default_factory=list, description="Per-element findings supporting the verdict."
    )
    verified_facts: dict = Field(
        default_factory=dict,
        description="Echo of the deterministic checks (callsign, structure) done outside the model.",
    )
