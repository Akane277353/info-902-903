# pip install pvrecorder
# pip install pyaudio


import wave
import pyaudio
import struct
import os
import sys
import json
import requests
import subprocess
import RPi.GPIO as GPIO


from time import sleep
from pvrecorder import PvRecorder

for index, device in enumerate(PvRecorder.get_available_devices()):
    print(f"[{index}] {device}")

CPT = 0

Channel = 1
Rate = 16000
Format = pyaudio.paInt16

INIT = False

recorder = None

audio = []


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

i = 0

login = ""
path = './temp/config.t'

IP = "http://141.145.207.6:8080/"
def get(ip):
    data = {

    }

    json_data = json.dumps(data)
    headers = {'Content-Type': 'application/json'}
    r = requests.get(ip, headers=headers, verify=False)
    if r.status_code == 200:
        return r.content

def newlogin():
    route = IP+"assistant/login"
    return str(int(get(route)))
def testLogin(login):
    route = IP+"assistant/isvalid/"+login
    res = get(route)
    if(str(res)=="b'true'"):
        return login
    else:
        return newlogin()
        

try:
    file = open(path)
    conf = file.readlines()[0]
    login = testLogin(conf)
    if(login != conf):
        file2 = open(path,"w")
        file2.write(login)
        file2.close()
    file.close()
except FileNotFoundError:
    print('Sorry the file we\'re looking for doesn\' exist')
    conf = newlogin()
    login = testLogin(conf)
    if not os.path.exists("./temp"):
        os.makedirs("./temp")
    file = open(path,"w")
    file.write(login)
    file.close()
    login = conf

print("Identifiant : "+login)

def sendAudio(nom):
    absPath = "/".join(os.path.abspath(__file__).split("/")[:-2])
    path = absPath+"/RPI-Jon/temp/"+nom
    exe = absPath+"/rasperry/client.py"
    
    #hntts ipServeur portServeur
    #local https://localhost 8080
    address = "https://localhost"
    port = "8080"
    methode = "local"
    
    
    cmd = "python "+exe+" --mode '"+methode+"' --address '"+address+"' --port '"+port+"' --audio "+path
    #subprocess.run(cmd, shell = True, executable="/bin/bash")
    os.system(cmd)

while True:
    if GPIO.input(5) == GPIO.HIGH:
        if(INIT == False):
            print("Rec")
            recorder = PvRecorder(device_index=Channel, frame_length=512)
            recorder.start()
            INIT = True

        frame = recorder.read()
        audio.extend(frame)
        
    elif(INIT == True):
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

