import RPi.GPIO as GPIO
import time
import signal
import sys
import vibrate
import pyttsx

# use Raspberry Pi BCM pin numbers
GPIO.setmode(GPIO.BCM)

# Assigning GPIO pins for trigger and echos to the sensors
pinTrigger = [24,2]
pinEcho = [16,10]

#Exit function - cleans up the ports
def close(signal, frame):
	print("\nTurning off ultrasonic distance detection...\n")
	GPIO.cleanup()
	vibrate.stop_vibration()
	sys.exit(0)
	
signal.signal(signal.SIGINT, close)

# set GPIO input and output channels
GPIO.setup(pinTrigger, GPIO.OUT)
GPIO.setup(pinEcho, GPIO.IN)

#Distance function
def distance(sensor_num):
        # set GPIO input and output channels
        GPIO.setup(pinTrigger[sensor_num], GPIO.OUT)
        GPIO.setup(pinEcho[sensor_num], GPIO.IN)
        
	# set Trigger to HIGH
	GPIO.output(pinTrigger[sensor_num], True)
	# set Trigger after 0.01ms to LOW
	time.sleep(0.00001)
	GPIO.output(pinTrigger[sensor_num], False)

	startTime = time.time()
	stopTime = time.time()

	#Saves start time
	while 0 == GPIO.input(pinEcho[sensor_num]):
		startTime = time.time()

	#Saves stop time
	while 1 == GPIO.input(pinEcho[sensor_num]):
		stopTime = time.time()

	#Time difference between start and stop
	TimeElapsed = stopTime - startTime
	
	#Multiply with the Sonic Speed (34300 cm/s) and divide by 2, because there and back
	distance = (TimeElapsed * 34300) / 2
	return distance

#Main loop
while True:
	#Distance array
        dist = [0,0]
  	
	#Reading of first sensor
        dist[0] = distance(0)
	print ("Distance1 : %.1f cm" % dist[0])
	time.sleep(0.1)

	#Reading of second sensor
	dist[1] = distance(1)
	print ("Distance 2: %.1f cm" % dist[1])
	time.sleep(0.1)
	
