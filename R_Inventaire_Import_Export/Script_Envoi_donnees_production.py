import mysql.connector
import os, csv
import datetime
import json

# ---------------------------------------------------------------------
# FONCTIONS ET CLASSES
# ---------------------------------------------------------------------

def chercher_ds_JSON(dictionnaire, cle1=None, cle2=None, cle3=None, contenu=None, sett=''):
    tableau_valideur_action = []
    data = {}
    if sett == 'valeurcles' or sett == 'valeurdictionnaire': # si la cle est un dictionnaire qui contient un tableau, retourne les valeurs
        # Dictionnaire
        for dictionnaires in dictionnaire[cle1] :
            if (dictionnaires, (list, tuple)) :
                for cle, val in dictionnaires.items():
                    if val is not None:
                        # cle2 -> est le nom du dictionnaire renfermant directement la cle
                        if cle == cle2 :
                            return val
                        elif not isinstance(val, int) :
                            # cle2 -> doit etre une variable dans la valeur a chercher. Pas la cle
                            if cle2 in val or val == cle2 :
                                return val
    elif sett == '[]-{-valeur':
        for element in dictionnaire[cle1]:
            if element == cle2:
                return element[cle2]

    elif sett == 'tableau' or sett == 'liste': # si le conteneur est un tableau qui contient un dictionnaire, retourne le tableau
        # Dictionnaire
        for key in dictionnaire :
                for cle, val in key.items():
                    if cle == cle1 :
                        tableau_valideur_action.append(cle)
                        data[cle1] = tableau_valideur_action
                return data               
    else :
        print(f'chercher_ds_JSON 1=>{cle1}, 2=>{cle2}, 3=>{cle3}', "fonction", "une des cles manque...")

def detecter_encodage(fichier): # Détecter l'encodage d'un fichier afin de pouvoir le retourner en UTF 8 pour Python
    with open(fichier, 'rb') as f:
        signature = f.read(4)

    if signature.startswith(b'\xff\xfe'):
        return 'utf-16-le'  # UTF-16 Little Endian
    elif signature.startswith(b'\xfe\xff'):
        return 'utf-16-be'  # UTF-16 Big Endian
    elif signature.startswith(b'\xef\xbb\xbf'):
        return 'utf-8-sig'  # UTF-8 avec BOM
    else:
        return 'utf-8'  # Probablement UTF-8 sans BOM

def encodage_UTF(fichier, target='utf-16') : # Lecture et écriture du fichier à transformer the UTF 16 en utf 8. Ceuxci fonctionnent avec d'autres formats tels qu'indiqué dans la fonction qui le précède ' Détecter_encodage'
    target = detecter_encodage(fichier)
    if target != 'utf-8' :
        with open(fichier, 'r', encoding=target) as read :
            UTFCODE = read.read()
        with open(fichier, 'w', encoding='utf-8') as wr :
            wr.write(UTFCODE)
    return fichier

def lireJSON(fichier, cible='', sett=0, code='utf-8'):
    if code != 'utf-8' :
        encodage_UTF(fichier)
    try:
        with open(fichier, 'r', encoding='utf-8') as dictio :
            if sett == 0:
                return json.load(dictio)
    except UnicodeDecodeError : 
        encodage_UTF(fichier)
        lireJSON(fichier=fichier, cible='', set=sett, code=code)


# ---------------------------------------------------------------------
# VARIABLES GLOBALES
# ---------------------------------------------------------------------
dictionnaire_informations = 'Credentials.json'

with open(dictionnaire_informations, 'r', encoding='utf-8') as f:
    dict_cred = json.load(f)

HOST        = dict_cred['HTTP']
USER        = dict_cred['DB_USER']
PASSWORD    = dict_cred['DB_PASSWORD']
LOG_FILE    = dict_cred['LOG_FILE']
dossier_import = dict_cred['IMPORT']
dossier_init= dict_cred['INIT']
DB_NAME = CSV_FILE_RH = CSV_FILE_IN = SQL_FILE_RH = SQL_FILE_IN = None
Confirmation_IN = Confirmation_RH = False
processus_deja_enclenchee = []

