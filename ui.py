# --- ui.py ---
import tkinter as tk
from tkinter import ttk

def creer_fenetre():
    # --- Création fenêtre principale ---
    fenetre = tk.Tk()
    fenetre.title("🕵️ Murder Party : Le Manoir Mystérieux 🕵️")
    fenetre.geometry("1000x700")
    fenetre.configure(bg="#1c1c1c")

    # --- Canvas scrollable ---
    canvas = tk.Canvas(fenetre, width=1000, height=700, bg="#2c2c2c")
    canvas.pack(fill="both", expand=True, side="left")
    scrollbar = ttk.Scrollbar(fenetre, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    scroll_frame = tk.Frame(canvas, bg="#2c2c2c")
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")

    def update_scrollregion(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
    scroll_frame.bind("<Configure>", update_scrollregion)

    return fenetre, canvas, scroll_frame

def creer_style():
    style = ttk.Style()
    style.theme_use("default")
    style.configure("TButton",
                    font=("Arial", 12, "bold"),
                    foreground="white",
                    background="#B3583F",
                    padding=10,
                    borderwidth=2)
    style.map("TButton",
              background=[("active", "#9a8cff")],
              foreground=[("disabled", "gray")])
    style.configure("TLabel",
                    font=("Consolas", 14),
                    foreground="#f0f0f0",
                    background="#1c1c1c",
                    wraplength=950)
