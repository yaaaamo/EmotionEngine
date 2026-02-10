import sys
import json

def react(emotion, confidence):
    emo = emotion.lower() if isinstance(emotion, str) else None
    conf = confidence.lower() if isinstance(confidence, str) else None

    valid_emotions = {'joy', 'sadness', 'anger', 'fear', 'disgust', 'surprise'}
    valid_confidences = {'low', 'medium', 'high'}

    if emo not in valid_emotions or conf not in valid_confidences:
        return "ask_clarification", "I'm not sure I understand how you feel. Could you tell me more?"

    if conf == "low":
        return "ask_clarification", "I think I sense something, but could you clarify your feelings?"

    mapping = {
        "joy": {"medium": "continue", "high": "continue"},
        "sadness": {"medium": "offer_support", "high": "offer_support"},
        "anger": {"medium": "slow_down", "high": "de_escalate"},
        "fear": {"medium": "slow_down", "high": "offer_support"},
        "disgust": {"medium": "slow_down", "high": "de_escalate"},
        "surprise": {"medium": "continue", "high": "continue"}
    }

    messages = {
        "continue": "I hear you, please go on.",
        "offer_support": "I'm here for you. Tell me what's on your mind.",
        "slow_down": "Let's take a moment to process this slowly.",
        "de_escalate": "Let’s pause and try to lower the tension."
    }

    action = mapping[emo][conf]
    message = messages.get(action, "Please continue.")
    return action, message

def main():
    try:
        # On lit l'intégralité de l'entrée (STDIN)
        input_data = sys.stdin.read().strip()
        if not input_data:
            return

        # On charge le JSON (peut être un objet unique {} ou une liste [])
        data = json.loads(input_data)

        # CAS 1 : C'est une liste d'objets (ton format avec crochets et virgules)
        if isinstance(data, list):
            for entry in data:
                action, message = react(entry.get("emotion"), entry.get("confidence"))
                print(json.dumps({"action": action, "message": message}))

        # CAS 2 : C'est un objet JSON unique
        else:
            action, message = react(data.get("emotion"), data.get("confidence"))
            print(json.dumps({"action": action, "message": message}))

    except Exception:
        # En cas de JSON vraiment cassé (ex: guillemet manquant)
        print(json.dumps({
            "action": "ask_clarification",
            "message": "Invalid JSON format. Please provide a valid object or list."
        }))

if __name__ == "__main__":
    main()