import time
import board
import displayio
import terminalio
import analogio
import digitalio

import ssl
import wifi
import adafruit_requests

from adafruit_display_text import label
import adafruit_displayio_ssd1306
import pwmio

import storage
import json
import lib.adafruit_bus_device.adafruit_sdcard as carte
import asyncio
import os
import lib._MQTT_ as _MQTT_
import _Functions_


# ____________________________________________________________________________
# ____________________________________________________________________________
# ____________________________________________________________________________
# V A R I A B L E S - G L O B A L E S
JSON = _MQTT_.JSON
# ____________________________________________________________________________
# ___________________R E C H E R C H E R_________________________________________________________
# ____________________________________________________________________________
# 000 TABLE DES MATIERES _______________________________________________________________
# I -  SD CARTE
# II - V A R I A B L E S   E S P
# III - SEND DATA : ENVOI DE DONNEES ADAFRUIT
# IV - STOCKAGE DES DONNEES
# IX - A F F I C H A G E - E C R A N
# ____________________________________________________________________________
# ____________________________________________________________________________
# I - SD CARTE

class CARTE_SD :
    def __init__(self) :
        """Initialise la carte SD.

        Args:
        SDCS : Appel Du PIN Adéquat.
        CS: Appel de la carte SD.
        SD card: Appels de la classe SD_card
        VFS: Appels de la classe VFSFat

        """
        # The SD_CS pin is the chip select line.
        SD_CS = board.SD_CS

        # Connect to the card and mount the filesystem.
        cs = digitalio.DigitalInOut(SD_CS)
        sdcard = carte.SDCard(board.SPI(), cs)
        vfs = storage.VfsFat(sdcard)
        storage.mount(vfs, "/sd")
        # print("Carte SD montée avec succès")

    def obtenir_heure_formateeCSV(self):
        t = time.localtime()
        return "{:04}/{:02}/{:02}-{:02}:{:02}:{:02}".format(t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec)

    def ecrire_mesures_csv(self, fichier, temp_actuelle, temp_max, appel_Mode):
        try:

            with open(fichier, "a") as f:
                ligne = f"{self.obtenir_heure_formateeCSV()} | {temp_actuelle:.1f} | {temp_max:.1f}\n | {appel_Mode:.1f}\n"
                f.write(ligne)

        except Exception as e:
            print(f"Erreur d'enregistrement dans {fichier} : {e}")

    def listeDataSD(self):
        try : 
            os.chdir('E:/sd/')
            reponse = os.listdir(os.getcwd())
            os.chdir('../Personnel')
            with open('../Personnel/sd.txt', 'w') as read :
                read.write(reponse)
        except OSError as o :
            print("Erreur lors de la lecture des données SD :", o)

    def ecrireSD (self, fichier, valeur) :
        donnees = []
        # Ajouter la nouvelle entrée et écrire le fichier
        donnees.append(valeur)        
        with open(fichier, 'w') as wr :
            wr.write(valeur)
        
    def lireSD (self, fichier, valeur) :
        donnees = []
        # Ajouter la nouvelle entrée et écrire le fichier
        donnees.append(valeur)        
        with open(fichier, 'r') as read :
            read.readlines()
    
def ecrire_sur_sd(fichier, cible) :  
        """Écriture sur la carte SD en manque de connexion internet,
        Ou de connexion à adafruit.

        Args:
        j_son: Variable json contenant le string log.json.
        nouvelle_entree : Variable contenant la date et la valeur à écrire.
        donnees : Tableau contenant les données à écrire.
        json.dump: Variable contenant le fichier à écrire Sous format .Json

        Returns:
        Retourne ici la valeur a réussi ou pas du tout.

        Raises:
        OSError, ValueError : S'assurer sur le fichier est corrompu ou n'existe pas.
        Retourne False si jamais la carte SD n'a pas pu permettre l'écriture
        """
        j_son = "log.json"
        
        # if not os.path.exists(fichier) :
        #     return False
        
        try :
            
            # Obtenir l'heure actuelle formatée
            date_str = _MQTT_.UTC_heure()
            # Préparer la nouvelle entrée

            # Lire le fichier existant ou créer une liste vide
            donnees = []
            
            try :            
                with open(f"{fichier}/{j_son}", "r") as f :
                    donnees = json.load(f)
                    
            except (OSError, ValueError) :
                # Fichier n'existe pas ou est corrompu
                pass
            # Ajouter la nouvelle entrée et écrire le fichier
            donnees.append(cible)        
            with open(f"{fichier}/{j_son}", "w") as f :
                json.dump(donnees, f)
                print("Ecriture dans le fichier .JSON")
                return True
            with open("../fichier.txt", 'w') as wr :
                wr.write(donnees)
            
        except Exception as e :
            print(f"Erreur lors de l'écriture sur la carte SD: {e}")
            return False              

