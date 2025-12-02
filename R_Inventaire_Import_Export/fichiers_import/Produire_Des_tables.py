import csv
from datetime import date, timedelta
import random

def appel(fichier):
    header = None
    # Définir l'en-tête
    if 'rh_' in fichier or '_RH'.lower() in fichier or '_RH' in fichier:
        header = [
            '_NOM', '_PRENOM', '_ADRESSE', '_AGE', '_COURRIEL', '_EDITEUR_RH', '_DEPARTEMENT',
            '_FONCTION', '_LIEN', '_PHONE', '_PRIVILEGE', '_DATE_RH', '_ENTREPRISE'
        ]
        
        # Générer 30 lignes de données factices
        rows = []
        base_date = date(2025, 1, 1)

        for i in range(30):
            row = {
                "_NOM": f"Nom{i}",
                "_PRENOM": f"Prenom{i}",
                "_ADRESSE": f"{random.randint(1, 200)} Rue Exemple, Ville{i}",
                "_AGE": random.randint(20, 65),
                "_COURRIEL": f"user{i}@example.com",
                "_EDITEUR_RH": random.choice(["RH_A", "RH_B", "RH_C"]),
                "_DEPARTEMENT": random.choice(["Finance", "IT", "Marketing", "RH"]),
                "_FONCTION": random.choice(["Analyste", "Manager", "Développeur", "Assistant"]),
                "_LIEN": f"http://intranet.example.com/profil{i}",
                "_PHONE": f"+33{random.randint(600000000, 699999999)}",
                "_PRIVILEGE": random.choice(["Admin", "User", "Guest"]),
                "_DATE_RH": (base_date + timedelta(days=i)).isoformat(),
                "_ENTREPRISE": "Delifruit"

            }
            rows.append(row)
            
    elif 'inv_' in fichier or '_IN'.lower() in fichier or '_IN' in fichier:
        header = [
            '_PRODUIT', '_TYPE', '_ANNEE', '_DESTINATION', '_QUANTITE', '_EDITEUR_IN', '_PROVENANCE',
            '_FABRICANT', '_LIEN', '_PRIX', '_APPROBATIONS', '_DATE_IN'
        ]
        
        # Générer 30 lignes de données factices
        rows = []
        base_date = date(2025, 1, 1)

        for i in range(30):
            row = {
                "_DATE_IN": (base_date + timedelta(days=i)).isoformat(),
                "_TYPE": random.choice(["Livre", "Jeu", "Film", "Logiciel"]),
                "_ANNEE": random.randint(2000, 2025),
                "_DESTINATION": random.choice(["Paris", "Londres", "New York", "Tokyo"]),
                "_PRIX": round(random.uniform(10, 200), 2),
                "_QUANTITE": random.randint(1, 50),
                "_EDITEUR_IN": random.choice(["EditeurA", "EditeurB", "EditeurC"]),
                "_PROVENANCE": random.choice(["France", "USA", "Canada", "Japon"]),
                "_FABRICANT": random.choice(["FabA", "FabB", "FabC"]),
                "_LIEN": f"http://example.com/item{i}",
                "_PRODUIT": f"Produit{i}",
                "_APPROBATIONS": random.choice(["Oui", "Non"])
            }
            rows.append(row)
    
    if header:


        # Écriture dans un fichier CSV
        with open(fichier, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=header)
            writer.writeheader()
            writer.writerows(rows)
            
        print("✅ Fichier donnees.csv généré avec 30 lignes.")
        
    else :
        print('fichier non valide !')


appel(fichier="fichiers_import/donnees_rh.csv")