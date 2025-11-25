# pyinstaller --noconsole --onefile RH_Billeterie_IN.pyw --add-data "option.json;." --add-data "lib/_init_IN.json;lib" --add-data "lib/cred.json;lib"  --add-data "lib/csv_cv_rh.csv;lib" --add-data "lib/envoi_vers_BD.ps1;lib" --add-data "lib/git_send.bat;lib" --add-data "lib/requirements.txt;lib" --add-data "lib/credentials.env;lib" --add-data "lib/Blocnotes/Dates.txt;lib/Blocnotes" --add-data "lib/Blocnotes/Infos_RH.txt;lib/Blocnotes" --add-data "lib/Blocnotes/LiensUtiles.txt;lib/Blocnotes" --add-data "lib/Blocnotes/Plan.txt;lib/Blocnotes"  --add-data "lib;lib" --add-data "assets;assets" --add-data "Sortie/formulaireIN.json;Sortie" --add-data "Sortie/formulaireRH.json;Sortie" --add-data "lib/Blocnotes;lib/Blocnotes" --add-data "lib/erreurs.txt;lib" --add-data "archives;archives" --add-data "archives/sauvegardeIN.json;archives" --add-data "archives/sauvegardeRH.json;archives" --add-data "lib/_init_RH.json;lib" --add-data "lib/csv_cv_inventaire.csv;lib" --add-data "lib/Blocnotes/Infos_RH.txt;lib/Blocnotes" --add-data "lib/Blocnotes/Infos_inventaire.txt;lib/Blocnotes" --add-data "Sortie;Sortie" --add-data "lib/Aide.txt;lib" 

import subprocess as psh
import os, sys, platform
import datetime, locale, calendar
import __initial_RH_IN as initM
if platform.system() == 'Linux' :
    psh.check_call(['sudo', 'bash', '/d/Stockage/Scripts/venv/bin/activate'])
try :
    import kivy
except ModuleNotFoundError as m :
    print ('Pas de module associee')
    import traceback
    print("\033[1;31m", traceback.extract_tb(sys.exc_info()[2]), 'FileNotFoundError', m, "\033[0m")
    cible = 'kivy'
    if cible in f"{m}":
        
        print("----------->", f"{cible} en manque...")
        
        packages = {
            "kivy": "kivy[base,media,tuio,full,dev,gstreamer,angle,sdl2,glew]",
        }
        
        DossierPrincipal = initM.Repertoire
        
        _venvI = f'{DossierPrincipal}/.venv/Scripts/activate'
        _venvII = './.venv/Scripts/activate'

        for module, package in packages.items():
            try:
                initM.importlib.import_module(package)
                print(f"{package} est déjà installé.")
            except ImportError:
                print(f"{package} manquant. Installation...")
                try:
                    systeme = platform.system() 
                    if systeme == "Linux" :
                        psh.check_call(['python3', "-m", "pip", "install", "--upgrade", package], stdout=psh.DEVNULL, stderr=psh.STDOUT,)
                        
                    elif systeme == "Windows" :
                        psh.check_call([sys.executable, "-m", "pip", "install", "--upgrade", package])
                        psh.check_call([sys.executable, "-m", "pip", "install", "--upgrade", 'pip', 'setuptools', 'venv'])
                        if os.path.exists(_venvI):
                            psh.check_call([sys.executable, "-m", _venvI])
                        elif os.path.exists(_venvII):
                            psh.check_call([sys.executable, "-m", _venvII])
                    print(f"{package} installé avec succès.")
                except psh.CalledProcessError as e:
                    print(f"Échec de l'installation de {package}.")
                    print("Erreur :", e)
                    exit(1)

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from functools import partial
from kivy.uix.checkbox import CheckBox
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.animation import Animation
from kivy.metrics import dp
from kivy.config import Config
from kivy.core.window import Window
from kivy.clock import Clock
import csv
# ___________________________________________________________________________________________________________________

# Définir la locale en français (valable sur systèmes compatibles)
locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
# Commande provnant de Functions.py
ry = initM.ry
rcp = initM.rcp
err = initM.err
dictio = initM.dictio
Repertoire = initM.Repertoire
Window.title = "RH - Billeterie - Inventaire"
APP = f"{Repertoire}/RH_Billeterie_IN.pyw"
# ry.load_dotenv(dotenv_path=f"{initM.librairie}/credentials.env")
fichier_configuration = initM.fichier_configuration
# ___________________________________________________________________________________________________________________

try:
    credential = initM.credentials
    fichier_credentials = initM.fichier_credentials
except Exception as e:
    pass

markdownobject = 'mark_cv'
            # Fichiers initiales
INITfileRH = initM.fichier_initial_RH
INITfileIN = initM.fichier_initial_IN

INITfile_sqlRH = initM.fichier_initial_sqlRH
INITfile_sqlIN = initM.fichier_initial_sqlIN

date_archivable = initM.date('archive')
date_formatee = initM.date('date_pour_BD')
texteWord = initM.texte_support
                # Fichiers de formulaire
LETTREFichierRH = initM.fichier_form_RH
LETTREFichierIN = initM.fichier_form_IN
LETTRE_RH = initM.contenu_formulaireRH
LETTRE_IN = initM.contenu_formulaireIN
                # Fichiers de sql
LETTREFichier_sqlRH = initM.fichier_form_sqlRH
LETTREFichier_sqlIN = initM.fichier_form_sqlIN
LETTRE_SQL_RH = initM.contenu_formulaire_sqlRH
LETTRE_SQL_IN = initM.contenu_formulaire_sqlIN

ARCHIVES = initM.ARCHIVES
file_git_send = f"{Repertoire}/lib/git_send.bat" 
DOSSIER = initM.chemin_ressource(ry.chercher_ds_JSON(dictionnaire=dictio, cle1="Liste_Dossiers", cle2='Liste_ouverture', sett='{-[]-{}-[]'))
# ___________________________________________________________________________________________________________________

BLEUFONCE = initM.BLEUFONCE ; BLEUPALE = initM.BLEUPALE ; GRISCLAIR = initM.GRISCLAIR
NOIR = initM.NOIR; WHITE = initM.WHITE
VERT = initM.VERT
VIOLET = initM.VIOLET
ROUGE = initM.ROUGE
ORANGE = initM.ORANGE
# ___________________________________________________________________________________________________________________

def generer_fichier(fichierentree, fichiersortie):
    with open(fichierentree, 'r') as read :
        recup_content = read.read()
    with open(fichiersortie, 'w') as write :
        write.write(f"{recup_content}\n")
        
generer_fichier(INITfileRH, LETTREFichierRH)
generer_fichier(INITfileIN, LETTREFichierIN)
generer_fichier(INITfile_sqlRH, LETTREFichier_sqlRH)
generer_fichier(INITfile_sqlIN, LETTREFichier_sqlIN)

dictio = ry.lireJSON(fichier=fichier_configuration)

blocnotes_dossier = initM.chemin_ressource(ry.chercher_ds_JSON(dictionnaire=dictio, cle1='Repertoires', cle2='BlocNotesLib', sett='valeurcles'))
DossierSORTIE = initM.DossierSORTIE
DossierDOC = initM.chemin_ressource(ry.chercher_ds_JSON(dictionnaire=dictio, cle1='Repertoires', cle2='DossierDoc', sett='valeurcles'))

checker = 'checkbox'
# rcp(ry.Violet, LETTRE)
# _____________R_H___V_A_R_I_A_B_L_E_S______________________________
_DATE_RH = LETTRE_RH['Date_de_creation']
_PRENOM = LETTRE_RH['Prenom']
_NOM = LETTRE_RH['Nom']
_AGE = LETTRE_RH['Age']
_PHONE = LETTRE_RH['Telephone']
_COURRIEL = LETTRE_RH['Courriel']
_ENTREPRISE = LETTRE_RH['Entreprise']
_EDITEUR_RH = LETTRE_RH['Editeur']
_DEPARTEMENTS = LETTRE_RH['Departements']
_FONCTIONS = LETTRE_RH['Fonctions']
_PRIVILEGES = LETTRE_RH['Privileges']
_LIEN = LETTRE_RH['Lien']
_ADRESSE = LETTRE_RH['Adresse']

# _____________I_N___V_A_R_I_A_B_L_E_S______________________________
_DATE_IN = LETTRE_IN['Date_de_creation']
_PRODUIT = LETTRE_IN['Produit']
_TYPE = LETTRE_IN['Types']
_ANNEE = LETTRE_IN['Annee']
_FABRICANT = LETTRE_IN['Fabricant']
_PROVENANCE = LETTRE_IN['Provenance']
_PRIX = LETTRE_IN['Prix']
_EDITEUR_IN = LETTRE_IN['Editeur']
_DESTINATION = LETTRE_IN['Destination']
_SIMILAIRES = LETTRE_IN['Similaires']
_QUANTITE = LETTRE_IN['Quantite']
_LIEN = LETTRE_IN['Lien']
_APPROBATIONS = LETTRE_IN['Approbations']

cle_DATE = 'Date_de_creation'
cle_PRENOM = 'Prenom'
cle_NOM = 'Nom'
cle_AGE = 'Age'
cle_PHONE = 'Telephone'
cle_COURRIEL = 'Courriel'
cle_ENTREPRISE = 'Entreprise'
cle_EDITEUR = 'Editeur'
cle_DEPARTEMENTS = 'Departements'
cle_FONCTIONS = 'Fonctions'
cle_PRIVILEGES = 'Privileges'
cle_LIEN = 'Lien'
cle_ADRESSE = 'Adresse'
cle_JOUR = 'Jour'

cle_PRODUIT = 'Produit'
cle_TYPE = 'Types'
cle_ANNEE = 'Année'
cle_FABRICANT = 'Fabricant'
cle_PROVENANCE = 'Provenance'
cle_EDITEUR = 'Editeur'
cle_DESTINATION = 'Destination'
cle_SIMILAIRES = 'Similaires'
cle_QUANTITE = 'Quantité'
cle_APPROBATIONS = 'Approbations'
cle_PRIX = 'Prix'

def recuperateur_poste(tableau, contenu):
    if f'{tableau}' in contenu:
        print("--> Occurrence Trouvée")
        return f"{tableau}"
    else :
        return None

valideur_cocheur = None

_lien_ = "CSV "
autre_lien_ = "Liens"
_jour_ = "Date "
_prenom_ = "Prenom "
_nom_ = "Nom "
_age_ = "Age "
_entreprise_ = "Entreprise "
_adresse_ = "Adresse "
_phone_ = "Phone"
_courriel_ = "courriel"
_fonctions_ = "Fonctions"
_privileges_ = "Privileges"
_departements_ = "Departements"
_editeur_ = "Editeur"
_utilitaires_ = "Important :"

_produit_ = "Produit "
_type_ = "Type "
_annee_ = "Année "
_fabricant_ = "Fabricant "
_provenance_ = "Provenance"
_destination_ = "Destination "
_similaires_ = "Similaires"
_quantite_ = "Quantité"
_prix_ = "Prix"
_approbation_ = "Approbations"

x = dictio['x']
y = dictio['y']
# Définir la position et la taille au lancement
Config.set('graphics', 'width', '100')
Config.set('graphics', 'height', '300')
Window.left = x
Window.top = y

# V A R I A B L E S   G L O B A L E S __________________________________________________
def colorer(self, bouton, couleur):
    bouton.background_normal = ''   # désactive l'image par défaut du bouton
    bouton.background_color = couleur  # vert foncé (R, G, B, Alpha)
    return bouton

