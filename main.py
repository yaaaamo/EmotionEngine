#!/usr/bin/env python3
"""
Emotion–Reaction Engine: Dialogue Extension (Week 2)

Reads multiple JSON objects from STDIN (one per line),
and for each line outputs one JSON object with:
  - action
  - message
  - next_state

It wraps the Week 1 react(emotion, confidence) core logic from program.py
inside a multi-turn dialogue loop with an internal state machine.
"""

import sys
import json

from program import react


def update_state(current_state: str, action: str) -> str:
    """
    Update dialogue state according to the specification.

    States: START, SUPPORT, DEESCALATE, END
    Rules (deterministic):
      - if action == offer_support  -> next_state = SUPPORT
      - if action == de_escalate    -> next_state = DEESCALATE
      - if action == suggest_pause  -> next_state = END
      - otherwise                   -> next_state = current_state
      - if current_state == END     -> stays END for all following turns
    """
    if current_state == "END":
        return "END"

    if action == "offer_support":
        return "SUPPORT"
    if action == "de_escalate":
        return "DEESCALATE"
    if action == "suggest_pause":
        return "END"

    return current_state


def ensure_message_constraints(message: str, next_state: str) -> str:
    """
    Enforce the message constraints required in the assignment.

    - message must be non-empty
    - If next_state == SUPPORT, message must contain (case-insensitive)
      at least one of: help, support, here
    - If next_state == DEESCALATE, message must contain (case-insensitive)
      at least one of: calm, pause, slow
    """
    if not isinstance(message, str) or not message.strip():
        message = "I am here to support you."

    lower_msg = message.lower()

    if next_state == "SUPPORT":
        if not any(k in lower_msg for k in ("help", "support", "here")):
            message = message.rstrip() + " I am here to support you."

    if next_state == "DEESCALATE":
        if not any(k in lower_msg for k in ("calm", "pause", "slow")):
            message = message.rstrip() + " Let's pause and slow down to stay calm."

    return message


def process_line(line: str, current_state: str):
    """Process a single JSON line and return (output_dict, next_state)."""
    line = line.strip()
    if not line:
        # Empty line: no output, state unchanged
        return None, current_state

    try:
        data = json.loads(line)
        emotion = data.get("emotion")
        confidence = data.get("confidence")
        action, message = react(emotion, confidence)
    except Exception:
        # Invalid JSON or unexpected error ⇒ ask_clarification
        action = "ask_clarification"
        message = "Invalid JSON format. Could you please clarify?"

    # Compute next_state according to the rules
    next_state = update_state(current_state, action)

    # If we already were in END, we must stay in END
    if current_state == "END":
        next_state = "END"

    # Enforce message constraints depending on next_state
    message = ensure_message_constraints(message, next_state)

    output = {
        "action": action,
        "message": message,
        "next_state": next_state,
    }
    return output, next_state


def main():
    """
    Main loop: read JSON objects line by line from STDIN and
    print one JSON object per line on STDOUT.
    """
    state = "START"

    for line in sys.stdin:
        output, state = process_line(line, state)
        if output is not None:
            # Output must be valid JSON, no extra text
            print(json.dumps(output))


if __name__ == "__main__":
    main()