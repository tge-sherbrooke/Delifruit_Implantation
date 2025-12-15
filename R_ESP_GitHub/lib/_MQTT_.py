import os
import rtc
import ssl
import wifi
import time
import _Main_
import socketpool
import adafruit_ntp
import _Functions_
import asyncio

import adafruit_minimqtt.adafruit_minimqtt as MQTT
from adafruit_io.adafruit_io import IO_MQTT

# ____________________________________________________________________________
# ____________________________________________________________________________
# ____________________________________________________________________________
# Pour les variables globales de connexion, aller a la LIGNE III
fichier_configuration = "../Utilitaires/config.json"
JSON = _Functions_.lireJSON(fichier_configuration) 
FILESD = "log_ESP"
WIFISSIDPERSO = _Functions_.chercher_ds_JSON(dictionnaire=JSON, cle1='PERSONAL_SSID', sett='-')
WiFiSSID = _Functions_.chercher_ds_JSON(dictionnaire=JSON, cle1='WiFiSSID', sett='-')
PASSWORD = _Functions_.chercher_ds_JSON(dictionnaire=JSON, cle1='PASSWORDCegep', sett='-')
THING_NAME = _Functions_.chercher_ds_JSON(dictionnaire=JSON, cle1='THING_NAME', sett='-')
     
# ____________________________________________________________________________
# ___________________R E C H E R C H E R_________________________________________________________
# ____________________________________________________________________________
# 000 TABLE DES MATIERES _______________________________________________________________
# I -  TEMPS - NTP - RTC
# II - NOTES SUR LA CARTE SD
# III - PRECONNEXION - WIFI - MQTT
# IV - METHODE DE CONNEXION - WIFI - MQTT
# V - CONNEXION - WIFI - MQTT
# VI - RECONNEXION - WIFI - MQTT
# VII - PUBLICATION - MOSQUITTO - MQTT
# ____________________________________________________________________________
# ____________________________________________________________________________
# ____________________________________________________________________________
# I -  TEMPS - NTP - RTC

def TempsP() :
    """Échange de  Temps.

    Args:
      Fonctions: Appel de la fonction afin de délivrer l'heure UTC
        ColorPrint: Affichage de l'heure UTC dans la console

    Returns:
      Retourne l'heure UTC.

    Raises:
      OverflowError: Si jamais une erreur dans leur UTC est détectée.
    """
    if not wifi.radio.connected:
        try:
            _Functions_.colorPrint(_Functions_.Red, "\nCONNEXION PERDUE") 
            return UTC_heure()
        except OverflowError as o :
            return obtenir_heure_formatee()
    else:
        _Functions_.colorPrint(_Functions_.Blue, "\nEN CONNEXION")
        try:
            return UTC_heure()
        except OverflowError as o :
            return obtenir_heure_formatee()

def synchroniser_heure():
    """ Appel de la synchronisation de l'heure.

    Args:
       Pool: Appel  Connecter_wifi().
       NTP: Appel de NTP sur le site pool.ntp.org
        RTC: Appel de la RTC pour la synchronisation de l'heure

    Returns:
      The new minimum port.

    Raises:
      ConnectionError: If no available port is found.
    """
    try:
        if wifi.radio.connected :
            # ntp = adafruit_ntp.NTP(pool, tz_offset=-4, cache_seconds=3600)
            # rtc.RTC().datetime = ntp.datetime
            pool = connecter_wifi()
            ntp = adafruit_ntp.NTP(pool, server="pool.ntp.org")
            rtc.RTC().datetime = ntp.datetime
            print("Heure synchronisée")
            return True
    except Exception as e:
        if "[Errno 116] ETIMEDOUT" in str(e) :
            print("Heure locale enclenchee !")
        if "timestamp hors intervalle pour le 'time_t' de la plateforme" in str(e) :
            print("Heure desynchronisee !")
        if (not "(-2, 'Nom ou service inconnu')" in str(e)) and (not "[Errno 116] ETIMEDOUT" in str(e)):
            print(f"Erreur lors de la synchronisation de l'heure: {e}")
        return False

