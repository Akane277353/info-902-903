# pip install pvrecorder
# pip install pyaudio


import wave
import pyaudio
import struct
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
        
        with wave.open( "audio"+str(CPT)+".wav", 'w') as f:
            f.setparams((1, 2, Rate, 512, "NONE", "NONE"))
            f.writeframes(struct.pack("h" * len(audio), *audio))
            CPT = CPT+1
            print("END")
            recorder.delete()
            recorder = None
            audio = []
            INIT = False