def add_object(self, cols=None, col1=2, col2=None, col3=None, sticky=None, row_f=None, col_f=None, sett='normal', cadrage=None, forme=None, couleur=NOIR):
        """_summary_

        Args:
            cols (_type_): _description_
            sticky (_type_, optional): Active automatiquement les valeurs attachees. Defaults to None.
            row_f (_type_, optional): designe directement le cadrant. Il peut entrer en conflit avec les autres cadres, ne les reconnaissant pas. . Defaults to None.
            col_f (_type_, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """
        # Le ScrollView
        self.scroll_view = ScrollView(size_hint=(1, 1))

        if sett == 'normal':
            if sticky is None :
                cadre = GridLayout(size_hint_y=None, row_force_default=False, row_default_height=row_f)
                cadre.cols = cols
                self.add_widget(cadre)  
                return cadre  
            elif sticky is not None :
                cadre = GridLayout(
                    row_force_default=True, row_default_height=row_f,
                    col_force_default=True, col_default_width=col_f,
                )
                cadre.cols = cols
                self.add_widget(cadre)  
                return cadre  
                
        elif sett == 'doublecadre':      
            if forme == 'grid' :
                if sticky is None :
                    cadre = GridLayout(size_hint_y=None, row_force_default=False, row_default_height=row_f)
                    cadre.cols = col1
                    
                    gchecadre = GridLayout(size_hint_y=None, row_force_default=False, row_default_height=row_f)
                    gchecadre.cols = col2
                    gchecadre = colorer(self, gchecadre, BLEUPALE)  # gris clair, valeurs entre 0 et 1 RGBA
                    dtecadre = GridLayout(size_hint_y=None, row_force_default=False, row_default_height=row_f)
                    dtecadre.cols = col3
                    dtecadre = colorer(self, dtecadre, VERT)
                    
                    cadre.add_widget(gchecadre)
                    cadre.add_widget(dtecadre)
                    self.add_widget(cadre)  
                    if cadrage == 'gche' :
                        return gchecadre  
                    elif cadrage == 'dte':
                        return dtecadre
                    
                elif sticky is not None :
                    cadre = GridLayout(
                        row_force_default=True, row_default_height=row_f,
                        col_force_default=True, col_default_width=col_f,
                    )
                    
                    gchecadre = GridLayout(size_hint_y=None, row_force_default=False, row_default_height=row_f)
                    gchecadre.cols = col2
                    dtecadre = GridLayout(size_hint_y=None, row_force_default=False, row_default_height=row_f)
                    dtecadre.cols = col3
                    
                    cadre.add_widget(gchecadre)
                    cadre.add_widget(dtecadre)
                    self.add_widget(cadre)  
                    if cadrage == 'gche' :
                        return gchecadre  
                    elif cadrage == 'dte':
                        return dtecadre
            
            elif forme == 'scroll':
                if sticky is None :
                    # Layout qui contiendra les widgets et sera défilable
                    cadre = GridLayout(size_hint_y=None, row_force_default=False, row_default_height=row_f)
                    cadre.cols = col1
                    # gauche ____________________________________________________
                    self.scroll_viewgche = ScrollView(size_hint=(1, 1))
                    self.scroll_viewdte = ScrollView(size_hint=(1, 1))
                    gchecadre = GridLayout(
                        size_hint_y=None,   # ← important pour permettre le scroll vertical
                        size_hint_x=1       # ← occupe toute la largeur
                    )
                    gchecadre.bind(minimum_height=gchecadre.setter('height'))
                    gchecadre.cols = col2                    
                    gchecadre = colorer(self, gchecadre, BLEUPALE)  # gris clair, valeurs entre 0 et 1 RGBA
                    self.scroll_viewgche.add_widget(gchecadre)
                    # droite ____________________________________________________
                    dtecadre = GridLayout(
                        size_hint_y=None,   # ← important pour permettre le scroll vertical
                        size_hint_x=1       # ← occupe toute la largeur
                    )
                    dtecadre.bind(minimum_height=dtecadre.setter('height'))
                    dtecadre.cols = col3
                    dtecadre = colorer(self, dtecadre, VERT)
                    
                    self.scroll_viewdte.add_widget(dtecadre)
                    
                    cadre.add_widget(self.scroll_viewgche)
                    cadre.add_widget(self.scroll_viewdte)
                    self.add_widget(cadre)  
                    
                    if cadrage == 'gche' :
                        return gchecadre  
                    elif cadrage == 'dte':
                        return dtecadre
                    
                elif sticky is not None :

                    cadre = GridLayout(size_hint_y=None, row_force_default=False, row_default_height=row_f)
                    
                    # gauche
                    gchecadre = GridLayout(
                        spacing=1,
                        row_force_default=True, row_default_height=row_f,
                        col_force_default=True, col_default_width=col_f,
                        size_hint_y=None,   # ← important pour permettre le scroll vertical
                        size_hint_x=1       # ← occupe toute la largeur
                        )
                    gchecadre.bind(minimum_height=gchecadre.setter('height'))
                    gchecadre.cols = col2
                    gchecadre = colorer(self, gchecadre, BLEUPALE)  # gris clair, valeurs entre 0 et 1 RGBA
                    # droite
                    dtecadre = GridLayout(
                        spacing=1,
                        row_force_default=True, row_default_height=row_f,
                        col_force_default=True, col_default_width=col_f,
                        size_hint_y=None,   # ← important pour permettre le scroll vertical
                        size_hint_x=1       # ← occupe toute la largeur
                        )
                    dtecadre.bind(minimum_height=dtecadre.setter('height'))
                    dtecadre.cols = col3
                    dtecadre = colorer(self, dtecadre, VERT)
                    
                    cadre.add_widget(gchecadre)
                    cadre.add_widget(dtecadre)
                    self.add_widget(cadre)  
                    if cadrage == 'gche' :
                        return gchecadre  
                    elif cadrage == 'dte':
                        return dtecadre
                
        # Le ScrollView       
        elif sett == 'scroll' :
            
            if sticky is None :
                # Layout qui contiendra les widgets et sera défilable
                cadre = GridLayout(
                    size_hint_y=None,   # ← important pour permettre le scroll vertical
                    size_hint_x=1       # ← occupe toute la largeur
                )
                
                with cadre.canvas.before :
                    Color(*couleur)
                    cadre.bg_rect = Rectangle(size=cadre.size, pos=cadre.pos)

                # Mise à jour automatique de la taille/position du rectangle
                def update_rect(*args):
                    cadre.bg_rect.size = cadre.size
                    cadre.bg_rect.pos = cadre.pos

                cadre.bind(size=update_rect, pos=update_rect)
                # ------------------------------------
                                    
                cadre.bind(minimum_height=cadre.setter('height'))
                # On place le layout dans le ScrollView
                cadre.cols = cols
                # On place le layout dans le ScrollView
                self.scroll_view.add_widget(cadre)
                self.add_widget(self.scroll_view)  
                
                return cadre  

            elif sticky is not None :
                # Layout qui contiendra les widgets et sera défilable
                cadre = GridLayout(
                    spacing=1,
                    row_force_default=True, row_default_height=row_f,
                    col_force_default=True, col_default_width=col_f,
                    size_hint_y=None,   # ← important pour permettre le scroll vertical
                    size_hint_x=1       # ← occupe toute la largeur
                    )
                cadre.bind(minimum_height=cadre.setter('height'))

                # On place le layout dans le ScrollView
                cadre.cols = cols
                self.scroll_view.add_widget(cadre)
                self.add_widget(self.scroll_view)  
                
                return cadre  
         
        # La page
        Page = ScreenManager()
        screen = Screen(name="scroll_page")
            # Le ScrollView       
        if sett == 'PgScroll' :
            
            if sticky is None :
                # Layout qui contiendra les widgets et sera défilable
                cadre = GridLayout(
                    size_hint_y=None,   # ← important pour permettre le scroll vertical
                    size_hint_x=1       # ← occupe toute la largeur
                )
                cadre.bind(minimum_height=cadre.setter('height'))
                # On place le layout dans le ScrollView
                cadre.cols = cols
                # On place le layout dans le ScrollView
                self.scroll_view.add_widget(cadre)
                screen.add_widget(self.scroll_view)
                Page.add_widget(screen)
                self.add_widget(Page)  
                
                return cadre  

            elif sticky is not None :
                # Layout qui contiendra les widgets et sera défilable
                cadre = GridLayout(
                    spacing=1,
                    row_force_default=True, row_default_height=row_f,
                    col_force_default=True, col_default_width=col_f,
                    size_hint_y=None,   # ← important pour permettre le scroll vertical
                    size_hint_x=1       # ← occupe toute la largeur
                    )
                cadre.bind(minimum_height=cadre.setter('height'))

                # On place le layout dans le ScrollView
                cadre.cols = cols
                self.scroll_view.add_widget(cadre)
                Page.add_widget(self.scroll_view)
                self.add_widget(Page)  
                
                return cadre  

def Menu(self, tableau, cadre, haut=10, police=10, largeur=50, x=None, y=None, titre=None, 
            dictio=None, color=None, color2=None, sett='Quitter'):
        
        def colorer(self, bouton, couleur):
            bouton.background_normal = ''   # désactive l'image par défaut du bouton
            bouton.background_color = couleur  # vert foncé (R, G, B, Alpha)
            return bouton
        # Menu 
        for text, commande in tableau.items():
            self.menu_element = commandes_bouton(self, objet=cadre, text=text, commande=commande,
                                police=police, hauteur=haut, largeur=largeur, x=x, y=y)

            colorer(self, self.menu_element, color)
            dictio[text] = self.menu_element
            
        if sett == 'Quitter' :
            colorer(self, dictio['Quitter'], couleur=color2)

        return dictio

def commandes_bouton(self, text, commande=None, objet=None, police=11,
                     hauteur=None, largeur=None, x=None, y=None, couleur=None):
    if objet is None :
        self.submit = Button(text=text, font_size=police)
        if commande is not None:
            self.submit.bind(on_press=commande)
        self.add_widget(self.submit)
    elif objet is not None:
        if hauteur == 5 and largeur == 5:
            self.submit = Button(text=text, font_size=police, size_hint=(x, y))
        elif hauteur is not None and largeur is not None:
            self.submit = Button(text=text, font_size=police, size=(hauteur, largeur), size_hint=(x, y))
        elif largeur is None:
            self.submit = Button(text=text, font_size=police, height=hauteur, size_hint=(x, y))
        if commande is not None and commande != '':
            self.submit.bind(on_press=commande)
            if couleur is not None :
                self.submit.background_normal = ''   # désactive l'image par défaut du bouton
                self.submit.background_color = couleur  # vert foncé (R, G, B, Alpha)
        objet.add_widget(self.submit)
        
    return self.submit
          

def remplisseur(self, texte, objet=None, multiline=False, couleur=None, width=100, height=None, sett='default') :     
    if couleur and sett == 'default':   
        self.name = TextInput(multiline=multiline, background_color=couleur)
        self.name.bind(text=self.on_text_change)
    elif couleur is None and sett == 'default' :
        self.name = TextInput(multiline=multiline)
    elif sett == 'hauteur' and height is not None and couleur is None:
        self.name = TextInput(multiline=multiline, size_hint_y=None, height=height)
        self.name.bind(minimum_height=self.name.setter("height"))
    elif sett == 'hauteur' and height is not None and couleur is not None:
        self.name = TextInput(multiline=multiline, size_hint_y=None, height=height, background_color=couleur)
        self.name.bind(minimum_height=self.name.setter("height"))
    else :
        self.name = TextInput(multiline=multiline)            
        self.name.bind(text=self.on_text_change)
    if sett == 'default':
        # TEXTE : # halign -> alignement horizontal du texte , # valign -> alignement vertical
        label_Input = Label(text=texte, size_hint_x=None, width=width, halign='center', valign='middle') 
    else :
        label_Input = Label(text=texte, height=height, width=width, size_hint=(None, None), halign='center', valign='middle')
         
    if objet is None :
        self.add_widget(label_Input)
        # Ajout d'une boite de dialogue
        self.add_widget(self.name)
        return self.name
    elif objet is not None:
        objet.add_widget(label_Input)
        # Ajout d'une boite de dialogue
        objet.add_widget(self.name)
        
    return self.name  

def entry(self, texte, objet=None, multiline=False, couleur=None, txtColor=None, width=80, height=None, sett='default'):
    if sett == 'hauteur' and height is not None and couleur is not None and txtColor is not None: 
        self.name = TextInput(multiline=multiline, size_hint=(None, None), height=dp(height), width=dp(width), background_color=couleur, foreground_color=txtColor)
        self.name.bind(minimum_height=self.name.setter("height"))
        self.name.text = f"{texte}"
    else :
        self.name = TextInput(multiline=multiline)            
        self.name.bind(text=f"{texte}")
    
    if objet is None :
        # self.add_widget(label_Input)
        # Ajout d'une boite de dialogue
        self.add_widget(self.name)
        return self.name
    elif objet is not None:
        # objet.add_widget(label_Input)
        # Ajout d'une boite de dialogue
        objet.add_widget(self.name)
    
    return self.name  

