import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from ui import creer_fenetre, creer_style
from donnees import suspects, enquete
import jeu_enquete_logic as logic

# --- Création fenêtre et style ---
fenetre, canvas, frame_boutons = creer_fenetre()
creer_style()

# --- Texte principal ---
texte = tk.StringVar()
label = ttk.Label(frame_boutons, textvariable=texte, style="TLabel", justify="left")
label.pack(padx=25, pady=20, anchor="w")

# --- Chargement images suspects ---
images_suspects = {}
for nom in suspects.keys():
    try:
        img = Image.open(f"images/{nom.lower()}.JPG")
        img = img.resize((120, 120))
        images_suspects[nom] = ImageTk.PhotoImage(img)
    except Exception:
        images_suspects[nom] = None

# --- Fonctions GUI ---
dossier_indices_win = None

def afficher_boutons(boutons):
    for widget in frame_boutons.winfo_children():
        if widget != label:
            widget.destroy()
    for texte_btn, commande in boutons:
        btn = ttk.Button(frame_boutons, text=texte_btn, command=commande)
        btn.pack(pady=5, anchor="center")
    fenetre.update_idletasks()
    canvas.yview_moveto(0)

def afficher_dossier_indices():
    global dossier_indices_win, text_widget
    if dossier_indices_win and tk.Toplevel.winfo_exists(dossier_indices_win):
        text_widget.configure(state="normal")
        text_widget.delete("1.0", "end")
        if logic.indices_trouves:
            lignes = [f"{nom} : {indice}" for nom, data in suspects.items() for indice in data["indice"] if indice in logic.indices_trouves]
            text_widget.insert("1.0", "\n".join(lignes))
        else:
            text_widget.insert("1.0", "Aucun indice découvert.")
        text_widget.configure(state="disabled")
        dossier_indices_win.lift()
        return

    dossier_indices_win = tk.Toplevel(fenetre)
    dossier_indices_win.title("📜 Dossier des indices")
    dossier_indices_win.geometry("600x400")
    frame = tk.Frame(dossier_indices_win)
    frame.pack(fill="both", expand=True)

    text_widget = tk.Text(frame, wrap="word", font=("Consolas", 12))
    if logic.indices_trouves:
        lignes = [f"{nom} : {indice}" for nom, data in suspects.items() for indice in data["indice"] if indice in logic.indices_trouves]
        text_widget.insert("1.0", "\n".join(lignes))
    else:
        text_widget.insert("1.0", "Aucun indice découvert.")
    text_widget.configure(state="disabled")
    text_widget.pack(side="left", fill="both", expand=True)

    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=text_widget.yview)
    text_widget.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    btn_fermer = ttk.Button(dossier_indices_win, text="⬅️ Revenir à l'entrée", command=dossier_indices_win.destroy)
    btn_fermer.pack(pady=5)

# --- Accusation finale ---
def accuser():
    boutons = []
    for nom in suspects.keys():
        boutons.append((nom, lambda n=nom: afficher_resultat_accusation(n)))  # capture n=nom
    boutons.append(("⬅️ Revenir en arrière", lambda: afficher_etape("debut")))
    boutons.append(("📜 Consulter mes indices", afficher_dossier_indices))
    texte.set(f"Qui accusez-vous ?\nScore actuel : {logic.score}")
    afficher_boutons(boutons)


def afficher_resultat_accusation(nom):
    coupable, message = logic.verifier_accusation(nom)
    texte.set(message)
    afficher_boutons([
        ("🔄 Recommencer le jeu", relancer_jeu),
        ("📜 Consulter mes indices", afficher_dossier_indices)
    ])

# --- Fonction pour recommencer le jeu ---
def relancer_jeu():
    logic.recommencer_jeu()
    afficher_intro()

# --- Introduction ---
def afficher_intro():
    texte.set(enquete["debut"]["texte"])
    boutons = []
    for choix, destination in enquete["debut"]["choix"].items():
        if "interroger_" in destination:
            dest_command = lambda n=destination.replace("interroger_", ""): interroger_suspect(n)
        else:
            dest_command = lambda dest=destination: afficher_etape(dest)
        boutons.append((choix, dest_command))
    boutons.append(("📜 Consulter mes indices", afficher_dossier_indices))
    afficher_boutons(boutons)

# --- Étapes du jeu ---
def afficher_etape(etape):
    if etape == "accuser":
        accuser()
        return
    texte.set(enquete[etape]["texte"])
    boutons = []
    for choix, destination in enquete[etape].get("choix", {}).items():
        if "interroger_" in destination:
            dest_command = lambda n=destination.replace("interroger_", ""): interroger_suspect(n)
        else:
            dest_command = lambda dest=destination: afficher_etape(dest)
        boutons.append((choix, dest_command))
    boutons.append(("📜 Consulter mes indices", afficher_dossier_indices))
    afficher_boutons(boutons)

# --- Interrogatoire ---
def interroger_suspect(nom):
    questions = logic.obtenir_questions(nom)
    logic.ajouter_indices(nom)
    

    def afficher_question(q, r):
        analyse = "Nerveux" if "étrange" in r or "suspicious" in r else "Calme et cohérent"
        texte.set(f"{nom} : {r}\n\nAnalyse comportementale : {analyse}\n\n📜 Indices collectés : {len(logic.indices_trouves)}")
        boutons = [(ques, lambda ques=ques, resp=resp: afficher_question(ques, resp)) for ques, resp in questions.items()]
        boutons.append(("✅ Terminer l'interrogatoire", lambda: afficher_etape("debut")))
        boutons.append(("📜 Consulter mes indices", afficher_dossier_indices))
        afficher_boutons(boutons)

    boutons_initiaux = [(q, lambda q=q, r=r: afficher_question(q, r)) for q, r in questions.items()]
    boutons_initiaux.append(("📜 Consulter mes indices", afficher_dossier_indices))
    afficher_boutons(boutons_initiaux)

# --- Lancement ---
afficher_intro()
fenetre.mainloop()
