import RPi.GPIO as GPIO
import time
import signal
import sys
import vibrate
import pyttsx

# use Raspberry Pi BCM pin numbers
GPIO.setmode(GPIO.BCM)

# Assigning GPIO pins for trigger and echos to the sensors
pinTrigger = [24,23,18,6,17,5,26,2,9]
pinEcho = [16,12,21,20,4,19,22,10,11]

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
        dist = [0,0,0,0,0,0,0,0,0]
  	
	#Reading of first sensor
        dist[0] = distance(0)
	print ("Distance1 : %.1f cm" % dist[0])
	time.sleep(0.1)

	#Reading of second sensor
	dist[1] = distance(1)
	print ("Distance 2: %.1f cm" % dist[1])
	time.sleep(0.1)
	
	# Reading of third sensor
	dist[2] = distance(2)
	print ("Distance 3: %.1f cm" % dist[2])
	time.sleep(0.1)
	
	#Reading of fourth sensor
	dist[3] = distance(3)
	print ("Distance 4: %.1f cm" % dist[3])
	time.sleep(0.1)
	
	# Reading of fifth sensor
	dist[4] = distance(4)
	print ("Distance 5: %.1f cm" % dist[4])
	time.sleep(0.1)
	
	##Reading of sixth sensor
	dist[5] = distance(5)
	print ("Distance 6: %.1f cm" % dist[5])
	time.sleep(0.1)
	
	#Reading of seventh sensor
	dist[6] = distance(6)
	print ("Distance 7: %.1f cm" % dist[6])
	
	#Reading of eigth sensor (left side)
	dist[7] = distance(7)
	print ("Distance 8: %.1f cm" % dist[7])
	
	#Reading of 9th sensort (right side)
	dist[8] = distance(8)
	print ("Distance 8: %.1f cm" % dist[8])
	
	
	
	##NAVIGTIONAL LOGIC
	#0 -100 cm close - high vibration
	
	#If the first sensor detects an object within 100 cm, go into this statement
	if 0 < dist[0] <= 100:
            x = 0
            for i in range (1, 7):
                if dist[i] > 100:
                    x = x + 1
            if 4 <= x <= 6:
                vibrate.high_vibration(1)
                print("Right Sensors Activated: buzz high left")
                continue
            else:
		if dist[7] > 100:
			vibrate.high_vibration(1)
			print("Wall ahead: rotate left")
		else:
                	vibrate.high_vibration(0)
                	print("Right  Sensors Activated: buzz high right")
                	continue
        
        # center sensors  
        elif 0 < dist[3] <= 100 or 0 < dist[4] <= 100:
            x = 0
            for i in range (0, 3):
                if dist[i] > 100:
                    x = x + 1
            if x == 3:
                vibrate.high_vibration(0)
                print("Center Sensors Activated: buzz low right")
                continue
        
            if x < 3:
                x = 0
                for i in range (5, 7):
                    if dist[i] > 100:
                        x = x + 1
            if x==2:
                vibrate.high_vibration(1)
                print("Centers Sensors Activated: buzz low left")
                continue
    
        #left sensors
        elif 0 < dist[5] <= 100 or 0 < dist[6] <= 100:
            x = 0
            for i in range (0, 5):
                if dist[i] > 100:
                    x = x + 1
            if 3 <= x <= 5:
                vibrate.high_vibration(0)
                print("Left Sensors Activated: buzz low right")
                continue
            else:
		if dist[8] > 100:
			vibrate.high_vibration(0)
			print("Wall ahead: rotate right") #hallway to right is open
		else:
                	vibrate.high_vibration(1)
                	print("Left Sensors Activated: buzz low left")
                	continue
    
	######100-200 med vibration
##      right sensor
        elif 100 < dist[0] <= 150:
            x = 0
            for i in range (1, 7):
                if dist[i] > 150:
                    x = x + 1
            if 4 <= x <= 6:
                vibrate.medium_vibration(1)
                print("right sensor: buzz medium  left")
                continue
            else:
		if dist[7] > 150:
			vibrate.medium_vibration(1)
			print("Wall ahead: rotate left") #wall ahead, left hallway clear
		else:
                	vibrate.medium_vibration(0)
                	print("Right  Sensors Activated: buzz medium right")
                	continue
        
        # center sensors  
        elif 100 < dist[3] <= 150 or 100 < dist[4] <= 150:
            x = 0
            for i in range (0, 3):
                if dist[i] > 150:
                    x = x + 1
            if x == 3:
                vibrate.medium_vibration(0)
                print("Center: buzz med right")
                continue
        
            if x < 3:
                x = 0
                for i in range (5, 7):
                    if dist[i] > 150:
                        x = x + 1
            if x==2:
                vibrate.medium_vibration(1)
                print("Center: buzz med  left")
                continue
    
        #left sensors
        elif 100 < dist[5] <= 150 or 100 < dist[6] <= 150:
            x = 0
            for i in range (0, 5):
                if dist[i] > 150:
                    x = x + 1
            if 3 <= x <= 5:
                vibrate.medium_vibration(0)
                print("Left: buzz med  right")
                continue
            else:
		if dist[8] > 150:
			vibrate.medium_vibration(0)
			print("Wall ahead: rotate right") #hallway to right is open
		else:
                	vibrate.medium_vibration(1)
                	print("Left Sensors Activated: buzz low left")
                	continue
           
	###### >200 far vibration
##      right sensor
        elif 150 <  dist[0] < 200:
            x = 0
            for i in range (0, 7):
                if dist[i] > 200:
                    x = x + 1
            if 4 <= x <= 6:
                vibrate.low_vibration(1)
                print("Right: buzz high left")
                continue
            else:
		if dist[7] > 200:
			vibrate.low_vibration(1)
			print("Wall ahead: rotate left") #wall ahead, left hallway clear
		else:
                	vibrate.low_vibration(0)
                	print("Right  Sensors Activated: buzz low right")
                	continue

        # center sensors  
        elif 150 < dist[3] < 200  or 150 < dist[4] < 200:
            x = 0
            for i in range (0, 3):
                if dist[3] > 200:
                    if dist[i] > 200:
                        x = x + 1
                elif dist[4] > 200:
                    if dist[i] > 200:
                        x = x + 1
            if x == 3:
                vibrate.low_vibration(0)
                print("Center: buzz high  right")
                continue
        
            if x < 3:
                x = 0
                for i in range (5, 7):
                    if dist[i] > 200:
                        x = x + 1
            if x==2:
                vibrate.low_vibration(1)
                print("Center: buzz high left")
                continue
    
        #left sensors
        elif 150 <  dist[5] < 200 or 150 < dist[6] < 200:
            x = 0
            for i in range (0, 5):
                if dist[i] > 200:
                    x = x + 1
            if 3 <= x <= 5:
                vibrate.low_vibration(0)
                print("Left: high buzz right")
                continue
            else:
		if dist[8] > 200:
			vibrate.low_vibration(0)
			print("Wall ahead: rotate right") #hallway to right is open
		else:
                	vibrate.low_vibration(1)
                	print("Left Sensors Activated: buzz high left")
                	continue
      
