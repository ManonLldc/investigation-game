# --- logique_jeu.py ---
from donnees import suspects, COUPABLE, enquete

# --- Variables globales ---
indices_trouves = []
etat_suspect = {nom: "neutre" for nom in suspects}
score = 0

# --- Interrogatoire ---
def interroger_suspect(nom, mise_a_jour_affichage):
    """
    nom : nom du suspect à interroger
    mise_a_jour_affichage : fonction callback pour mettre à jour l'affichage (texte et boutons)
    """
    # Ajouter les indices trouvés
    for indice in suspects[nom]["indice"]:
        if indice not in indices_trouves:
            indices_trouves.append(indice)

    # Préparer les questions
    questions = {
        "Où étiez-vous la soirée du crime ?": f"{suspects[nom]['alibi']}.",
        "Avez-vous remarqué quelque chose d’inhabituel ?": f"{suspects[nom]['secret']}."
    }
    for q, r in suspects[nom].get("question_speciale", {}).items():
        questions[q] = r

    def afficher_question(q, reponse):
        analyse = "Nerveux" if "étrange" in reponse or "suspicious" in reponse else "Calme et cohérent"
        texte = f"{nom} : {reponse}\n\nAnalyse comportementale : {analyse}\n\n📜 Indices collectés : {len(indices_trouves)}"

        # Préparer les boutons
        boutons = []
        for ques, resp in questions.items():
            boutons.append((ques, lambda ques=ques, resp=resp: afficher_question(ques, resp)))
        boutons.append(("✅ Terminer l'interrogatoire", lambda: mise_a_jour_affichage("debut")))
        boutons.append(("📜 Consulter mes indices", lambda: mise_a_jour_affichage("indices")))

        mise_a_jour_affichage("update", texte, boutons)

    # Boutons initiaux pour les questions
    boutons_initiaux = []
    for q, r in questions.items():
        boutons_initiaux.append((q, lambda ques=q, resp=r: afficher_question(ques, resp)))
    boutons_initiaux.append(("📜 Consulter mes indices", lambda: mise_a_jour_affichage("indices")))

    texte_intro = f"Vous interrogez {nom}."
    mise_a_jour_affichage("update", texte_intro, boutons_initiaux)

# --- Accusation ---
def accuser(mise_a_jour_affichage):
    """
    Affiche les suspects pour accuser quelqu'un
    """
    texte = "Qui souhaitez-vous accuser ?"
    boutons = []

    for nom in suspects.keys():
        boutons.append((nom, lambda n=nom: verifier_accusation(n, mise_a_jour_affichage)))

    boutons.append(("⬅️ Revenir à l'entrée", lambda: mise_a_jour_affichage("debut")))
    boutons.append(("📜 Consulter mes indices", lambda: mise_a_jour_affichage("indices")))

    mise_a_jour_affichage("update", texte, boutons)

def verifier_accusation(nom, mise_a_jour_affichage):
    if nom == COUPABLE:
        texte = f"🎉 Bravo ! {nom} est bien le coupable !"
    else:
        texte = f"❌ {nom} n'est pas le coupable. Continuez l'enquête."

    boutons = [("⬅️ Revenir à l'entrée", lambda: mise_a_jour_affichage("debut"))]
    mise_a_jour_affichage("update", texte, boutons)

# --- Relancer le jeu ---
def relancer_jeu(mise_a_jour_affichage):
    global indices_trouves, etat_suspect, score
    indices_trouves = []
    etat_suspect = {nom: "neutre" for nom in suspects}
    score = 0
    mise_a_jour_affichage("debut")
