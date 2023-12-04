import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)
GPIO.setup(32, GPIO.OUT)

for t in range(5):
    for i in range(0, 500, 5):
        GPIO.output(32, GPIO.HIGH)
        sleep(0.01*i/1000)
        GPIO.output(32, GPIO.LOW)
        sleep(0.01-0.01*i/1000)
    for i in range(500, 0, -5):
        GPIO.output(32, GPIO.HIGH)
        sleep(0.01*i/1000)
        GPIO.output(32, GPIO.LOW)
        sleep(0.01-0.01*i/1000)

GPIO.cleanup()

