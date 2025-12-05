import csv
from datetime import date, timedelta
import random

def appel(fichier):
    header = None
    # Définir l'en-tête
    if 'rh_' in fichier or '_RH'.lower() in fichier or '_RH' in fichier:
        header = [
            '_FONCTION', '_PRENOM', '_NOM', '_DEPARTEMENT', '_PHONE', '_COURRIEL', '_PRIVILEGE',
            '_AGE','_ENTREPRISE', '_ADRESSE', '_DATE_RH', '_EDITEUR_RH', '_LIEN' 
        ]
        
        # Générer 30 lignes de données factices
        rows = []
        base_date = date(2025, 1, 1)

        for i in range(30):
            row = {
                "_FONCTION": random.choice(["Analyste", "Manager", "Développeur", "Assistant"]),
                "_PRENOM": f"Prenom{i}",
                "_NOM": f"Nom{i}",
                "_DEPARTEMENT": random.choice(["Finance", "IT", "Marketing", "RH"]),
                "_PHONE": f"+33{random.randint(600000000, 699999999)}",
                "_COURRIEL": f"user{i}@example.com",
                "_PRIVILEGE": random.choice(["Admin", "User", "Guest"]),
                "_AGE": f"{random.randint(1945, 2025)}-{random.randint(1,12)}-{random.randint(1, 29)}",
                "_ENTREPRISE": "Delifruit",
                "_ADRESSE": f"{random.randint(1, 200)} Rue Exemple, Ville{i}",
                "_DATE_RH": (base_date + timedelta(days=i)).isoformat(),
                "_EDITEUR_RH": random.choice(["RH_A", "RH_B", "RH_C"]),
                "_LIEN": f"http://intranet.example.com/profil{i}",
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


appel(fichier="fichiers_import/donnees_in.csv")