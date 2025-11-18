import os, sys
import platform, importlib
# ________________COMPARER
import json
import difflib
import pprint
# ________________
import math
import random
import json
import re
import ctypes
import  datetime
import subprocess as psh
import traceback

def resoudre_chemins(chemin_I, chemin_II):
   if os.path.exists(chemin_I) :
       return chemin_I
   else : 
       return chemin_II
try :
    from dotenv import load_dotenv
    from pymongo import MongoClient   
    import logging 
    import psutil
except ModuleNotFoundError as m :
    print ('Pas de module associee')
    import traceback
    print("\033[1;31m", traceback.extract_tb(sys.exc_info()[2]), 'FileNotFoundError', m, "\033[0m")
        
    cibles = [ 'kivy', "pymongo", "python-dotenv" ]
    
    for cible in cibles:
        if cible in f"{m}":
            
            print("----------->", f"{cible} en manque...")
            
            packages = {
                "psutil": "psutil",
                "pymongo": "pymongo",
                "dotenv": "python-dotenv"
            }
            
            DossierPrincipal = resoudre_chemins("D:\\_A\\GitHub\\Delifruit_Implantation\\R_Inventaire",
                                                "D:\\UCDownloads\\OneDrive\\A2025\\Implantation_reseau\\ESP\\Delifruit_Implantation\\R_Inventaire")
            
            _venvI = f'{DossierPrincipal}\\.venv\\Scripts\\activate'
            _venvII = '.\\.venv\\Scripts\\activate'

            for module, package in packages.items():
                try:
                    importlib.import_module(package)
                    print(f"{package} est déjà installé.")
                except ImportError:
                    print(f"{package} manquant. Installation...")
                    try:
                        systeme = platform.system() 
                        if systeme == "Linux" :
                            psh.check_call(['python3', "-m", "pip", "install", "--upgrade", package], stdout=psh.DEVNULL, stderr=psh.STDOUT,)
                            
                        elif systeme == "Windows" :
                            psh.check_call([sys.executable, "-m", "pip", "install", "--upgrade", package])
                            try: 
                                psh.check_call([sys.executable, "-m", "pip", "install", "--upgrade", 'pip', 'setuptools', 'venv'])
                            except psh.CalledProcessError as p :
                                print('Functions', '-> subprocess.CalledProcessError ->', p)
                            if os.path.exists(_venvI):
                                psh.check_call([sys.executable, "-m", _venvI])
                            elif os.path.exists(_venvII):
                                psh.check_call([sys.executable, "-m", _venvII])
                        print(f"{package} installé avec succès.")
                    except psh.CalledProcessError as e:
                        print(f"Échec de l'installation de {package}.")
                        print("Erreur :", e)
                        exit(1)
#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------

# import importlib.util
# import os

# chemin = r"D:/UCDownloads/OneDrive/H2025/DÉVELOPPEMENT D'APPLICATIONS AVEC DES OBJETS... - 420-473-SH"
# fichier = os.path.join(chemin, "Functions.py")

# spec = importlib.util.spec_from_file_location("Functions", fichier)
# Functions = importlib.util.module_from_spec(spec)
# spec.loader.exec_module(Functions)

# ##################################################### D E F I N I T I O N S ######################################################################################
DossierPARENT = os.environ.get('PYTHR')
DossierInterfaceApp = os.environ.get('CONSOLE')
DossierLOGPY = f"{DossierInterfaceApp}\\The_Beginning\\log"
LOGERREUR = f"{DossierLOGPY}\\erreurs.txt"
fichier_conf = "conf.txt"
fichier_configuration = f"{DossierLOGPY}\\{fichier_conf}"

DossierLOG = os.environ.get('LOG')
contenuFichier = f"{DossierLOG}\\A_Ref_Notifications.txt"
fichierTemp = f"{DossierLOG}\\temp.txt"

print(DossierLOG)

# Pour Windows
def effacer_ecran() : # Efface l'écran
    if os.name == 'nt':
        os.system('cls')  # Efface l'écran sur Windows
        
# _______________________________________________________________________________
def __restart__(): # Redemarre le script comme l'application
    USER = os.getlogin()
    programme = os.path.abspath(__file__)
    psh.Popen(
        [ f"C:/Users/{USER}/AppData/Local/Microsoft/WindowsApps/python3.13.exe",
         f"{programme}"
         ]
    )
    sys.exit()        
# _______________________________________________________________________________        

        
# C o u l e u r
start_color = "\033[1;32m"
end_color = "\033[0m"

Rouge = "\033[1;31m"
Green = "\033[1;32m"
Jaune = "\033[1;33m"
Violet = "\033[1;35m"
Cyan = "\033[1;36m"
Bleu = "\033[1;34m"
Red = "\033[1;41m"
Blue = "\033[1;44m"
Yellow = "\033[1;43m"
Magenta = "\033[1;45m"

# <style> : Définit le style du texte (facultatif) :
# 0 : Reset (par défaut)
# 1 : Texte en gras
# 4 : Souligné
# 7 : Inverse (texte et arrière-plan échangés)
# <text color> : Définit la couleur du texte (0–7) :
# 30 : Noir
# 31 : Rouge
# 32 : Vert
# 33 : Jaune
# 34 : Bleu
# 35 : Magenta
# 36 : Cyan
# 37 : Blanc
# <background color> : Définit la couleur d'arrière-plan (40–47) :
# 40 : Noir
# 41 : Rouge
# 42 : Vert
# 43 : Jaune
# 44 : Bleu
# 45 : Magenta
# 46 : Cyan
# 47 : Blanc
# Pour terminer le formatage, utilisez \033[0m.


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------

def color (colour, value) : # Couleur neutre, Pas de qualification
    final = colour, value, end_color
    return final

def colorPrint_(colour="", message1="", message2="", setting=0) : # Fonction d'affichage avec couleur
    
    if message2 == "" and setting == 0 :
        print (f"{colour}{message1}{end_color}")
    elif message2 != "" and setting == 0 :
        print (f"{message2}{colour}{message1}{end_color}")
        
    elif setting == 1 and len(message2) == 3 :
            print(message1.format(f"{Green}{message2[0]}{end_color}", f"{Green}{message2[1]}{end_color}", f"{Green}{message2[2]}{end_color}"))
    elif setting == 1 and len(message2) == 4 :
            print(message1.format(f"{Green}{message2[0]}{end_color}", f"{Green}{message2[1]}{end_color}", f"{Green}{message2[2]}{end_color}", f"{Green}{message2[3]}{end_color}"))
            
    else :
        print(Rouge, "Fonction d'affichage incompatible", end_color)
        
def colorPrint(colour="", message1="", message2="", setting=0):
    colorPrint_(colour=colour, message2=message2, message1=message1, setting=setting)
        
        
