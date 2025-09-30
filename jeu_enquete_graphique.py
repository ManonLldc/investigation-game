import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from donnees import suspects, COUPABLE, enquete
from logique_jeu import interroger_suspect, accuser, relancer_jeu, afficher_intro

# --- Initialisation fenêtre, styles, canvas, etc. ---
fenetre = tk.Tk()
fenetre.title("🕵️ Murder Party")
fenetre.geometry("1000x700")
# ... configuration canvas et style ...


# --- Lancement du jeu ---
afficher_intro(fenetre)  # tu passes la fenêtre pour que les fonctions puissent mettre à jour l'affichage

fenetre.mainloop()
