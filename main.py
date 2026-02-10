import sys
import json

def react(emotion, confidence):
    # Listes des entrées valides
    valid_emotions = {'joy', 'sadness', 'anger', 'fear', 'disgust', 'surprise'}
    valid_confidences = {'low', 'medium', 'high'}

    # Règle d'entrée invalide
    if emotion not in valid_emotions or confidence not in valid_confidences:
        return "ask_clarification", "I'm not sure I understand how you feel. Could you tell me more?"

    # Cas de confiance basse (identique pour toutes les émotions)
    if confidence == "low":
        return "ask_clarification", "I think I sense something, but could you clarify your feelings?"
    # Mapping des réactions pour Medium et High

    # Mapping des réactions pour Medium et High
    mapping = {
        "joy": {"medium": "continue", "high": "continue"},
        "sadness": {"medium": "offer_support", "high": "offer_support"},
        "anger": {"medium": "slow_down", "high": "de_escalate"},
        "fear": {"medium": "slow_down", "high": "offer_support"},
        "disgust": {"medium": "slow_down", "high": "de_escalate"},
        "surprise": {"medium": "continue", "high": "continue"}
    }

    # Messages personnalisés selon l'action
    messages = {
        "continue": "I hear you, please go on.",
        "offer_support": "I'm here for you. Tell me what's on your mind.",
        "slow_down": "Let's take a moment to process this slowly.",
        "de_escalate": "Let’s pause and try to lower the tension."
    }

    action = mapping[emotion][confidence]
    message = messages[action]

    return action, message

def main():
    try:
        # Lecture du JSON depuis STDIN
        input_data = sys.stdin.read()
        if not input_data.strip():
            return

        data = json.loads(input_data)

        # Extraction des données
        emo = data.get("emotion")
        conf = data.get("confidence")

        # Calcul de la réponse
        action, message = react(emo, conf)

        # Sortie JSON strictement formatée
        output = {
            "action": action,
            "message": message
        }
        print(json.dumps(output))

    except Exception:
        # En cas de JSON malformé, on suit la règle d'input invalide
        print(json.dumps({
            "action": "ask_clarification",
            "message": "I encountered an error processing your input."
        }))

if __name__ == "__main__":
    main()