def conversion_heure() :
    """Conversion de l'heure pour obtenir le fuseau horaire Canada/Eastern.

    Args:
      minimum: A port value greater or equal to 1024.

    Returns:
      The new minimum port.

    Raises:
      ConnectionError: If no available port is found.
    """
    secondes = -4 * 3600  # Offset pour UTC-4 (heure normale de l'Est)
    d = rtc.RTC().datetime
    conversionSecondes = time.mktime(
    (   d[0],   # année
        d[1],   # mois
        d[2],   # jour
        d[3],   # heure
        d[4],   # minute
        d[5],   # seconde
        d[6],   # jour de la se_Main_e (0-6, 0=dimanche)
        0,  # jour de l'année (0-365, 0=1er janvier)
        -1  # DST (0=pas d'heure d'été, 1=heure d'été, -1=inconnu
    )) + secondes

    return time.localtime(conversionSecondes)

def UTC_heure() :
    """Affichage et envoi de  L'heure sous format UTC.

    Args:
       Appels de la variable T qui va contenir la fonction conversion de l'heure()

    Returns:
       Retourne l'heure sous format UTC.
    """
    t = conversion_heure()
    return "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(
                t.tm_year, t.tm_mon, t.tm_mday,
                t.tm_hour, t.tm_min, t.tm_sec
            )
def UTC_heureI() :

    t = rtc.RTC().datetime
    return "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(
                t.tm_year, t.tm_mon, t.tm_mday,
                t.tm_hour, t.tm_min, t.tm_sec
            )

def obtenir_heure_formateeI(tm_year, tm_mon, tm_mday,
                tm_hour, tm_min, tm_sec):
    """ Reproduit le même chemin que obtenir heure.

    Args:
       Appel de la Classe RTC Dans la variable t.

    Returns:
      Retourne l'affichage sous format normal, Pas d'UTC.

    """
    t = rtc.RTC().datetime
    return "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
                t.tm_year, t.tm_mon, t.tm_mday,
                t.tm_hour, t.tm_min, t.tm_sec
            )

def obtenir_heure_formatee():
    """Obtiens l'heure exacte en le formatant.

    Args:
       t: Usage de RTC dans une variable t.

    Returns:
      Retourne l'heure Et l'affiche dans la console.

    Raises:
      Exception: retourne à format '0000-00-00 00:00:00' si jamais  L'heure NTP n'est pas disponible.
    """
    try:
            t = rtc.RTC().datetime

            if not wifi.radio.connected:
                return obtenir_heure_formateeI(t.tm_year, t.tm_mon, t.tm_mday,
                    t.tm_hour, t.tm_min, t.tm_sec)
            else :
                return "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
                    t.tm_year, t.tm_mon, t.tm_mday,
                    t.tm_hour, t.tm_min, t.tm_sec
                )

    except Exception as e:
            print(f"Erreur lors de l'obtention de l'heure: {e}")
            return "0000-00-00 00:00:00"

# ____________________________________________________________________________
# ____________________________________________________________________________
# ____________________________________________________________________________
# II - NOTES SUR LA CARTE SD

def noteSD_EtatConnexion() :
    connectee = "EN CONNEXION"
    deconnectee = "CONNEXION PERDUE"
       
    if not wifi.radio.connected:        
        _Main_.ecrire_sur_sd(fichier=FILESD, cible={"date": TEMPS, "sujet": deconnectee})
    else :
        _Main_.ecrire_sur_sd(fichier=FILESD, cible={"date": TEMPS, "sujet": connectee})

def noteSD(DATA="") :
    _Main_.ecrire_sur_sd(FILESD, {"date": TEMPS, "sujet": DATA})

