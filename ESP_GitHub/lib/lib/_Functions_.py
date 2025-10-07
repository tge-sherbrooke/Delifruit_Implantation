#

#Functions
import random
import time
import board
import analogio, digitalio, terminalio, displayio
import pwmio
import os, sys
import json
import re
import math
import traceback
#from adafruit_display_text import label
import adafruit_displayio_ssd1306
# import supervisor
# supervisor.runtime.autoreload = False

['__class__', '__name__', 'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'D0', 'D1', 'D10', 'D11', 'D12', 'D13', 'D2', 'D3', 
 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DEBUG_RX', 'DEBUG_TX', 'I2C', 'IO1', 'IO10', 'IO11', 
 'IO12', 'IO13', 'IO14', 'IO15', 'IO16', 'IO17', 'IO18', 'IO2', 'IO21', 'IO3', 'IO39', 'IO4', 
 'IO40', 'IO41', 'IO42', 'IO46', 'IO47', 'IO48', 'IO5', 'IO6', 'IO7', 'IO8', 'IO9', 'LED', 'MISO', 
 'MOSI', 'NEOPIXEL', 'RX', 'SCK', 'SCL', 'SDA', 'SD_CS', 'SPI', 'STEMMA_I2C', 'TX', 'UART', '__dict__', 'board_id']

#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- V A R I A B L E S -----------------------------------------
#   -----------------------------------------------------------------------------------------------
LOGERREUR = f"../Utilitaires/erreurs.txt"
fichierTemp = f"../Utilitaires/temp.txt"

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
#   ---------------------------------- AFFICHAGE -----------------------------------------
#   -----------------------------------------------------------------------------------------------

def affichage () :
    i2c = board.I2C()  # uses board.SCL and board.SDA

    displayio.release_displays()

    display_bus = displayio.I2CDisplay(i2c, device_address=0x3c)
    display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64, rotation=180)


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


#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- DETECTER L'ENCODAGE -----------------------------------------
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
#   ---------------------------------- E R R E U R S -----------------------------------------
#   -----------------------------------------------------------------------------------------------


def rapporter_erreur(contenu): # Rapporte les erreurs Dans un fichier Erreur.TXT
    fichier = LOGERREUR
    dateErreur = time.localtime()
    with open(fichier, 'a') as edit:
        edit.write(f"{time.strftime('%d-%B-%Y-%H-%M-%S', dateErreur)} : {contenu}\n")
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
    
def PrintColor (color="", message1="", message2="") :
    if message2 == "" :
        print(f"{color}{message1}{end_color}")
    else :
        print(f"{message2}{color}{message1}{end_color}")

#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- clignoter -----------------------------------------
#   -----------------------------------------------------------------------------------------------

# def boutonRetour () :
#     if bouton.value:
#         PrintColor (Jaune, "retour...") 
#         mode = (mode + 1) % 3
#         time.sleep(0.1)
#         return 1
#     else :
#         return 0

# def clignoter (composant) :
#     if composant == 1 :
#         tool = board.A3
#     else :
#         tool = board.D6
#     led = digitalio.DigitalInOut(tool)
#     led.direction = digitalio.Direction.OUTPUT
#     while True :
#         led.value = True
#         print()
#         PrintColor ("Clignoter --> ", Jaune, "LED") 
#         time.sleep(0.5)
#         led.value = False
#         time.sleep(0.5)
#         boutonRetour ()

#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------

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

def choiceActif (mode) :
    if mode == 1 :
        clignoter(2)
    else : 
        print("Ceci : Vide")

def monInterstice(intervalles, dernier_temps) :
    if time.monotonic() - dernier_temps <= intervalles :
        choiceActif(1)
        dernier_temps = time.monotonic()

def boutonRetour () :
    bouton = 0
    if bouton.value:
        PrintColor (Jaune, "retour...") 
        return 1
        #supervisor.reload()
        #time.sleep(0.1) 



#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------

def clignoter (composant) :
    if composant == 1 :
        tool = board.A3
    else :
        tool = board.D6
    led = digitalio.DigitalInOut(tool)
    led.direction = digitalio.Direction.OUTPUT
    while True :
        led.value = True
        PrintColor ("Clignoter --> ", Jaune, "LED") 
        time.sleep(0.5)
        led.value = False
        time.sleep(0.5)
        boutonRetour ()

#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------

# Pour Windows
def effacer_ecran() :
    if os.name == 'nt':
        os.system('cls')  # Efface l'écran sur Windows

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


    elif sett == 'tableau' or sett == 'liste': # si le conteneur est un tableau qui contient un dictionnaire, retourne le tableau
        # Dictionnaire
        for key in dictionnaire :
            for cle, val in key.items():
                if cle == cle1 :
                    tableau_valideur_action.append(cle)
                    data[cle1] = tableau_valideur_action
        return data
    
    elif sett == '{[]}-valeur' :
        for key, tableau in dictionnaire:
            if key == cle1:
                for tab in dictionnaire[cle1]:
                    for titre, valeur in tab.items():
                        return valeur
                    
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

    elif sett == '-' or sett == 'valeur':
        for key, valeur in dictionnaire.items():
            if key == cle1:
                return valeur

    else :
        errorPrint(f'chercher_ds_JSON 1=>{cle1}, 2=>{cle2}, 3=>{cle3}', "fonction", "une des cles manque...")