def checkResult (valeur) : # Fonction d'affichage de résultats, Avec exception
    try :
        result = valeur
    except ZeroDivisionError :
        result = "Quelque chose cloche"
    except TypeError :
        result = "Le type d'erreur: "
    finally :
        return result    
    
#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------

def rapporter_erreur(contenu): # Rapporte les erreurs Dans un fichier Erreur.TXT
    fichier = LOGERREUR
    dateErreur = datetime.datetime.now()
    with open(fichier, 'a') as edit:
        edit.write(f"{dateErreur.strftime("%d-%B-%Y-%H-%M-%S")} : {contenu}\n")
        print(f"{fichier} a été enregistré")

def errorPrint(NomErreur='', NomFonction='', ValeurErreur='', tabErreur=[], set=0): # Affiche les erreurs avec une couleur rouge forte ou Simple
    
    if tabErreur == []:
        if set == 0:
            colorPrint(Rouge, ValeurErreur, f"{NomErreur} '{NomFonction}' : ")
        elif set == 1 :
            colorPrint(Red, ValeurErreur, f"{NomErreur} '{NomFonction}' : ")
    elif tabErreur is not None:
        tabErreurs = tabErreur[-1]
        NoErreur = tabErreurs.lineno
        NomFonction = tabErreurs.name
        if set == 0:
            colorPrint(Rouge, ValeurErreur, f"[{NoErreur}] {NomErreur}=>'{NomFonction}' : ")
        elif set == 1 :
            colorPrint(Red, ValeurErreur, f"[{NoErreur}] {NomErreur}=>'{NomFonction}' : ")

    rapporter_erreur(f"{NomErreur} '{NomFonction}' : {ValeurErreur}")
    return f"{NomErreur} '{NomFonction}' : {ValeurErreur}"
    
#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------
 
    
    

def choice(ranges) : # Réalise une suite de couleurs à partir d'un Random
    for i in range(1, 11) :
        for u in ranges :
            rand = random.randint(u, 30)
            for j in ranges :
                rand = random.randint(-30, j)
        
        if (rand <= -100 or rand >= -30) :
            print(f"Couleur {i} : {Violet}Bleu{end_color}")
            
        elif (rand <= -29 or rand >= -10) :
            print(f"Couleur {i} : {Green}Vert{end_color}")
            
        elif (rand <= -9 or rand >= 10) :
            print(f"Couleur {i} : {Jaune}Jaune{end_color}")
            
        elif (rand <= 11 or rand >= 30) :
            print(f"Couleur {i} : {Violet}Orange{end_color}")
            
        elif (rand <= 31 or rand >= 100) :
            print(f"Couleur {i} : {Rouge}Rouge{end_color}")
                        
        else : 
            print(f"{Rouge}inconnu...{end_color}")
        

liste0 = []

def choice(n, pack) : # Méthode inférieure servant à choisir une couleur pour l'affichage, Couleur verte par défaut
    match n:
        case "Affiche" :
            for i in pack :
                print(", ".join(f"{Green}{i}{end_color}"))
            return
        case _:
            return
        
def check (element) : # Vérifie si un élément se trouve dans une liste
    found = False
    for contenu in liste0 :
        
        if (element == "Affiche") :
            print(Green, ", ".join(liste0), end_color)
            found = True
            break
        
        if (element == contenu) :
            print(f"{Green}{element}{end_color} est dans la liste")     
            found = True             

    if found == False :
        print(f"{Violet}{element}{end_color} n’est pas dans la liste")
        liste0.append(element) 


def OutOfRange (Entree, tableau, functionName) : # Vérifie Les limites d'une valeur par rapport à la taille d'un tableau
    longueur = len(tableau)
    if Entree >= longueur or  Entree < 0 : 
        print(f"{Rouge}{functionName} : Ce nombre depasse le nombre acceptee par le programme...\nVueillez reprendre...{end_color}")
        return 0
    else :
        return 1



#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------
        
        
def intChecking () : # Vérifie L'entrée est positive Et se trouve être un integer. Le cycle se répète tant que la valeur n'est pas correcte
    Entree = ""
    while (Entree != 'q') :
    # V a r i a b l e s
        Entree = input(f"\ndonner un nombre : ")
        if Entree == 'q':
            break
        elif Entree == '':
            break
        else :
            nbrePairImpair = int(Entree)
            # n = nbrePairImpair  
            
        
#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------

def dossierNotExist(dossier, set='') : # Vérifie si un Dossier existe sinon il le craignent
    if not os.path.exists(dossier) and set == 'd' :
        os.makedirs(dossier, exist_ok=True)
    if not os.path.exists(dossier) and set == 'f' :
        with open(dossier, 'a') as wr :
            wr.write('')


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------

# /////////////////////// 02 --> CONNEXION : CREDENTIAL /////////////////////////
def recuperateur (dossier, fichier, cible, SEPARATEUR="=", sett='') : # Récupère la valeur se trouvant dans un fichier à partir de son mot clé. Un séparateur est utilisé afin de pouvoir faire la différence entre la clé et sa valeur
    """Récupère les informations de connexion à partir d'un fichier spécifique.
    Args:
    Credentiel: Variable contenant la fonction lireFiDict()Destinée à récupérer les identifiants de connections.
    Returns:
    Retourne à l'information prélevée du dictionnaire prudentiel.
    """
    credential = lireFiDict(dossier, fichier, SEPARATEUR, set=sett)
    if sett == '' :
        for key, detailsConnect in credential.items() :
            if key == cible :
                information = detailsConnect
                return information
    else :
        # colorPrint(Green, f"{credential} a été lu avec succès")
        return credential
# sys.path.append("D:/UCDownloads/OneDrive/H2025/DÉVELOPPEMENT D'APPLICATIONS AVEC DES OBJETS... - 420-473-SH")  # Ajouter le dossier au PATH
# import Functions


# chemin = "D:/UCDownloads/OneDrive/H2025/DÉVELOPPEMENT D'APPLICATIONS AVEC DES OBJETS... - 420-473-SH"
# sys.path.append(chemin)
# import Functions
#print("Contenu du dossier :", os.listdir(chemin))  # Afficher les fichiers du dossier

#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------

def trouverFichiers (folder, setting=0) : # Recherche dans un sous répertoire à partir D'un Répertoire spécifique
    if setting == 0 :
        dossier = os.chdir(folder)
    elif setting == 1 :
        dossiers = os.listdir(folder)
        for dossier in dossiers :
            if dossier == folder :
                os.chdir(dossier)
    return dossier

#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------