#   C L A S S E S ______________________________________________________________________
class Home(GridLayout):
    
    def __init__(self, **kwargs):
        # Appel du constructeur de grille
        super(Home, self).__init__(**kwargs)
        self.nombre_postulee = self.afficher_nbre_postulee('nbreEntreeJour')
        self.nbreEntreeTotal = self.afficher_nbre_postulee('nbreEntreeTotal')
        self.colorationunique = False
        self.nom_sans_ext = None
        self.tableau_insertion = None
        self.csv_cv = None
        self.pdf = self.doc = self.soum = None
        self.INITfileRH = INITfileRH
        self.LETTRE = LETTRE_RH
        self.valideur_insert = self.valideur_nbre_jr = False
        self.dict_boutonvalideur = {}
        self.dictionnaire_bouton_menu = {} 
        # Nom du fichier CSV
        self.fichier_csv = initM.chemin_ressource("lib/csv_cv_rh.csv")
        # self.Jour = self.Entreprise = self.Poste = self.Site = self.Scripts = self.Signature = self.NomD = self.NomDII = None
        
        self.liste_rapide = dictio['Liste_Rapide']
        self.Cadres()
        #   M E N U 
        self.menu_options = {
            "Log": lambda *args: self.__ouvrir__(fichierdossier=Repertoire),
            "Inventaire": '',
            "Save": lambda instance, val1='all', val2=None: self.save(instance=instance, sett=val1, option_envoi=val2),
            "Clear": self.clear,
            "Restart": self.__restart__,
            "Quitter": self.quitter,
            "Clean": self.supprimerTout,
            "Aperçu ": '',
            "Notes": None,
            "Texte": lambda instance, file=texteWord: self.__ouvrir__(fichierdossier=file),
            f"{self.nombre_postulee}": None,
            f"{self.nbreEntreeTotal}":lambda instance, val=0: self.set_nbre_Postulee_jour(val),
        }

        self.dictionnaire_bouton_menu = Menu(self=self, cadre=self.cadreI, tableau=self.menu_options, dictio=self.dictionnaire_bouton_menu,
                                             haut=30, police=20, largeur=None, color=BLEUFONCE, x=0.2, y=None, color2=ROUGE)

        # Ajout de widgets
        self.objects = {}
        # 1er groupe case
        self.affichage_special_boutons()
        self.affichage_special_boutons('others')
    
        self.tableau_insertion = [
                self.Jour,
                self.Entreprise,
                self.Adresse,
                self.Lien,
                self.AutreLien,
                self.Prenom,
                self.Nom,
                self.Phone,
                self.Courriel,
                self.Departements,
                self.Fonctions,
                self.Age,
        ]
        
        self.cellules_non_remplies = len(self.tableau_insertion)
        self.dictionnaire_bouton_menu['Save'].text = f"{len(self.tableau_insertion)}"
        # COULEUR d'ecran
        colorer(self, self.dictionnaire_bouton_menu[f"{self.nombre_postulee}"], couleur=NOIR)
        colorer(self, self.dictionnaire_bouton_menu[f"{self.nbreEntreeTotal}"], couleur=NOIR)

        # Detection des entrees 
        self.initiateur_compteur()
        
    def Cadres(self) :
        # Colonnes
        self.cols = 1
        # Menu
        self.cadreI = add_object(self=self, cols=6, row_f=5)
        # FORMULAIRE
        self.cadreIV = add_object(self, cols=6, sett='scroll', couleur=ORANGE, sticky=None)
        # Cadre interne - JOBNAMES
        # self.cadreIII = add_object(self, row_f=2, col1=2, col2=3, sett='doublecadre', cadrage='gche', forme='scroll')
        # Cadre interne - COCHEUR
        # self.cadreII = add_object(self, row_f=1, col1=2, col3=4, sett='doublecadre', cadrage='dte', forme='scroll')
        self.cadreII = add_object(self, row_f=1, cols=8)
        # Renommer
        self.cadreV = add_object(self, cols=1, row_f=1, col_f=10, sticky=None)
        
        # FICHIER EN COURS
        # self.cadreIV_I = add_object(self, cols=3, sett='scroll')
    
    def affichage_special_boutons(self, sett='action'):

        if sett == 'auto':
            self.ciblerEnvoyer(cible=f"{self.Prenom.text}", tag=cle_PRENOM,  sett='all')
            self.ciblerEnvoyer(cible=f"{self.Nom.text}", tag=cle_NOM, sett='all')      
            self.ciblerEnvoyer(cible=f"{self.Age.text}", tag=cle_AGE, sett='all')
            self.ciblerEnvoyer(cible=f"{self.Fonctions.text}", tag=cle_FONCTIONS, sett='all')
            self.ciblerEnvoyer(cible=f"{self.Jour.text}", tag=cle_DATE, sett='all')
            self.ciblerEnvoyer(cible=f"{self.AutreLien.text}", tag=cle_LIEN, sett='all')
            self.ciblerEnvoyer(cible=f"{self.Entreprise.text}", tag=cle_ENTREPRISE, sett='all')
            self.ciblerEnvoyer(cible=f"{self.Phone.text}", tag=cle_PHONE, sett='all')
            self.ciblerEnvoyer(cible=f"{self.Courriel.text}", tag=cle_COURRIEL, sett='all')
            self.ciblerEnvoyer(cible=f"{self.Privileges.text}", tag=cle_PRIVILEGES, sett='all')
            self.ciblerEnvoyer(cible=f"{self.Departements.text}", tag=cle_DEPARTEMENTS, sett='all')
            self.ciblerEnvoyer(cible=f"{self.Editeur.text}", tag=cle_EDITEUR, sett='all')
            self.ciblerEnvoyer(cible=f"{self.Adresse.text}", tag=cle_ADRESSE, sett='all')
                        
        elif sett == 'others':
            self.Prenom = remplisseur(self, objet=self.cadreIV, texte=_prenom_)
            commandes_bouton(self, objet=self.cadreIV, text="Go", police=20, hauteur=70, largeur=50,
                                commande=lambda *args: self.ciblerEnvoyer(cible=f"{self.Prenom.text}", tag=cle_PRENOM, tagII=cle_PRENOM, sett='all'))
            
            self.Age = remplisseur(self, objet=self.cadreIV, texte=_age_)
            commandes_bouton(self, objet=self.cadreIV, text="Go", police=20, hauteur=70, largeur=50,
                                commande=lambda *args: self.ciblerEnvoyer(cible=f"{self.Age.text}", tag=cle_AGE, sett='all'))
            
            self.Nom = remplisseur(self, objet=self.cadreIV, texte=_nom_)
            commandes_bouton(self, objet=self.cadreIV, text="Go", police=20, hauteur=70, largeur=50, 
                                commande=lambda *args: self.ciblerEnvoyer(cible=f"{self.Nom.text}", tag=cle_NOM,  sett='all'))

            self.Phone = remplisseur(self, objet=self.cadreIV, texte=_phone_)
            commandes_bouton(self, objet=self.cadreIV, text="Go", police=20, hauteur=70, largeur=50,
                                commande=lambda *args: self.ciblerEnvoyer(cible=f"{self.Phone.text}", tag=cle_PHONE, sett='all'))
            
            # CSV : numero de phone____________________________________________________________________
            self.Courriel = remplisseur(self, objet=self.cadreIV, texte=_courriel_)
            commandes_bouton(self, objet=self.cadreIV, text="Go", police=20, hauteur=70, largeur=50,
                                commande=lambda *args: self.ciblerEnvoyer(cible=f"{self.Courriel.text}", tag=cle_COURRIEL, sett='all'))
            # CSV : adresse courriel
            self.Departements = remplisseur(self, objet=self.cadreIV, texte=_departements_)
            commandes_bouton(self, objet=self.cadreIV, text="Go", police=20, hauteur=70, largeur=50,
                                commande=lambda *args: self.ciblerEnvoyer(cible=f"{self.Departements.text}", tag=cle_DEPARTEMENTS, sett='all'))
    
            self.Adresse = remplisseur(self, objet=self.cadreIV, texte=_adresse_)
            commandes_bouton(self, objet=self.cadreIV, text="Go", police=20, hauteur=70, largeur=50,
                              commande=lambda *args: self.ciblerEnvoyer(cible=f"{self.Adresse.text}", tag=cle_ADRESSE, sett='all')) 
            
            
            self.AutreLien = remplisseur(self, objet=self.cadreIV, texte=autre_lien_)
            commandes_bouton(self, objet=self.cadreIV, text="Go", police=20, hauteur=70, largeur=50, 
                                commande=lambda *args: self.ciblerEnvoyer(cible=f"{self.AutreLien.text}", tag=cle_LIEN, sett='all'))
            
            # CSV _______________________________________________________________________________
            self.Lien = remplisseur(self, objet=self.cadreIV, texte=_lien_)
            self.csv_bouton = commandes_bouton(self, objet=self.cadreIV, text="Go", police=20, hauteur=70, largeur=50, 
                                commande=lambda *args: self.csv())
            # LETTRE ________________________________________________________________________________________
            
            self.Entreprise = remplisseur(self, objet=self.cadreIV, texte=_entreprise_)
            commandes_bouton(self, objet=self.cadreIV, text="Go", police=20, hauteur=70, largeur=50, 
                                commande=lambda *args: self.ciblerEnvoyer(cible=f"{self.Entreprise.text}", tag=cle_ENTREPRISE, sett='all'))  
            
            
            # AUTOMATIQUE ______________________________________________________________________________________
            self.Fonctions = remplisseur(self, objet=self.cadreIV, texte=_fonctions_, couleur=GRISCLAIR)
            commandes_bouton(self, objet=self.cadreIV, text="Go", police=20, hauteur=70, largeur=50,
                                commande=lambda *args: self.ciblerEnvoyer(cible=f"{self.Fonctions.text}", tag=cle_FONCTIONS,  sett='all'))

            self.Jour = remplisseur(self, objet=self.cadreIV, texte=_jour_, couleur=GRISCLAIR)
            commandes_bouton(self, objet=self.cadreIV, text="Go", police=20, hauteur=70, largeur=50, 
                                commande=lambda *args: self.ciblerEnvoyer(tag=cle_DATE, tagII=cle_DATE, cible=f"{self.Jour.text}", sett='all'))

            self.Privileges = remplisseur(self, objet=self.cadreIV, texte=_privileges_, couleur=GRISCLAIR)
            commandes_bouton(self, objet=self.cadreIV, text="Go", police=20, hauteur=70, largeur=50,
                                commande=lambda *args: self.ciblerEnvoyer(cible=f"{self.Privileges.text}", tag=cle_PRIVILEGES, sett='all'))
            
            self.Editeur = remplisseur(self, objet=self.cadreIV, texte=_editeur_, couleur=GRISCLAIR)
            commandes_bouton(self, objet=self.cadreIV, text="Go", police=20, hauteur=70, largeur=50,
                                commande=lambda *args: self.ciblerEnvoyer(cible=f"{self.Editeur.text}", tag=cle_EDITEUR, sett='all'))

            self.Notes = remplisseur(self, objet=self.cadreV, texte=_utilitaires_, width=len(_utilitaires_*10),
                                              couleur=GRISCLAIR, height=20, sett='hauteur')
            
            notess = ry.chercher_ds_JSON(dictionnaire=dictio, cle1='Profil', cle2='Lien RH', sett='valeurcles')
            
            self.Notes.text = ry.lireFichier(initM.chemin_ressource(notess))

            self.affichage_boutons(tagger=self.Jour, text=_jour_, tag=_DATE_RH, sett='manuel')
            self.affichage_boutons(tagger=self.Editeur, text=_editeur_, tag=_EDITEUR_RH, sett='manuel')
            self.affichage_boutons(tagger=self.Fonctions, text=_fonctions_, tag=_FONCTIONS, sett='manuel')
            self.affichage_boutons(tagger=self.Entreprise, text=_entreprise_, tag=_ENTREPRISE, sett='manuel')
            self.affichage_boutons(tagger=self.Departements, text=_departements_, tag=_DEPARTEMENTS, sett='manuel')

            # for jobssite_ in self.liste_rapide:
            #     commandes_bouton(self, objet=self.cadreIII, text=jobssite_, police=17, hauteur=50, 
            #                         commande=lambda instance, jobssite_=jobssite_, objet=self.Site: self.remplir_input(text=jobssite_, objet=objet))

    def affichage_boutons(self, tagger=None, text='vide', tag='', sett='default'):
        
        if valideur_cocheur :
            auto = True
        else :
            auto = False
            
        if sett == 'default':
            tagger = remplisseur(self, objet=self.cadreIV, texte=text)
            commandes_bouton(self, objet=self.cadreIV, text="Go", police=20, hauteur=70, largeur=50,
                                commande=lambda *args: self.ciblerEnvoyer(cible=f"{tagger.text}", tag=tag, sett=sett))
            self.objects[tag] = tagger
            # Cadrant
            if text == _jour_ :
                self.cocheur_bouton(objet=self.cadreIII, text=date_formatee, cadrant=tagger, auto=auto)
            if text == _editeur_ :
                self.cocheur_bouton(objet=self.cadreIII, text='Ryan Moise Badye Kayamba', cadrant=tagger, auto=auto)
            
        elif sett == 'manuel':
            if text == _jour_ :
                self.cocheur_bouton(objet=self.cadreII, text=date_formatee, titre=text, cadrant=tagger, auto=auto)
            if text == _editeur_ :
                self.cocheur_bouton(objet=self.cadreII, text='Ryan', titre=text, cadrant=tagger, auto=auto)
            if text == _fonctions_ :
                self.cocheur_bouton(objet=self.cadreII, text='Administrateur', titre=text, cadrant=tagger, auto=auto)
            if text == _entreprise_ :
                self.cocheur_bouton(objet=self.cadreII, text='Delifruit', titre=text, cadrant=tagger, auto=auto)
            if text == _departements_ :
                self.cocheur_bouton(objet=self.cadreII, text='Direction', titre=text, cadrant=tagger, auto=auto)
            
    def pageMD(self):
        texte = "Texte déroulant"
        # Cadre de bouton, menu déroulant
        self.scroll = ScrollView(size_hint_y=None, height=0)
        self.label = Label(
            text=texte,
            size_hint_y=None,
            text_size=(400, None),
            halign="left",
            valign="top"
        )
        self.label.bind(texture_size=self._resize_label)
        self.scroll.add_widget(self.label)
        self.add_widget(self.scroll)
       
    def cocheur_bouton(self, text=None, objet=None, titre=None, cadrant=None, auto=False):
        self.cocheur = CheckBox(size_hint_y=None, height=20)
        if objet is None :
            self.cocheur.bind(active=lambda instance, value, checkbox=text: self.autoremplir(checkbox, cadrant, value))
            self.add_widget(self.cocheur)
            self.add_widget(Label(text=text))
            
        if objet and auto == False :
            dictio[checker] = 'cochee'
            ry.ecrire_ds_json(fichier=fichier_configuration, contenu=dictio)
            self.cocheur.bind(active=lambda instance, value, checkbox=text: self.autoremplir(checkbox, cadrant, value))
            objet.add_widget(self.cocheur)
            objet.add_widget(Label(text=titre))
            
        if objet and auto == True :
            self.cocheur.active = auto
            self.cocheur.bind(active=partial(self.autoremplir, checkbox=text, objet=cadrant))
            objet.add_widget(self.cocheur)
            objet.add_widget(Label(text=titre))
        
        return self.cocheur
  
    def taillefichier(self, btn=None):
        self.csvnbre = ry.lireFile(self.fichier_csv, set=2)
        self.csvnbre = len(self.csvnbre.split('\n')) - 1
        self.apresclic(btn, f"{self.csvnbre}", couleur=VERT)

    def apresclic(self, bouton, valeur=None, couleur=VERT):
        bouton.text = valeur
        colorer(self, bouton, couleur)

    def remplir_input(self, text=None, objet=None):
        if text and objet:
            objet.text = text            
            self.on_text_change(objet, objet.text, sett='cocher')

    def binder(self, obj, text):
        if text == "Aperçu " :
            self.submit.bind(on_release=self.toggle)
            self.pageMD()
            # obj.add_widget(self.submit)

    def afficher_nbre_postulee(self, valeur=None) :
        if valeur == 'nbreEntreeJour':
            return ry.chercher_ds_JSON(dictionnaire=dictio, cle1='Nombres_Utilisateurs', 
                                        cle2='nbreEntreeJour', sett='valeurcles')
        elif valeur == 'nbreEntreeTotal':
            return ry.chercher_ds_JSON(dictionnaire=dictio, cle1='Nombres_Utilisateurs', 
                                        cle2='nbreEntreeTotal', sett='valeurcles')

    def save(self, instance, sett='all', option_envoi=None):
        envoi = []
        self.nombre_postulee = self.afficher_nbre_postulee('nbreEntreeJour')
        self.nbreEntreeTotal = self.afficher_nbre_postulee('nbreEntreeTotal')
        dictio = ry.lireJSON(fichier=fichier_configuration)
        if option_envoi is None :
            option_envoi = ry.chercher_ds_JSON(dictionnaire=dictio, cle1='Methode_D_Envoi', cle2='langage', sett='valeurcles')
        
        if sett == 'all' :
            if self.csv_cv is not None :
                try:
                    self.nbre_changee_a_l_affichage()
                    self.affichage_special_boutons(sett='auto')
                    self.save(instance=instance, sett='sql', option_envoi=option_envoi)
                    # self.ouvrir_fichier(self.INITfileRH, sett='lire')
                    # self.renommer_fichier(fichier=self.INITfileRH, objet=self.cadreV)
                    if option_envoi == 'py' or option_envoi == 'python':      
                        rcp(ry.Magenta, f"Envoi des données vers la base de données via {option_envoi}...")   
                        if initM.os.path.exists(fichier_credentials):               
                            mongoHEAD = ry.chercher_ds_JSON(dictionnaire=credential, cle1="Credentials", cle2='SRV', sett='valeurcles')
                            DB_USER = ry.chercher_ds_JSON(dictionnaire=credential, cle1="Credentials", cle2='DB_USER', sett='valeurcles')
                            DB_PASSWORD = ry.chercher_ds_JSON(dictionnaire=credential, cle1="Credentials", cle2='DB_PASSWORD', sett='valeurcles')
                            mongoEND = ry.chercher_ds_JSON(dictionnaire=credential, cle1="Credentials", cle2='API_KEY', sett='valeurcles')
                            mongoDB = ry.chercher_ds_JSON(dictionnaire=credential, cle1="Credentials", cle2='DB_RH', sett='valeurcles')
                            mongoCOL = ry.chercher_ds_JSON(dictionnaire=credential, cle1="Credentials", cle2='COL', sett='valeurcles')
                        
                            mongoLIEN = f"{mongoHEAD}//{DB_USER}:{DB_PASSWORD}@{mongoEND}/?retryWrites=true&w=majority"
                            ry.envoi_BD_MONGO(lien=mongoLIEN, BD=mongoDB, collection=mongoCOL, 
                                            fichier=LETTREFichierRH)
                    elif option_envoi == 'psh' or option_envoi.lower() == 'powershell':
                        psh.run([
                            "Powershell.exe",
                            "-NoLogo", "-NoProfile", "-ExecutionPolicy", "Bypass",
                            "-File", rf"{initM.librairie}/envoi_vers_BD.ps1"
                        ])
                                            
                except Exception as arr:
                    pass; # err(tabErreur=initM.traceback.extract_tb(initM.sys.exc_info()[2]), NomErreur='save', ValeurErreur=arr)
            
            else :
                colorer(self, bouton=self.Lien, couleur=ROUGE)
                colorer(self, self.dictionnaire_bouton_menu['Save'], couleur=ROUGE)
                
        elif sett == 'sql':
            dictio_form_RH = ry.lireJSON(fichier=LETTREFichierRH)
            if option_envoi is None :
                option_envoi = ry.chercher_ds_JSON(dictionnaire=dictio_form_RH, cle1='Methode_D_Envoi', cle2='langage', sett='valeurcles')
            if dictio_form_RH is not None :
                _DATE_IN = LETTRE_IN['Date_de_creation']
                _PRODUIT = LETTRE_IN['Produit']
                _TYPE = LETTRE_IN['Types']
                _ANNEE = LETTRE_IN['Annee']
                _FABRICANT = LETTRE_IN['Fabricant']
                _PROVENANCE = LETTRE_IN['Provenance']
                _PRIX = LETTRE_IN['Prix']
                _EDITEUR_IN = LETTRE_IN['Editeur']
                _DESTINATION = LETTRE_IN['Destination']
                _SIMILAIRES = LETTRE_IN['Similaires']
                _QUANTITE = LETTRE_IN['Spécificités']
                _LIEN = LETTRE_IN['Lien']
                _APPROBATIONS = LETTRE_IN['Approbations']
                
                ry.rajouter_ds_fichier(fichier=LETTREFichier_sqlRH, contenu=f"INSERT INTO Date_de_creation (date_production) VALUES\n('{_DATE_IN}')")
                ry.rajouter_ds_fichier(fichier=LETTREFichier_sqlRH, contenu=f"INSERT INTO Produit (nom) VALUES\n('{_PRODUIT}')")
                ry.rajouter_ds_fichier(fichier=LETTREFichier_sqlRH, contenu=f"INSERT INTO Type (nom) VALUES\n('{_TYPE}')")
                ry.rajouter_ds_fichier(fichier=LETTREFichier_sqlRH, contenu=f"INSERT INTO Annee (valeur) VALUES\n('{_ANNEE}')")
                ry.rajouter_ds_fichier(fichier=LETTREFichier_sqlRH, contenu=f"INSERT INTO Fabricant (nom) VALUES\n('{_FABRICANT}')")
                ry.rajouter_ds_fichier(fichier=LETTREFichier_sqlRH, contenu=f"INSERT INTO Provenance (pays) VALUES\n('{_PROVENANCE}')")
                ry.rajouter_ds_fichier(fichier=LETTREFichier_sqlRH, contenu=f"INSERT INTO Prix (montant, devise) VALUES\n('{_PRIX}')")
                ry.rajouter_ds_fichier(fichier=LETTREFichier_sqlRH, contenu=f"INSERT INTO Editeur (nom) VALUES\n('{_EDITEUR_IN}')")
                ry.rajouter_ds_fichier(fichier=LETTREFichier_sqlRH, contenu=f"INSERT INTO Destination (pays) VALUES\n('{_DESTINATION}')")
                ry.rajouter_ds_fichier(fichier=LETTREFichier_sqlRH, contenu=f"INSERT INTO Similaires (produit_id, similaire_id) VALUES\n('{_SIMILAIRES}')")
                ry.rajouter_ds_fichier(fichier=LETTREFichier_sqlRH, contenu=f"INSERT INTO Specificites (description) VALUES\n('{_QUANTITE}')")
                ry.rajouter_ds_fichier(fichier=LETTREFichier_sqlRH, contenu=f"INSERT INTO Lien (url) VALUES\n('{_LIEN}')")
                ry.rajouter_ds_fichier(fichier=LETTREFichier_sqlRH, contenu=f"INSERT INTO Approbations (produit_id, organisme, date_approbation) VALUES\n('{_APPROBATIONS}')")
            
        elif sett == 'espace' :
                self.espacer(5)
        else :
            self.add_widget(Label(text="Vide !"))
            self.name = None

    def apresclicmessage(self, bouton, valeur=None, sett=None):
        if sett == 'messageautotaille':
            self.taillefichier(bouton)
        elif sett == 'messageavecbouton':
            bouton.bind(on_release=lambda btn, valeur=valeur: self.apresclic(btn, f"{valeur}"))
        elif sett == 'message':
            bouton.text = str(valeur)

    def csv(self):

        self.apresclicmessage(bouton=self.csv_bouton, sett='messageautotaille')      
        self.csv_cv = True
        # Les noms des colonnes (en-tête)
        entetes = [
                    "Date d'envoi du CV et de la lettre",
                    "Nom de l'entreprise",
                    "Adresse de l'entreprise",
                    "Lien d'affichage du stage/poste",
                    "CV et lettre remis en main propre",
                    "Titre du poste",
                    "Nom du contact",
                    "Numéro de téléphone",
                    "Adresse courriel",
                    "Réponse/Relance/informations supplémentaires",
                    "Autres liens sites"
                   ]

        # Données à écrire
        donnees = [
            {
                "Date d'envoi du CV et de la lettre": self.Jour.text,
                "Nom de l'entreprise": self.Entreprise.text,
                "Adresse de l'entreprise": self.Adresse.text,
                "Lien d'affichage du stage/poste": self.Lien.text,
                "CV et lettre remis en main propre": self.nom_sans_ext,
                # "Titre du poste": self.Poste.text,
                # "Nom du contact": self.NomD.text,
                "Numéro de téléphone": self.Phone.text,
                "Adresse courriel": self.Courriel.text,
                "Réponse/Relance/informations supplémentaires": "En attente",
                "Autres liens sites": self.AutreLien.text
            }
        ]

        # Ouvrir le fichier en mode écriture
        with open(self.fichier_csv, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=entetes)

            if csvfile.tell() == 0:
                # Écrire l'en-tête
                writer.writeheader()
                
            # Écrire les lignes de données
            writer.writerows(donnees)

    def nbre_changee_a_l_affichage(self):
        self.valideur_nbre_jr = False
        add_post_simple = self.nbreEntreeTotal + 1
        add_post_global = self.nombre_postulee + 1
        ry.ecrire_ds_json(fichier=fichier_configuration, dictionnaire=dictio, contenu=add_post_simple, 
                            cle1='Nombres_Utilisateurs', cle2='nbreEntreeTotal', sett='remplacer')
        ry.ecrire_ds_json(fichier=fichier_configuration, dictionnaire=dictio, contenu=add_post_global, 
                            cle1='Nombres_Utilisateurs', cle2='nbreEntreeJour', sett='remplacer')
        
        try :
            self.apresclicmessage(bouton=self.dictionnaire_bouton_menu[f"{self.nbreEntreeTotal}"], 
                                valeur=add_post_simple, sett='message')
            self.apresclicmessage(bouton=self.dictionnaire_bouton_menu[f"{self.nombre_postulee}"], 
                                valeur=add_post_global, sett='message')
        except KeyError as krr:
            pass; # err("nbreEntreeJour", "nbre_changee_a_l_affichage", krr)

    def autredossier(self, instance):
        for dossier in DOSSIER:
            try:
                os.startfile(dossier)
            except Exception:
                continue

    def ouvrir_fichier(self, fichier, sett='ouvrir'):
        if sett == 'ouvrir':
            # psh.run(['explorer.exe', fichier],
            #                             capture_output=True, text=True, check=True)
            os.startfile(fichier)
        elif sett == 'lire':
            ry.lireFile(fichier)

    def renommer_fichier(self, fichier, objet=None):
        def renomme(newname) :
            os.rename(fichier, os.path.join(os.path.dirname(fichier), f"{newname}.md"))
            def pdf_convert(newname) :
                newname = newname
                self.nom_sans_ext = os.path.splitext(newname)[0]
                
                self.INITfileRH = os.path.join(os.path.dirname(fichier), newname)
                psh.Popen(['Powershell.exe', '-Command', 'pandoc', self.INITfileRH, '-o', f"{DossierSORTIE}/{self.nom_sans_ext}.pdf"])

            def doc_convert(newname) :
                newname = newname
                self.nom_sans_ext = os.path.splitext(newname)[0]
                
                self.INITfileRH = os.path.join(os.path.dirname(fichier), newname)
                fichierDOC = f"{DossierSORTIE}/{self.nom_sans_ext}.docx"
                psh.Popen(['Powershell.exe', '-Command', 'pandoc', self.INITfileRH, '-o', fichierDOC])
                os.startfile(DossierSORTIE)
                
                # Appeler le fichier word
                if os.path.exists(fichierDOC):
                    os.startfile(fichierDOC)
                
            self.pdf = Button(text='ConvertirPDF', font_size=20, size_hint_y=None, height=30)
            self.pdf.bind(on_press=lambda *args: pdf_convert(f"{newname}.md"))
            self.add_widget(self.pdf)
            
            self.doc = Button(text='ConvertirDOC', font_size=20, size_hint_y=None, height=30)
            self.doc.bind(on_press=lambda *args: doc_convert(f"{newname}.md"))
            self.add_widget(self.doc)

        self.soum = Button(text='Renommer', font_size=20, size_hint_y=None, height=30)
        file = os.path.basename(fichier)
        self.renommerfichier = remplisseur(self, texte=file, objet=objet, height=2, sett='hauteur')
        self.soum.bind(on_press=lambda *args: renomme(self.renommerfichier.text))
        self.add_widget(self.soum)
        
    def autoremplir(self, checkbox=None, objet=None, value=None):
        if value:
            objet.text = checkbox
        else:
            objet.text = ''
            dictio[checker] = None
            ry.ecrire_ds_json(fichier=fichier_configuration, contenu=dictio)
            
        self.on_text_change(objet, objet.text, sett='cocher')

    def ciblerEnvoyer(self, instance=None, tag=None, tagII=None, cible=None, a_changer=None, avec=None, sett='all'):
        envoi = []
        if cible is not None:
            if sett == 'all':
                print
                rcp(ry.Green, f"{self.Prenom.text}", f"{_PRENOM}")
                ry.ecrire_ds_json(fichier=LETTREFichierRH, dictionnaire=self.LETTRE, cle1=tag, val=cible, sett='remplacer')
            elif sett == 'adresse':
                
                adresse_complete = cible.split()
                
                adresseII = adresse_complete[-4:]
                adresseII = " ".join(adresseII)
                adresseII = adresseII.replace(f'{a_changer}', f'{avec}')
                adresseI = adresse_complete[:-4]
                adresseI = " ".join(adresseI)
                
                envoi = LETTRE_RH.replace(f"{tag}", f"{adresseI}")
                envoi = envoi.replace(f"{tagII}", f"{adresseII}")
                with open(self.INITfileRH, 'w', encoding='utf-8') as write :
                    if cible != '' and cible is not None:
                        initM.json.dump(envoi, write, indent=4, ensure_ascii=False)
                    else:
                        initM.json.dump(LETTRE_RH, write, indent=4, ensure_ascii=False)

            elif sett == 'espace' :
                self.espacer(5)
            elif sett == 'test':
                self.add_widget(Label(text=f"Test: {cible} \nADRESSE: {tag}"))
        else :
            self.add_widget(Label(text="Vide !"))
            self.name = None
            
    def show_input_dialog(self, instance=None):
        dialog = InputDialog()
        dialog.bind(on_dismiss=lambda x: self.store_value(dialog.valeur))
        dialog.open()
        
    def store_value(self, valeur):
        if valeur:
            self.valeur_stockee = valeur
            print(f"Valeur stockée : {self.valeur_stockee}")
            
    def espacer(self, nombre): # 
        with open(self.INITfileRH, 'a') as write :
            write.write("\n" * nombre)

    def clear(self, instance):        
        for element in self.tableau_insertion:
            element.text = ""            
        generer_fichier(INITfileRH, LETTREFichierRH)
          
    def supprimerTout(self, instance):
        def recycler_word(self, source, destination, extension) :
            if os.path.exists(source):
                dossier_de_travail = os.listdir(source)
                if dossier_de_travail is not None :
                    fichier_trouvees = [i for i in dossier_de_travail if extension in i]
                    if fichier_trouvees != []:
                        for fichier in fichier_trouvees:
                            fichier_trouvee = f'{source}/{fichier}'
                            try :
                                initM.shutil.move(fichier_trouvee, destination)
                            except PermissionError as p:
                                pass; # err('PermissionError', 'recycler_word', p)                                 
                            except initM.shutil.Error:
                                fichier_restant = f'{source}/{fichier}'
                                fichier = fichier.replace('.', '_0.')   
                                destination = f'{destination}/{fichier}'                             
                                try :
                                    initM.shutil.move(fichier_restant, destination)
                                except PermissionError as p:
                                    pass; # err('PermissionError', 'recycler_word', p) 
            else :
                self.show_input_dialog()  
                if os.path.exists(self.valeur_stockee):  
                    source = self.valeur_stockee        
                    if os.path.exists():
                        recycler_word(self, source, destination, extension)
                    else :
                        self.show_input_dialog()
                        destination = self.valeur_stockee  
                        recycler_word(self, source, destination, extension)
                
        dossier_de_travail = os.listdir(initM.DossierMarkdown)
        fichier_inutiles = [i for i in dossier_de_travail if markdownobject in i and '.md' in i]
        fichier_restants = [i for i in dossier_de_travail if markdownobject not in i and '.md' in i]
        if fichier_inutiles != []:
            dossier_exclus, fichier_exclus = os.path.split(INITfileRH)
            for fichier in fichier_inutiles:
                if fichier != fichier_exclus:
                    chemin = os.path.join(initM.DossierMarkdown, fichier)
                    os.remove(chemin)
                    if self.colorationunique == False:                
                        colorer(self, bouton=self.dictionnaire_bouton_menu['Clean'], couleur=BLEUPALE) 
                        self.colorationunique = True
        if fichier_restants != []:
            for fichier in fichier_restants:
                fichier_restant = f'{initM.DossierMarkdown}/{fichier}'
                try :
                    initM.shutil.move(fichier_restant, ARCHIVES)
                except PermissionError as p:
                    pass; # err('PermissionError', 'recycler_word', p) 
                except initM.shutil.Error:
                    fichier_restant = f'{initM.DossierMarkdown}/{fichier}'
                    try :
                        initM.shutil.move(fichier_restant, ARCHIVES)
                    except PermissionError as p:
                        pass; # err('PermissionError', 'recycler_word', p) 
                
        recycler_word(self, DossierSORTIE, DossierDOC, '.docx')
            
    def _resize_label(self, instance, size):
        self.label.height = size[1]

    def toggle(self, *args):
        if not self.ouvert:
            anim = Animation(height=200, d=0.5)  # déroule
            anim.start(self.scroll)
        else:
            anim = Animation(height=0, d=0.5)  # replie
            anim.start(self.scroll)
        self.ouvert = not self.ouvert
   
    def quitter(self, instance):
        ry.ecrire_ds_json(fichier=LETTREFichierRH, dictionnaire=initM.contenu_init_RH, sett=4)
        ry.ecrire_ds_json(fichier=LETTREFichierIN, dictionnaire=initM.contenu_init_IN, sett=4)
        App.get_running_app().stop()
    # Compteur d'entrees ________________________________________________________
    def initiateur_compteur(self):       
        for element in self.tableau_insertion:
            self.on_text_change(element, element.text, sett='accumulation')

    def on_text_change(self, instance, valeur, sett='accumulation'):
        if sett == 'accumulation':
            mots = valeur.split()
            
            # On garde une liste des mots déjà comptés
            if not hasattr(self, '_mots_comptes'):
                self._mots_comptes = set()
            
            for mot in mots:
                if len(mot) == 3 and mot not in self._mots_comptes:
                    self.cellules_non_remplies -= 1
                    self._mots_comptes.add(mot)
                elif '=' in mot and mot not in self._mots_comptes:
                    self.cellules_non_remplies -= 1
                    self._mots_comptes.add(mot)

        elif sett == 'cocher':
            if valeur:
                self.cellules_non_remplies -= 1

        # Mise à jour du bouton Save
        if self.cellules_non_remplies <= len(self.tableau_insertion) - 2:
            self.dictionnaire_bouton_menu['Save'].text = 'Save'
            colorer(self, self.dictionnaire_bouton_menu['Save'], couleur=VERT)
            self.csv_bouton.text = '>'
            colorer(self, self.csv_bouton, couleur=ORANGE)
            colorer(self, self.Lien, couleur=ORANGE)
        else:
            self.dictionnaire_bouton_menu['Save'].text = str(self.cellules_non_remplies)

    def set_nbre_Postulee_jour(self, nbre):
        if self.valideur_nbre_jr == False :
            self.apresclicmessage(bouton=self.dictionnaire_bouton_menu[f"{self.nbreEntreeTotal}"], 
                                valeur=nbre, sett='message')
            self.nbreEntreeTotal = nbre
            self.valideur_nbre_jr = True

    def get_nbre_Postulee_jour(self):
        return self.nbreEntreeTotal
    
    def changer_valeur_a_l_ecran(self, cible, nbre=0):
        cible = nbre
        return cible
    # Methode universelle _______________________________________________________
    def envoi_donnees_ds_JSON(self):
        ry.ecrire_ds_json(fichier=fichier_configuration, dictionnaire=dictio, contenu=self.get_nbre_Postulee_jour(), 
                            cle1='Nombres_Utilisateurs', cle2='nbreEntreeTotal', sett='remplacer')
        ry.ecrire_ds_json(fichier=fichier_configuration, dictionnaire=dictio, contenu=self.nombre_postulee, 
                            cle1='Nombres_Utilisateurs', cle2='nbreEntreeJour', sett='remplacer')
    
    def git_push(self, git=None, f_git=None, instance=None):
        
        try :
            process = psh.run([file_git_send],  capture_output=True, text=True, check=True)
            if process.stdout is not None and process.stdout != '':
                rcp(ry.Green, "STDOUT:", process.stdout)
            else :
                rcp(ry.Red, "STDERR:", process.stderr)
        except (psh.CalledProcessError, Exception) as cpe:
            pass; # err('Exception', 'git_push', cpe)                  
    
    def __ouvrir__(self, fichierdossier, valeur=None, color=BLEUPALE, sett=0): # color orange
        if sett == 0 :
            os.startfile(fichierdossier)
        if sett == 1 :
            os.startfile(Repertoire)

        if valeur is not None :
            colorer(self, self.dictionnaire_bouton_menu[valeur], couleur=color)
        
    def __restart__(self, instance):
        self.git_push(git='restart')
        self.envoi_donnees_ds_JSON()

        USER = os.getlogin()
        programme = f"{APP}"
        print(programme)

        psh.Popen([ sys.executable, f"{programme}" ])
        # Fermer proprement la fenêtre après 1 seconde
        Clock.schedule_once(lambda dt: App.get_running_app().stop(), 1)
     