# ____________________________________________________________________________
# ____________________________________________________________________________
# ____________________________________________________________________________
# II - V A R I A B L E S   E S P

# 1. Initialiser le PIR sensor
pir = digitalio.DigitalInOut(board.D2) # Pin LED intégrée
pir.direction = digitalio.Direction.INPUT
# 2. Connexion variables Adafruit
ADAFRUIT_AIO_USERNAME = _Functions_.chercher_ds_JSON(dictionnaire=JSON, cle1='ADAFRUIT_AIO_USERNAME', sett='-')
ADAFRUIT_AIO_KEY      = _Functions_.chercher_ds_JSON(dictionnaire=JSON, cle1='ADAFRUIT_AIO_KEY', sett='-')
# 3. Carte SD
try :
    CARTE_SD()
except OSError as o :
    print("Erreur carte SD : ", o)
# 4. Temps   
TEMPS = _MQTT_.TempsP()
# ____________________________________________________________________________
# ____________________________________________________________________________
# ____________________________________________________________________________
# III - SEND DATA : ENVOI DE DONNEES ADAFRUIT

def feed(data_to_send) :
    """ Le fit vérifie si l'information dans le dossier est valide, 
    ensuite le l'intervertit pour donner la valeur nécessaire à envoyer sur  Adafruit.

    Args:
        key, valeur in data_to_send.items()
        data_to_send["value"].

    Returns:
      Retourne le topic censé être le nom du feed à envoyer
    """
    for key, valeur in data_to_send.items():        
        if key == "temperatureactuelle" :    
            data_to_send["value"] = data_to_send.pop(key)       
            return "temperatureactuelle"
        if key == "temperaturemoyenne" :
            data_to_send["value"] = data_to_send.pop(key)   
            return "temperaturemoyenne"
        
def url_web (siteWeb, DONNEES="") :
    """  Délivre l'adresse url d'Adafruit.

    Args:
       Réalise une condition afin de s'assurer qu'il s'agit bien d'Adafruit.

    Returns:
      Retourne l'adresse courriel formatée avec le nom de l'utilisateur adafruit ainsi que son feed.
    """
    if siteWeb  == 'adafruit' or siteWeb == 1 or siteWeb == 'public' :
        return f"https://io.adafruit.com/api/v2/{ADAFRUIT_AIO_USERNAME}/feeds/{DONNEES}/data"
    
def donnees (data_to_send, requests, siteWeb) :
    """ Fonction servant à prélever les données nécessaires à envoyer à adafruit.

    Args:
        Headers: {"Content-Type": "application/json"}
        headers["x-aio-key"] = f"{ADAFRUIT_AIO_KEY}"
        feeds = feed(data_to_send)

    Returns:
      Fais appel à la fonction send_data pour renvoyer les données dans une autre fonction
    """
    headers = {"Content-Type": "application/json"}  
    feeds = ""   
    feeds = feed(data_to_send)
    if siteWeb  == 'adafruit' or siteWeb == 1 or siteWeb == 'public' :
        headers["x-aio-key"] = f"{ADAFRUIT_AIO_KEY}"
        ry.colorPrint(ry.Yellow, feeds, data_to_send)
        send_data(data_to_send, requests, 'adafruit', headers, feeds)