def lireJSON(fichier, cible='', sett=0, code='utf-8'):
    if code != 'utf-8' :
        encodage_UTF(fichier)
    # try:
    with open(fichier, 'r') as dictio :
            if sett == 0:
                return json.load(dictio)
    # except  : 
    #     encodage_UTF(fichier)
    #     lireJSON(fichier=fichier, cible='', set=sett, code=code)
        

def ecrire_ds_json(fichier, dictionnaire=None, contenu=None, cle1=None, cle2=None, cle3=None, val=None, indent=4, sett='normal'): # Écrit dans un fichier
    data = {}
    try :
        if sett == 'normal' and dictionnaire is None:
            with open(fichier, "w") as edit:
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

def lireFile(fichier, cible='', set=0, code='utf-8') : # Fichier en format d'encodage UTF 8. Lecture efficace Récupère les lignes de fichiers les unes après les autres en effaçant les espaces et les sauts de ligne. Options secondaires pour laisser les sauts de ligne
    if code != 'utf-8' :
        encodage_UTF(fichier)
    try:
        with open(fichier, 'r', encoding='utf-8') as listFichier :
            print(f"{fichier} en cours de lecture")
            if set == 0 :
                return [ligne.rstrip('\n') for ligne in listFichier.readlines() if ligne != '' and ligne != '\n' and ligne is not None]
            elif set == 1 :
                return listFichier.readlines()
            else :
                return listFichier.read()

    except UnicodeDecodeError : 
        encodage_UTF(fichier)
        lireFichier(fichier=fichier, cible='', set=set, code=code)

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

def ecrire_ds_fichier(fichier, contenu, encoding='utf-8'): # Écrit dans un fichier
    try :
        if encoding == '' :
            with open(fichier, 'w') as edit:
                edit.write(f"{contenu}")
        else :
            with open(fichier, 'w', encoding=encoding) as edit:
                edit.write(f"{contenu}")
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

def color (colour, value) :
    final = colour, value, end_color
    return final

def colorPrint(colour="", message1="", message2="", setting=0) :
    
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
        
        
def checkResult (valeur) :
    try :
        result = valeur
    except ZeroDivisionError :
        result = "Quelque chose cloche"
    except TypeError :
        result = "Le type d'erreur: "
    finally :
        return result      
        
# -------------------------------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------------------------------


# exercice 2 ---->   question 3
def whileII () :
    choix = ''

    while (choix != 'q') :

        # V a r i a b l e s
        nbrePairImpair = int(input("\ndonner un entier positif : "))

        print(type(nbrePairImpair))

        annee = nbrePairImpair

        if (int(nbrePairImpair) and nbrePairImpair > 0) :

            if (((annee % 4 == 0) and not (annee % 100 == 0) or (annee % 400 == 0))) :
                print(Green, "T R U E", end_color)
            else :
                print(Violet, "F A L S E", end_color)

        else : print(Rouge, "Veuillez donner un nombre entier positif, svp...", end_color)

        choix = input('pour arreter [ q ], sinon cliquer sur E N T E R : ')

    effacer_ecran()

# sys.path.append("D:/UCDownloads/OneDrive/H2025/DÉVELOPPEMENT D'APPLICATIONS AVEC DES OBJETS... - 420-473-SH")  # Ajouter le dossier au PATH
# import Functions


# chemin = "D:/UCDownloads/OneDrive/H2025/DÉVELOPPEMENT D'APPLICATIONS AVEC DES OBJETS... - 420-473-SH"
# sys.path.append(chemin)
# import Functions
#print("Contenu du dossier :", os.listdir(chemin))  # Afficher les fichiers du dossier

#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------

def trouverFichiers (folder) :
    dossiers = os.listdir(os.getcwd())
    for dossier in dossiers :
        if dossier == folder :
            os.chdir(dossier)
    return dossier

#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------

#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------

def trouverI2C () :
    import board
    import busio

    # Initialisation de l'interface I2C
    i2c = busio.I2C(board.SCL, board.SDA)

    print("Scan des périphériques I2C...")

    # Essayer d'obtenir un verrou pour l'accès I2C
    if i2c.try_lock():
        try:
            # Scan des périphériques I2C
            devices = i2c.scan()

            # Affichage des résultats
            if devices:
                print("Périphériques trouvés:", devices)
            else:
                print("Aucun périphérique trouvé.")
        finally:
            # Relâcher le verrou une fois l'opération terminée
            i2c.unlock()
    else:
        print("Le verrou I2C n'a pas pu être obtenu.")



#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------

# /////////////////////// 02 --> CONNEXION : CREDENTIAL /////////////////////////

#   -----------------------------------------------------------------------------------------------
#   ---------------------------------- CHECK HEXADECIMAL -----------------------------------------
#   -----------------------------------------------------------------------------------------------

def success(texte):
    colorPrint(Green, texte)
    
def erreur(texte):
    colorPrint(Rouge, texte)
    
def warnings(texte):
    colorPrint(Red, texte)
    
def txtmosquitto(texte):
    colorPrint(Violet, texte)
    
def txtmqtt(texte):
    colorPrint(Jaune, texte)
    



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