# --- Première page (menu principal) ---
class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        accueil = Home()
        accueil.dictionnaire_bouton_menu['Inventaire'].bind(on_press=lambda x: setattr(self.manager, 'current', 'Inventaire'))
        accueil.dictionnaire_bouton_menu['Aperçu '].bind(on_press=lambda x: setattr(self.manager, 'current', 'Lettre'))
        accueil.dictionnaire_bouton_menu['Notes'].bind(on_press=lambda x: setattr(self.manager, 'current', 'BlocNotes'))
        self.add_widget(accueil) 
        
# --- Deuxième page ---
class InventaireScreen(Screen):    
    def __init__(self, **kwargs):
        # Appel du constructeur de grille
        super().__init__(**kwargs)
        accueil = Inventaire()
        accueil.dictionnaire_bouton_menu['Accueil'].bind(on_press=lambda x: setattr(self.manager, 'current', 'Accueil'))
        accueil.dictionnaire_bouton_menu['Aperçu '].bind(on_press=lambda x: setattr(self.manager, 'current', 'Lettre'))
        accueil.dictionnaire_bouton_menu['Notes'].bind(on_press=lambda x: setattr(self.manager, 'current', 'BlocNotes'))
        self.add_widget(accueil) 

# --- Deuxième page ---
class Inventaire(GridLayout):
    
    def __init__(self, **kwargs):
        # Appel du constructeur de grille
        super(Inventaire, self).__init__(**kwargs)
        self.nombre_postulee = self.afficher_nbre_postulee('nbreEntreeJour')
        self.nbreEntreeTotal = self.afficher_nbre_postulee('nbreEntreeTotal')
        self.colorationunique = False
        self.nom_sans_ext = None
        self.tableau_insertion = None
        self.csv_cv = None
        self.pdf = self.doc = self.soum = None
        self.INITfileRH = INITfileRH
        self.LETTRE = LETTRE_IN
        self.valideur_insert = self.valideur_nbre_jr = False
        self.dict_boutonvalideur = {}
        self.dictionnaire_bouton_menu = {} 
        # Nom du fichier CSV
        self.fichier_csv = initM.chemin_ressource("lib/csv_cv_inventaire.csv")
        # self.Jour = self.Entreprise = self.Poste = self.Site = self.Scripts = self.Signature = self.NomD = self.NomDII = None
        
        self.liste_rapide = dictio['Liste_Rapide']
        self.Cadres()
        #   M E N U 
        self.menu_options = {
            "Accueil": '',
            "Log": lambda *args: self.__ouvrir__(fichierdossier=Repertoire),
            "Save": lambda instance, val1='all', val2=None: self.save(instance=instance, sett=val1, option_envoi=val2),
            "Clear": self.clear,
            "Restart": self.__restart__,
            "Quitter": self.quitter,
            "Clean": self.supprimerTout,
            "Aperçu ": '',
            "Notes": None,
            "Texte": lambda instance, file=texteWord: self.__ouvrir__(fichierdossier=file),
            f"{self.nombre_postulee}": None,
            f"{self.nbreEntreeTotal}":lambda instance, val=0: self.set_nbre_Postulee_jour(val),
        }

        self.dictionnaire_bouton_menu = Menu(self=self, cadre=self.cadreI, tableau=self.menu_options, dictio=self.dictionnaire_bouton_menu,
                                             haut=30, police=20, largeur=None, color=VIOLET, x=0.2, y=None, color2=ROUGE)

        # Ajout de widgets
        self.objects = {}
        # 1er groupe case
        self.affichage_special_boutons()
        self.affichage_special_boutons('others')
    
        self.tableau_insertion = [
                self.Jour,
                self.Prix,
                self.Produit,
                self.Lien,
                self.Type,
                self.Annee,
                self.Fabricant,
                self.Destination,
                self.Provenance,
                self.Similaires,
                self.Specificites,
                self.Editeur,
        ]
        
        self.cellules_non_remplies = len(self.tableau_insertion)
        self.dictionnaire_bouton_menu['Save'].text = f"{len(self.tableau_insertion)}"
        # COULEUR d'ecran
        colorer(self, self.dictionnaire_bouton_menu[f"{self.nombre_postulee}"], couleur=NOIR)
        colorer(self, self.dictionnaire_bouton_menu[f"{self.nbreEntreeTotal}"], couleur=NOIR)

        # Detection des entrees 
        self.initiateur_compteur()
        
    def Cadres(self) :
        # Colonnes
        self.cols = 1
        # Menu
        self.cadreI = add_object(self=self, cols=6, row_f=5)
        # FORMULAIRE
        self.cadreIV = add_object(self, cols=6, sett='scroll', couleur=ORANGE, sticky=None)
        # Cadre interne - JOBNAMES
        # self.cadreIII = add_object(self, row_f=2, col1=2, col2=3, sett='doublecadre', cadrage='gche', forme='scroll')
        # Cadre interne - COCHEUR
        # self.cadreII = add_object(self, row_f=1, col1=2, col3=4, sett='doublecadre', cadrage='dte', forme='scroll')
        self.cadreII = add_object(self, row_f=1, cols=8)
        # Renommer
        self.cadreV = add_object(self, cols=1, row_f=1, col_f=10, sticky=None)
        
        # FICHIER EN COURS
        # self.cadreIV_I = add_object(self, cols=3, sett='scroll')
    
    def affichage_special_boutons(self, sett='action'):

        if sett == 'auto':
            self.ciblerEnvoyer(cible=f"{self.Produit.text}", tag=cle_PRODUIT,  sett='all')
            self.ciblerEnvoyer(cible=f"{self.Type.text}", tag=cle_TYPE, sett='all')      
            self.ciblerEnvoyer(cible=f"{self.Annee.text}", tag=cle_ANNEE, sett='all')
            self.ciblerEnvoyer(cible=f"{self.Fabricant.text}", tag=cle_FABRICANT, sett='all')
            self.ciblerEnvoyer(cible=f"{self.Jour.text}", tag=cle_DATE, sett='all')
            self.ciblerEnvoyer(cible=f"{self.Prix.text}", tag=cle_PRIX, sett='all')
            self.ciblerEnvoyer(cible=f"{self.Destination.text}", tag=cle_DESTINATION, sett='all')
            self.ciblerEnvoyer(cible=f"{self.Similaires.text}", tag=cle_SIMILAIRES, sett='all')
            self.ciblerEnvoyer(cible=f"{self.Provenance.text}", tag=cle_PROVENANCE, sett='all')
            self.ciblerEnvoyer(cible=f"{self.Lien.text}", tag=cle_LIEN, sett='all')
            self.ciblerEnvoyer(cible=f"{self.Editeur.text}", tag=cle_EDITEUR, sett='all')
            self.ciblerEnvoyer(cible=f"{self.Specificites.text}", tag=cle_QUANTITE, sett='all')
                        
        elif sett == 'others':
            self.Produit = remplisseur(self, objet=self.cadreIV, texte=_produit_)
            commandes_bouton(self, objet=self.cadreIV, text="Go", police=20, hauteur=70, largeur=50,
                                commande=lambda *args: self.ciblerEnvoyer(cible=f"{self.Produit.text}", tag=cle_PRODUIT, sett='all'))
            
            self.Annee = remplisseur(self, objet=self.cadreIV, texte=_annee_)
            commandes_bouton(self, objet=self.cadreIV, text="Go", police=20, hauteur=70, largeur=50,
                                commande=lambda *args: self.ciblerEnvoyer(cible=f"{self.Annee.text}", tag=cle_ANNEE, sett='all'))
            
            self.Type = remplisseur(self, objet=self.cadreIV, texte=_type_)
            commandes_bouton(self, objet=self.cadreIV, text="Go", police=20, hauteur=70, largeur=50, 
                                commande=lambda *args: self.ciblerEnvoyer(cible=f"{self.Type.text}", tag=cle_TYPE, sett='all'))

            # CSV : numero de phone____________________________________________________________________
            self.Provenance = remplisseur(self, objet=self.cadreIV, texte=_provenance_)
            commandes_bouton(self, objet=self.cadreIV, text="Go", police=20, hauteur=70, largeur=50,
                                commande=lambda *args: self.ciblerEnvoyer(cible=f"{self.Provenance.text}", tag=cle_PROVENANCE, sett='all'))
            # CSV : adresse courriel
            self.Destination = remplisseur(self, objet=self.cadreIV, texte=_destination_)
            commandes_bouton(self, objet=self.cadreIV, text="Go", police=20, hauteur=70, largeur=50,
                                commande=lambda *args: self.ciblerEnvoyer(cible=f"{self.Destination.text}", tag=cle_DESTINATION, sett='all'))
    
            self.Similaires = remplisseur(self, objet=self.cadreIV, texte=_similaires_)
            commandes_bouton(self, objet=self.cadreIV, text="Go", police=20, hauteur=70, largeur=50,
                              commande=lambda *args: self.ciblerEnvoyer(cible=f"{self.Similaires.text}", tag=cle_SIMILAIRES, sett='all')) 
            
            self.Prix = remplisseur(self, objet=self.cadreIV, texte=_prix_)
            commandes_bouton(self, objet=self.cadreIV, text="Go", police=20, hauteur=70, largeur=50, 
                                commande=lambda *args: self.ciblerEnvoyer(cible=f"{self.Prix.text}", tag=cle_PRIX, sett='all')) 

            # CSV _______________________________________________________________________________
            self.Lien = remplisseur(self, objet=self.cadreIV, texte=_lien_)
            self.csv_bouton = commandes_bouton(self, objet=self.cadreIV, text="Go", police=20, hauteur=70, largeur=50, 
                                commande=lambda *args: self.csv())
            # LETTRE ________________________________________________________________________________________
            self.Specificites = remplisseur(self, objet=self.cadreIV, texte=_quantite_)
            commandes_bouton(self, objet=self.cadreIV, text="Go", police=20, hauteur=70, largeur=50,
                                commande=lambda *args: self.ciblerEnvoyer(cible=f"{self.Specificites.text}", tag=cle_QUANTITE,  sett='all'))
            
            
            # AUTOMATIQUE ______________________________________________________________________________________
            self.Fabricant = remplisseur(self, objet=self.cadreIV, texte=_fabricant_, couleur=GRISCLAIR)
            commandes_bouton(self, objet=self.cadreIV, text="Go", police=20, hauteur=70, largeur=50,
                                commande=lambda *args: self.ciblerEnvoyer(cible=f"{self.Fabricant.text}", tag=cle_FABRICANT, sett='all'))
            
            self.Jour = remplisseur(self, objet=self.cadreIV, texte=_jour_, couleur=GRISCLAIR)
            commandes_bouton(self, objet=self.cadreIV, text="Go", police=20, hauteur=70, largeur=50, 
                                commande=lambda *args: self.ciblerEnvoyer(tag=cle_DATE, cible=f"{self.Jour.text}", sett='all'))
            
            self.Editeur = remplisseur(self, objet=self.cadreIV, texte=_editeur_, couleur=GRISCLAIR)
            commandes_bouton(self, objet=self.cadreIV, text="Go", police=20, hauteur=70, largeur=50,
                                commande=lambda *args: self.ciblerEnvoyer(cible=f"{self.Editeur.text}", tag=cle_EDITEUR, sett='all'))

            self.Notes = remplisseur(self, objet=self.cadreV, texte=_utilitaires_, width=len(_utilitaires_*10),
                                              couleur=GRISCLAIR, height=20, sett='hauteur')
            
            notess = ry.chercher_ds_JSON(dictionnaire=dictio, cle1='Profil', cle2='Lien Inventaire', sett='valeurcles')
            
            self.Notes.text = ry.lireFichier(initM.chemin_ressource(notess))

            self.affichage_boutons(tagger=self.Provenance, text=_provenance_, tag=_PROVENANCE, sett='manuel')
            self.affichage_boutons(tagger=self.Jour, text=_jour_, tag=_DATE_IN, sett='manuel')
            self.affichage_boutons(tagger=self.Editeur, text=_editeur_, tag=_EDITEUR_IN, sett='manuel')
            self.affichage_boutons(tagger=self.Fabricant, text=_fabricant_, tag=_FABRICANT, sett='manuel')
            self.affichage_boutons(tagger=self.Similaires, text=_similaires_, tag=_SIMILAIRES, sett='manuel')
            self.affichage_boutons(tagger=self.Destination, text=_destination_, tag=_DESTINATION, sett='manuel')

            # for jobssite_ in self.liste_rapide:
            #     commandes_bouton(self, objet=self.cadreIII, text=jobssite_, police=17, hauteur=50, 
            #                         commande=lambda instance, jobssite_=jobssite_, objet=self.Site: self.remplir_input(text=jobssite_, objet=objet))

    def affichage_boutons(self, tagger=None, text='vide', tag='', sett='default'):
        
        if valideur_cocheur :
            auto = True
        else :
            auto = False
            
        if sett == 'default':
            tagger = remplisseur(self, objet=self.cadreIV, texte=text)
            commandes_bouton(self, objet=self.cadreIV, text="Go", police=20, hauteur=70, largeur=50,
                                commande=lambda *args: self.ciblerEnvoyer(cible=f"{tagger.text}", tag=tag, sett=sett))
            self.objects[tag] = tagger
            # Cadrant
            if text == _jour_ :
                self.cocheur_bouton(objet=self.cadreIII, text=date_formatee, cadrant=tagger, auto=auto)
            if text == _editeur_ :
                self.cocheur_bouton(objet=self.cadreIII, text='Ryan Moise Badye Kayamba', cadrant=tagger, auto=auto)
            
        elif sett == 'manuel':
            if text == _jour_ :
                self.cocheur_bouton(objet=self.cadreII, text=date_formatee, titre=text, cadrant=tagger, auto=auto)
            if text == _editeur_ :
                self.cocheur_bouton(objet=self.cadreII, text='Ryan', titre=text, cadrant=tagger, auto=auto)
            if text == _provenance_ :
                self.cocheur_bouton(objet=self.cadreII, text='Sherbrooke', titre=text, cadrant=tagger, auto=auto)
            if text == _destination_ :
                self.cocheur_bouton(objet=self.cadreII, text='Montreal', titre=text, cadrant=tagger, auto=auto)
            if text == _prix_ :
                self.cocheur_bouton(objet=self.cadreII, text='"250", "CAD"', titre=text,  cadrant=tagger, auto=auto)
            if text == _fabricant_ :
                self.cocheur_bouton(objet=self.cadreII, text='Delifruit Enterprise', titre=text,  cadrant=tagger, auto=auto)
            
    def pageMD(self):
        texte = "Texte déroulant"
        # Cadre de bouton, menu déroulant
        self.scroll = ScrollView(size_hint_y=None, height=0)
        self.label = Label(
            text=texte,
            size_hint_y=None,
            text_size=(400, None),
            halign="left",
            valign="top"
        )
        self.label.bind(texture_size=self._resize_label)
        self.scroll.add_widget(self.label)
        self.add_widget(self.scroll)
       
    def cocheur_bouton(self, text=None, objet=None, titre=None, cadrant=None, auto=False):
        self.cocheur = CheckBox(size_hint_y=None, height=20)
        if objet is None :
            self.cocheur.bind(active=lambda instance, value, checkbox=text: self.autoremplir(checkbox, cadrant, value))
            self.add_widget(self.cocheur)
            self.add_widget(Label(text=titre))
            
        if objet and auto == False :
            dictio[checker] = 'cochee'
            ry.ecrire_ds_json(fichier=fichier_configuration, contenu=dictio)
            self.cocheur.bind(active=lambda instance, value, checkbox=text: self.autoremplir(checkbox, cadrant, value))
            objet.add_widget(self.cocheur)
            objet.add_widget(Label(text=titre))
            
        if objet and auto == True :
            self.cocheur.active = auto
            self.cocheur.bind(active=partial(self.autoremplir, checkbox=text, objet=cadrant))
            objet.add_widget(self.cocheur)
            objet.add_widget(Label(text=titre))
        
        return self.cocheur
  
    def taillefichier(self, btn=None):
        self.csvnbre = ry.lireFile(self.fichier_csv, set=2)
        self.csvnbre = len(self.csvnbre.split('\n')) - 1
        self.apresclic(btn, f"{self.csvnbre}", couleur=VERT)

    def apresclic(self, bouton, valeur=None, couleur=VERT):
        bouton.text = valeur
        colorer(self, bouton, couleur)

    def remplir_input(self, text=None, objet=None):
        if text and objet:
            objet.text = text            
            self.on_text_change(objet, objet.text, sett='cocher')

    def binder(self, obj, text):
        if text == "Aperçu " :
            self.submit.bind(on_release=self.toggle)
            self.pageMD()
            # obj.add_widget(self.submit)

    def afficher_nbre_postulee(self, valeur=None) :
        if valeur == 'nbreEntreeJour':
            return ry.chercher_ds_JSON(dictionnaire=dictio, cle1='Nombres_Utilisateurs', 
                                        cle2='nbreEntreeJour', sett='valeurcles')
        elif valeur == 'nbreEntreeTotal':
            return ry.chercher_ds_JSON(dictionnaire=dictio, cle1='Nombres_Utilisateurs', 
                                        cle2='nbreEntreeTotal', sett='valeurcles')

    def save(self, instance, sett='all', option_envoi='py'):

        def save_sql():
            dictio_form_RH = ry.lireJSON(fichier=LETTREFichierRH)
            if option_envoi is None :
                option_envoi = ry.chercher_ds_JSON(dictionnaire=dictio_form_RH, cle1='Methode_D_Envoi', cle2='langage', sett='valeurcles')
            if dictio_form_RH is not None :
                _DATE_IN = dictio_form_RH['Date_de_creation']
                _PRODUIT = dictio_form_RH['Produit']
                _TYPE = dictio_form_RH['Types']
                _ANNEE = dictio_form_RH['Annee']
                _FABRICANT = dictio_form_RH['Fabricant']
                _PROVENANCE = dictio_form_RH['Provenance']
                _PRIX = dictio_form_RH['Prix']
                _EDITEUR_IN = dictio_form_RH['Editeur']
                _DESTINATION = dictio_form_RH['Destination']
                _SIMILAIRES = dictio_form_RH['Similaires']
                _QUANTITE = dictio_form_RH['Spécificités']
                _LIEN = dictio_form_RH['Lien']
                _APPROBATIONS = dictio_form_RH['Approbations']
                print(_APPROBATIONS)
                ry.rajouter_ds_fichier(fichier=LETTREFichier_sqlIN, contenu=f"INSERT INTO Date_de_creation (date_production) VALUES\n('{_DATE_IN}')")
                ry.rajouter_ds_fichier(fichier=LETTREFichier_sqlIN, contenu=f"INSERT INTO Produit (nom) VALUES\n('{_PRODUIT}')")
                ry.rajouter_ds_fichier(fichier=LETTREFichier_sqlIN, contenu=f"INSERT INTO Type (nom) VALUES\n('{_TYPE}')")
                ry.rajouter_ds_fichier(fichier=LETTREFichier_sqlIN, contenu=f"INSERT INTO Annee (valeur) VALUES\n('{_ANNEE}')")
                ry.rajouter_ds_fichier(fichier=LETTREFichier_sqlIN, contenu=f"INSERT INTO Fabricant (nom) VALUES\n('{_FABRICANT}')")
                ry.rajouter_ds_fichier(fichier=LETTREFichier_sqlIN, contenu=f"INSERT INTO Provenance (pays) VALUES\n('{_PROVENANCE}')")
                ry.rajouter_ds_fichier(fichier=LETTREFichier_sqlIN, contenu=f"INSERT INTO Prix (montant, devise) VALUES\n('{_PRIX}')")
                ry.rajouter_ds_fichier(fichier=LETTREFichier_sqlIN, contenu=f"INSERT INTO Editeur (nom) VALUES\n('{_EDITEUR_IN}')")
                ry.rajouter_ds_fichier(fichier=LETTREFichier_sqlIN, contenu=f"INSERT INTO Destination (pays) VALUES\n('{_DESTINATION}')")
                ry.rajouter_ds_fichier(fichier=LETTREFichier_sqlIN, contenu=f"INSERT INTO Similaires (produit_id, similaire_id) VALUES\n('{_SIMILAIRES}')")
                ry.rajouter_ds_fichier(fichier=LETTREFichier_sqlIN, contenu=f"INSERT INTO Specificites (description) VALUES\n('{_QUANTITE}')")
                ry.rajouter_ds_fichier(fichier=LETTREFichier_sqlIN, contenu=f"INSERT INTO Lien (url) VALUES\n('{_LIEN}')")
                ry.rajouter_ds_fichier(fichier=LETTREFichier_sqlIN, contenu=f"INSERT INTO Approbations (produit_id, organisme, date_approbation) VALUES\n('{_APPROBATIONS}')")
            


        envoi = []
        self.nombre_postulee = self.afficher_nbre_postulee('nbreEntreeJour')
        self.nbreEntreeTotal = self.afficher_nbre_postulee('nbreEntreeTotal')

        dictio = ry.lireJSON(fichier=fichier_configuration)
        if option_envoi is None :
            option_envoi = ry.chercher_ds_JSON(dictionnaire=dictio, cle1='Methode_D_Envoi', cle2='langage', sett='valeurcles')
        
        if sett == 'all' :
            if self.csv_cv is not None :
                try:
                    self.nbre_changee_a_l_affichage()
                    self.affichage_special_boutons(sett='auto')
                    save_sql()
                    
                    if option_envoi == 'py' or option_envoi == 'python':     
                        if initM.os.path.exists(fichier_credentials):                    
                            mongoHEAD = ry.chercher_ds_JSON(dictionnaire=credential, cle1="Credentials", cle2='SRV', sett='valeurcles')
                            DB_USER = ry.chercher_ds_JSON(dictionnaire=credential, cle1="Credentials", cle2='DB_USER', sett='valeurcles')
                            DB_PASSWORD = ry.chercher_ds_JSON(dictionnaire=credential, cle1="Credentials", cle2='DB_PASSWORD', sett='valeurcles')
                            mongoEND = ry.chercher_ds_JSON(dictionnaire=credential, cle1="Credentials", cle2='API_KEY', sett='valeurcles')
                            mongoDB = ry.chercher_ds_JSON(dictionnaire=credential, cle1="Credentials", cle2='DB_IN', sett='valeurcles')
                            mongoCOL = ry.chercher_ds_JSON(dictionnaire=credential, cle1="Credentials", cle2='COL_IN', sett='valeurcles')
                            
                            mongoLIEN = f"{mongoHEAD}//{DB_USER}:{DB_PASSWORD}@{mongoEND}/?retryWrites=true&w=majority"
                            ry.envoi_BD_MONGO(lien=mongoLIEN, BD=mongoDB, collection=mongoCOL, 
                                            fichier=LETTREFichierIN)
                    elif option_envoi == 'psh' or option_envoi.lower() == 'powershell':
                        psh.run([
                            "Powershell.exe",
                            "-NoLogo", "-NoProfile", "-ExecutionPolicy", "Bypass",
                            "-File", rf"{initM.librairie}/envoi_vers_BD.ps1"
                        ])
                                            
                except Exception as arr:
                    pass; # err(tabErreur=initM.traceback.extract_tb(initM.sys.exc_info()[2]), NomErreur='save', ValeurErreur=arr)
            
            else :
                colorer(self, bouton=self.Lien, couleur=ROUGE)
                colorer(self, self.dictionnaire_bouton_menu['Save'], couleur=ROUGE)


        elif sett == 'espace' :
                self.espacer(5)
        
        else :
            self.add_widget(Label(text="Vide !"))
            self.name = None

    def apresclicmessage(self, bouton, valeur=None, sett=None):
        if sett == 'messageautotaille':
            self.taillefichier(bouton)
        elif sett == 'messageavecbouton':
            bouton.bind(on_release=lambda btn, valeur=valeur: self.apresclic(btn, f"{valeur}"))
        elif sett == 'message':
            bouton.text = str(valeur)

    def csv(self):

        self.apresclicmessage(bouton=self.csv_bouton, sett='messageautotaille')      
        self.csv_cv = True
        # Les noms des colonnes (en-tête)
        entetes = [
                    "Date d'envoi du CV et de la lettre",
                    "Nom de l'entreprise",
                    "Adresse de l'entreprise",
                    "Lien d'affichage du stage/poste",
                    "CV et lettre remis en main propre",
                    "Titre du poste",
                    "Nom du contact",
                    "Numéro de téléphone",
                    "Adresse courriel",
                    "Réponse/Relance/informations supplémentaires",
                    "Autres liens sites"
                   ]

        # Données à écrire
        donnees = [
            {
                "Date d'envoi du CV et de la lettre": self.Jour.text,
                "Nom de l'entreprise": self.Prix.text,
                "Adresse de l'entreprise": self.Provenance.text,
                "Lien d'affichage du stage/poste": self.Lien.text,
                "CV et lettre remis en main propre": self.Produit.text,
                # "Titre du poste": self.Poste.text,
                # "Nom du contact": self.NomD.text,
                "Numéro de téléphone": self.Destination.text,
                "Adresse courriel": self.Type.text,
                "Réponse/Relance/informations supplémentaires": self.Similaires.text,
                "Autres liens sites": self.Fabricant.text
            }
        ]

        # Ouvrir le fichier en mode écriture
        with open(self.fichier_csv, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=entetes)

            if csvfile.tell() == 0:
                # Écrire l'en-tête
                writer.writeheader()
                
            # Écrire les lignes de données
            writer.writerows(donnees)

    def nbre_changee_a_l_affichage(self):
        self.valideur_nbre_jr = False
        add_post_simple = self.nbreEntreeTotal + 1
        add_post_global = self.nombre_postulee + 1
        ry.ecrire_ds_json(fichier=fichier_configuration, dictionnaire=dictio, contenu=add_post_simple, 
                            cle1='Nombres_Utilisateurs', cle2='nbreEntreeTotal', sett='remplacer')
        ry.ecrire_ds_json(fichier=fichier_configuration, dictionnaire=dictio, contenu=add_post_global, 
                            cle1='Nombres_Utilisateurs', cle2='nbreEntreeJour', sett='remplacer')
        
        try :
            self.apresclicmessage(bouton=self.dictionnaire_bouton_menu[f"{self.nbreEntreeTotal}"], 
                                valeur=add_post_simple, sett='message')
            self.apresclicmessage(bouton=self.dictionnaire_bouton_menu[f"{self.nombre_postulee}"], 
                                valeur=add_post_global, sett='message')
        except KeyError as krr:
            pass; # err("nbreEntreeJour", "nbre_changee_a_l_affichage", krr)

    def autredossier(self, instance):
        for dossier in DOSSIER:
            try:
                os.startfile(dossier)
            except Exception:
                continue

    def ouvrir_fichier(self, fichier, sett='ouvrir'):
        if sett == 'ouvrir':
            # psh.run(['explorer.exe', fichier],
            #                             capture_output=True, text=True, check=True)
            os.startfile(fichier)
        elif sett == 'lire':
            ry.lireFile(fichier)

    def renommer_fichier(self, fichier, objet=None):
        def renomme(newname) :
            os.rename(fichier, os.path.join(os.path.dirname(fichier), f"{newname}.md"))
            def pdf_convert(newname) :
                newname = newname
                self.nom_sans_ext = os.path.splitext(newname)[0]
                
                self.INITfileRH = os.path.join(os.path.dirname(fichier), newname)
                psh.Popen(['Powershell.exe', '-Command', 'pandoc', self.INITfileRH, '-o', f"{DossierSORTIE}/{self.nom_sans_ext}.pdf"])

            def doc_convert(newname) :
                newname = newname
                self.nom_sans_ext = os.path.splitext(newname)[0]
                
                self.INITfileRH = os.path.join(os.path.dirname(fichier), newname)
                fichierDOC = f"{DossierSORTIE}/{self.nom_sans_ext}.docx"
                psh.Popen(['Powershell.exe', '-Command', 'pandoc', self.INITfileRH, '-o', fichierDOC])
                os.startfile(DossierSORTIE)
                
                # Appeler le fichier word
                if os.path.exists(fichierDOC):
                    os.startfile(fichierDOC)
                
            self.pdf = Button(text='ConvertirPDF', font_size=20, size_hint_y=None, height=30)
            self.pdf.bind(on_press=lambda *args: pdf_convert(f"{newname}.md"))
            self.add_widget(self.pdf)
            
            self.doc = Button(text='ConvertirDOC', font_size=20, size_hint_y=None, height=30)
            self.doc.bind(on_press=lambda *args: doc_convert(f"{newname}.md"))
            self.add_widget(self.doc)

        self.soum = Button(text='Renommer', font_size=20, size_hint_y=None, height=30)
        file = os.path.basename(fichier)
        self.renommerfichier = remplisseur(self, texte=file, objet=objet, height=2, sett='hauteur')
        self.soum.bind(on_press=lambda *args: renomme(self.renommerfichier.text))
        self.add_widget(self.soum)
        
    def autoremplir(self, checkbox=None, objet=None, value=None):
        if value:
            objet.text = checkbox
        else:
            objet.text = ''
            dictio[checker] = None
            ry.ecrire_ds_json(fichier=fichier_configuration, contenu=dictio)
            
        self.on_text_change(objet, objet.text, sett='cocher')

    def ciblerEnvoyer(self, instance=None, tag=None, tagII=None, cible=None, a_changer=None, avec=None, sett='all'):
        envoi = []
        if cible is not None:
            if sett == 'all':
                rcp(ry.Green, f"{cible}", f"{tag} : ")
                ry.ecrire_ds_json(fichier=LETTREFichierIN, dictionnaire=self.LETTRE, cle1=tag, val=cible, sett='remplacer')
            elif sett == 'adresse':
                
                adresse_complete = cible.split()
                
                adresseII = adresse_complete[-4:]
                adresseII = " ".join(adresseII)
                adresseII = adresseII.replace(f'{a_changer}', f'{avec}')
                adresseI = adresse_complete[:-4]
                adresseI = " ".join(adresseI)
                
                envoi = LETTRE_IN.replace(f"{tag}", f"{adresseI}")
                envoi = envoi.replace(f"{tagII}", f"{adresseII}")
                with open(self.INITfileIN, 'w', encoding='utf-8') as write :
                    if cible != '' and cible is not None:
                        initM.json.dump(envoi, write, indent=4, ensure_ascii=False)
                    else:
                        initM.json.dump(LETTRE_IN, write, indent=4, ensure_ascii=False)

            elif sett == 'espace' :
                self.espacer(5)
            elif sett == 'test':
                self.add_widget(Label(text=f"Test: {cible} \nADRESSE: {tag}"))
        else :
            self.add_widget(Label(text="Vide !"))
            self.name = None
            
    def show_input_dialog(self, instance=None):
        dialog = InputDialog()
        dialog.bind(on_dismiss=lambda x: self.store_value(dialog.valeur))
        dialog.open()
        
    def store_value(self, valeur):
        if valeur:
            self.valeur_stockee = valeur
            print(f"Valeur stockée : {self.valeur_stockee}")
            
    def espacer(self, nombre): # 
        with open(self.INITfileRH, 'a') as write :
            write.write("\n" * nombre)

    def clear(self, instance):        
        for element in self.tableau_insertion:
            element.text = ""
        generer_fichier(self.INITfileIN, self.LETTREFichierIN)
            
    def supprimerTout(self, instance):
        def recycler_word(self, source, destination, extension) :
            if os.path.exists(source):
                dossier_de_travail = os.listdir(source)
                if dossier_de_travail is not None :
                    fichier_trouvees = [i for i in dossier_de_travail if extension in i]
                    if fichier_trouvees != []:
                        for fichier in fichier_trouvees:
                            fichier_trouvee = f'{source}/{fichier}'
                            try :
                                initM.shutil.move(fichier_trouvee, destination)
                            except PermissionError as p:
                                pass; # err('PermissionError', 'recycler_word', p)                                 
                            except initM.shutil.Error:
                                fichier_restant = f'{source}/{fichier}'
                                fichier = fichier.replace('.', '_0.')   
                                destination = f'{destination}/{fichier}'                             
                                try :
                                    initM.shutil.move(fichier_restant, destination)
                                except PermissionError as p:
                                    pass; # err('PermissionError', 'recycler_word', p) 
            else :
                self.show_input_dialog()  
                if os.path.exists(self.valeur_stockee):  
                    source = self.valeur_stockee        
                    if os.path.exists():
                        recycler_word(self, source, destination, extension)
                    else :
                        self.show_input_dialog()
                        destination = self.valeur_stockee  
                        recycler_word(self, source, destination, extension)
                
        dossier_de_travail = os.listdir(initM.DossierMarkdown)
        fichier_inutiles = [i for i in dossier_de_travail if markdownobject in i and '.md' in i]
        fichier_restants = [i for i in dossier_de_travail if markdownobject not in i and '.md' in i]
        if fichier_inutiles != []:
            dossier_exclus, fichier_exclus = os.path.split(INITfileRH)
            for fichier in fichier_inutiles:
                if fichier != fichier_exclus:
                    chemin = os.path.join(initM.DossierMarkdown, fichier)
                    os.remove(chemin)
                    if self.colorationunique == False:                
                        colorer(self, bouton=self.dictionnaire_bouton_menu['Clean'], couleur=BLEUPALE) 
                        self.colorationunique = True
        if fichier_restants != []:
            for fichier in fichier_restants:
                fichier_restant = f'{initM.DossierMarkdown}/{fichier}'
                try :
                    initM.shutil.move(fichier_restant, ARCHIVES)
                except PermissionError as p:
                    pass; # err('PermissionError', 'recycler_word', p) 
                except initM.shutil.Error:
                    fichier_restant = f'{initM.DossierMarkdown}/{fichier}'
                    try :
                        initM.shutil.move(fichier_restant, ARCHIVES)
                    except PermissionError as p:
                        pass; # err('PermissionError', 'recycler_word', p) 
                
        recycler_word(self, DossierSORTIE, DossierDOC, '.docx')
            
    def _resize_label(self, instance, size):
        self.label.height = size[1]

    def toggle(self, *args):
        if not self.ouvert:
            anim = Animation(height=200, d=0.5)  # déroule
            anim.start(self.scroll)
        else:
            anim = Animation(height=0, d=0.5)  # replie
            anim.start(self.scroll)
        self.ouvert = not self.ouvert
   
    def quitter(self, instance):
        ry.ecrire_ds_json(fichier=LETTREFichierRH, dictionnaire=initM.contenu_init_RH, sett=4)
        ry.ecrire_ds_json(fichier=LETTREFichierIN, dictionnaire=initM.contenu_init_IN, sett=4)
        App.get_running_app().stop()
    # Compteur d'entrees ________________________________________________________
    def initiateur_compteur(self):       
        for element in self.tableau_insertion:
            self.on_text_change(element, element.text, sett='accumulation')

    def on_text_change(self, instance, valeur, sett='accumulation'):
        if sett == 'accumulation':
            mots = valeur.split()
            
            # On garde une liste des mots déjà comptés
            if not hasattr(self, '_mots_comptes'):
                self._mots_comptes = set()
            
            for mot in mots:
                if len(mot) == 3 and mot not in self._mots_comptes:
                    self.cellules_non_remplies -= 1
                    self._mots_comptes.add(mot)
                elif '=' in mot and mot not in self._mots_comptes:
                    self.cellules_non_remplies -= 1
                    self._mots_comptes.add(mot)

        elif sett == 'cocher':
            if valeur:
                self.cellules_non_remplies -= 1

        # Mise à jour du bouton Save
        if self.cellules_non_remplies <= len(self.tableau_insertion) - 2:
            self.dictionnaire_bouton_menu['Save'].text = 'Save'
            colorer(self, self.dictionnaire_bouton_menu['Save'], couleur=VERT)
            self.csv_bouton.text = '>'
            colorer(self, self.csv_bouton, couleur=ORANGE)
            colorer(self, self.Lien, couleur=ORANGE)
        else:
            self.dictionnaire_bouton_menu['Save'].text = str(self.cellules_non_remplies)

    def set_nbre_Postulee_jour(self, nbre):
        if self.valideur_nbre_jr == False :
            self.apresclicmessage(bouton=self.dictionnaire_bouton_menu[f"{self.nbreEntreeTotal}"], 
                                valeur=nbre, sett='message')
            self.nbreEntreeTotal = nbre
            self.valideur_nbre_jr = True

    def get_nbre_Postulee_jour(self):
        return self.nbreEntreeTotal
    
    def changer_valeur_a_l_ecran(self, cible, nbre=0):
        cible = nbre
        return cible
    # Methode universelle _______________________________________________________
    def envoi_donnees_ds_JSON(self):
        ry.ecrire_ds_json(fichier=fichier_configuration, dictionnaire=dictio, contenu=self.get_nbre_Postulee_jour(), 
                            cle1='Nombres_Utilisateurs', cle2='nbreEntreeTotal', sett='remplacer')
        ry.ecrire_ds_json(fichier=fichier_configuration, dictionnaire=dictio, contenu=self.nombre_postulee, 
                            cle1='Nombres_Utilisateurs', cle2='nbreEntreeJour', sett='remplacer')
    
    def git_push(self, git=None, f_git=None, instance=None):
        
        try :
            process = psh.run([file_git_send],  capture_output=True, text=True, check=True)
            if process.stdout is not None and process.stdout != '':
                rcp(ry.Green, "STDOUT:", process.stdout)
            else :
                rcp(ry.Red, "STDERR:", process.stderr)
        except (psh.CalledProcessError, Exception) as cpe:
            pass; # err('Exception', 'git_push', cpe)                  
    
    def __ouvrir__(self, fichierdossier, valeur=None, color=BLEUPALE, sett=0): # color orange
        if sett == 0 :
            os.startfile(fichierdossier)
        if sett == 1 :
            os.startfile(Repertoire)

        if valeur is not None :
            colorer(self, self.dictionnaire_bouton_menu[valeur], couleur=color)
        
    def __restart__(self, instance):
        self.git_push(git='restart')
        self.envoi_donnees_ds_JSON()

        USER = os.getlogin()
        programme = f"{APP}"
        print(programme)

        psh.Popen([ sys.executable, f"{programme}" ])
        # Fermer proprement la fenêtre après 1 seconde
        Clock.schedule_once(lambda dt: App.get_running_app().stop(), 1)
     
