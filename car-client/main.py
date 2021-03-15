import time
import RPi.GPIO as GPIO
import requests
import picamera
from picamera.array import PiRGBArray
import base64
import json
import multiprocessing


BackRight, purple = [21, 20], [21, 20]
FrontLeft, blue = [19, 26], [19, 26]
FrontRight, green = [12, 16], [12, 16]
BackLeft, yellow = [6, 13], [6, 13]

forward = [green[1], blue[1], yellow[1], purple[1]]
backward = [green[0], blue[0], yellow[0], purple[0]]
leftward = [purple[1], blue[0]]
rightward = [yellow[1], green[0]]

motors = [purple, yellow, green, blue]

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

FrontLeftServo = 18
FrontRightServo = 4

for p in motors:
	GPIO.setup(p[1], GPIO.OUT)
	GPIO.setup(p[0], GPIO.OUT)

GPIO.setup(FrontLeftServo, GPIO.OUT)
GPIO.setup(FrontRightServo, GPIO.OUT)
fls = GPIO.PWM(FrontLeftServo, 50)
frs = GPIO.PWM(FrontRightServo, 50)

def Run(m, t=1, r=1):
	for x in range(r):
		for p in m:
			GPIO.output(p, 1)
		time.sleep(t/r)
		for p in m:
			GPIO.output(p, 0)
		#time.sleep(s)

def TurnAndRun(d, m):
	if d == 1:
		fls.start(8)
		frs.start(8)
	if d == 0:
		fls.start(6.5)
		frs.start(6.5)
	time.sleep(1.5)
	#Run(m)
	#fls.ChangeDutyCycle(7.5)
	#frs.ChangeDutyCycle(7.5)
	#time.sleep(1)
	#fls.stop()
	#frs.stop()
	#time.sleep(0.5)

camera = picamera.PiCamera()
time.sleep(0.5)

def Capture():
	camera.capture("image.jpg")
	b64 = ""
	with open("image.jpg", "rb") as img:
		b64 = base64.b64encode(img.read())
	return b64

t = time.time()

def CommandProcess():
	global t
	try:
		while True:
			r = requests.get("http://83.254.235.138:8000/command")
			data = json.loads(r.text)
			t = int(data[1])
			commands = data[0]
			if commands != []:
				for c in commands:
					if c["command"] == 0:
						multiprocessing.Process(target=Run, args=([forward])).start()
					elif c["command"] == 1:
						multiprocessing.Process(target=Run, args=([backward])).start()
					elif c["command"] == 2:
						multiprocessing.Process(target=TurnAndRun, args=([0, forward])).start()
					elif c["command"] == 3:
						multiprocessing.Process(target=TurnAndRun, args=([1, rightward])).start()
				print("commands executed")
			if time.time()-t < 30:
				time.sleep(0.1)
			else:
				time.sleep(5)
	except KeyboardInterrupt:
	        for m in motors:
        	        GPIO.output(m[0], 0)
                	GPIO.output(m[1], 0)



def StartCameraStream():
	global t
	while True:
		print(t)
		if time.time()-t < 30:
			try:
				r = requests.post("http://83.254.235.138:8000/image", data=Capture())
				t = int(r.text)
			except Exception as e:
				print(e)
			print("image sent")
			time.sleep(1)
			continue
		time.sleep(1)

p = multiprocessing.Process(target=CommandProcess)
p.start()
StartCameraStream()
