import os
import board
import digitalio
import analogio
import time
import pwmio
import adafruit_bmp280
import asyncio
import _Main_
import _Functions_

# ____________________________________________________________________________
# ____________________________________________________________________________
# ____________________________________________________________________________
# ____________________________________________________________________________
# 000 T A B L E   D E S   M A T I E R E S
# I. V A R I A B L E S
# II. C O N N E X I O N S
# III. E X E C U T E U R   P R I N C I P A L
# IV. E X E C U T E U R   F I N A L
# ____________________________________________________________________________
# ____________________________________________________________________________
# ______________________I. V A R I A B L E S______________________________________________________
# ____________________________________________________________________________
# Mise en place des objets de la carte Arduino
i2c = board.I2C()
bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)
bmp280.sea_level_pressure = 1016.10

# Initialiser la LED
led = digitalio.DigitalInOut(board.D6) # Pin PIR sensor
led.direction = digitalio.Direction.OUTPUT
led_last_time = time.monotonic()
last_time = 0.0

temp_actuelle: float = 0
temp_max: float = 0
compteur_de_connexion = 0
# Variables codees -------------------------
accumulation = []  

client = _Main_.ADAFRUIT_AIO_USERNAME  #-
tampons = _Main_.TamponDonnees(100)      #-
levier = 'Celcius'                        #-
temperatures_recentes = 0.0               #-
temp_debut = bmp280.temperature           #-
timestamp = _Main_.TEMPS                 #-
detecter_tache = None
wifi_check = _Main_._MQTT_.wifi.radio.connected
connecteeIO = "Connecté à Adafruit !"
connecteeMosquitto = "Connecté à Mosquitto !"
# ------------------------------------------
# récupère l'objet io depuis la fonction connecter_mqtt
declencheur = ''
# ____________________________________________________________________________
# ____________________________________________________________________________
# ___________________II. C O N N E X I O N S_________________________________________________________
# ____________________________________________________________________________

MOSQUITTO = _Main_._MQTT_.ip_address()
_Functions_.txtmosquitto(MOSQUITTO)
if MOSQUITTO == "" :
    _Functions_.colorPrint(_Functions_.Red, "Vide")

CheckMosquitto = _Main_._MQTT_.connecter_mosquitto()
CheckIO = _Main_._MQTT_.connecter_io()
# Tableau 
if CheckMosquitto != False :
    ao = CheckMosquitto
    ao = _Main_._MQTT_.reabonnement_mosquitto(CheckMosquitto)
if CheckIO != False :
    io = _Main_._MQTT_.reabonnement_io()
else :
    _Functions_.colorPrint(_Functions_.Violet, "Le code est operataonnel malgree le manque de connexaon wi-fi")

_Main_._MQTT_.noteSD_MQTT()

# ____________________________________________________________________________
# ____________________________________________________________________________
# _____________________III. E X E C U T E U R   P R I N C I P A L_______________________________________________________
# ____________________________________________________________________________


async def principale () : 
    global CheckIO, CheckMosquitto, ao, io, last_time, levier, compteur_de_connexion
    
    fin_time = (time.monotonic_ns()) / 10**9
    #-  Boucle while ---------------------------------
    while True:
        print(time.monotonic(), " <----  T E M P S")
        # 00 -> Chargement ao -----------------
        if (CheckMosquitto != False) and (CheckMosquitto is not None) :                  #-
            ao.loop()                        #-    
            if compteur_de_connexion >= 0 and compteur_de_connexion < 3 :
                print(connecteeMosquitto)
                compteur_de_connexion += 1
        if CheckIO != False :                  #-
            io.loop()                        #-    
            if compteur_de_connexion >= 0 and compteur_de_connexion < 3:
                print(connecteeIO)
                compteur_de_connexion += 1
        
        time_actuel = (time.monotonic_ns()) / 10**9

        _Functions_.colorPrint(_Functions_.Bleu, f"{timestamp}")
        
        if (CheckMosquitto != False) and (CheckMosquitto is not None):
            pass    # Si vous avez des affaires qui doivent necessiter la connexion Mosquitto            
        if CheckIO != False :
            pass    # Si vous avez des affaires qui doivent necessiter la connexion Adafruit            
        
        temp_actuelle = bmp280.temperature                                    #-
        accumulation.append(temp_actuelle)    
        temp_max = max(accumulation)   
        
        if (CheckMosquitto != False) and (CheckMosquitto is not None) :                
            levier = _Main_._MQTT_.message(client, 'TemperatureActuelle', levier)          #-

        # Affichage de la température, de la connexion MQTT et du déclencheur
        tmperature = _Main_.affichage(temp_actuelle, temp_max, wifi=False)
        print(tmperature) 
        
        await asyncio.sleep(0.5)
        
        # 01 ---> Envoi de température -----------------------------------
        if (time.monotonic() - last_time > 5):                                #-
            last_time = time.monotonic()                                      #-                
        # ----------------------------------------------------------------------
        # 03 ---> Publication des données sur Adafruit ----------------------------------------       
            intervalle_ns = 5 * 2 * 3     
                    
            if ((time_actuel - fin_time) >= intervalle_ns) and (CheckMosquitto != False) and (CheckMosquitto is not None) :            #-
                fin_time = time_actuel    
                try :                                                                       #-
                    _Functions_.txtmosquitto("Envoi -> Mosquitto")
                    _Main_._MQTT_.publier(ao, tmperature, "temperature")                         
                except OSError as o :                                                       #-
                    print("Erreur d'envoi")
                    
            if ((time_actuel - fin_time) >= intervalle_ns) and (CheckIO != False) :
                fin_time = time_actuel  
                try :
                    _Functions_.txtmqtt("Envoi -> Adafruit")
                    _Main_._MQTT_.publier(io, tmperature, "temperature")      
                except OSError as o :                                                       #-
                    print("Erreur d'envoi")

# ____________________________________________________________________________
# ____________________________________________________________________________
# _____________________IV. E X E C U T E U R   F I N A L_______________________________________________________
# ____________________________________________________________________________


async def mainP() :
    #   A S Y N C H R O N E
    if( (CheckMosquitto != False) and (CheckMosquitto is not None)) or (CheckIO != False):
        pass
    PRINCIPALE = asyncio.create_task(principale())
    await asyncio.gather(PRINCIPALE)


asyncio.run(mainP())