import os, sys, shutil, datetime, platform
import subprocess as psh
import importlib.util
import traceback
import difflib
import json
import time
if platform.system() == 'Linux' :
    psh.check_call(['sudo', 'bash', 'venv/bin/activate'])
try :
    import lib._Functions as ry
    import chardet
except ModuleNotFoundError as m:
    import traceback
    print("\033[1;31m", traceback.extract_tb(sys.exc_info()[2]), 'FileNotFoundError', m, "\033[0m")
    
def resoudre_chemins(chemin_I, chemin_II):
    if os.path.exists(chemin_I) :
        return chemin_I
    else : 
        return chemin_II

def chemin_ressource(chemin=None):
    if chemin is not None:
        try:
            if hasattr(sys, "_MEIPASS"):
                # On est dans un executable
                Repertoire = sys._MEIPASS
                return os.path.join(Repertoire, chemin)                
        except AttributeError:
            Repertoire = os.path.abspath(".")
    if chemin is None:
        return sys._MEIPASS
    
WHITE = (1, 1, 1, 1)
BLEUPALE = (0.68, 0.85, 0.90, 1)
BLEUFONCE = (0.0, 0.0, 0.55, 1)
ORANGE = (1, 0.65, 0, 1)
ROUGE = (1, 0, 0, 1)
VERT = (0, 0.5, 0, 1)
GRISCLAIR = (0.7, 0.7, 0.7, 1)
GRISFONCE = (0.25,0.25,0.25,1)
NOIR = (0, 0 , 0, 1)

rcp = ry.colorPrint
err = ry.errorPrint

try :
    Repertoire = os.path.dirname(os.path.abspath(__file__))
except Exception as e :
    try: 
        Repertoire = chemin_ressource()
    except Exception as i:
        print(e)
        exit(1)
    
fichier_credentials = chemin_ressource("lib/cred.json")
fichier_credentials_env = chemin_ressource("lib/credentials.env")
fichier_configuration = chemin_ressource("option.json")
dictio = ry.lireJSON(fichier=fichier_configuration)
credentials = ry.lireJSON(fichier=fichier_credentials)
fichier_sauvegarde_json = chemin_ressource(ry.chercher_ds_JSON(dictionnaire=dictio, cle1="Fichiers_Configurations", 
                                                               cle2='Sauvegarde', sett='valeurcles'))
librairie = chemin_ressource(ry.chercher_ds_JSON(dictionnaire=dictio, cle1="Repertoires", 
                                                 cle2='librairie', sett='valeurcles'))
                             
# ______________I_N_I_T_______________________________________________
fichier_initial = chemin_ressource(ry.chercher_ds_JSON(dictionnaire=dictio, cle1="Fichiers_Configurations", cle2='INIT', sett='valeurcles'))
contenu_init = ry.lireJSON(fichier_initial)
DossierSORTIE = chemin_ressource(ry.chercher_ds_JSON(dictionnaire=dictio, cle1='Repertoires', cle2='DossierSortie', sett='valeurcles'))
# ______________F_O_R_M_U_L_A_I_R_E_________________________________________
fichier_form = chemin_ressource(ry.chercher_ds_JSON(dictionnaire=dictio, cle1="Fichiers_Configurations", cle2='Formulaire', sett='valeurcles')    )
#
contenu_formulaire = ry.lireJSON(fichier_form)
reponse = ry.comparer_contenu_fichiers(fichier1=fichier_initial, fichier2=fichier_form,
                             sett='json', option='return')

#
# ______________S_A_U_V_E_G_A_R_D_E_________________________________________
if reponse == True:   
    lecture_validante = ry.lireJSON(fichier_sauvegarde_json)
    if lecture_validante is not None and lecture_validante != '':
        ry.rajouter_ds_json(fichier=fichier_sauvegarde_json, dictionnaire=f",{contenu_init}, {contenu_formulaire}", sett=4)
    else :
        ry.rajouter_ds_json(fichier=fichier_sauvegarde_json, dictionnaire=f"{contenu_init}, {contenu_formulaire}", sett=4)

ry.ecrire_ds_json(fichier=fichier_form, dictionnaire=contenu_init, sett=4)
#
ARCHIVES = f"{Repertoire}/archives"
CACHE = chemin_ressource(ry.chercher_ds_JSON(dictionnaire=dictio, cle1="Fichiers_Configurations", cle2='Cache', sett='valeurcles'))
texte_support = chemin_ressource(ry.chercher_ds_JSON(dictionnaire=dictio, cle1="Fichiers_Configurations", cle2='texte_support', sett='valeurcles'))