# ---------------------------------------------------------------------
# BOUCLES FOR
# ---------------------------------------------------------------------
            # SQL ________________
if os.path.exists(dossier_init):
    for fichier in os.listdir(dossier_init):
        if fichier.endswith('_IN.sql'):
            SQL_FILE_IN = os.path.join(dossier_init, fichier)
        elif fichier.endswith('_RH.sql'):
            SQL_FILE_RH = os.path.join(dossier_init, fichier)
            
            # CSV ________________
if os.path.exists(dossier_import):
    for fichier in os.listdir(dossier_import):
        if fichier.endswith('.csv'):
            if 'db_inv_' in fichier or '_IN'.lower() in fichier or '_IN' in fichier :
                CSV_FILE_IN = os.path.join(dossier_import, fichier)

            elif 'db_rh_' in fichier or '_RH'.lower() in fichier or '_RH' in fichier: 
                CSV_FILE_RH = os.path.join(dossier_import, fichier)


# ---------------------------------------------------------------------
# FONCTIONS ET CLASSES
# ---------------------------------------------------------------------

class MariaDB():
    # ---------------------------------------------------------------------
    # CONFIGURATION
    # ---------------------------------------------------------------------
    def __init__(self, IP, user, password, bd_name, sql_file, log_file, **kwargs):
        super().__init__(**kwargs)
        self.HOST        = IP
        self.USER        = user
        self.PASSWORD    = password
        self.DB_NAME     = bd_name
        self.SQL_FILE    = sql_file
        self.LOG_FILE    = log_file
    # ---------------------------------------------------------------------
    # FONCTIONS UTILITAIRES
    # ---------------------------------------------------------------------

    def log(self, message):
        """Écrit dans un fichier de log avec un timestamp."""
        with open(self.LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.datetime.now()}] {message}\n")
        print(message)
        return message

    def connect(self, database=None):
        """Connexion MySQL, optionnellement à une base donnée."""
        return mysql.connector.connect(
            host=self.HOST,
            user=self.USER,
            password=self.PASSWORD,
            database=database,
            connection_timeout=5,
            autocommit=True
        )

    # ---------------------------------------------------------------------
    # 1. VÉRIFIER SI LA BASE EXISTE
    # ---------------------------------------------------------------------

    def database_exists(self):
        self.conn = self.connect()
        cursor = self.conn.cursor()
        cursor.execute("SHOW DATABASES;")
        exists = self.DB_NAME.lower() in [db[0] for db in cursor.fetchall()]
        # conn.close()
        return exists

    # ---------------------------------------------------------------------
    # 2. CRÉER LA BASE SI NÉCESSAIRE
    # ---------------------------------------------------------------------

    def create_database(self, argument):
        cursor = self.conn.cursor()
        cursor.execute(f"CREATE DATABASE `{argument}`;")
        # self.conn.close()
        self.log(f"✔ Base de données '{argument}' créée.")

    # ---------------------------------------------------------------------
    # 3. IMPORT DU FICHIER SQL
    # ---------------------------------------------------------------------

    def import_sql_file(self, sql_file):
        if not os.path.exists(sql_file):
            self.log(f"❌ Fichier SQL introuvable : {sql_file}")
            return

        self.log(f"⌛ Import du fichier SQL : {sql_file}")
        self.conn = self.connect(self.DB_NAME)
        cursor = self.conn.cursor()

        with open(sql_file, "r", encoding="utf-8") as f:
            sql_content = f.read()

        commands = sql_content.split(";")

        for cmd in commands:
            cmd = cmd.strip()
            if cmd:
                try:
                    cursor.execute(cmd)
                except mysql.connector.Error as e:
                    self.log(f"❌ ERREUR SQL : {e} | Commande : {cmd}")

        # self.conn.close()
        self.log("✔ Import SQL terminé avec succès.")

    # ---------------------------------------------------------------------
    # 4. ENVOYER DES DONNÉES ENSUITE
    # ---------------------------------------------------------------------

    def insert_after_import(self, query, values, bd=None, valideur=[], sett='insertion_mormale'):
        if bd is None or len(valideur) > 1 :
            cursor = self.conn.cursor()
        elif bd is not None and len(valideur) < 1:
            print(valideur)
            self.conn = self.connect(bd)
            cursor = self.conn.cursor()
            valideur.append('Connexion ajoutee')

        # # Exemple d'insertion adaptable
        # query = "INSERT INTO utilisateurs (nom, age) VALUES (%s, %s)"
        # values = ("Ryan", 30)

        try:
            if sett == 'insertion_mormale':
                cursor.execute(query, values)
                # self.conn.commit()
                inserted_id = cursor.lastrowid   # <-- essentiel           
            elif sett == 'insertion_globale': 
                cursor.execute(query, values)
                self.conn.commit()
                
            self.log("✔ Donnée insérée après import.")
                    
        except mysql.connector.Error as e:
            return self.log(f"❌ Erreur d'insertion : {e}")

        cursor.close()
        
        if inserted_id is not None and sett == 'insertion_mormale':
            return inserted_id
        else :
            self.conn.close()
        
     