# --- Troisième page ---
class Lettre(Screen):
    # def __init__(self, page, instance, **kwargs):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.nombre_postulee = self.afficher_nbre_postulee('nbreEntreeJour')
        self.nbreEntreeTotal = self.afficher_nbre_postulee('nbreEntreeTotal')
        GRILLE = GridLayout()
        # colorer
        self.INITfileRH = INITfileRH
        self.dictionnaire_bouton_menu = {} 
        self.Cadres(GRILLE)
        self.menu_options = {
            "Accueil": None,
            "<=": None,
            "=>": None,            
            "Archives": lambda *args: os.startfile(ARCHIVES),
            "Restart": self.__restart__,
            "Quitter": self.quitter,
            "Refresh RH": lambda instance: self.refresh_RH(),
            "Refresh IN": lambda instance: self.refresh_IN(),
            "Save RH": lambda instance: self.Save_RH(),
            "Save IN": lambda instance: self.Save_IN(),
            "Other": self.autredossier,
            "Log": lambda *args: self.__ouvrir__(fichierdossier=Repertoire),
        }

        self.dictionnaire_bouton_menu = Menu(self=self, cadre=GRILLE.cadreI, tableau=self.menu_options, dictio=self.dictionnaire_bouton_menu,
                                             haut=30, police=20, largeur=None, color=VERT, x=0.2, y=None, color2=ROUGE)

        self.dictionnaire_bouton_menu['Accueil'].bind(on_press=lambda x: setattr(self.manager, 'current', 'Accueil'))
        self.dictionnaire_bouton_menu['<='].bind(on_press=lambda x: setattr(self.manager, 'current', 'Inventaire'))
        self.dictionnaire_bouton_menu['=>'].bind(on_press=lambda x: setattr(self.manager, 'current', 'BlocNotes'))
        
        fichiers_json = [ self.lire_ecrire_json(fichier=LETTREFichierRH),
                        self.lire_ecrire_json(fichier=LETTREFichierIN),
                        self.lire_ecrire_json(fichier=initM.fichier_sauvegarde_json_IN),
                        self.lire_ecrire_json(fichier=initM.fichier_sauvegarde_json_RH) ]
        
        for contenu in fichiers_json :
            self.json_input = entry(self=GRILLE, texte=contenu, objet=self.cadreII, couleur=GRISCLAIR, multiline=True,
                txtColor=WHITE, width=400, height=20, sett='hauteur')

        self.add_widget(GRILLE)

    def Cadres(self, GRILLE) :
        # Colonnes
        GRILLE.cols = 1
        # Menu
        GRILLE.cadreI = add_object(self=GRILLE, cols=6, row_f=5)
        # FORMULAIRE
        GRILLE.cadreII = add_object(self=GRILLE, cols=2, sett='scroll')
        # FICHIER EN COURS
        self.cadreI = GRILLE.cadreI
        self.cadreII = GRILLE.cadreII

    def envoi_donnees_ds_JSON(self):
        ry.ecrire_ds_json(fichier=fichier_configuration, dictionnaire=dictio, contenu=self.get_nbre_Postulee_jour(), 
                            cle1='Nombres_Utilisateurs', cle2='nbreEntreeTotal', sett='remplacer')
        ry.ecrire_ds_json(fichier=fichier_configuration, dictionnaire=dictio, contenu=self.nombre_postulee, 
                            cle1='Nombres_Utilisateurs', cle2='nbreEntreeJour', sett='remplacer')
        
    def afficher_nbre_postulee(self, valeur=None) :
        if valeur == 'nbreEntreeJour':
            return ry.chercher_ds_JSON(dictionnaire=dictio, cle1='Nombres_Utilisateurs', 
                                        cle2='nbreEntreeJour', sett='valeurcles')
        elif valeur == 'nbreEntreeTotal':
            return ry.chercher_ds_JSON(dictionnaire=dictio, cle1='Nombres_Utilisateurs', 
                                        cle2='nbreEntreeTotal', sett='valeurcles')

    def refresh_RH(self):
        self.json_input.text = ry.lireFile(LETTREFichierRH, set=2)

    def Save_RH(self):        
        ry.ecrire_ds_json(fichier=LETTREFichierRH, dictionnaire=self.json_input.text, sett=4)
        
    def refresh_IN(self):
        self.json_input.text = ry.lireFile(LETTREFichierIN, set=2)

    def Save_IN(self):        
        ry.ecrire_ds_json(fichier=LETTREFichierIN, dictionnaire=self.json_input.text, sett=4)

    def git_push(self, git=None, f_git=None, instance=None):
        
        try :
            process = psh.run([file_git_send],  capture_output=True, text=True, check=True)
            if process.stdout is not None and process.stdout != '':
                rcp(ry.Green, "STDOUT:", process.stdout)
            else :
                rcp(ry.Red, "STDERR:", process.stderr)
        except (psh.CalledProcessError, Exception) as cpe:
            pass; # err('Exception', 'git_push', cpe)                  
    
    def __ouvrir__(self, fichierdossier, valeur=None, color=BLEUPALE, sett=0): # color orange
        if sett == 0 :
            os.startfile(fichierdossier)
        if sett == 1 :
            os.startfile(Repertoire)

        if valeur is not None :
            colorer(self, self.dictionnaire_bouton_menu[valeur], couleur=color)

    def lire_ecrire_json(self, fichier, sett='lire'):
        if sett == 'lire' or sett == 'r':
            contenu = ry.lireFile(fichier, set=2)
        elif sett == 'ecrire' or sett == 'w':
            ry.ecrire_ds_fichier(fichier, contenu)
        elif sett == 'lireecrire' or sett == 'rw' or sett == 'wr':
            contenu = ry.lireFile(fichier, set=2)
            ry.ecrire_ds_fichier(fichier, contenu)
        
        return contenu

    def set_nbre_Postulee_jour(self, nbre):
        if self.valideur_nbre_jr == False :
            self.apresclicmessage(bouton=self.dictionnaire_bouton_menu[f"{self.nbreEntreeTotal}"], 
                                valeur=nbre, sett='message')
            self.nbreEntreeTotal = nbre
            self.valideur_nbre_jr = True

    def get_nbre_Postulee_jour(self):
        return self.nbreEntreeTotal
    
    def changer_valeur_a_l_ecran(self, cible, nbre=0):
        cible = nbre
        return cible
    
    def quitter(self, instance):
        ry.ecrire_ds_json(fichier=LETTREFichierRH, dictionnaire=initM.contenu_init_RH, sett=4)
        ry.ecrire_ds_json(fichier=LETTREFichierIN, dictionnaire=initM.contenu_init_IN, sett=4)
        App.get_running_app().stop()

    def __restart__(self, instance):
        self.git_push(git='restart')
        self.envoi_donnees_ds_JSON()

        USER = os.getlogin()
        programme = f"{APP}"
        print(programme)

        psh.Popen([ sys.executable, f"{programme}" ])
        # Fermer proprement la fenêtre après 1 seconde
        Clock.schedule_once(lambda dt: App.get_running_app().stop(), 1)

    def autredossier(self, instance):
        for dossier in DOSSIER:
            try:
                os.startfile(dossier)
            except Exception:
                continue

