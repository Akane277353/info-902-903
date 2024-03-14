# pip install pvrecorder
# pip install pyaudio
# pip install simpleaudio


#=============================================================
# Import
#=============================================================
import wave
import pyaudio
import struct
import os
import sys
import json
import requests
import subprocess
import RPi.GPIO as GPIO
import simpleaudio as sa

from time import sleep
from pvrecorder import PvRecorder
from subprocess import Popen

#=============================================================
# Constantes & Variable Global
#=============================================================

for index, device in enumerate(PvRecorder.get_available_devices()):
    print(f"[{index}] {device}")

#Audio Constantes
CPT = 0
Channel = 1
Rate = 16000
Format = pyaudio.paInt16
#Stockage Audio
INIT = False
recorder = None
audio = []
#Configuration GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#Identifiant Unique
login = ""
config = {}
AbsolPath = '/home/pi/Documents/info-902-903/RPI-Jon/'
pathLogin = AbsolPath+'temp/config.t'
pathConfig = AbsolPath+'temp/config.json'
#Serveur Cible
IP = "http://141.145.207.6:8080/"
#Connecter à Internet
internet = False

outputSound = AbsolPath+"a.wav"

#=============================================================
# Serveur
#=============================================================
#Fonction de requet GET Générique
def get(ip):
    data = {

    }

    json_data = json.dumps(data)
    headers = {'Content-Type': 'application/json'}
    r = requests.get(ip, headers=headers, verify=False)
    if r.status_code == 200:
        return r.content

#Demande un nouveau identifiant au serveur
def newlogin():
    route = IP+"assistant/login"
    return str(int(get(route)))
#Test si l'identifiant est toujours valide si il ne l'est pas il en demande un nouveau
def testLogin(login):
    route = IP+"assistant/isvalid/"+login
    res = get(route)
    if(str(res)=="b'true'"):
        return login
    else:
        return newlogin()
        
def getConf(login):
    route = IP+"assistant/config/"+login
    res = get(route)
    res = str(res)
    res = res[2:-1]
    res = json.loads(res)
    return res
    
    
    
        

#=============================================================
# Client.py
#=============================================================
#envoie l'audio au serveur via le client et reçois un audio en retour
def sendAudio(nom):
    absPath = "/".join(os.path.abspath(__file__).split("/")[:-2])
    path = absPath+"/RPI-Jon/temp/"+nom
    exe = absPath+"/rasperry/client.py"
    
    #hntts ipServeur portServeur
    #local https://localhost 8080
    address = "https://localhost"
    port = "8080"
    methode = "local"
    model = "mistral"
    
    if(internet):
        address = "https://141.145.207.6"
        port = "4444"
        methode = "hntts"
        model = "mistral"
    
    
    cmd = "python "+exe+" --mode '"+methode+"' --address '"+address+"' --port '"+port+"' --audio "+path+" --id '"+login+"' --model '"+model+"'"
    print(cmd)
    #subprocess.run(cmd, shell = True, executable="/bin/bash")
    os.system(cmd)
    print("TTS Terminer !")
    playSound(outputSound)

#=============================================================
# Sound
#=============================================================
    
def playSound(filename):
    print("Playing ...")
    wave_obj = sa.WaveObject.from_wave_file(filename)
    play_obj = wave_obj.play()
    play_obj.wait_done()
    print("End Playing")
    
def UpdateLoginSound():
    global login
    log = login[:]
    log = list(log)
    txt = ""
    for i in range(len(log)-1):
        txt = txt + "Le numéro "+log[i]+", "
    txt = txt + "Le numéro "+log[len(log)-1]+"."
    absPath = "/".join(os.path.abspath(__file__).split("/")[:-2])
    #exe = absPath+"/rasperry/client.py"
    exe = "../rasperry/client.py"
    

    
    
    cmd = "python "+exe+" --tts '"+txt+"'"
    print(cmd)
    #subprocess.run(cmd, shell = True, executable="/bin/bash")
    BackOn = False
    os.system("rm "+outputSound)
    while BackOn == False:
        try:
            cmd = "python "+exe+" --tts '"+txt+"'"
            os.system(cmd)
            print("TTS Login Terminer !")
            cmd = "cp '"+outputSound+"' ./temp/login.wav"
            os.system(cmd)
            playSound("./temp/login.wav")
            print("BackOn : ON")
            BackOn = True
            print("UpdateLoginSound try")
        except:
            print("BackOn : OFF")
            BackOn = False
            print("UpdateLoginSound except")
            sleep(7)
    
    