# ____________________________________________________________________________
# ____________________________________________________________________________
# ____________________________________________________________________________
# III - PRECONNEXION - WIFI - MQTT

def preconnection(param) :
    """Connects to the next available port.

    Args:
      minimum: A port value greater or equal to 1024.

    Returns:
      The new minimum port.

    Raises:
      ConnectionError: If no available port is found.
    """
    global THING_NAME, WiFiSSID, PASSWORD
    IP = _Functions_.chercher_ds_JSON(dictionnaire=JSON, cle1='Mosquitto', sett='-') 
    THING_NAME = THING_NAME
    
    if param == 1 :
        
        WiFiSSID = WiFiSSID
        PASSWORD = PASSWORD
        THING_NAME = THING_NAME
        
    elif param == 2 :        
        WiFiSSID = _Functions_.chercher_ds_JSON(dictionnaire=JSON, cle1='ORDI_1', sett='-')
        PASSWORD = _Functions_.chercher_ds_JSON(dictionnaire=JSON, cle1='WPASS', sett='-')
        THING_NAME = _Functions_.chercher_ds_JSON(dictionnaire=JSON, cle1='CLUE', sett='-')
        
    elif param == 3 :        
        WiFiSSID = _Functions_.chercher_ds_JSON(dictionnaire=JSON, cle1='cell', sett='-')
        PASSWORD = _Functions_.chercher_ds_JSON(dictionnaire=JSON, cle1='CPASS', sett='-')
        IP = _Functions_.chercher_ds_JSON(dictionnaire=JSON, cle1='Mosquitto', sett='-')
        THING_NAME = _Functions_.chercher_ds_JSON(dictionnaire=JSON, cle1='CLUE', sett='-')
        
    elif param == 4 :        
        WiFiSSID = _Functions_.chercher_ds_JSON(dictionnaire=JSON, cle1='ORDI_2', sett='-')
        PASSWORD = _Functions_.chercher_ds_JSON(dictionnaire=JSON, cle1='WDPASS', sett='-')
        THING_NAME = _Functions_.chercher_ds_JSON(dictionnaire=JSON, cle1='CLUE', sett='-')
        
    else :
        WiFiSSID = _Functions_.chercher_ds_JSON(dictionnaire=JSON, cle1='PERSONAL_SSID', sett='-')
        PASSWORD = _Functions_.chercher_ds_JSON(dictionnaire=JSON, cle1='PASSWORD', sett='-')
        THING_NAME = _Functions_.chercher_ds_JSON(dictionnaire=JSON, cle1='THING_NAME', sett='-')
        IP = _Functions_.chercher_ds_JSON(dictionnaire=JSON, cle1='IP_PERSO', sett='-')
        
    return WiFiSSID, PASSWORD, IP, THING_NAME

ADAFRUIT_AIO_USERNAME   = _Functions_.chercher_ds_JSON(dictionnaire=JSON, cle1='ADAFRUIT_AIO_USERNAME', sett='-')
ADAFRUIT_AIO_KEY        = _Functions_.chercher_ds_JSON(dictionnaire=JSON, cle1='ADAFRUIT_AIO_KEY', sett='-')
TRACKPC                 = _Functions_.recuperateur("Utilitaires", "track.txt", "TRACKING")
TEMPS = TempsP()
CONNEXION = preconnection(3) #3
connex = preconnection(2) #2
PORT = _Functions_.chercher_ds_JSON(dictionnaire=JSON, cle1='port', sett='-')
# ____________________________________________________________________________
# ____________________________________________________________________________
# ____________________________________________________________________________
# IV - METHODE DE CONNEXION - WIFI - MQTT