# Envoi de données à  Adafruit par le passage de API Restfull.
def send_data(data, requests, siteWeb, headers={"Content-Type": "application/json"}, key=""): 
    """Envoie des données à  Adafruit par le passage de API Restfull.

    Args:
       URL: Appel de la fonction url_web().
       Response: Appel de la fonction requests.post().
       ColorPrint: Affichage de la réponse dans la console.
       S'assure de fermer Response après l'envoi de la requête.

    Returns:
      The new minimum port.
    """
    try :
        url = url_web(siteWeb, key) 
        response = requests.post(url, json=data, headers=headers)
        # response = requests.post(url, data=json.dumps(data), headers=headers)
        ry.colorPrint(ry.Green, response.text, "\nRéponse POST: \n")
    finally :
        print("fermeture")
        response.close()        

# ____________________________________________________________________________
# ____________________________________________________________________________
# ____________________________________________________________________________
# IV - STOCKAGE DES DONNEES

class TamponDonnees:
    """ Récupération des données par le tampon.
     Se déclenche lorsque la connexion internet est manquante,
     si le site officiel Adafruit ou n'importe quel autre site n'est pas disponible

    Args:
        Appels des variables -> 
        Prétempérature:  Dictionnaire
        Température: Tableau        
        Prémoyenne: Dictionnaire
        Moyenne: Tableau
        
        Init : Inseize la taille maximale à 100
        Ajouter: Rajoute valeur après valeur
        Séparermoyenne: Récupère les données du tableau initialisée dans la fonction ajouter.
        Séparertempérature: Récupère les données du tableau initialisée dans la fonction ajouter.
        Est_vide: Vérifie si le tableau est vide ou non.
        Obtenir_prochain: Récupère la première valeur du tableau.
        Supprimer_premier: Supprime la première valeur du tableau.
        RetournerDonnees: Retourne les données du tableau.
    """
    temperature = []
    pretemperature = {}
    moyenne = []
    premoyenne = {}

    def __init__(self, taille_max=100):
        self.taille_max = taille_max
        self.donnees = []

    def ajouter(self, created_at, temperature, moyenne):
        if len(self.donnees) >= self.taille_max:
            self.donnees.pop(0)  # Supprimer la plus ancienne entrée
            
        self.donnees.append({
                "created_at": created_at,
                "temperatureactuelle": temperature,
                "temperaturemoyenne": moyenne
                })
    
    def separerMoyenne(self) :
        for initial in self.donnees :
            for key, Elements in initial.items() :
                if key == "temperaturemoyenne" :
                    self.premoyenne["temperaturemoyenne"] = Elements
                if key == "created_at" :
                    self.premoyenne["created_at"] = Elements
                
        self.moyenne.append(self.premoyenne)
        return self.moyenne
        
    def separerTemperature(self) :
        
        for initial in self.donnees :
            for key, Elements in initial.items() :
                
                if key == "temperatureactuelle" :
                    self.pretemperature["temperatureactuelle"] = f"{Elements}"
                if key == "created_at" :
                    self.pretemperature["created_at"] = Elements
                
        self.temperature.append(self.pretemperature)
        return self.temperature
                
    def est_vide(self):
        return len(self.donnees) == 0

    def obtenir_prochain(self):
        if self.est_vide():
            return None
        return self.donnees[0]

    def supprimer_premier(self):
        if not self.est_vide():
            self.donnees.pop(0)
    
    def retourner_donnees(self) :
        return self.donnees

