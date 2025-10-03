from donnees import suspects, COUPABLE

# --- Variables globales ---
indices_trouves = []
score = 0

# --- Fonctions logiques ---
def obtenir_questions(nom):
    """Retourne les questions et réponses d'un suspect."""
    questions = {
        "Où étiez-vous la soirée du crime ?": f"{suspects[nom]['alibi']}.",
        "Avez-vous remarqué quelque chose d’inhabituel ?": f"{suspects[nom]['secret']}."
    }
    for q, r in suspects[nom].get("question_speciale", {}).items():
        questions[q] = r
    return questions

def ajouter_indices(nom):
    """Ajoute les indices découverts d'un suspect."""
    global indices_trouves
    for indice in suspects[nom]["indice"]:
        if indice not in indices_trouves:
            indices_trouves.append(indice)

def verifier_accusation(nom):
    """Vérifie si le suspect accusé est le coupable et calcule le score."""
    global score
    if nom == COUPABLE:
        score += 10 + len(indices_trouves)
        return True, f"Coupable trouvé : {nom} ! Score final : {score}"
    else:
        return False, "Ce n'est pas le coupable."

def recommencer_jeu():
    """Réinitialise le jeu."""
    global indices_trouves, score
    indices_trouves = []
    score = 0