# Fonctions pour MQTT
# Définir les fonctions de rappel qui seront appelées lorsque certains événements se produisent.
# pylint: disable=unused-argument
def connected (client) :
    # La fonction Connected sera appelée lorsque le client sera connecté à Adafruit IO.
    # C'est un bon endroit pour s'abonner aux changements de flux. Le paramètre client
    # passé à cette fonction est le client MQTT Adafruit IO, vous pouvez donc effectuer
    # des appels facilement.
    _Functions_.colorPrint(_Functions_.Green, "Connecté à Adafruit IO !")
def subscribe(client, userdata, topic, granted_qos) :
    # Cette méthode est appelée lorsque le client s'abonne à un nouveau flux.
    print("Abonné à {0} avec un niveau de QOS {1}".format(topic, granted_qos))

def unsubscribe(client, userdata, topic, pid) :
    # Cette méthode est appelée lorsque le client se désabonne d'un flux.
    print("Désabonné de {0} avec PID {1}".format(topic, pid))
def disconnected (client) :
    # La fonction Disconnected sera appelée lorsque le client se déconnecte.
    _Functions_.colorPrint(_Functions_.Rouge, "Déconnecté d'Adafruit IO !")
def message(client, feed_id, payload) :
    """ Soit les valeurs venant de adafruit et
    permet d'afficher les valeurs dans la console.
    Args:
    Feed_id: Identifiant du flux.
        Payload : Variable associée au flux.
        minMax: Fonction retournant la valeur obtenue de la fonction,
                tout en récupérant le feed et le payload.
        LevierChoix: Fonction retournant la valeur obtenue de la fonction.
    Returns:
    Retourne la valeur de levierChoix().

    """
    # La fonction message sera appelée lorsque le flux auquel on est abonné a une nouvelle valeur.
    # Le paramètre feed_id identifie le flux, et le paramètre payload contient la nouvelle valeur.
    values = payload
    print("Valeur {} : {}".format(feed_id, values))


# ____________________________________________________________________________
# ____________________________________________________________________________
# ____________________________________________________________________________
# V - CONNEXION - WIFI - MQTT


def ip_address() :

    MOSQUITTO = ""

    if CONNEXION[0] != WiFiSSID or CONNEXION[0] != WIFISSIDPERSO :
        MOSQUITTO = CONNEXION[2]

    return MOSQUITTO

def connecter_wifi() :
    """Fais appel à la classe socketPool afin de pouvoir se connecter .

    Args:
       Wi-Fi.radio: Appel de la classe socketPool.

    Returns:
      Retourne le socketpool initialisé
    """
    return socketpool.SocketPool(wifi.radio)

def connecter_mosquitto() :

    try :

        if not wifi.radio.connected :

            topSecrets = {"ssid":f"{CONNEXION[0]}","password":f"{CONNEXION[1]}"}
            secrets = {"ssid":f"{connex[0]}","password":f"{connex[1]}"}

            if CONNEXION[3] == "Paho_MQTT" and TRACKPC == 'D':
                print(f"Connexion à {CONNEXION[0]}")
                wifi.radio.connect(topSecrets["ssid"], topSecrets["password"])
                _Functions_.colorPrint(_Functions_.Green, f"{CONNEXION[0]}", "Connectée à ")
            else :
                print(f"Connexion à {connex[0]}")
                wifi.radio.connect(secrets["ssid"], secrets["password"])
                _Functions_.colorPrint(_Functions_.Green, f"{connex[0]}",  "Connectée à ")

    except RuntimeError as err :
        _Functions_.colorPrint(_Functions_.Rouge, err, "Non connectée : ")
    except ConnectionError as cerr :
        _Functions_.colorPrint(_Functions_.Rouge, cerr, "Non connectée : ")

    noteSD_EtatConnexion()
    pool = socketpool.SocketPool(wifi.radio)

    MOSQUITTO = ip_address()

    ao = MQTT.MQTT(
                    broker=f"{MOSQUITTO}",
                    # broker="192.168.137.1",
                    username=f"{CONNEXION[0]}",
                    password=f"{CONNEXION[1]}",
                    socket_pool=pool,
                    ssl_context=None if PORT == 1883 else ssl.create_default_context(),
    )

    try :
        ao.connect()
        return ao

    except Exception as e :
        print("---> MOSQUITTO :", e)
        return False

