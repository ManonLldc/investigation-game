from donnees import suspects, COUPABLE, enquete
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


class JeuEnquete:
    def __init__(self, fenetre):
        self.fenetre = fenetre
        self.indices_trouves = []
        self.etat_suspect = {nom: "neutre" for nom in suspects}
        self.score = 0
        self.dossier_indices_win = None
        self.text_widget = None

        # Préparer choix pour l'interrogatoire
        enquete["choisir_suspect"]["choix"] = {
            nom: f"interroger_{nom}" for nom in suspects.keys()
        } | {"Retour à l'entrée": "debut"}

        # Canvas scrollable
        self.canvas = tk.Canvas(fenetre, width=1000, height=700, bg="#2c2c2c")
        self.canvas.pack(fill="both", expand=True, side="left")
        scrollbar = ttk.Scrollbar(fenetre, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.scroll_frame = tk.Frame(self.canvas, bg="#2c2c2c")
        self.frame_window = self.canvas.create_window((0,0), window=self.scroll_frame, anchor="nw")
        self.scroll_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.frame_boutons = self.scroll_frame

        self.texte = tk.StringVar()
        self.label = ttk.Label(self.scroll_frame, textvariable=self.texte, font=("Consolas", 14),
                               foreground="#f0f0f0", background="#000000", wraplength=950, justify="left")
        self.label.pack(padx=25, pady=20, anchor="w")

        # Chargement images suspects
        self.images_suspects = {}
        for nom in suspects.keys():
            try:
                img = Image.open(f"images/{nom.lower()}.JPG")
                img = img.resize((120, 120))
                self.images_suspects[nom] = ImageTk.PhotoImage(img)
            except Exception:
                self.images_suspects[nom] = None

        # Lancement
        self.afficher_intro()

    # --- Gestion des boutons ---
    def afficher_boutons(self, boutons):
        for widget in self.frame_boutons.winfo_children():
            if widget != self.label:
                widget.destroy()
        for texte_btn, commande in boutons:
            btn = ttk.Button(self.frame_boutons, text=texte_btn, command=commande)
            btn.pack(pady=5, anchor="center")
        self.fenetre.update_idletasks()
        self.canvas.yview_moveto(0)

    # --- Dossier des suspects ---
    def afficher_dossier_suspects(self):
        self.texte.set("Voici la liste des suspects. Cliquez sur une carte pour interroger.")
        for widget in self.frame_boutons.winfo_children():
            if widget != self.label:
                widget.destroy()

        cards_frame = tk.Frame(self.frame_boutons, bg="#2c2c2c")
        cards_frame.pack(pady=10)

        col, row = 0, 0
        for nom in suspects.keys():
            card = tk.Frame(cards_frame, bg="#3c3c3c", bd=3, relief="raised", width=150, height=200)
            card.grid(row=row, column=col, padx=15, pady=15, sticky="n")
            card.grid_propagate(False)

            if self.images_suspects[nom]:
                lbl_img = tk.Label(card, image=self.images_suspects[nom], bg="#3c3c3c")
                lbl_img.image = self.images_suspects[nom]
                lbl_img.pack(pady=5)

            lbl_nom = tk.Label(card, text=nom, font=("Arial", 14, "bold"), bg="#3c3c3c", fg="white")
            lbl_nom.pack()

            card.bind("<Button-1>", lambda e, n=nom: self.interroger_suspect(n))
            lbl_nom.bind("<Button-1>", lambda e, n=nom: self.interroger_suspect(n))
            if self.images_suspects[nom]:
                lbl_img.bind("<Button-1>", lambda e, n=nom: self.interroger_suspect(n))

            col += 1
            if col >= 3:
                col = 0
                row += 1

        btn_retour = ttk.Button(self.frame_boutons, text="⬅️", command=lambda: self.afficher_etape("debut"))
        btn_retour.pack(pady=10)
        btn_indices = ttk.Button(self.frame_boutons, text="📜 Consulter mes indices", command=self.afficher_dossier_indices)
        btn_indices.pack(pady=5)

    # --- Dossier des indices ---
    def afficher_dossier_indices(self):
        if self.dossier_indices_win and tk.Toplevel.winfo_exists(self.dossier_indices_win):
            self.text_widget.configure(state="normal")
            self.text_widget.delete("1.0", "end")
        else:
            self.dossier_indices_win = tk.Toplevel(self.fenetre)
            self.dossier_indices_win.title("📜 Dossier des indices")
            self.dossier_indices_win.geometry("600x400")
            frame = tk.Frame(self.dossier_indices_win)
            frame.pack(fill="both", expand=True)
            self.text_widget = tk.Text(frame, wrap="word", font=("Consolas", 12))
            self.text_widget.pack(side="left", fill="both", expand=True)
            scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.text_widget.yview)
            self.text_widget.configure(yscrollcommand=scrollbar.set)
            scrollbar.pack(side="right", fill="y")
            btn_fermer = ttk.Button(self.dossier_indices_win, text="⬅️ Revenir à l'entrée", command=self.dossier_indices_win.destroy)
            btn_fermer.pack(pady=5)

        if self.indices_trouves:
            lignes = [f"{nom} : {indice}" for nom, data in suspects.items() for indice in data["indice"] if indice in self.indices_trouves]
            self.text_widget.insert("1.0", "\n".join(lignes))
        else:
            self.text_widget.insert("1.0", "Aucun indice découvert.")
        self.text_widget.configure(state="disabled")
        self.dossier_indices_win.lift()

    # --- Afficher étape ---
    def afficher_etape(self, etape):
        if etape == "dossier_suspects":
            self.afficher_dossier_suspects()
            return
        elif etape == "accuser":
            self.accuser()
            return
        self.texte.set(enquete[etape]["texte"])
        boutons = []
        for choix, destination in enquete[etape].get("choix", {}).items():
            if "interroger_" in destination:
                boutons.append((choix, lambda n=destination.replace("interroger_", ""): self.interroger_suspect(n)))
            else:
                boutons.append((choix, lambda dest=destination: self.afficher_etape(dest)))
        boutons.append(("📜 Consulter mes indices", self.afficher_dossier_indices))
        self.afficher_boutons(boutons)

    # --- Interrogatoire ---
    def interroger_suspect(self, nom):
        questions = {
            "Où étiez-vous la soirée du crime ?": f"{suspects[nom]['alibi']}.",
            "Avez-vous remarqué quelque chose d’inhabituel ?": f"{suspects[nom]['secret']}."
        }
        for q, r in suspects[nom].get("question_speciale", {}).items():
            questions[q] = r

        for indice in suspects[nom]["indice"]:
            if indice not in self.indices_trouves:
                self.indices_trouves.append(indice)

        def afficher_question(q, reponse):
            analyse = "Nerveux" if "étrange" in reponse or "suspicious" in reponse else "Calme et cohérent"
            self.texte.set(f"{nom} : {reponse}\n\nAnalyse comportementale : {analyse}\n\n📜 Indices collectés : {len(self.indices_trouves)}")

            boutons = []
            for ques, resp in questions.items():
                boutons.append((ques, lambda ques=ques, resp=resp: afficher_question(ques, resp)))
            boutons.append(("✅ Terminer l'interrogatoire", lambda: self.afficher_etape("debut")))
            boutons.append(("📜 Consulter mes indices", self.afficher_dossier_indices))
            self.afficher_boutons(boutons)

        boutons_initiaux = []
        for q, r in questions.items():
            boutons_initiaux.append((q, lambda ques=q, resp=r: afficher_question(ques, resp)))
        boutons_initiaux.append(("📜 Consulter mes indices", self.afficher_dossier_indices))
        self.afficher_boutons(boutons_initiaux)

    # --- Accusation finale ---
    def accuser(self):
        self.texte.set(f"Qui accusez-vous ?\nScore actuel : {self.score}")
        boutons = [(nom, lambda n=nom: self.verifier_accusation(n)) for nom in suspects.keys()]
        boutons.append(("⬅️ Revenir en arrière", lambda: self.afficher_etape("debut")))
        boutons.append(("📜 Consulter mes indices", self.afficher_dossier_indices))
        self.afficher_boutons(boutons)

    def verifier_accusation(self, nom):
        if nom == COUPABLE:
            self.score += 10 + len(self.indices_trouves)
            self.texte.set(f"✅ Coupable trouvé : {nom} !\nScore final : {self.score}")
        else:
            self.texte.set(f"❌ Ce n'est pas le coupable.")
        self.afficher_boutons([("🔄 Recommencer le jeu", self.relancer_jeu), ("📜 Consulter mes indices", self.afficher_dossier_indices)])

    # --- Introduction ---
    def afficher_intro(self):
        self.texte.set(enquete["debut"]["texte"])
        boutons = []
        for choix, destination in enquete["debut"]["choix"].items():
            if "interroger_" in destination:
                boutons.append((choix, lambda n=destination.replace("interroger_", ""): self.interroger_suspect(n)))
            else:
                boutons.append((choix, lambda dest=destination: self.afficher_etape(dest)))
        boutons.append(("📜 Consulter mes indices", self.afficher_dossier_indices))
        self.afficher_boutons(boutons)

    # --- Recommencer le jeu ---
    def relancer_jeu(self):
        self.indices_trouves = []
        self.etat_suspect = {nom: "neutre" for nom in suspects}
        self.score = 0
        self.afficher_intro()