def recherche_complete(chemin, set='dossier_fichier'): # Fonction officielle de recherche de fichiers dossiers Dans tous les répertoires possibles
    resultat = []
    for racine, dossiers, fichiers in os.walk(chemin) :
        if set == 'dossier_fichier' :
            for nom in fichiers + dossiers:
                objet = os.path.abspath(os.path.join(racine, nom))
                resultat.append(objet)
        if set == 'dossier' :
            for dossier in dossiers:
                dossier = os.path.abspath(os.path.join(racine, dossier))
                resultat.append(dossier)
        if set == 'fichier' :
            for fichier in fichiers:
                fichier = os.path.abspath(os.path.join(racine, fichier))
                resultat.append(fichier)
    return resultat

def recherche_specifique(chemin, extension='.txt'): # Fonction officielle de Recherche d'un fichier spécifique Avec une extension spécifique
    resultat_specifique = []
    for racine, _, fichiers in os.walk(chemin) :
        for fichier in fichiers :
            if fichier.lower().endswith(extension) :
                    fichier = os.path.abspath(os.path.join(racine, fichier))
                    resultat_specifique.append(fichier)
    return resultat_specifique



#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------



#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------

def rechercherElement(cible, intervalle_debut='C', intervalle_fin='F'): # PSH + Py : Recherche d'un fichier/dossier dans tout le système où les répertoires du système de fichiers

    nbre = [chr(i) + ':\\' for i in range(ord(f'{intervalle_debut}'), ord(f'{intervalle_fin}')+1)]
    SCRIPT = f"""
    $Drivers = @({','.join(f"'{d}'" for d in nbre)})
        Get-ChildItem -Path $Drivers -Recurse -Filter '{cible}' -ErrorAction SilentlyContinue |
        Select-Object -ExpandProperty FullName
    """
    print("Debut de la resolution des variables...")
    result = psh.run(['Powershell.exe', '-Command', SCRIPT],
                capture_output=True, text=True)
    RESULTO = f"{result.stdout}"
    print(RESULTO)
    return RESULTO

#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------

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
#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------

def lireFiDict (folder, fichier, SEPARATEUR="=", set='') : # CFR Récupérateur() : Est utilisé pour vérifier tous les Occurrence dans un fichier. Serre à la fonction récupérateur()
    
    trouverFichiers (folder) 
    
    dictionnaire = {}
    
    with open(fichier, 'r') as lire :

        for ligne in lire :
            ligne = ligne.strip()
            if ligne == '' or ligne.startswith('#') :
                continue
            mots = ligne.replace(SEPARATEUR, " ").strip().split()
            
            if len(mots) >= 2 :
                avant, apres = mots[0], " ".join(mots[1:])
                if set == '' :
                    dictionnaire[avant] = apres
                else :
                    dictionnaire[avant] = avant 
                
    return dictionnaire



#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- JSON -----------------------------------------
#   -----------------------------------------------------------------------------------------------

def chercher_ds_JSON(dictionnaire, cle1=None, cle2=None, cle3=None, contenu=None, sett=''):
    tableau_valideur_action = []
    data = {}
    if cle1 is not None and cle2 is not None and sett == '' :
        index = next(i for i, d in enumerate(dictionnaire[cle1]) if cle2 in d)
        if sett == '' :
            dictionnaire[cle1][index][cle2] = contenu
            return dictionnaire
        else :
            return dictionnaire[cle1][index][cle2]     
                   
    elif sett == 'cles' or sett == 'dictionnaire': # si la cle est un dictionnaire qui contient un tableau, retourne le tableau
        # Dictionnaire
        for dictionnaires in dictionnaire[cle1] :
            if (dictionnaires, (list, tuple)) :
                for cle, val in dictionnaires.items():
                    tableau_valideur_action.append(cle)
                    data[cle1] = tableau_valideur_action
        return data

    elif sett == 'valeurcles' or sett == 'valeurdictionnaire': # si la cle est un dictionnaire qui contient un tableau, retourne les valeurs
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
    
    elif sett == '{[]}-valeur' :
        for key, tableau in dictionnaire.items():
            if key == cle1:
                for tab in dictionnaire[cle1]:
                    for titre, valeur in tab.items():
                        return valeur
                    
    elif sett == '{-[]-{}-[]' or sett == 'tableau-dictio' :
        for key, valeurs in dictionnaire.items():
            if key == cle1:
                for tab in valeurs:
                    for tableau in tab :
                        try :
                                return tableau
                        except Exception as e:
                            colorPrint_(Violet, f"{e}: -> {tableau}"); exit()
                        
    elif sett == '{[]}-dictionnaires' :
        for key, tableau in dictionnaire.items():
            if key == cle1:
                for tableau in dictionnaire[cle1]:
                    for titre, valeur in tableau.items():
                        data[titre] = valeur
                return data

    elif sett == 'valeurtableau' or sett == 'valeurliste': # si le conteneur est un tableau qui contient un dictionnaire, retourne les valeurs
        # Dictionnaire
        for key in dictionnaire :
            for cle, val in key.items():
                if cle == cle1 :
                    tableau_valideur_action.append(cle)
        return tableau_valideur_action


    else :
        errorPrint(f'chercher_ds_JSON 1=>{cle1}, 2=>{cle2}, 3=>{cle3}', "fonction", "une des cles manque...")

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
        

def ecrire_ds_json(fichier, dictionnaire=None, contenu=None, cle1=None, cle2=None, cle3=None, val=None, indent=4, sett='normal'): # Écrit dans un fichier
    data = {}
    try :
        if sett == 'normal' and dictionnaire is None:
            with open(fichier, "w", encoding="utf-8") as edit:
                json.dump(contenu, edit, indent=indent, ensure_ascii=False)
        elif sett == 'remplacer' and dictionnaire is not None :
            if dictionnaire is not None and contenu is not None :
                if isinstance(dictionnaire[cle1], (list, tuple)) and cle2 is not None and cle3 is None :
                    contenu = chercher_ds_JSON(dictionnaire=dictionnaire, cle1=cle1, cle2=cle2, cle3=cle3, contenu=contenu)
                elif cle1 is not None and isinstance(dictionnaire[cle2], (list, tuple)) and cle3 is None :
                    contenu = chercher_ds_JSON(dictionnaire=dictionnaire, cle1=cle1, cle2=cle2, cle3=cle3, contenu=contenu)
                elif cle1 is not None and cle2 is not None and isinstance(dictionnaire[cle3], (list, tuple)) :
                    contenu = chercher_ds_JSON(dictionnaire=dictionnaire, cle1=cle1, cle2=cle2, cle3=cle3, contenu=contenu)
                elif not isinstance(dictionnaire[cle1], (list, tuple)) and cle2 is not None and cle3 is None :
                    contenu = chercher_ds_JSON(dictionnaire=dictionnaire, cle1=cle1, cle2=cle2, cle3=cle3, contenu=contenu)
                # ECRIRE
                ecrire_ds_json(fichier, contenu, indent)

            else :
                if cle1 is not None and cle2 is None and cle3 is None :
                    # 1. Modification (ajout dans hobbies)
                    dictionnaire[cle1] = val
                elif cle1 is not None and cle2 is not None and cle3 is None :
                    # 2. Modification (ajout dans hobbies)
                    dictionnaire[cle1][cle2] = val
                elif cle1 is not None and cle2 is not None and cle3 is not None :
                    # 3. Modification (ajout dans hobbies)
                    dictionnaire[cle1][cle2][cle3] = val
                # ECRIRE
                ecrire_ds_json(fichier, val, indent)
            with open(fichier, "w", encoding="utf-8") as edit:
                json.dump(dictionnaire, edit, indent=indent, ensure_ascii=False)
        elif sett == 'direct':
            with open(fichier, "w", encoding="utf-8") as edit:
                json.dump(dictionnaire, edit, indent=indent, ensure_ascii=False)
    except UnicodeEncodeError as u :
        return errorPrint('UnicodeEncodeError', 'ecrire_ds_fichier', u)
            
