import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# === Caricamento dati dal file JSON ===
with open("biglietti_grattaevinci.json", "r") as f:
    dati_biglietti = json.load(f)

# === Funzioni ===
def calcola_probabilita_reale(biglietto, vincita):
    """Restituisce la probabilità reale in base alla vincita e al biglietto scelto"""
    vincita = float(vincita)
    categorie = dati_biglietti[biglietto]["vincite"]
    if vincita <= 500:
        return categorie["fino a 500"] * 100
    elif 501 <= vincita <= 10000:
        return categorie["da 501 a 10000"] * 100
    else:
        return categorie["oltre 10000"] * 100

def aggiorna_probabilita():
    try:
        biglietto = combo_biglietto.get()
        vincita = float(entry_vincita.get())
        prob = calcola_probabilita_reale(biglietto, vincita)
        label_risultato.config(text=f"Probabilità reale: {prob:.6f}%")
        disegna_grafico(prob)
    except ValueError:
        messagebox.showerror("Errore", "Inserisci una cifra valida.")

def simula_giocata():
    try:
        biglietto = combo_biglietto.get()
        vincita = float(entry_vincita.get())
        prob = calcola_probabilita_reale(biglietto, vincita)
        roll = random.uniform(0, 100)
        if roll < prob:
            messagebox.showinfo("Risultato", f"HAI VINTO {vincita} €!")
        else:
            messagebox.showinfo("Risultato", "Hai perso. Ritenta?")
    except ValueError:
        messagebox.showerror("Errore", "Inserisci una cifra valida.")

def disegna_grafico(prob):
    figure.clear()
    ax = figure.add_subplot(111)
    ax.pie([prob, 100 - prob], labels=["Vittoria", "Sconfitta"],
           colors=["green", "red"], autopct='%1.6f%%', startangle=90)
    ax.axis("equal")
    canvas.draw()

# === GUI ===
root = tk.Tk()
root.title("Simulatore Gratta e Vinci - Probabilità Reali")
root.geometry("600x550")
root.resizable(False, False)

tk.Label(root, text="Scegli un biglietto:", font=("Arial", 12)).pack(pady=5)
combo_biglietto = ttk.Combobox(root, values=list(dati_biglietti.keys()), font=("Arial", 12))
combo_biglietto.current(0)
combo_biglietto.pack()

tk.Label(root, text="Quanto vuoi vincere (€):", font=("Arial", 12)).pack(pady=10)
entry_vincita = tk.Entry(root, font=("Arial", 12))
entry_vincita.pack()

# Pulsanti
btn_calcola = tk.Button(root, text="Calcola Probabilità", font=("Arial", 12), command=aggiorna_probabilita)
btn_calcola.pack(pady=10)

label_risultato = tk.Label(root, text="Probabilità reale: --", font=("Arial", 14))
label_risultato.pack(pady=10)

btn_simula = tk.Button(root, text="Simula Giocata", font=("Arial", 12), command=simula_giocata)
btn_simula.pack(pady=10)

# Grafico
figure = plt.Figure(figsize=(4, 4), dpi=100)
canvas = FigureCanvasTkAgg(figure, root)
canvas.get_tk_widget().pack()

root.mainloop()
