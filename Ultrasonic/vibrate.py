import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
##GPIO.setwarnings(False)
left = 27
right = 25
def low_vibration(num):
    seconds = 0.9
    mtime=1
    if num == 1:
        num = left
    else:
        num = right
    for i in range(3):
        GPIO.setup(num, GPIO.OUT)
        print ("Led on")
        GPIO.output(num, GPIO.HIGH)
        time.sleep(mtime-seconds)
        print ("Led off")
    

        GPIO.output(num,GPIO.LOW)
        time.sleep(seconds)

def medium_vibration(num):
    seconds = 0.5
    mtime=1
    if num == 1:
        num = left
    else:
        num = right
    for i in range(3):
        GPIO.setup(num, GPIO.OUT)
        print ("Led on")
        GPIO.output(num, GPIO.HIGH)
        time.sleep(mtime-seconds)
        print ("Led off")
    

        GPIO.output(num,GPIO.LOW)
        time.sleep(seconds)
def high_vibration(num):
    seconds = 0.01
    mtime=1
    if num == 1:
        num = left
    else:
        num = right
    for i in range(3):
        GPIO.setup(num, GPIO.OUT)
        print ("Led on")
        GPIO.output(num, GPIO.HIGH)
        time.sleep(mtime-seconds)
        print ("Led off")
    

        GPIO.output(num,GPIO.LOW)
        time.sleep(seconds)
        
def stop_vibration():
    GPIO.output(left,GPIO.LOW)
    GPIO.output(right,GPIO.LOW)