def rajouter_ds_json(fichier, dictionnaire:dict, contenu=None, cle1=None, cle2=None, cle3=None, sett=0, indent=4): # Rajoute un élément à un fichier. Simple Fonction
    data = {}
    try :
        if sett == 0:
            if cle1 is not None and cle2 is None and cle3 is None :
                # 2. Modification (ajout dans hobbies)
                data[cle1].append(contenu)
            elif cle1 is not None and cle2 is not None and cle3 is None :
                # 2. Modification (ajout dans hobbies)
                data[cle1][cle2].append(contenu)                
            elif cle1 is not None and cle2 is not None and cle3 is not None :
                # 2. Modification (ajout dans hobbies)
                data[cle1][cle2][cle3].append(contenu)                
            ecrire_ds_json(fichier, contenu, indent)
        elif sett == 1:
            ecrire_ds_json(fichier, contenu, indent)
        # DICTIONNAIRE
        elif sett == 2:
            if cle1 is not None and cle2 is None and cle3 is None :
                # 2. Modification (ajout dans hobbies)
                dictionnaire[cle1].append(contenu)
            elif cle1 is not None and cle2 is not None and cle3 is None :
                # 2. Modification (ajout dans hobbies)
                dictionnaire[cle1][cle2].append(contenu)                
            elif cle1 is not None and cle2 is not None and cle3 is not None :
                # 2. Modification (ajout dans hobbies)
                dictionnaire[cle1][cle2][cle3].append(contenu) 
            ecrire_ds_json(fichier, dictionnaire, indent)
        elif sett == 4:
            with open(fichier, "a", encoding="utf-8") as edit:
                json.dump(dictionnaire, edit, indent=indent, ensure_ascii=False)
            
    except UnicodeEncodeError as u :
        err = errorPrint(tabErreur=traceback.extract_tb(sys.exc_info()[2]), NomErreur='UnicodeEncodeError', ValeurErreur=u)
        ecrire_ds_fichier(fichierTemp, err)
            
def rajout_avancee_ds_json(fichier, contenu=None, cle1=None, cle2=None, cle3=None, sett=0, indent=4): # Rajoute un élément à un fichier en vérifiant si ce dernier n'existe pas déjà dans le fichier
    checking = lireJSON(fichier=fichier, sett=1)

    if contenu not in checking :
            data = {}
            try :
                if sett == 0:
                    if cle1 is not None and cle2 is None and cle3 is None :
                        # 1. cle1
                        data[cle1].append(contenu)
                    elif cle1 is not None and cle2 is not None and cle3 is None :
                        # 2. cle1, cle2
                        data[cle1][cle2].append(contenu)                
                    elif cle1 is not None and cle2 is not None and cle3 is not None :
                        # 3. cle1, cle2 et cle3
                        data[cle1][cle2][cle3].append(contenu)                
                    ecrire_ds_json(fichier, contenu, indent)
                elif sett == 1:
                    ecrire_ds_json(fichier, contenu, indent)
            except UnicodeEncodeError as u :
                err = errorPrint(tabErreur=traceback.extract_tb(sys.exc_info()[2]), NomErreur='UnicodeEncodeError', ValeurErreur=u)
                ecrire_ds_fichier(fichierTemp, err)
    else :
        print("ligne deja existante...")
        
def supprimer_ds_json(fichier, dictionnaire=None, contenu=None, cle1=None, cle2=None, cle3=None, val=None, sett=0, indent=4):
    data = {}
    try :
        if sett == 0 and val is None and dictionnaire is None:
            if cle1 is not None and cle2 is None and cle3 is None :
                # 1. cle1 seul
                del data[cle1]
            elif cle1 is not None and cle2 is not None and cle3 is None :
                # 2. cle1 et cle2
                del data[cle1][cle2]               
            elif cle1 is not None and cle2 is not None and cle3 is not None :
                # 3. cle1, cle2 et cle3
                del data[cle1][cle2][cle3]               
            ecrire_ds_json(fichier, contenu, indent)
            
        elif sett == 0 and val is not None and dictionnaire is None:
            if cle1 is not None and cle2 is None and cle3 is None :
                # 1. cle1 seul
                data[cle1].remove(val)
            elif cle1 is not None and cle2 is not None and cle3 is None :
                # 2. cle1 et cle2
                data[cle1] = [x for x in data[cle1] if x.get(cle2) != val]
            elif cle1 is not None and cle2 is not None and cle3 is not None :
                # 3. cle1, cle2 et cle3
                data[cle1][cle2][cle3] 
                data[cle1][cle2] = [x for x in data[cle1][cle2] 
                                    if all(v.get(cle3) != val for v in x.values())]    
                ecrire_ds_json(fichier, contenu, indent)           
        elif sett == 0 and dictionnaire :
            if cle1 is not None and cle2 is None and cle3 is None :
                # 1. cle1 seul
                del dictionnaire[cle1]
            elif cle1 is not None and cle2 is not None and cle3 is None :
                # 2. cle1 et cle2
                # for sous_dict in dictionnaire[cle1]:
                #     if cle2 in sous_dict:
                #         del sous_dict[cle2]
                        
                # dictionnaire[cle1] = [x for x in dictionnaire[cle1] if x != {} and x != {"": ""}]
                for sous_dict in dictionnaire[cle1][:]:  # [:] = copie pour éviter problèmes en modifiant en place
                    if cle2 in sous_dict:
                        del sous_dict[cle2]
                    if not sous_dict:  # supprime dict vide
                        dictionnaire[cle1].remove(sous_dict)
            
            ecrire_ds_json(fichier, dictionnaire, indent, sett='direct')
        elif sett == 1:
            ecrire_ds_json(fichier, contenu, indent)
    except UnicodeEncodeError as u :
        err = errorPrint(tabErreur=traceback.extract_tb(sys.exc_info()[2]), NomErreur='UnicodeEncodeError', ValeurErreur=u)
        ecrire_ds_fichier(fichierTemp, err)