#=============================================================
# Login
#=============================================================

def loadLogin():
    global login
    try:
        file = open(pathLogin)
        lignes = file.readlines()
        file.close()

        login = lignes[0]
        return True
    except FileNotFoundError:# Si il n'y a pas d'identifiant il en demande un et le sauvegarde
        print('Identifiant Introuvable')
        if not os.path.exists("temp"):
            os.makedirs(AbsolPath+"temp")
        file = open(pathLogin,"w")
        file.write("")
        file.close()
        return False

def saveLogin(login):
    file = open(pathLogin,"w")
    file.write(login)
    file.close()


def setup_login():
    global login
    res = True
    #Prend l'identifiant sauvgardé si il existe et verifie si il est valide. Si il n'est plus valide il sauvegarde le nouveau login
    status = loadLogin()#load les config renvoie true si
    print(login,status)
    if(status):
        if(internet):
            conf = testLogin(login)
            if(conf != login):
                login = conf
                saveLogin(login)
    else:
        if(internet):
            conf = newlogin()
            login = testLogin(conf)
            saveLogin(login)
        else:
            res = False
            print("NO Identifiant")
    return res
    
#=============================================================
# Config
#=============================================================

def loadConfig():
    global config
    try:
        file = open(pathConfig)
        
        lignes = file.readlines()
        file.close()

        config = lignes[0]
        config = json.loads(config)
        return True
    except FileNotFoundError:# Si il n'y a pas d'identifiant il en demande un et le sauvegarde
        print('Config Introuvable')
        if not os.path.exists("./temp"):
            os.makedirs("./temp")
        file = open(pathConfig,"w")
        file.write("")
        file.close()
        return False

def saveConfig(config):
    config_s = json.dumps(config)
    file = open(pathConfig,"w")
    file.write(config_s)
    file.close()

def setup_config():
    global login
    global config
    res = True
    #Prend l'identifiant sauvgardé si il existe et verifie si il est valide. Si il n'est plus valide il sauvegarde le nouveau login
    status = loadConfig()#load les config renvoie true si
    if(status):
        if(internet):
            conf = getConf(login)
            if(conf != config):
                config = conf
                saveConfig(config)
    else:
        if(internet):
            config = getConf(login)
            saveConfig(config)
        else:
            res = False
            print("NO Config File")
    return res
            
#=============================================================
# Main
#=============================================================

print("Demarage Service")
#Test Connection
try:
    op = requests.get("https://www.google.com", timeout=20).status_code
    print("Internet : ON")
    internet = True
except:
    print("Internet : OFF")
    internet = False

#internet = False
isLogin = setup_login()
print("Setup Login")
if(isLogin):
    print("Identifiant : "+login)
    getConf(login)
    
    isConfig = setup_config()
    print("Setup Config")
    if(isConfig):
        print("Config :")
        print(config)
        print("Demarage Serveur")
        #p = Popen(["python","/home/pi/Documents/info-902-903/rasperry/server.py"])
        sleep(10)
        print("Login TTS")
        UpdateLoginSound()
        
        print("Start Listening ...")
        while True:
            if GPIO.input(5) == GPIO.HIGH:#Si on apuit sur le bouton on lance l'enregistrement
                if(INIT == False):
                    print("Rec")
                    recorder = PvRecorder(device_index=Channel, frame_length=512)
                    recorder.start()
                    INIT = True

                frame = recorder.read()
                audio.extend(frame)
                
            elif(INIT == True): #Si on enregistre pas et qu'on a fait un enregistrement on le sauvegarde en fichier WAV et on envoie au serveur IA
                print("Save")
                recorder.stop()
                nom = "audio"+str(CPT)+".wav"
                with wave.open( "./temp/"+nom, 'w') as f:
                    f.setparams((1, 2, Rate, 512, "NONE", "NONE"))
                    f.writeframes(struct.pack("h" * len(audio), *audio))
                    CPT = CPT+1
                    print("END")
                    sendAudio(nom)
                    recorder.delete()
                    recorder = None
                    audio = []
                    INIT = False