def tempusPush(Check, tampons, temperature, moyenne) :                          #////
    """ Ajoute les informations au tampon,
        Prélève les informations du tampon
        Et fais appel à la fonction Send_data.
    Args:
    Pool : Appel de la fonction _wifi_.connecter_wifi().
    ssl_context : Appel de la fonction ssl.create_default_context().
    requests : Appel de la fonction adafruit_requests.Session().
    Tampons: Appel de la classe TamponDonnees().
    Tempe_moyenne : Appel de la fonction separerMoyenne().
    Tempe_temperature : Appel de la fonction separerTemperature().
    Fonction donnéees : Appel de la fonction donnees().
    Returns:
    Retourne le tampons.retourner_donnees() si jamais la connexion est réussie.
    """
    if Check == False :                                                         #////
        tampons.ajouter(TEMPS, temperature, moyenne)                            #////
    #lecture des capteurs sur ESP32                                             #////
    pool = _MQTT_.connecter_wifi()                                                     #////
    ssl_context = ssl.create_default_context()                                  #////
    requests = adafruit_requests.Session(pool, ssl_context=ssl_context)         #////
    # for valeur in tampons.retourner_donnees() :                               #////
    #     ry.colorPrint(ry.Violet, valeur)                                      #////
        
    if wifi.radio.connected and (Check != False) and not tampons.est_vide():    #////
        for tempe_moyenne in tampons.separerMoyenne() :                         #////
            # ry.colorPrint(ry.Violet, tempe_moyenne)                           #////
            tampons.supprimer_premier()                                         #////
            donnees(tempe_moyenne, requests, 'adafruit')                        #////
        for tempe_temperature in tampons.separerTemperature() :                 #////
            # ry.colorPrint(ry.Yellow, tempe_temperature)                       #////
            tampons.supprimer_premier()                                         #////
            donnees(tempe_temperature, requests, 'adafruit')                    #////
    return len(tampons.retourner_donnees())                                     #////
        
  
     
# ____________________________________________________________________________
# ____________________________________________________________________________
# ____________________________________________________________________________
# V - 

# ____________________________________________________________________________
# ____________________________________________________________________________
# ____________________________________________________________________________
# VI - 

# ____________________________________________________________________________
# ____________________________________________________________________________
# ____________________________________________________________________________
# VII - 

# ____________________________________________________________________________
# ____________________________________________________________________________
# ____________________________________________________________________________
# VIII - 

# ____________________________________________________________________________
# ____________________________________________________________________________
# ____________________________________________________________________________
# VIII - 



# ____________________________________________________________________________
# ____________________________________________________________________________
# ____________________________________________________________________________
# IX - A F F I C H A G E - E C R A N

class ecran :
    """Initialise l'écran OLED et affiche le texte.

    Args:
       Init: Contient toutes les valeurs nécessaires pour l'affichage.
        Texte: Texte à afficher sur l'écran.

    """
    def __init__(self):
        displayio.release_displays()
        self.i2c = board.I2C()
        self.display_bus = displayio.I2CDisplay(self.i2c, device_address=0x3C)
        self.display = adafruit_displayio_ssd1306.SSD1306(self.display_bus, 
                                                          width=128, height=64,
                                                          rotation=180)                                                          
        self.splash = displayio.Group()
        self.display.root_group = self.splash
        
        self.text = ""
        self.text_area = label.Label(terminalio.FONT, text=self.text, color=0xFFFFFF, x=5, y=10)
        self.splash.append(self.text_area)
        
    def rafraichir_texte (self, texte) :
        self.text_area.text = texte
        self.display.refresh()
        
    @property
    def texte(self) :
        return self.text_area.text

# Initialisation de l'affichage
aff = ecran()

def affichage(temp_actuelle, temp_max, wifi) :
    """_summary_

    Args:
        wifi (bool): État de la connexion Wi-Fi.

    Returns:
        _type_: température actuelle, température moyenne, température minimale, température maximale
    """
    if wifi != False :
        connect = "Oui"
    else : 
        connect = "Non"
        
    aff.rafraichir_texte("T_act:{:.1f}F Wifi:{}\nMax:{}".format(
                        temp_actuelle, 
                        connect,
                        temp_max
                        ))
    # Connect n'a pas besoin d'etre retourné, changer cela par une variable utile a retourner...
    return temp_actuelle, temp_max

# ____________________________________________________________________________
# ____________________________________________________________________________
# ____________________________________________________________________________
# X 


# ____________________________________________________________________________
# ____________________________________________________________________________
# ____________________________________________________________________________
# 