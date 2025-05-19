
import random
import tkinter as tk
from tkinter import messagebox, filedialog
from collections import defaultdict
from openpyxl import Workbook
from lire_joueurs_spond import lire_joueurs_depuis_fichier

def generer_tournoi(joueurs, nb_courts, nb_rounds):
    nb_joueurs = len(joueurs)
    coequipiers = defaultdict(set)
    adversaires = defaultdict(set)
    compteur_participation = defaultdict(int)
    planning = []

    for round_num in range(1, nb_rounds + 1):
        round_matches = []
        essais = 0
        joueurs_ids = list(range(nb_joueurs))
        joueurs_trie = sorted(joueurs_ids, key=lambda j: compteur_participation[j])
        joueurs_dispo = joueurs_trie[:]

        while len(round_matches) < nb_courts and essais < 1000:
            essais += 1
            if len(joueurs_dispo) < 4:
                break
            selection = random.sample(joueurs_dispo, 4)
            a, b, c, d = selection
            pair1, pair2 = tuple(sorted((a, b))), tuple(sorted((c, d)))

            if b in coequipiers[a] or d in coequipiers[c]:
                continue
            if any(x in adversaires[y] for x in pair1 for y in pair2):
                continue

            round_matches.append((pair1, pair2))
            for x, y in [pair1, pair2]:
                coequipiers[x].add(y)
                coequipiers[y].add(x)
                compteur_participation[x] += 1
                compteur_participation[y] += 1
            for x in pair1:
                for y in pair2:
                    adversaires[x].add(y)
                    adversaires[y].add(x)
            for j in selection:
                joueurs_dispo.remove(j)

        if len(round_matches) < nb_courts:
            return None  # Échec
        planning.append(round_matches)
    return planning

def afficher_et_exporter(planning, joueurs, fichier_excel):
    wb = Workbook()
    ws = wb.active
    ws.title = "Tournoi Double"
    ws.append(["Round", "Court", "Joueur 1A", "Joueur 1B", "Joueur 2A", "Joueur 2B"])

    for i, round_match in enumerate(planning, 1):
        output_text.insert(tk.END, f"\nRound {i} :\n")
        for j, (p1, p2) in enumerate(round_match, 1):
            noms = [joueurs[p1[0]], joueurs[p1[1]], joueurs[p2[0]], joueurs[p2[1]]]
            output_text.insert(tk.END, f"  Court {j} : {noms[0]} & {noms[1]} vs {noms[2]} & {noms[3]}\n")
            ws.append([i, j] + noms)

    wb.save(fichier_excel)
    messagebox.showinfo("Succès", f"Planning exporté dans {fichier_excel}")

def lancer_generation():
    try:
        chemin = filedialog.askopenfilename(title="Sélectionnez le fichier exporté de Spond (.csv ou .xlsx)")
        joueurs = lire_joueurs_depuis_fichier(chemin)

        nb_c = int(entry_courts.get())
        nb_r = int(entry_matchs.get())

        if len(joueurs) < 4 or nb_c < 1 or nb_r < 1:
            raise ValueError

        planning = generer_tournoi(joueurs, nb_c, nb_r)
        output_text.delete(1.0, tk.END)

        if not planning:
            output_text.insert(tk.END, "Échec : Conflit dans la génération.")
        else:
            filepath = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Fichier Excel", "*.xlsx")])
            if filepath:
                afficher_et_exporter(planning, joueurs, filepath)

    except ValueError:
        messagebox.showerror("Erreur", "Veuillez entrer des valeurs valides.")
    except Exception as e:
        messagebox.showerror("Erreur", str(e))

# Interface graphique
root = tk.Tk()
root.title("Générateur de tournoi de tennis en double (Spond)")

tk.Label(root, text="Nombre de courts :").grid(row=0, column=0, sticky="e")
tk.Label(root, text="Nombre de rounds :").grid(row=1, column=0, sticky="e")

entry_courts = tk.Entry(root)
entry_matchs = tk.Entry(root)

entry_courts.grid(row=0, column=1)
entry_matchs.grid(row=1, column=1)

tk.Button(root, text="Charger fichier Spond et générer", command=lancer_generation).grid(row=2, columnspan=2, pady=10)

output_text = tk.Text(root, width=60, height=20)
output_text.grid(row=3, columnspan=2)

root.mainloop()
