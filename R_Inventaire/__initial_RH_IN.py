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
                Repertoire = getattr(sys, "_MEIPASS", os.path.dirname(__file__))
                return os.path.join(Repertoire, chemin)  
            else :
                Repertoire = os.path.abspath(".")   
                return os.path.join(Repertoire, chemin)
        except AttributeError:
            Repertoire = os.path.abspath(".")
    if chemin is None:
        return getattr(sys, "_MEIPASS", os.path.dirname(__file__))
    
WHITE = (1, 1, 1, 1)
BLEUPALE = (0.68, 0.85, 0.90, 1)
BLEUFONCE = (0.0, 0.0, 0.55, 1)
ORANGE = (1, 0.65, 0, 1)
ROUGE = (1, 0, 0, 1)
VIOLET = (0.5, 0.0, 0.5, 1)
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
try: 
    credentials = ry.lireJSON(fichier=fichier_credentials)
except Exception as e:
    pass
fichier_sauvegarde_json_RH = chemin_ressource(ry.chercher_ds_JSON(dictionnaire=dictio, cle1="Fichiers_Configurations", 
                                                               cle2='SauvegardeRH', sett='valeurcles'))
fichier_sauvegarde_json_IN = chemin_ressource(ry.chercher_ds_JSON(dictionnaire=dictio, cle1="Fichiers_Configurations", 
                                                               cle2='SauvegardeIN', sett='valeurcles'))
fichier_sauvegarde_sql_RH = chemin_ressource(ry.chercher_ds_JSON(dictionnaire=dictio, cle1="Fichiers_Configurations", 
                                                               cle2='Sauvegarde_sqlRH', sett='valeurcles'))
fichier_sauvegarde_sql_IN = chemin_ressource(ry.chercher_ds_JSON(dictionnaire=dictio, cle1="Fichiers_Configurations", 
                                                               cle2='Sauvegarde_sqlIN', sett='valeurcles'))

# ______________D_O_S_S_I_E_R___S_O_R_T_I_E_____________________________________
DossierSORTIE = chemin_ressource(ry.chercher_ds_JSON(dictionnaire=dictio, cle1='Repertoires', 
                                                     cle2='DossierSortie', sett='valeurcles'))
# ______________D_O_S_S_I_E_R___L_I_B_R_A_I_R_I_E_____________________________________
librairie = chemin_ressource(ry.chercher_ds_JSON(dictionnaire=dictio, cle1="Repertoires", 
                                                 cle2='librairie', sett='valeurcles'))
                             
# ______________I_N_I_T___R_H___________________________________________
fichier_initial_RH = chemin_ressource(ry.chercher_ds_JSON(dictionnaire=dictio, cle1="Fichiers_Configurations", cle2='INIT_RH', sett='valeurcles'))
contenu_init_RH = ry.lireJSON(fichier_initial_RH)
# ______________I_N_I_T___I_N___________________________________________
fichier_initial_IN = chemin_ressource(ry.chercher_ds_JSON(dictionnaire=dictio, cle1="Fichiers_Configurations", cle2='INIT_IN', sett='valeurcles'))
contenu_init_IN = ry.lireJSON(fichier_initial_IN)
# ______________I_N_I_T___R_H__S_Q_L_______________________________________
fichier_initial_sqlRH = chemin_ressource(ry.chercher_ds_JSON(dictionnaire=dictio, cle1="Fichiers_Configurations", cle2='_INIT_SQL_RH', sett='valeurcles'))
contenu_init_sqlRH = ry.lireFichier(fichier_initial_sqlRH)
# ______________I_N_I_T___I_N__S_Q_L_______________________________________
fichier_initial_sqlIN = chemin_ressource(ry.chercher_ds_JSON(dictionnaire=dictio, cle1="Fichiers_Configurations", cle2='_INIT_SQL_IN', sett='valeurcles'))
contenu_init_sqlIN = ry.lireFichier(fichier_initial_sqlIN)



# ______________F_O_R_M_U_L_A_I_R_E___R_H_____________________________________
fichier_form_RH = chemin_ressource(ry.chercher_ds_JSON(dictionnaire=dictio, cle1="Fichiers_Configurations", cle2='FormulaireRH', sett='valeurcles')    )
# ______________F_O_R_M_U_L_A_I_R_E___I_N_____________________________________
fichier_form_IN = chemin_ressource(ry.chercher_ds_JSON(dictionnaire=dictio, cle1="Fichiers_Configurations", cle2='FormulaireIN', sett='valeurcles')    )
# ______________F_O_R_M_U_L_A_I_R_E___R_H_____________________________________
fichier_form_sqlRH = chemin_ressource(ry.chercher_ds_JSON(dictionnaire=dictio, cle1="Fichiers_Configurations", cle2='SQL_RH', sett='valeurcles')    )
# ______________F_O_R_M_U_L_A_I_R_E___I_N_____________________________________
fichier_form_sqlIN = chemin_ressource(ry.chercher_ds_JSON(dictionnaire=dictio, cle1="Fichiers_Configurations", cle2='SQL_IN', sett='valeurcles')    )

