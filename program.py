#!/usr/bin/env python3
"""
Emotion-Reaction Engine
Maps emotion × confidence → action + message
"""

import sys
import json

# Allowed values
ALLOWED_EMOTIONS = {"joy", "sadness", "anger", "fear", "disgust", "surprise"}
ALLOWED_CONFIDENCES = {"low", "medium", "high"}

# Reaction mapping: emotion -> {confidence -> action}
REACTION_MAP = {
    "joy": {
        "low": "ask_clarification",
        "medium": "continue",
        "high": "continue"
    },
    "sadness": {
        "low": "ask_clarification",
        "medium": "offer_support",
        "high": "offer_support"
    },
    "anger": {
        "low": "ask_clarification",
        "medium": "slow_down",
        "high": "de_escalate"
    },
    "fear": {
        "low": "ask_clarification",
        "medium": "slow_down",
        "high": "offer_support"
    },
    "disgust": {
        "low": "ask_clarification",
        "medium": "slow_down",
        "high": "de_escalate"
    },
    "surprise": {
        "low": "ask_clarification",
        "medium": "continue",
        "high": "continue"
    }
}

# Messages for each action
ACTION_MESSAGES = {
    "continue": "Everything seems fine, let's keep going.",
    "slow_down": "Let's take a moment to process this calmly.",
    "ask_clarification": "I'm not quite sure I understand. Could you clarify?",
    "offer_support": "I'm here for you. How can I help?",
    "de_escalate": "Let's pause and try to lower the tension.",
    "suggest_pause": "Perhaps we should take a short break."
}


def react(emotion, confidence):
    """
    Determine the appropriate action and message based on emotion and confidence.
    
    Args:
        emotion: The detected emotion
        confidence: The confidence level of the detection
    
    Returns:
        tuple: (action, message)
    """
    # Validate inputs
    if emotion not in ALLOWED_EMOTIONS or confidence not in ALLOWED_CONFIDENCES:
        return "ask_clarification", "Invalid input provided. Could you please clarify?"
    
    # Get action from mapping
    action = REACTION_MAP[emotion][confidence]
    message = ACTION_MESSAGES[action]
    
    return action, message


def process_single(data):
    """Process a single emotion/confidence pair and return the output dict."""
    emotion = data.get("emotion", "")
    confidence = data.get("confidence", "")
    action, message = react(emotion, confidence)
    return {
        "action": action,
        "message": message
    }


def main():
    """Main function to read JSON from stdin and output reaction as JSON."""
    try:
        # Read input from stdin
        input_data = sys.stdin.read().strip()
        
        # Parse JSON
        data = json.loads(input_data)
        
        # Check if input is a list (multiple tests) or single object
        if isinstance(data, list):
            # Process each item in the array
            outputs = [process_single(item) for item in data]
            print(json.dumps(outputs))
        else:
            # Single object
            output = process_single(data)
            print(json.dumps(output))
        
    except json.JSONDecodeError:
        # Handle invalid JSON input
        output = {
            "action": "ask_clarification",
            "message": "Invalid JSON format. Could you please provide valid input?"
        }
        print(json.dumps(output))
    except Exception:
        # Handle any other errors
        output = {
            "action": "ask_clarification",
            "message": "An error occurred. Could you please clarify your input?"
        }
        print(json.dumps(output))


if __name__ == "__main__":
    main()