# --- Quatrième page ---
class BlocNotes(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        
        self.dictio = ry.lireJSON(fichier=fichier_configuration)
        self.option_envoi = ry.chercher_ds_JSON(dictionnaire=self.dictio, cle1='Methode_D_Envoi', cle2='langage', sett='valeurcles')
            
        self.plan = f"{blocnotes_dossier}/Plan.txt"
        self.liensUtiles = f"{blocnotes_dossier}/Infos_inventaire.txt"
        self.infos = f"{blocnotes_dossier}/Infos_RH.txt"
        self.dates = f"{blocnotes_dossier}/Dates.txt"
        GRILLE = GridLayout()
        # colorer
        self.INITfileRH = INITfileRH
        self.dictionnaire_bouton_menu = {} 
        self.Cadres(GRILLE)
        self.menu_options = {
            "Accueil": None,
            "<=": None,
            "=>": None,
            "Save": lambda instance: self.Save(),
            "Restart": self.__restart__,
            "Quitter": self.quitter,
            "Other": self.autredossier,
            "Log": lambda *args: self.__ouvrir__(fichierdossier=Repertoire),
            f"{self.get_methode_envoi()}":lambda instance, val=str("py"), val2=str("psh"): self.set_methode_envoi(instance, val, val2),
            }

        self.dictionnaire_bouton_menu = Menu(self=self, cadre=GRILLE.cadreI, tableau=self.menu_options, dictio=self.dictionnaire_bouton_menu,
                                             haut=30, police=20, largeur=None, color=ORANGE, x=0.2, y=None, color2=ROUGE)

        self.dictionnaire_bouton_menu['Accueil'].bind(on_press=lambda x: setattr(self.manager, 'current', 'Accueil'))
        self.dictionnaire_bouton_menu['<='].bind(on_press=lambda x: setattr(self.manager, 'current', 'Lettre'))
        self.dictionnaire_bouton_menu['=>'].bind(on_press=lambda x: setattr(self.manager, 'current', 'BlocNotes'))
        
        self.createur_de_blocs(GRILLE)
        self.add_widget(GRILLE)

    def Cadres(self, GRILLE) :
        # Colonnes
        GRILLE.cols = 1
        # Menu
        GRILLE.cadreI = add_object(self=GRILLE, cols=6, row_f=5)
        # # Cadre interne - JOBNAMES
        # self.cadreIII = add_object(self, row_f=5, col1=2, col2=3, sett='doublecadre', cadrage='gche', forme='scroll')
        # # Cadre interne - COCHEUR
        # self.cadreII = add_object(self, row_f=5, col1=2, col3=4, sett='doublecadre', cadrage='dte', forme='scroll')
        # FORMULAIRE
        GRILLE.cadreII = add_object(self=GRILLE, cols=2, sett='scroll')
        GRILLE.cadreIII = add_object(self=GRILLE, cols=2, sett='scroll')
        # # Renommer
        # self.cadreIII = add_object(self, cols=3, row_f=10, col_f=50, sticky=None)
        
        # FICHIER EN COURS
        # self.cadreIV_I = add_object(self, cols=3, sett='scroll')
        self.cadreI = GRILLE.cadreI
        self.cadreII = GRILLE.cadreII
        self.cadreIII = GRILLE.cadreIII

    def createur_de_blocs(self, GRILLE):
        largeur = 320; longueur = 50
        contenu_plan = self.lire_ecrire_json(fichier=self.plan)
        self.plan_input = entry(self=GRILLE, texte=contenu_plan, objet=self.cadreII, couleur=BLEUPALE, multiline=True,
              txtColor=WHITE, width=largeur, height=10, sett='hauteur')
        
        contenu_liens = self.lire_ecrire_json(fichier=self.liensUtiles)
        self.liens_input = entry(self=GRILLE, texte=contenu_liens, objet=self.cadreII, couleur=BLEUPALE, multiline=True,
              txtColor=WHITE, width=largeur, height=10, sett='hauteur')
        
        contenu_infos = self.lire_ecrire_json(fichier=self.infos)
        self.infos_input = entry(self=GRILLE, texte=contenu_infos, objet=self.cadreIII, couleur=BLEUPALE, multiline=True,
              txtColor=WHITE, width=largeur, height=10, sett='hauteur')
        
        contenu_dates = self.lire_ecrire_json(fichier=self.dates)
        self.dates_input = entry(self=GRILLE, texte=contenu_dates, objet=self.cadreIII, couleur=BLEUPALE, multiline=True,
              txtColor=WHITE, width=largeur, height=10, sett='hauteur')

    def envoi_donnees_ds_JSON(self):
        ry.ecrire_ds_json(fichier=fichier_configuration, dictionnaire=self.dictio, contenu=self.get_methode_envoi(), 
                            cle1='Methode_D_Envoi', cle2='langage', sett='remplacer')

    def set_methode_envoi(self, instance, val, val2):        
        print(self.get_methode_envoi(), val, val2)
        if self.get_methode_envoi() != val :            
            self.apresclicmessage(bouton=self.dictionnaire_bouton_menu[str(val2)], 
                                valeur=val, sett='message')
        else:
            self.apresclicmessage(bouton=self.dictionnaire_bouton_menu[str(val2)], 
                                valeur=val2, sett='message')
                
    def get_methode_envoi(self):
        return self.option_envoi

    def Save(self):    
        dict_input = {self.plan: self.plan_input.text, self.liensUtiles: self.liens_input.text, 
                     self.infos: self.infos_input.text, self.dates: self.dates_input.text}
        for key, valeur in dict_input.items():
            contenu = str(valeur)
            ry.ecrire_ds_fichier(key, contenu)

    def git_push(self, git=None, f_git=None, instance=None):
        
        try :
            process = psh.run([file_git_send],  capture_output=True, text=True, check=True)
            if process.stdout is not None and process.stdout != '':
                rcp(ry.Green, "STDOUT:", process.stdout)
            else :
                rcp(ry.Red, "STDERR:", process.stderr)
        except (psh.CalledProcessError, Exception) as cpe:
            pass; # err('Exception', 'git_push', cpe)                  
    
    def __ouvrir__(self, fichierdossier, valeur=None, color=BLEUPALE, sett=0): # color orange
        if sett == 0 :
            os.startfile(fichierdossier)
        if sett == 1 :
            os.startfile(Repertoire)

        if valeur is not None :
            colorer(self, self.dictionnaire_bouton_menu[valeur], couleur=color)

    def lire_ecrire_json(self, fichier, sett='lire'):
        if sett == 'lire' or sett == 'r':
            contenu = ry.lireFile(fichier, set=2)
        elif sett == 'ecrire' or sett == 'w':
            ry.ecrire_ds_fichier(fichier, contenu)
        elif sett == 'lireecrire' or sett == 'rw' or sett == 'wr':
            contenu = ry.lireFile(fichier, set=2)
            ry.ecrire_ds_fichier(fichier, contenu)
        
        return contenu
                
    def apresclicmessage(self, bouton, valeur=None, sett=None):
        if sett == 'messageavecbouton':
            bouton.bind(on_release=lambda btn, valeur=valeur: self.apresclic(btn, f"{valeur}"))
        elif sett == 'message':
            bouton.text = str(valeur)
            self.option_envoi = valeur
            self.envoi_donnees_ds_JSON()            

    def apresclic(self, bouton, valeur=None, couleur=VERT):
        bouton.text = valeur
        colorer(self, bouton, couleur)

    
    def changer_valeur_a_l_ecran(self, cible, nbre=0):
        cible = nbre
        return cible
    
    def quitter(self, instance):
        ry.ecrire_ds_json(fichier=LETTREFichierRH, dictionnaire=initM.contenu_init_RH, sett=4)
        ry.ecrire_ds_json(fichier=LETTREFichierIN, dictionnaire=initM.contenu_init_IN, sett=4)
        App.get_running_app().stop()

    def __restart__(self, instance):
        self.git_push(git='restart')
        self.envoi_donnees_ds_JSON()

        USER = os.getlogin()
        programme = f"{APP}"
        print(programme)

        psh.Popen([ sys.executable, f"{programme}" ])
        # Fermer proprement la fenêtre après 1 seconde
        Clock.schedule_once(lambda dt: App.get_running_app().stop(), 1)

    def autredossier(self, instance):
        for dossier in DOSSIER:
            try:
                os.startfile(dossier)
            except Exception:
                continue

class InputDialog(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Entrer une valeur"
        self.size_hint = (0.7, 0.4)

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        self.input_field = TextInput(hint_text="Tapez votre valeur ici", multiline=False)
        layout.add_widget(self.input_field)

        btn_layout = BoxLayout(size_hint_y=None, height=40, spacing=10)
        btn_ok = Button(text="OK")
        btn_ok.bind(on_release=self.on_ok)
        btn_cancel = Button(text="Annuler")
        btn_cancel.bind(on_release=self.dismiss)

        btn_layout.add_widget(btn_ok)
        btn_layout.add_widget(btn_cancel)

        layout.add_widget(btn_layout)
        self.add_widget(layout)

        # Stocke la valeur saisie
        self.valeur = None

    def on_ok(self, instance):
        self.valeur = self.input_field.text
        print(f"Valeur entrée : {self.valeur}")
        self.dismiss()

class MyApp(App):
    def build(self):

        Page = ScreenManager()
        Page.add_widget(HomeScreen(name="Accueil"))
        Page.add_widget(InventaireScreen(name="Inventaire"))
        Page.add_widget(Lettre(name="Lettre"))
        Page.add_widget(BlocNotes(name="BlocNotes"))

        return Page
    
    def on_stop(self):
        ry.ecrire_ds_json(fichier=fichier_configuration, dictionnaire=dictio, val=Window.left, cle1='x', sett='remplacer')
        ry.ecrire_ds_json(fichier=fichier_configuration, dictionnaire=dictio, val=Window.top, cle1='y', sett='remplacer')
        Home().envoi_donnees_ds_JSON()

MyApp().run()
    
    