#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- LECTURE [LECT] [READ] [RD] -----------------------------------------
#   -----------------------------------------------------------------------------------------------

def lireFile(fichier, comment='', set=0, code='utf-8') : # Fichier en format d'encodage UTF 8. Lecture efficace Récupère les lignes de fichiers les unes après les autres en effaçant les espaces et les sauts de ligne. Options secondaires pour laisser les sauts de ligne
    if code != 'utf-8' :
        encodage_UTF(fichier)
    try:
        with open(fichier, 'r', encoding='utf-8') as listFichier :
            if comment != '' :
                print(f"{fichier} en cours de lecture")
            if set == 0 :
                return [ligne.rstrip('\n') for ligne in listFichier.readlines() if ligne != '' and ligne != '\n' and ligne is not None]
            elif set == 1 :
                return listFichier.readlines()
            else :
                return listFichier.read()

    except UnicodeDecodeError : 
        encodage_UTF(fichier)
        lireFichier(fichier=fichier, comment=comment, set=set, code=code)

def lireFichier(fichier) : # Fichier en format d'encodage UTF 8. Lecture efficace Récupère les lignes de fichiers les unes après les autres en effaçant les espaces et les sauts de ligne. Options secondaires pour laisser les sauts de ligne
    with open(fichier, 'r') as read :
        return read.read()
    

#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- ECRIRE [ECR] [WRITE] [WR] -----------------------------------------
#   -----------------------------------------------------------------------------------------------

def creerSupp(fichier, valeur) : # Écrit dans un fichier Elle efface si jamais une erreur est détectée lors de l'écriture
    with open(fichier, 'w') as wr :
        try :
            wr.write(valeur)
        except TypeError as t :
            rapporter_erreur(f"TypeError dans creerSupp() dans _Functions :  {t}")
            wr.write('')

def ecrire_ds_fichier(fichier, contenu, encoding='utf-8', comment=''): # Écrit dans un fichier
    try :
        if encoding == '' :
            with open(fichier, 'w') as edit:
                edit.write(f"{contenu}")
        else :
            with open(fichier, 'w', encoding=encoding) as edit:
                edit.write(f"{contenu}")
        if comment != '':
            colorPrint(Jaune, f"{fichier} a été créé")
    except UnicodeEncodeError as u :
        errorPrint('UnicodeEncodeError', 'ecrire_ds_fichier', u)
            
def rajouter_ds_fichier(fichier, contenu): # Rajoute un élément à un fichier. Simple Fonction
    try :
        with open(fichier, 'a') as edit:
            edit.write(contenu)
            colorPrint(Jaune, f"{fichier} a recu un ajout")
    except UnicodeEncodeError as u :
        err = errorPrint(tabErreur=traceback.extract_tb(sys.exc_info()[2]), NomErreur='UnicodeEncodeError', ValeurErreur=u)
        ecrire_ds_fichier(fichierTemp, err)
            
def rajout_avancee_ds_fichier(fichier, contenu): # Rajoute un élément à un fichier en vérifiant si ce dernier n'existe pas déjà dans le fichier
    checking = lireFile(fichier=fichier, set=1)

    if contenu not in checking :
        with open(fichier, 'a') as edit:
            edit.write(f"\n{contenu}")
            colorPrint(Jaune, f"{fichier} a été enregistré")
    else :
        print("ligne deja existante...")

            
def attacher_file_au_chemin(dossier='', fichierI=None, fichierII=None, chemin_de_base=None, chemin_complet=None, 
                            SEPARATEUR=None, intervalle_debut='C', intervalle_fin='F'): # Recherche tous les occurrences d'un mot dans tout le système de fichiers et retourne le chemin complet de ce fichier ou de ce chemin dans un fichier spécifique. Un élément séparateur est proposé pour pouvoir vérifier la chose et l'écrire de cette manière. Fonctions complexes
    if chemin_complet is not None:
        fichierI = chemin_complet
    elif dossier != '' and fichierI != '':
        fichierI = f"{dossier}\\{fichierI}"
    
    if chemin_de_base is None:        
        chemin_officiel = recuperateur(DossierLOGPY, fichier_conf, 'chemin_officiel')
    else :
        chemin_officiel = chemin_de_base
    # Sous-Fonction de controle :
    def Rechercher_comparer(fichierI, fichierII, SEPARATEUR=None, intervalle_debut='C', intervalle_fin='F', sett='fichier'):
        if sett == 'fichier':
            nomApp = lireFile(fichier=fichierI)
            for i in nomApp : 
                if '.' in i :     
                    print(f"{i}{SEPARATEUR}")
                    comparaison = chercher_ds_fichier(pattern=f"{i}{SEPARATEUR}", fichier=fichierII)       
                    # print(i, '<-->', comparaison)
                    if comparaison == None or comparaison == '':        
                        RESULTO = rechercherElement(i, intervalle_debut=intervalle_debut, intervalle_fin=intervalle_fin)
                        if RESULTO != '' and RESULTO is not None :
                            contenu = f"{i}{SEPARATEUR}{RESULTO}" 
                            print(contenu)
                            if not os.path.exists(fichierII):
                                ecrire_ds_fichier(fichierII, contenu)
                            else :
                                rajout_avancee_ds_fichier(fichierII, contenu)
        else :
            nomApp = fichierI
            if isinstance(nomApp, (tuple, list)) :
                for i in nomApp : 
                    if '.' in i :  
                        RESULTO = rechercherElement(i, intervalle_debut=intervalle_debut, intervalle_fin=intervalle_fin)
                        if RESULTO != '' and RESULTO is not None :
                            contenu = RESULTO
                            print(contenu)
                            contenu = contenu.rstrip()
                            if os.path.exists(fichierII):
                                dictio = lireJSON(fichier=fichierII)
                                ecrire_ds_json(fichier=fichierII, dictionnaire=dictio, contenu=contenu, cle1=SEPARATEUR, cle2=nomApp, sett='remplacer')
            else :
                if '.' in nomApp :  
                    RESULTO = rechercherElement(nomApp, intervalle_debut=intervalle_debut, intervalle_fin=intervalle_fin)
                    if RESULTO != '' and RESULTO is not None :
                        contenu = RESULTO
                        print(contenu)
                        contenu = contenu.rstrip()
                        if os.path.exists(fichierII):  
                            dictio = lireJSON(fichier=fichierII)
                            ecrire_ds_json(fichier=fichierII, dictionnaire=dictio, contenu=contenu, cle1=SEPARATEUR, cle2=nomApp, sett='remplacer')

    if chemin_officiel != DossierPARENT and '%' not in DossierPARENT :
        Rechercher_comparer(fichierI, fichierII, '|->|', intervalle_debut, intervalle_fin)
    elif chemin_officiel != DossierPARENT and '%' in DossierPARENT :
        Rechercher_comparer(fichierI, fichierII, '==', intervalle_debut, intervalle_fin)
    elif fichier_conf in fichierII :
        Rechercher_comparer(fichierI, fichierII, '==>', intervalle_debut, intervalle_fin)
    elif '.json' in fichierII :
        Rechercher_comparer(fichierI, fichierII, SEPARATEUR=SEPARATEUR, sett='dictionnaire')
            

