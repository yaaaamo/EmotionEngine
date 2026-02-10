Emotion-Reaction Engine
========================

Authors: Yagmur AYDEMIR, Meriem BACHI

================================================================================
PROGRAMMING LANGUAGE
================================================================================
Python 3

================================================================================
COMPILATION STEPS
================================================================================
None required (Python is an interpreted language)


================================================================================
USAGE
================================================================================

   With a JSON file:
   python3 program.py < input.json


================================================================================
INPUT FORMAT
================================================================================

Single input:
    {"emotion":"<emotion>","confidence":"<confidence>"}

Multiple inputs (array):
    [
        {"emotion":"<emotion1>","confidence":"<confidence1>"},
        {"emotion":"<emotion2>","confidence":"<confidence2>"}
    ]

Valid emotions:
    joy, sadness, anger, fear, disgust, surprise

Valid confidence levels:
    low, medium, high

================================================================================
OUTPUT FORMAT
================================================================================

Single input:
    {"action":"<action>","message":"<message>"}

Multiple inputs:
    [
        {"action":"<action1>","message":"<message1>"},
        {"action":"<action2>","message":"<message2>"}
    ]

Possible actions:
    continue, slow_down, ask_clarification, offer_support, de_escalate

================================================================================
REACTION MAPPING
================================================================================

Emotion     | Low               | Medium        | High
------------|-------------------|---------------|----------------
joy         | ask_clarification | continue      | continue
sadness     | ask_clarification | offer_support | offer_support
anger       | ask_clarification | slow_down     | de_escalate
fear        | ask_clarification | slow_down     | offer_support
disgust     | ask_clarification | slow_down     | de_escalate
surprise    | ask_clarification | continue      | continue

================================================================================
INVALID INPUT HANDLING
================================================================================

If emotion or confidence is not in the allowed list, the program returns:
    {"action":"ask_clarification","message":"Invalid input provided. Could you please clarify?"}

If the JSON format is invalid, the program returns:
    {"action":"ask_clarification","message":"Invalid JSON format. Could you please provide valid input?"}

================================================================================
EXAMPLES
================================================================================

Example 1 - Single input:
    Input:  {"emotion":"anger","confidence":"high"}
    Output: {"action":"de_escalate","message":"Let's pause and try to lower the tension."}

Example 2 - Multiple inputs:
    Input:  [{"emotion":"joy","confidence":"medium"},{"emotion":"fear","confidence":"low"}]
    Output: [{"action":"continue","message":"Everything seems fine, let's keep going."},{"action":"ask_clarification","message":"I'm not quite sure I understand. Could you clarify?"}]

Example 3 - Invalid input:
    Input:  {"emotion":"happy","confidence":"high"}
    Output: {"action":"ask_clarification","message":"Invalid input provided. Could you please clarify?"}