def connecter_io() :
    """Connexion à MQTT.
    Args:
    Récupération des identifiants de connexion,
    Appel de la fonction synchroniser_heure().
    Appel de la fonction  TempsP().
    Appels de la fonction disconnected(), message(), subscribe(), unsubscribe().
    Returns:
    Retourne io: MQTT connecté à Adafruit IO.
    Retourne false si jamais la connexion n'est pas réussie.
    """
    # Connexion au WIFI à partir des informations de settings.toml
    try :
        if os.getenv('AIO_USERNAME') and os.getenv('AIO_KEY') :

            secrets = {
                    'aio_username': os.getenv('AIO_USERNAME'),
                    'aio_key': os.getenv('AIO_KEY'),
                    'ssid': os.getenv("CIRCUITPY_WIFI_SSID"),
                    'password': os.getenv("CIRCUITPY_WIFI_PASSWORD")
                    }
        else :
            raise ImportError

    except ImportError :
        print("Les informations pour la connexion au WIFI et pour Adafruit IO ne sont pas disponibles dans le fichier settings.toml... ")
        raise

    aio_username = secrets["aio_username"]
    aio_key = secrets["aio_key"]

    if not wifi.radio.connected :
        try :
            print("Connexion à %s" % secrets["ssid"])
            wifi.radio.connect(secrets["ssid"], secrets["password"])
            print("Connecté à %s!" % secrets["ssid"])
    # --------------------- RYAN : CONNECTION ---------------------
        except ConnectionError :
            if not wifi.radio.connected :
                try :
                    connex = preconnection(0)
                    # _Functions_.colorPrint(_Functions_.Red, connex[0])

                    topSecrets = {
                        "aio_username" : f"{ADAFRUIT_AIO_USERNAME}",
                        "aio_key" : f"{ADAFRUIT_AIO_KEY}",
                        "ssid" : f"{connex[0]}",
                        "password" : f"{connex[1]}"
                    }

                    print("Connexion à %s" % topSecrets["ssid"])
                    wifi.radio.connect(topSecrets["ssid"], topSecrets["password"])
                    print("Connecté à %s!" % topSecrets["ssid"])

                except ConnectionError :
                    print("Wifi inconnu")
    # ------------------------------------------------------------------------------------
    pool = connecter_wifi()
    # --------------------------------------------------------------------------
    synchroniser_heure()
    # --------------------------------------------------------------------------
    TempsP()
    noteSD_EtatConnexion()
    # --------------------------------------------------------------------------
    mqtt = MQTT.MQTT(   socket_pool=pool,
                        username=secrets["aio_username"],
                        password=secrets["aio_key"],
                        ssl_context=ssl.create_default_context(),
                        broker="io.adafruit.com",
                        is_ssl=True,
                        port=8883
                    )

    io = IO_MQTT(mqtt)
    io.on_connect = connected
    io.on_disconnect = disconnected
    io.on_subscribe = subscribe
    io.on_unsubscribe = unsubscribe
    io.on_message = message

    try :

        io.connect()
        return io

    except Exception as e :
        disconnected (io)
        return False
    except ConnectionError as c :
        disconnected (io)
        return False

def noteSD_MQTT() :   
     
    if connecter_io() != False :     
        noteSD("MQTT connectee")
    elif connecter_io() == False :
        noteSD("MQTT non connectee")
    
    if connecter_mosquitto() != False :        
        noteSD("Mosquitto connectee")
    elif connecter_io() == False :
        noteSD("Mosquitto non connectee")
        

# ____________________________________________________________________________
# ____________________________________________________________________________
# ____________________________________________________________________________
# VI - RECONNEXION - WIFI - MQTT