#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------

def inscription_ds_fichier(fichier_d_ecriture, result_fichier, verifier=None): # Si résultats se trouvent dans un fichier Effectue la recherche dans le système de fichiers pour trouver le chemin ou la valeur correspondante. Ci trouvé retourne les informations dans le fichier
    try:
        for resultat in result_fichier:
            if os.path.exists(fichier_d_ecriture) :
                verifier = [ i for i in lireFile(fichier_d_ecriture) if resultat == i ]
                print(verifier)
            if verifier == [] or verifier is None :                
                rajouter_ds_fichier(fichier_d_ecriture, f"{resultat}\n")
    except UnicodeEncodeError as u :
        errorPrint('UnicodeEncodeError', 'repertorier_fichier.py', u)

#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------

def success(texte): # Affiche l'information en couleur Verte
    colorPrint(Green, texte)
    
def erreur(texte): # Affiche l'information en couleur rouge Simple
    colorPrint(Rouge, texte)
    
def warnings(texte): # Affiche l'information en couleur rouge avancé
    colorPrint(Red, texte)
    
def txtmosquitto(texte): # Affiche l'information en couleur violette
    colorPrint(Violet, texte)
    
def txtmqtt(texte): # Affiche l'information en couleur jaune
    colorPrint(Jaune, texte)
    

#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------

def contenuAIntroduire(set=0, pattern='Remplacer', contenuFichier=f"{DossierLOG}\\A_Ref_Notifications.txt", content=''): # Lecture et écriture dans le fichier temporaire The beginning. À vérifier
    if set == 0 :
        fichierTemp = f"{DossierLOG}\\temp.txt"
        with open(contenuFichier, 'r') as Read :
            consult = Read.read()
        changement = re.sub(pattern=rf'{pattern}', repl=content, string=consult, flags=re.IGNORECASE)
        with open(fichierTemp, 'w') as Wr :
            Wr.write(changement)
        with open(fichierTemp, 'r') as R :
            return R.read()

def chercher_ds_fichier(pattern, fichier) : # Lire un fichier, Détecter le mot ou la cible Et la retourne
    with open(fichier, 'r') as Read :
        consult = Read.read()
    try:
        re_pattern = re.escape(pattern)
        resultat = re.search(pattern=rf'{re_pattern}', string=consult, flags=re.IGNORECASE)
        return resultat.group()
    except AttributeError as a :
        errorPrint('AttributeError', 'chercher_ds_fichier', a)
        return None

#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------

def replicas(cibleI, cibleII, suffixeI, suffixeII, contenu='', set=0) : # Retire un groupe de mots ou une lettre d'un mot Se trouvant dans un fichier
    global fichierTemp
    cible = os.listdir(cibleI)
    cibleCheck = os.listdir(cibleII)

    cible = [nom.removesuffix(f'{suffixeI}') for nom in cible]

    for i in cible : 
        if not os.path.exists(f"{cibleII}\\{i}{suffixeII}") :
            if set == 1 :
                contenu = contenuAIntroduire(set=0, pattern='Remplacer', content=f"{i}{suffixeII}")
                print(i, " : le fichier etait manquant. Nous avons proceder a son ajout...")
                with open(f"{cibleII}\\{i}{suffixeII}", 'a') as creer :
                    creer.write(contenu)
            else :
                print(i, " : le fichier etait manquant. Nous avons proceder a son ajout...")
                with open(f"{cibleII}\\{i}{suffixeII}", 'a') as creer :
                    creer.write(contenu)
            print(f"{i}{suffixeII} : ", "fichier cree !")
            


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------

def detecterOS() : # Détecte le système d'exploitation
    systeme = platform.system()
    if systeme == "Windows" :
        print("Environnement Windows !\n\n")
    if systeme == "Linux" :
        print("Environnement Linux !\n\n")
    if systeme == "Darwin" :
        print("Environnement macOS !\n\n")
        
    return systeme   

#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------

def mesEnvironnements() : # Retourne les Chemins environnements les plus utilisés
    DossierFirst = os.environ.get('RACINE')
    DossierRacine = os.environ.get('PRINCIPAL')
    DossierEmpire = os.environ.get('EMPIRE')
    DossierPython = os.environ.get('PYTHR')
    

#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------

def initial() : # Cherche toute occurrence d'une information dans les répertoires ou Disques du système
    nbre = [chr(i) + ':\\' for i in range(ord('C'), ord('F')+1)]
    SCRIPT = f"""
    $Drivers = @({','.join(f"'{d}'" for d in nbre)})
        Get-ChildItem -Path $Drivers -Recurse -Filter 'Environment.ps1' -ErrorAction SilentlyContinue |
        Select-Object -ExpandProperty FullName
    """
    print("Debut de la resolution des variables...")
    result = psh.run(['Powershell.exe', '-Command', SCRIPT],
                capture_output=True, text=True)
    RESULTO = f"{result.stdout}"
    print(RESULTO)
    ps_command = f'Start-Process Powershell.exe -ArgumentList \'-ExecutionPolicy Bypass -File "{RESULTO}"\' -WindowStyle Minimized -Wait'
    resultat = psh.run(['Powershell.exe', '-Command', ps_command],
                capture_output=True, text=True)


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------

#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------