# ---------------------------------------------------------------------
# PROGRAMME PRINCIPAL
# ---------------------------------------------------------------------

def mysql_save(MYSQL_, query, values=None, sql_file=None, log_file=None, confirmation=None,
               message_debut=None, message_fin=None, message_confirmation=None):
           
    if processus_deja_enclenchee == []:
        if message_debut:
            MYSQL_.log("=== LANCEMENT DU SCRIPT AUTOMATISÉ ===")
        # Étape 1 : vérifier si base existe
        if MYSQL_.database_exists() :
            if message_confirmation is None:
                message_confirmation = f"Base '{MYSQL_.DB_NAME}' déjà existante."           
                MYSQL_.log(message_confirmation)
        else:
            MYSQL_.log(f"Base '{MYSQL_.DB_NAME}' inexistante, création en cours...")
            MYSQL_.create_database(MYSQL_.DB_NAME)            
        # Étape 2 : Import SQL
        if sql_file and message_confirmation is None:
            MYSQL_.import_sql_file(sql_file)
    else :
        message_confirmation = True
            
    # Étape 3 : Insertion de données
    if message_confirmation is None:
        inserted_id = MYSQL_.insert_after_import(query=query, values=values)  
    else : 
        inserted_id = MYSQL_.insert_after_import(query=query, values=values, bd=MYSQL_.DB_NAME, valideur=processus_deja_enclenchee)   
           
    if isinstance(inserted_id, int):    
        if message_fin:
            print(f"{inserted_id}e ligne insérée avec succès !")
            processus_deja_enclenchee.append(True)
        
        return inserted_id
    else :
        Lien = f"{inserted_id}"  

def appel_CSV(sql_fichier, a, b , c , d, e, f, g, h, i, j, k, l, m=None, confirmation=None):
    
    _A = a;      _B = b;         _M = m
    _C = c;      _D = d
    _E = e;      _F = f
    _G = g;      _H = h
    _I = i;      _J = j
    _K = k;      _L = l
    # print(
    #     _A, _B,_C,_D,_E,_F,_G,_H,_I,_J,_K,_L,_M
    # )

    if sql_fichier.endswith('_IN.sql'):
        DB_NAME = dict_cred['DB_IN']
        MYSQL_ = MariaDB(sql_file=sql_fichier, log_file=LOG_FILE, bd_name=DB_NAME, IP=HOST, user=USER, password=PASSWORD)
        mysql_save(MYSQL_=MYSQL_, query="INSERT INTO Produits (\
                                                                                                    produit,\
                                                                                                    types,\
                                                                                                    annee,\
                                                                                                    fabricant,\
                                                                                                    provenance,\
                                                                                                    destination,\
                                                                                                    date_production,\
                                                                                                    liens,\
                                                                                                    quantite,\
                                                                                                    prix,\
                                                                                                    approbations,\
                                                                                                    editeur) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",  
            values=(f"{_A}",
                    f"{_B}",
                    f"{_C}",
                    f"{_D}",
                    f"{_E}",
                    f"{_F}",
                    f"{_G}",
                    f"{_H}",
                    f"{_I}",
                    f"{_J}",
                    f"{_K}",
                    f"{_L}",), sql_file=sql_fichier, message_debut='Actif', confirmation=confirmation,
            message_fin='Actif')



    elif sql_fichier.endswith('_RH.sql'):
        DB_NAME = dict_cred['DB_RH']
        MYSQL_ = MariaDB(sql_file=sql_fichier, log_file=LOG_FILE, bd=DB_NAME, IP=HOST, user=USER, password=PASSWORD)

        
        mysql_save(MYSQL_=MYSQL_, query="INSERT INTO Employe (\
                                                                                                    fonctions,\
                                                                                                    prenom,\
                                                                                                    nom,\
                                                                                                    departement,\
                                                                                                    phone,\
                                                                                                    courriel,\
                                                                                                    privilege,\
                                                                                                    age,\
                                                                                                    entreprise,\
                                                                                                    adresses,\
                                                                                                    date_creation,\
                                                                                                    editeur,\
                                                                                                    liens) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",  
            values=(f"{_A}",
                    f"{_B}",
                    f"{_C}",
                    f"{_D}",
                    f"{_E}",
                    f"{_F}",
                    f"{_G}",
                    f"{_H}",
                    f"{_I}",
                    f"{_J}",
                    f"{_K}",
                    f"{_L}", f"{_M}"), sql_file=sql_fichier, message_debut='Actif', confirmation=confirmation,
            message_fin='Actif')
                
    return MYSQL_