def date(sett='') :
    date_ajourdhui = datetime.datetime.now()
    if sett == 'archive':
        return date_ajourdhui.strftime("%Y-%m-%d-%H-%M-%S")
    elif sett == 'date_pour_BD':
        date_formatee = date_ajourdhui.strftime("%d %B %Y")
        return date_formatee.lower()
    elif sett == '':
        return date_ajourdhui

def detecterOS() :
    systeme = platform.system()
    if systeme == "Windows" :
        print("Environnement Windows !\n\n")
    if systeme == "Linux" :
        print("Environnement Linux !\n\n")
    if systeme == "Darwin" :
        print("Environnement macOS !\n\n")
        
    return systeme  

def encodage_(fichier):
    with open(fichier, 'rb') as f:
        donnee = f.read()
        resultat = chardet.detect(donnee)
    return resultat['encoding']

def __restart__():
    USER = os.getlogin()
    programme = os.path.abspath(__file__)
    psh.Popen(
        [ f"C:/Users/{USER}/AppData/Local/Microsoft/WindowsApps/python3.13.exe",
         f"{programme}"
         ]
    )
    sys.exit()
# ___________________________________________________________________________________________________________________
# ___________________________________________________________________________________________________________________
# ___________________________________________________________________________________________________________________

def cleaner():
    with open("", 'w') as Wr :
        Wr.write('')

def rechercherElement(cible):
    nbre = [chr(i) + ':/' for i in range(ord('C'), ord('F')+1)]
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

def terminal(message, set='ecrire'):
    if set == 'ecrire' :
        ry.ecrire_ds_fichier(f"{CACHE}", message)
    elif set == 'rajouter' or set == 'append' :
        ry.rajouter_ds_fichier(f"{CACHE}", message)

def repertorier_files():
    
    CHEMIN = f"{Repertoire}"       
        
    nomFile = "repertorier_fichier"
    fichier = os.path.join(CHEMIN, f"{nomFile}.py")
    spec = importlib.util.spec_from_file_location(nomFile, fichier)
    repertorier_fichiers = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(repertorier_fichiers)
    return repertorier_fichiers

# ___________________________________________________________________________________________________________________
# ___________________________________________________________________________________________________________________
# ___________________________________________________________________________________________________________________
    
def installer_module(packages):
    
    for module, package in packages.items():
        try:
            print(f"Installation de {module}...")
            importlib.import_module(package)
        except ImportError:
            try:
                psh.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
                psh.check_call([sys.executable, "-m", "pip", "install", "--upgrade", package])
            except psh.CalledProcessError as e:
                print("Erreur :", e)

def deja_installee(programme):
    try:
        # Vérifie si pandoc est disponible
        result = psh.run([f"{programme}", "--version"], capture_output=True, text=True, check=True)
        print("Pandoc est installé :", result.stdout.splitlines()[0])
        return True
    except FileNotFoundError:
        print("Pandoc n'est pas installé ou n'est pas dans le PATH.")
        return False
    except psh.CalledProcessError as e:
        print("Erreur lors de l'exécution de pandoc :", e)
        return False    

def check_install(dictionnaire, application=None):
    info = list(dictionnaire.keys())[0]
    # Premiere Verification
    process = psh.Popen(["Powershell", "-Command", f"Get-Command *{info}*"], stdout=psh.PIPE, stderr=psh.PIPE)
    output, error = process.communicate()
    
    if process.returncode == 0:
        print(f"{info} est installé :", output.decode().strip())
    else:
        print(f"{info} n'est pas installé ou n'est pas dans le PATH.")
        if application:
            os.startfile(application)
        # Seconde Verification
        if deja_installee(dictionnaire[info]):
            print(f"{info} est déjà installé.")
        else:                           
            installer_module(packages=dictionnaire)

def verificateur_module(m):
    if "pypandoc" in f"{m}":
        check_install({"pypandoc":"pypandoc"}, var_app_pandoc)
    if "wkhtmltopdf" in f"{m}":
        check_install({"wkhtmltopdf":"wkhtmltopdf"}, var_app_wkhtmltopdf)

# _____________________________________________________________________________________________________________________________
# _____________________________________________________________________________________________________________________________
# _____________________________________________________________________________________________________________________________


