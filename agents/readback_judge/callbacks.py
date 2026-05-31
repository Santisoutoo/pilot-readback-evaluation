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
