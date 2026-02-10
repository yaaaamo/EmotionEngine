import sys
import json

def react(emotion, confidence):
    # 1. Normalisation : on passe tout en minuscules pour gérer "Anger" ou "HIGH"
    # On vérifie d'abord que ce sont bien des chaînes de caractères
    emo = emotion.lower() if isinstance(emotion, str) else None
    conf = confidence.lower() if isinstance(confidence, str) else None

    # Listes des entrées valides (strictement en minuscules)
    valid_emotions = {'joy', 'sadness', 'anger', 'fear', 'disgust', 'surprise'}
    valid_confidences = {'low', 'medium', 'high'}

    # 2. Règle d'entrée invalide (Cas limites : émotion inconnue, None, ou mauvais type)
    if emo not in valid_emotions or conf not in valid_confidences:
        return "ask_clarification", "I'm not sure I understand how you feel. Could you tell me more?"

    # 3. Cas de confiance basse (prioritaire)
    if conf == "low":
        return "ask_clarification", "I think I sense something, but could you clarify your feelings?"

    # 4. Mapping des réactions pour Medium et High
    mapping = {
        "joy": {"medium": "continue", "high": "continue"},
        "sadness": {"medium": "offer_support", "high": "offer_support"},
        "anger": {"medium": "slow_down", "high": "de_escalate"},
        "fear": {"medium": "slow_down", "high": "offer_support"},
        "disgust": {"medium": "slow_down", "high": "de_escalate"},
        "surprise": {"medium": "continue", "high": "continue"}
    }

    # 5. Messages personnalisés selon l'action
    messages = {
        "continue": "I hear you, please go on.",
        "offer_support": "I'm here for you. Tell me what's on your mind.",
        "slow_down": "Let's take a moment to process this slowly.",
        "de_escalate": "Let’s pause and try to lower the tension."
    }

    # Récupération sécurisée de l'action
    action = mapping[emo][conf]
    message = messages.get(action, "Please continue.")

    return action, message

def main():
    try:
        # Lecture robuste du flux STDIN
        input_data = sys.stdin.read().strip()
        if not input_data:
            return

        # Parsing du JSON
        data = json.loads(input_data)

        # Extraction sécurisée des clés (gère le cas où une clé manque)
        emo = data.get("emotion")
        conf = data.get("confidence")

        # Calcul de la réponse
        action, message = react(emo, conf)

        # Sortie JSON strictement formatée sans texte parasite
        output = {
            "action": action,
            "message": message
        }
        print(json.dumps(output))

    except (json.JSONDecodeError, Exception):
        # Cas limite : JSON malformé (ex: une virgule en trop) ou erreur critique
        # La consigne demande de renvoyer ask_clarification en cas d'erreur
        print(json.dumps({
            "action": "ask_clarification",
            "message": "I encountered an error processing your input. Please provide valid data."
        }))

if __name__ == "__main__":
    main()