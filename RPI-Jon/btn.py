import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

i = 0
while True:
    if GPIO.input(5) == GPIO.HIGH:
        print("ON")
    else:
        print("OFF")
    sleep(0.5)