def reconnecter_IO() :
    """Reconnexion à MQTT .
    Args:
        Check: Appel de la fonction connecter_io().
        Affichage de l'adresse IP si connexion établie
    Returns:
    Retourne La valeur de la fonction ConnectionAdafruit()
    Retourne False si la connexion n'est pas réussie
    """
    Check = connecter_io()
    if Check != False :
        _Functions_.colorPrint(_Functions_.Blue, f"Connected avec {wifi.radio.ipv4_address}")
        return reabonnement_io()
    else :
        return False

def reconnecter_mosquitto() :
    """Reconnexion à MQTT .
    Args:
        Check: Appel de la fonction connecter_io().
        Affichage de l'adresse IP si connexion établie
    Returns:
    Retourne La valeur de la fonction ConnectionAdafruit()
    Retourne False si la connexion n'est pas réussie
    """
    Check = connecter_mosquitto()
    if Check != False :
        _Functions_.colorPrint(_Functions_.Blue, f"Connected avec {wifi.radio.ipv4_address}")
        return reabonnement_mosquitto(Check)
    else :
        return

def reabonnement_io() :                                                                       #////
    """Connexion a Adafruit au moyen d'un subscribe et d'un publish.
    Args:
        io: Appel de la fonction connecter_io().
        feeds: Liste contenant les flux à souscrire.
    Returns:
    Retourne à io: MQTT connecté à Adafruit IO.

    """
    io = connecter_io()                                                                       #////

    feeds = [                                                                                   #////
            'TemperatureActuelle',                                                              #////
            'TemperatureMax',                                                                   #////
            'Mode',
            'LED'
        ]                                                                                       #////
    for feed in feeds :                                                                         #////
        io.subscribe(feed)                                                                      #////
    # io.publish('Mode', 'Normal')
    return io     

def reabonnement_mosquitto(ao) :                                                                       #////
    """Connexion a Adafruit au moyen d'un subscribe et d'un publish.
    Args:
        io: Appel de la fonction connecter_mqtt().
        feeds: Liste contenant les flux à souscrire.
    Returns:
    Retourne à io: MQTT connecté à Adafruit IO.

    """
    print("Connecté à Mosquitto")
    #io = connect_mqtt()                                                                       #////

    feeds = [                                                                                   #////
            'TemperatureActuelle',                                                              #////
            'TemperatureMax',   
            'Mode',
            'LED'
        ]                                                                                       #////
    for feed in feeds :                                                                         #////
        ao.subscribe(feed)                                                                      #////
    return ao


# ____________________________________________________________________________
# ____________________________________________________________________________
# ____________________________________________________________________________
# VII - PUBLICATION - MOSQUITTO - MQTT

def publier (client, Valeur, cible="temperature") :                                                             #////
    """ Envoi de Publish pour publier les données.
    Args:
    Appelle de MQTT au moyen du terme client
    Message est appelé pour la température maximale.
.
    """

    if cible == "temperature" :
        temperature = Valeur
        client.publish('TemperatureActuelle', temperature[0])                                       #////
        client.publish('TemperatureMax', temperature[1])                                            #////
        message(client, 'TemperatureActuelle', temperature[0])                                           #////
        message(client, 'TemperatureMax', temperature[1])                                           #////

    if cible == "Mode" :
        mode =  Valeur
        client.publish(cible, mode)
        message(client, cible, mode)                                           #////

    if cible == "Music" :
        musique = Valeur
        client.publish(cible, musique)
        message(client, cible, musique)                                           #////

    if cible == "LED" :
        led = Valeur
        client.publish(cible, led)
        message(client, cible, led)                                           #////
        
    if cible == "Light" :
        light = Valeur
        client.publish(cible, light)
        message(client, cible, light)                                           #////
        
    if cible == "Micro" :
        micro = Valeur
        client.publish(cible, micro)
        message(client, cible, micro)                                           #////
