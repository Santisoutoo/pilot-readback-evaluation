"""Deterministic pre-checks for the readback judge — run OUTSIDE the model.

Everything that can be verified structurally (the callsign matches, the readback
contains the mandatory elements in a valid shape) is checked here, in the ADK
`before_agent_callback`, NOT by the LLM. The model is left to judge only the
qualitative aspects (phraseology, completeness).

The ADK contract: `before_agent_callback(callback_context) -> Optional[Content]`.
Returning `Content` would SKIP the model run and return that content directly —
that is how a structurally-invalid readback can later be short-circuited without
spending a model call. For now these are stubs (`pass`); the logic will port the
phonetic extractors from AIrport's validate_agents.py into pilot_eval/extractors.py.
"""

from __future__ import annotations

from google.adk.agents.callback_context import CallbackContext


def check_callsign(callback_context: CallbackContext) -> None:
    """Verify the readback's callsign matches the controller's callsign.

    Planned: extract the callsign from the controller instruction and from the
    pilot readback, compare them, and record the result in
    callback_context.state['verified_facts']['callsign'].
    """
    pass


def check_structure(callback_context: CallbackContext) -> None:
    """Verify the readback's structure is correct for the phase (DEL/GND/TWR).

    Planned: confirm the mandatory elements for the phase are present and in a
    valid order/shape (e.g. DEL: SID, altitude, squawk, QNH, runway, callsign
    last), and record per-element results in
    callback_context.state['verified_facts']['structure'].
    """
    pass


def before_judge(callback_context: CallbackContext) -> None:
    """Run the deterministic pre-checks before the model judges the turn.

    Orchestrates the structural checks (callsign + structure) and, once
    implemented, writes their results to callback_context.state['verified_facts']
    so the judge prompt can treat them as ground truth and TurnEvaluation can
    echo them back. Returns None for now (does not short-circuit the model).
    """
    check_callsign(callback_context)
    check_structure(callback_context)
