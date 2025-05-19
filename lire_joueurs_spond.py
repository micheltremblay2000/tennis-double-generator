
import pandas as pd
import os

def lire_joueurs_depuis_fichier(chemin_fichier):
    """
    Lit un fichier CSV ou Excel exporté depuis Spond et retourne la liste des noms des joueurs.
    Le fichier doit contenir une colonne avec le nom 'Nom' ou 'Name'.
    """
    if not os.path.exists(chemin_fichier):
        raise FileNotFoundError(f"Fichier non trouvé : {chemin_fichier}")

    # Lecture en fonction de l'extension
    if chemin_fichier.endswith(".csv"):
        df = pd.read_csv(chemin_fichier)
    elif chemin_fichier.endswith(".xlsx") or chemin_fichier.endswith(".xls"):
        df = pd.read_excel(chemin_fichier)
    else:
        raise ValueError("Format de fichier non supporté (utilisez .csv ou .xlsx)")

    # Recherche de la colonne des noms
    for col in df.columns:
        if col.lower() in ["nom", "name", "full name"]:
            noms = df[col].dropna().astype(str).tolist()
            return noms

    raise ValueError("Colonne contenant les noms des joueurs non trouvée.")