def comparaison_fichiers(extension, fichier_d_ecriture, rep_de_recherche, lecture_dossier_cree) : # Vérifie si des fichiers se trouvent dans un même répertoire Ou s'ils se ressemblent Après comparaison retourne une réponse claire

    result_fichier = recherche_specifique(chemin=rep_de_recherche, extension=extension) 
    inscription_ds_fichier(fichier_d_ecriture, result_fichier)

    f_exe = [ i for i in lireFile(fichier_d_ecriture) if extension in i ]
    difference = len(f_exe) - len(lecture_dossier_cree)

    if difference != 0 :
        colorPrint(Green, f"Nouveaux fichiers {extension} detectee : {difference}")
        os.startfile("check_exe.py")
        return f"Nouveaux fichiers {extension} detectee : {difference}"
    else :
        colorPrint(Green, f"Les fichiers {extension} sont dans leurs repertoires respectifs")
        return f"Les fichiers {extension} sont dans leurs repertoires respectifs"

#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------

def check_total_memoire() : # Vérifie le niveau de mémoire Du processus Python en action. Détails et fonctionnalités avancées

    PROCESS_QUERY_INFORMATION = 0x0400
    PROCESS_VM_READ = 0x0010

    class PROCESS_MEMORY_COUNTERS_EX(ctypes.Structure):
        _fields_ = [
            ('cb', ctypes.c_ulong),
            ('PageFaultCount', ctypes.c_ulong),
            ('PeakWorkingSetSize', ctypes.c_size_t),
            ('WorkingSetSize', ctypes.c_size_t),
            ('QuotaPeakPagedPoolUsage', ctypes.c_size_t),
            ('QuotaPagedPoolUsage', ctypes.c_size_t),
            ('QuotaPeakNonPagedPoolUsage', ctypes.c_size_t),
            ('QuotaNonPagedPoolUsage', ctypes.c_size_t),
            ('PagefileUsage', ctypes.c_size_t),
            ('PeakPagefileUsage', ctypes.c_size_t),
            ('PrivateUsage', ctypes.c_size_t),
        ]

    pid = os.getpid()
    handle = ctypes.windll.kernel32.OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_VM_READ, False, pid)

    counters = PROCESS_MEMORY_COUNTERS_EX()
    cb = ctypes.sizeof(counters)
    ctypes.windll.psapi.GetProcessMemoryInfo(handle, ctypes.byref(counters), cb)

    private_memory = counters.PrivateUsage / (1024 * 1024)

    # print(f"Private memory (Windows - proche de Gestionnaire tâches): {private_memory:.2f} Mo")
    return f"{private_memory:.2f}"


def check_memory_usage(): # Vérifie l'état de la mémoire totale pour le processus Python en cours. Fonction simple
    """Vérifie l'utilisation de la mémoire du processus Python en cours."""
    pid = os.getpid()  # PID de ton processus Python
    process = psutil.Process(pid)
    memory_info = process.memory_info()

    # print(f"Utilisation mémoire (RSS) : {memory_info.rss / (1024 * 1024):.2f} Mo")
    return memory_info.rss / (1024 * 1024)


def action_memoire(): # Retourne à l'état de la mémoire pour un fichier sans devoir toucher directement aux autres fonctions
    """Effectue une action liée à l'utilisation de la mémoire."""
    fichierstart = f"{DossierLOGPY}\\start.txt"
    memoire = float(check_total_memoire())
    if memoire > 360.0:
        if not os.path.exists(fichierstart) :
            ecrire_ds_fichier(fichierstart,'debut')
        else :
            with open(fichierstart, 'r') as read :
                rd = read.read()
            if rd == '' or rd != 'debut' :
                ecrire_ds_fichier(fichierstart,'debut')
                print("Alerte : Utilisation mémoire critique !")
                return 'Alerte'
            else:
                ecrire_ds_fichier(fichierstart,'en action')
                



#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------

def openFiles(fichier, alternative='') :
    try : 
        os.startfile(fichier)
    except FileNotFoundError as f :
        os.startfile(alternative)
        errorPrint(tabErreur=traceback.extract_tb(sys.exc_info()[2]), NomErreur='FileNotFoundError', ValeurErreur=f)

def ouvrir_fichier(fichier, alternative='') :
    try : 
        os.startfile(fichier)
    except FileNotFoundError as f :
        os.startfile(alternative)
        errorPrint(tabErreur=traceback.extract_tb(sys.exc_info()[2]), NomErreur='FileNotFoundError', ValeurErreur=f)

#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- MONGODB ENVOI -----------------------------------------
#   -----------------------------------------------------------------------------------------------