# _________________C_O_M_P_A_R_A_I_S_O_N___F_I_C_H_I_E_R_S______________________________
# RH  
contenu_formulaireRH = ry.lireJSON(fichier_form_RH)
reponse = ry.comparer_contenu_fichiers(fichier1=fichier_initial_RH, fichier2=fichier_form_RH,
                             sett='json', option='return')
# IN
contenu_formulaireIN = ry.lireJSON(fichier_form_IN)
reponse = ry.comparer_contenu_fichiers(fichier1=fichier_initial_IN, fichier2=fichier_form_IN,
                             sett='json', option='return')
# SQL RH  
contenu_formulaire_sqlRH = ry.lireFichier(fichier_form_sqlRH)
reponse = ry.comparer_contenu_fichiers(fichier1=fichier_initial_sqlRH, fichier2=fichier_form_sqlRH,
                             sett='txt', option='return')
# SQL IN
contenu_formulaire_sqlIN = ry.lireFichier(fichier_form_sqlIN)
reponse = ry.comparer_contenu_fichiers(fichier1=fichier_initial_sqlIN, fichier2=fichier_form_sqlIN,
                             sett='txt', option='return')

#
# ______________S_A_U_V_E_G_A_R_D_E___R_H_____________________________________
if reponse == True:   
    lecture_validante = ry.lireJSON(fichier_sauvegarde_json_RH)
    if lecture_validante is not None and lecture_validante != '':
        ry.rajouter_ds_json(fichier=fichier_sauvegarde_json_RH, dictionnaire=f",{contenu_init_RH}, {contenu_formulaireRH}", sett=4)
    else :
        ry.rajouter_ds_json(fichier=fichier_sauvegarde_json_RH, dictionnaire=f"{contenu_init_RH}, {contenu_formulaireRH}", sett=4)

ry.ecrire_ds_json(fichier=fichier_form_RH, dictionnaire=contenu_init_RH, sett=4)
# ______________S_A_U_V_E_G_A_R_D_E___I_N_____________________________________
if reponse == True:   
    lecture_validante = ry.lireJSON(fichier_sauvegarde_json_IN)
    if lecture_validante is not None and lecture_validante != '':
        ry.rajouter_ds_json(fichier=fichier_sauvegarde_json_IN, dictionnaire=f",{contenu_init_IN}, {contenu_formulaireIN}", sett=4)
    else :
        ry.rajouter_ds_json(fichier=fichier_sauvegarde_json_IN, dictionnaire=f"{contenu_init_IN}, {contenu_formulaireIN}", sett=4)

ry.ecrire_ds_json(fichier=fichier_form_IN, dictionnaire=contenu_init_IN, sett=4)
#       S Q L
# ______________S_A_U_V_E_G_A_R_D_E___R_H____S_Q_L_______________________________
if reponse == True:   
    lecture_validante = ry.lireFichier(fichier_sauvegarde_sql_RH)
    if lecture_validante is not None and lecture_validante != '':
        ry.rajouter_ds_fichier(fichier=fichier_sauvegarde_sql_RH, contenu=f"{contenu_formulaire_sqlRH}")
    else :
        ry.rajouter_ds_fichier(fichier=fichier_sauvegarde_sql_RH, contenu=f"{contenu_formulaire_sqlRH}")

ry.ecrire_ds_fichier(fichier=fichier_form_sqlRH, contenu=contenu_init_sqlRH)
# ______________S_A_U_V_E_G_A_R_D_E___I_N____S_Q_L_______________________________
if reponse == True:   
    lecture_validante = ry.lireFichier(fichier_sauvegarde_sql_IN)
    if lecture_validante is not None and lecture_validante != '':
        ry.rajouter_ds_fichier(fichier=fichier_sauvegarde_sql_IN, contenu=f"{contenu_formulaire_sqlIN}")
    else :
        ry.rajouter_ds_fichier(fichier=fichier_sauvegarde_sql_IN, contenu=f"{contenu_formulaire_sqlIN}")

ry.ecrire_ds_fichier(fichier=fichier_form_sqlIN, contenu=contenu_init_sqlIN)

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


