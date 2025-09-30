# --- jeu_enquete_graphique.py ---
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from donnees import suspects, COUPABLE, enquete

# --- Variables globales ---
indices_trouves = []
etat_suspect = {nom: "neutre" for nom in suspects}
score = 0
dossier_indices_win = None  # fenêtre du dossier des indices

# --- Préparer choix pour l'interrogatoire ---
enquete["choisir_suspect"]["choix"] = {
    nom: f"interroger_{nom}" for nom in suspects.keys()
} | {"Retour à l'entrée": "debut"}

# --- Création fenêtre principale ---
fenetre = tk.Tk()
fenetre.title("🕵️ Murder Party : Le Manoir Mystérieux 🕵️")
fenetre.geometry("1000x700")
fenetre.configure(bg="#1c1c1c")

# --- Styles ---
style = ttk.Style()
style.theme_use("default")
style.configure("TButton", font=("Arial", 12, "bold"), foreground="white",
                background="#B3583F", padding=10, borderwidth=2)
style.map("TButton", background=[("active", "#9a8cff")], foreground=[("disabled", "gray")])
style.configure("TLabel", font=("Consolas", 14), foreground="#f0f0f0", background="#1c1c1c", wraplength=950)

# --- Canvas scrollable ---
canvas = tk.Canvas(fenetre, width=1000, height=700, bg="#2c2c2c")
canvas.pack(fill="both", expand=True, side="left")
scrollbar = ttk.Scrollbar(fenetre, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")
scroll_frame = tk.Frame(canvas, bg="#2c2c2c")
frame_window = canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
def update_scrollregion(event):
    canvas.configure(scrollregion=canvas.bbox("all"))
scroll_frame.bind("<Configure>", update_scrollregion)

frame_boutons = scroll_frame

texte = tk.StringVar()
label = ttk.Label(scroll_frame, textvariable=texte, style="TLabel", justify="left")
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

# --- Affichage boutons ou cartes ---
def afficher_boutons(boutons):
    for widget in frame_boutons.winfo_children():
        if widget != label:
            widget.destroy()
    for texte_btn, commande in boutons:
        btn = ttk.Button(frame_boutons, text=texte_btn, command=commande)
        btn.pack(pady=5, anchor="center")
    fenetre.update_idletasks()
    canvas.yview_moveto(0)

# --- Affichage du dossier des suspects en cartes ---
def afficher_dossier_suspects():
    texte.set("Voici la liste des suspects. Cliquez sur une carte pour interroger.")

    for widget in frame_boutons.winfo_children():
        if widget != label:
            widget.destroy()

    cards_frame = tk.Frame(frame_boutons, bg="#2c2c2c")
    cards_frame.pack(pady=10)

    col, row = 0, 0
    for nom in suspects.keys():
        card = tk.Frame(cards_frame, bg="#3c3c3c", bd=3, relief="raised", width=150, height=200)
        card.grid(row=row, column=col, padx=15, pady=15, sticky="n")
        card.grid_propagate(False)

        if images_suspects[nom]:
            lbl_img = tk.Label(card, image=images_suspects[nom], bg="#3c3c3c")
            lbl_img.image = images_suspects[nom]
            lbl_img.pack(pady=5)

        lbl_nom = tk.Label(card, text=nom, font=("Arial", 14, "bold"), bg="#3c3c3c", fg="white")
        lbl_nom.pack()

        # Clic sur la carte → interrogatoire
        card.bind("<Button-1>", lambda e, n=nom: interroger_suspect(n))
        lbl_nom.bind("<Button-1>", lambda e, n=nom: interroger_suspect(n))
        if images_suspects[nom]:
            lbl_img.bind("<Button-1>", lambda e, n=nom: interroger_suspect(n))

        col += 1
        if col >= 3:
            col = 0
            row += 1

    btn_retour = ttk.Button(frame_boutons, text="⬅️", command=lambda: afficher_etape("debut"))
    btn_retour.pack(pady=10)

    btn_indices = ttk.Button(frame_boutons, text="📜 Consulter mes indices", command=afficher_dossier_indices)
    btn_indices.pack(pady=5)

# --- Affichage dossier des indices ---
def afficher_dossier_indices():
    global dossier_indices_win, text_widget
    if dossier_indices_win and tk.Toplevel.winfo_exists(dossier_indices_win):
        text_widget.configure(state="normal")
        text_widget.delete("1.0", "end")
        if indices_trouves:
            lignes = [f"{nom} : {indice}" for nom, data in suspects.items() for indice in data["indice"] if indice in indices_trouves]
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
    if indices_trouves:
        lignes = [f"{nom} : {indice}" for nom, data in suspects.items() for indice in data["indice"] if indice in indices_trouves]
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

# --- Étapes du jeu ---
def afficher_etape(etape):
    if etape == "dossier_suspects":
        afficher_dossier_suspects()
        return
    elif etape == "accuser":
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
    questions = {
        "Où étiez-vous la soirée du crime ?": f"{suspects[nom]['alibi']}.",
        "Avez-vous remarqué quelque chose d’inhabituel ?": f"{suspects[nom]['secret']}."
    }
    for q, r in suspects[nom].get("question_speciale", {}).items():
        questions[q] = r

    for indice in suspects[nom]["indice"]:
        if indice not in indices_trouves:
            indices_trouves.append(indice)

    def afficher_question(q, reponse):
        analyse = "Nerveux" if "étrange" in reponse or "suspicious" in reponse else "Calme et cohérent"
        texte.set(f"{nom} : {reponse}\n\nAnalyse comportementale : {analyse}\n\n📜 Indices collectés : {len(indices_trouves)}")

        boutons = []
        for ques, resp in questions.items():
            boutons.append((ques, lambda ques=ques, resp=resp: afficher_question(ques, resp)))

        boutons.append(("✅ Terminer l'interrogatoire", lambda: afficher_etape("debut")))
        boutons.append(("📜 Consulter mes indices", afficher_dossier_indices))
        afficher_boutons(boutons)

    boutons_initiaux = []
    for q, r in questions.items():
        boutons_initiaux.append((q, lambda ques=q, resp=r: afficher_question(ques, resp)))
    boutons_initiaux.append(("📜 Consulter mes indices", afficher_dossier_indices))
    afficher_boutons(boutons_initiaux)

# --- Accusation finale ---
def accuser():
    texte.set(f"Qui accusez-vous ?\nScore actuel : {score}")
    boutons = [(nom, lambda n=nom: verifier_accusation(n)) for nom in suspects.keys()]
    boutons.append(("⬅️ Revenir en arrière", lambda: afficher_etape("debut")))
    boutons.append(("📜 Consulter mes indices", afficher_dossier_indices))
    afficher_boutons(boutons)

def verifier_accusation(nom):
    global score
    if nom == COUPABLE:
        score += 10 + len(indices_trouves)
        texte.set(f"✅ Coupable trouvé : {nom} !\nScore final : {score}")
    else:
        texte.set(f"❌ Ce n'est pas le coupable.")
    afficher_boutons([("🔄 Recommencer le jeu", relancer_jeu), ("📜 Consulter mes indices", afficher_dossier_indices)])

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

# --- Recommencer le jeu ---
def relancer_jeu():
    global indices_trouves, etat_suspect, score
    indices_trouves = []
    etat_suspect = {nom: "neutre" for nom in suspects}
    score = 0
    afficher_intro()

# --- Lancement ---
afficher_intro()
fenetre.mainloop()
