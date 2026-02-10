=====================================================
PROJECT: EMOTION-REACTION ENGINE
=====================================================

1. TECHNICAL INFORMATION
------------------------
* Programming Language: Python 3.10+
* Interface: Standard Input/Output (STDIN/STDOUT)
* Data Format: JSON
* Main Script: main.py

2. HOW TO RUN
-------------
To execute the program, use the following command in your terminal:

    py main.py

The program expects a single JSON object as input. For example:
{"emotion": "anger", "confidence": "high"}

3. FEATURES & ROBUSTNESS
------------------------
* Full Mapping: Implements the complete emotion x confidence matrix as specified.
* Case Insensitivity: Handles inputs like "ANGER" or "High" automatically.
* Input Validation:
    - If the emotion or confidence level is not in the allowed list, returns 'ask_clarification'.
    - If a JSON key is missing (e.g., only emotion provided), returns 'ask_clarification'.
* Error Handling:
    - If the input is not a valid JSON format, the program gracefully returns a JSON response with the 'ask_clarification' action instead of crashing.

4. DEPENDENCIES
---------------
* None (uses only Python standard libraries: sys, json).