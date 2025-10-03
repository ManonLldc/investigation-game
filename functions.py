# --- Fonctions pour les boutons ---
def afficher_boutons(boutons):
    global fenetre
    for widget in frame_boutons.winfo_children():
        if widget != label:
            widget.destroy()
    for texte_btn, commande in boutons:
        btn = ttk.Button(frame_boutons, text=texte_btn, command=commande)
        btn.pack(pady=5, anchor="center")
    fenetre.update_idletasks()
    canvas.yview_moveto(0)