def envoi_BD_MONGO(lien:str, BD, collection=None, fichier=None, message='Insertion terminée.', verbose=None):
    
    if verbose is None:
        logging.getLogger("pymongo").setLevel(logging.WARNING)
    
    # Connexion à MongoDB
    if verbose is not None:
        print(lien, BD, collection, fichier)
        
    client = MongoClient(lien, serverSelectionTimeoutMS=5000)
    db = client[BD]
    if collection is not None :
        collection = db[collection]
    # # Charger le fichier JSON
    with open(fichier, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    if verbose is not None :
        try :
            dbs = client.list_database_names()
            print(dbs)
            client.admin.command("ping")
        except Exception as e :
            print("-> ", e)
    
    # # Insérer dans la collection
    if isinstance(data, list):
        collection.insert_many(data)
    else :
        collection.insert_one(data)
        
    if verbose is not None:
        for collect in collection.find():
            print(collect)
            
#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------




def couleur_texte(self, obj='', cible='', debut='', fin='', color='#1AEDA3', set=0) :
    if any(s in cible for s in ['#', "-------", ":\\", ':/']) :
        obj.tag_add('comment', debut, fin)
        obj.tag_config('comment', foreground='#1AEDA3')
    # __________________________________________________________________
    elif any(s in cible for s in ['-->', '->', '[]']):
        obj.tag_add('important', debut, fin)
        obj.tag_config('important', foreground='#DD8410')
    # __________________________________________________________________

    elif any(s in cible for s in ['!']):
        obj.tag_add('topic', debut, fin)
        obj.tag_config('topic', foreground='yellow')
    # __________________________________________________________________
    elif any(s in cible for s in ["invoquee", "Invoquee : ", "Reussi : "]):
        obj.tag_add('succes', debut, fin)
        obj.tag_config('succes', foreground="#2CED1A")
    # __________________________________________________________________
    elif any(s in cible for s in ["' : ", "Command '", "ATTENTION ", "UnboundLocalError", 'ValueError'\
        'KeyError', 'AttributeError', 'FileNotFoundError', 'FileExistsError']):
        obj.tag_add('erreur', debut, fin)
        obj.tag_config('erreur', foreground="#EA0D0D")          
    # __________________________________________________________________
        
    elif any(s in cible for s in ["expected", "M O D E"]):
        obj.tag_add('erreur', debut, fin)
        obj.tag_config('erreur', foreground="#8635E8")
    
def colorer_titre(self, obj='', cible='#', color='yellow'):
    obj.tag_remove("titre", "1.0", 'end')
    lignes = obj.get("1.0", "end-1c").splitlines()
    for i, ligne in enumerate(lignes, start=1) :
        if cible in ligne :
            trouver = ry.re.search(r'(.+?)\s*' + ry.re.escape(cible) + '(.*)', ligne)
            if trouver :
                mot = trouver.group(1)
                index_debut = ligne.find(mot)
                index_fin = index_debut + len(mot)
                debut = f"{i}.{index_debut}"
                fin = f"{i}.{index_fin}"
                obj.tag_add("titre", debut, fin)
    if color == '-' :
        color = 'white'
    elif color == '' :
        color = 'yellow'
    obj.tag_config("titre", foreground=color)
    
def colorer_commentaire(self, obj='', cible='#', color="#1AEDA3"):
    obj.tag_remove("commentaire", "1.0", END)
    lignes = obj.get("1.0", "end-1c").splitlines()
    for i, ligne in enumerate(lignes, start=1) :
        if cible in ligne :
            index_debut = ligne.index(cible)
            debut = f"{i}.{index_debut}"
            fin = f"{i}.end"
            obj.tag_add("commentaire", debut, fin)
    if color == '-' :
        color = 'white'
    elif color == '' :
        color = '#1AEDA3'
    obj.tag_config("commentaire", foreground=color)

    
def colorer_titre_commentaire(self, obj='', cible_comment='#', color_titre='yellow', color_comment='#1AEDA3'):
    
    obj.tag_remove("titre", "1.0", 'end')
    obj.tag_remove("commentaire", "1.0", "end")
    tableau_cibles = []
    lignes = obj.get("1.0", "end-1c").splitlines()
    for i, ligne in enumerate(lignes, start=1) :
        if isinstance(cible_comment, list) :
            for cible in cible_comment : 
                if cible in ligne :
                    tableau_cibles.append(cible)
                    
            for valider in tableau_cibles : 
                trouver = ry.re.search(r'(.+?)\s*' + ry.re.escape(valider) + '(.*)', ligne)
                if trouver :
                    mot = trouver.group(1)
                    index_debut_titre = ligne.find(mot)
                    index_fin = index_debut_titre + len(mot)
                    debut_titre = f"{i}.{index_debut_titre}"
                    fin_titre = f"{i}.{index_fin}"
                    obj.tag_add("titre", debut_titre, fin_titre)
                    
                    index_debut_comment = ligne.index(valider)
                    debut_comment = f"{i}.{index_debut_comment}"
                    fin_comment = f"{i}.end"
                    obj.tag_add("commentaire", debut_comment, fin_comment)
                
    if color_titre == '-' :
        color_titre = 'white'
    elif color_titre == '' :
        color_titre = 'yellow'
    if color_comment == '-' :
        color_comment = 'white'
    elif color_comment == '' :
        color_comment = '#1AEDA3'
        
    obj.tag_config("titre", foreground=color_titre, wrap='word')
    obj.tag_config("commentaire", foreground=color_comment, wrap='word')
    
def colorer_all(self, obj='', cible='', color='green', set=0):
    if set == 0 :
        obj.tag_delete(*obj.tag_names())
        lignes = obj.get("1.0", "end-1c").splitlines()
        for i, ligne in enumerate(lignes, start=1) :
            if isinstance(cible, list) :
                for valider in cible : 
                    if valider in ligne :
                        index_debut = ligne.index(valider)
                        debut = f"{i}.{index_debut}"
                        fin = f"{i}.end"
                        obj.tag_add("cible", debut, fin)
                        
                        couleur_texte(self, obj=obj, cible=valider, debut=debut, fin=fin, color=color)
            
    
    elif set == 1 :
        obj.tag_remove("cible", "1.0", 'end')
        lignes = obj.get("1.0", "end-1c").splitlines()
        for i, ligne in enumerate(lignes, start=1) :
            if isinstance(cible, list) :
                for valider in cible : 
                    if valider in ligne :
                        index_debut = ligne.index(valider)
                        debut = f"{i}.{index_debut}"
                        fin = f"{i}.end"
                        obj.tag_add("cible", debut, fin)
        if color == '-' :
            color = 'white'
        elif color == '' :
            color = '#1AEDA3'
        obj.tag_config("cible", foreground=color)
            
        
def colorer_fin_ligne(self, obj='', tag='all', cible='#', color_titre='yellow',
                      color_comment='#1AEDA3', color_cible='yellow', tab_cibles='[]' ):
    if tag == 'titre' :            
        colorer_titre(obj=obj, cible=cible, color=color_titre)
        
    if tag == 'commentaire' :            
        colorer_commentaire(obj=obj, cible=cible, color=color_comment)
    if tag == 'cible' :            
        colorer_all(self, obj=obj, cible=cible, color=color_cible)
    elif tag == 'all' :
        if tab_cibles != '[]' :
            colorer_titre_commentaire(obj=obj, cible_comment=tab_cibles, color_titre=color_titre, color_comment=color_comment)
        else :
            colorer_titre_commentaire(obj=obj, cible_comment=cible, color_titre=color_titre, color_comment=color_comment)


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- DIFFLIB COMPARAISON FICHIERS -----------------------------------------
#   -----------------------------------------------------------------------------------------------

def comparer_contenu_fichiers(fichier1, fichier2, sett='txt', option='return'):
    
    if sett == 'txt':
        # Charger le contenu de deux fichiers JSON
        with open(fichier1, 'r', encoding='utf-8') as f1, open(fichier2, 'r', encoding='utf-8') as f2:
            fichier1_lignes = f1.readlines()
            fichier2_lignes = f2.readlines()

        # Créer un objet Differ
        diff = difflib.unified_diff(
            fichier1_lignes,
            fichier2_lignes,
            fromfile=fichier1,
            tofile=fichier2,
            lineterm=''
        )

    elif sett == 'json':
        # Charger les fichiers comme objets Python
        with open(fichier1, 'r', encoding='utf-8') as f1, open(fichier2, 'r', encoding='utf-8') as f2:
            data1 = json.load(f1)
            data2 = json.load(f2)

        # Convertir en texte formaté identique
        data1_str = pprint.pformat(data1, indent=2).splitlines()
        data2_str = pprint.pformat(data2, indent=2).splitlines()

        # Comparer avec difflib
        diff = difflib.unified_diff(
            data1_str, data2_str,
            fromfile=fichier1,
            tofile=fichier2,
            lineterm=''
        )
        
    if option == 'return' :
        if not list(diff):
            return False
        else :
            True
                
    if option == 'test' or option == 'afficher' :
        if not list(diff):
            print('\n', '-' * 20,'\n Vide\n', '-' * 20, '\n')
        else:
            for ligne in diff:
                print(ligne)
            


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------




#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------


