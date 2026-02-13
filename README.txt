=====================================================
PROJECT: EMOTION-REACTION ENGINE – WEEK 2
=====================================================

This project extends the Week 1 emotion–reaction engine into a
multi-turn dialogue system with an internal state machine.

-----------------------------------------------------
1. FILES AND OVERVIEW
-----------------------------------------------------

* main.py
  - Entry point of the program.
  - Reads one JSON object per line from standard input (STDIN).
  - Maintains the dialogue state: START, SUPPORT, DEESCALATE, END.
  - For each input line, calls the core reaction logic, updates the state,
    enforces message constraints, then prints exactly one JSON object.

* program.py
  - Contains the core function:
        react(emotion, confidence) -> (action, message)
  - Implements the full emotion × confidence → action mapping.
  - Normalizes inputs to lowercase to accept values like "ANGER" or "High".
  - Returns one of the allowed actions:
        continue, slow_down, ask_clarification,
        offer_support, de_escalate, suggest_pause

* dialogue_example.jsonl
  - Sample test file with many dialogue turns.
  - Each line is a JSON object containing:
        "user_text", "emotion", "confidence"
  - Covers all emotions, all confidence levels, and several invalid cases
    to demonstrate error handling.

-----------------------------------------------------
2. HOW TO RUN (INTERACTIVE MODE)
-----------------------------------------------------

Open a terminal (PowerShell) in the project directory:

    cd C:\Users\merie\IdeaProjects\EmotionEngine

Run the dialogue engine:

    py main.py

Then type JSON objects line by line. Each line must be a valid JSON object
with the following fields:

    "user_text"   (string)
    "emotion"     (string, one of: joy, sadness, anger, fear, disgust, surprise)
    "confidence"  (string, one of: low, medium, high)

Example input (you type this, then press Enter):

    {"user_text":"I failed again.","emotion":"sadness","confidence":"high"}

Example output (printed by the program):

    {"action": "offer_support", "message": "I'm here for you. How can I help?", "next_state": "SUPPORT"}

You can keep entering new JSON lines. The internal state is preserved
from one line to the next. To finish, press:

    Ctrl+Z then Enter   (on Windows)

-----------------------------------------------------
3. HOW TO RUN WITH THE EXAMPLE FILE
-----------------------------------------------------

Instead of typing everything by hand, you can use the provided
dialogue_example.jsonl file as input:

    cd C:\Users\merie\IdeaProjects\EmotionEngine
    type dialogue_example.jsonl | py main.py

The program will:
  - read each JSON line from dialogue_example.jsonl,
  - process it through the emotion–reaction logic and state machine,
  - print one JSON object per line on STDOUT.

-----------------------------------------------------
4. CORE LOGIC: REACT(emotion, confidence)
-----------------------------------------------------

The function react(emotion, confidence) (in program.py) performs:

  1) Normalization:
     - emotion  = emotion.lower()
     - confidence = confidence.lower()

  2) Validation:
     - Allowed emotions:
           joy, sadness, anger, fear, disgust, surprise
     - Allowed confidence levels:
           low, medium, high
     - If either is invalid, the function returns:
           action  = "ask_clarification"
           message = non-empty clarification message.

  3) Mapping:
     - Uses a predefined dictionary to map (emotion, confidence)
       to one of the allowed actions.

  4) Message:
     - Chooses a human-readable message based on the action.

The mapping and messages are centralized in program.py so that
the same logic can be reused in other contexts if needed.

-----------------------------------------------------
5. DIALOGUE STATE MACHINE
-----------------------------------------------------

The internal state is one of:

  START, SUPPORT, DEESCALATE, END

Initial state:
  - state = START

After computing the action for a given turn, the next state is:

  - if action == "offer_support"  -> next_state = SUPPORT
  - if action == "de_escalate"    -> next_state = DEESCALATE
  - if action == "suggest_pause"  -> next_state = END
  - otherwise                     -> next_state = current_state

Once the state becomes END, it stays END for all following turns.
The value of next_state is included in every output JSON object.

Example of a typical progression:
  - User expresses sadness with high confidence -> offer_support -> SUPPORT
  - User continues with anger, medium -> slow_down -> SUPPORT
  - User escalates to anger, high -> de_escalate -> DEESCALATE

-----------------------------------------------------
6. MESSAGE CONSTRAINTS AND ROBUSTNESS
-----------------------------------------------------

The program enforces several constraints on the output messages
to make them easy to test automatically:

  - Every message is a non-empty string.

  - If next_state == SUPPORT:
        the message contains (case-insensitive) at least one of:
            "help", "support", or "here"

  - If next_state == DEESCALATE:
        the message contains (case-insensitive) at least one of:
            "calm", "pause", or "slow"

If the core reaction logic ever returns an empty or missing message,
the program fixes it before printing the final JSON.

If a line of input is not valid JSON, the program answers with:

  action  = "ask_clarification"
  message = error message explaining that the input is invalid JSON.

-----------------------------------------------------
7. DEPENDENCIES
-----------------------------------------------------

The project only uses Python standard libraries:

  - sys
  - json