def enregistrement_des_fichiers(CSV_FILE, sql_fichier, a, b , c, d, e, f, g, h, i, j, k, l, m=None, confirmation=None):
    if CSV_FILE:
        if os.path.exists(CSV_FILE):
            with open(CSV_FILE, newline='', encoding='utf-8') as fre:
                dict_ = csv.DictReader(fre)

                if dict is not None:
                    for dict_json in dict_:
                        if m is not None: # BD_RH
                            MYSQL_ = appel_CSV(sql_fichier, dict_json[a], dict_json[b], dict_json[c], dict_json[d], dict_json[e], 
                                    dict_json[f], dict_json[g], dict_json[h], dict_json[i], dict_json[j],
                                    dict_json[k], dict_json[l], dict_json[m], confirmation=confirmation)
                        else: # BD_INV
                            MYSQL_ = appel_CSV(sql_fichier, dict_json[a], dict_json[b], dict_json[c], dict_json[d], dict_json[e], 
                                    dict_json[f], dict_json[g], dict_json[h], dict_json[i], dict_json[j],
                                    dict_json[k], dict_json[l], confirmation=confirmation)
                    MYSQL_.log("=== FIN DU SCRIPT AUTOMATISÉ ===")
                    MYSQL_.conn.close()
                    
                else :
                    print(f"Le fichier {CSV_FILE} est vide !")
        else:
            print(f'Le fichier appelé nommé [ {CSV_FILE} ] est introuvable !')
    else : 
        print(f"Nom du fichier CSV : {CSV_FILE}... Probleme rencontree : Ligne 330 a 334")
        
def main():
    
    print(f"\n\n{CSV_FILE_RH} + {SQL_FILE_RH} + {CSV_FILE_IN} + {SQL_FILE_IN}\n\n")
    # exit()
    if CSV_FILE_RH and SQL_FILE_RH:
        enregistrement_des_fichiers(CSV_FILE_RH, SQL_FILE_RH, '_FONCTION', '_PRENOM', '_NOM', '_DEPARTEMENT', '_PHONE', '_COURRIEL', '_PRIVILEGE', 
                                    '_AGE', '_ENTREPRISE', '_ADRESSE', '_DATE_RH', '_EDITEUR_RH', '_LIEN', confirmation=Confirmation_RH)
    if CSV_FILE_IN and SQL_FILE_IN:
        enregistrement_des_fichiers(CSV_FILE_IN, SQL_FILE_IN, '_PRODUIT', '_TYPE', '_ANNEE', '_FABRICANT', '_PROVENANCE', '_DESTINATION', '_DATE_IN',
                            '_LIEN', '_QUANTITE', '_PRIX', '_APPROBATIONS', '_EDITEUR_IN', confirmation=Confirmation_IN)
       
# LANCEMENT
if __name__ == "__main__":
    main()
