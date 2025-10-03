import tkinter as tk
from jeu import JeuEnquete

if __name__ == "__main__":
    fenetre = tk.Tk()
    fenetre.title("🕵️ Murder Party : Le Manoir Mystérieux 🕵️")
    fenetre.geometry("1000x700")
    fenetre.configure(bg="#000000")
    
    jeu = JeuEnquete(fenetre)  # initialisation du jeu
    fenetre.mainloop()
