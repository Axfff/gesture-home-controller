import RPi.GPIO as GPIO
from time import sleep
import threading
import TCP

GPIO.setmode(GPIO.BOARD)

class LIGHT:
    def __init__(self, name, port=None):
        self.port = port
        self.name = name

    def swich(self, operation):
        if operation == 1:
            threading.Thread(target=lambda: TCP.sendData(f'{self.name}_on')).start()
            if self.port:
                GPIO.output(self.port, GPIO.HIGH)
        elif operation == 2:
            threading.Thread(target=lambda: TCP.sendData(f'{self.name}_off')).start()
            if self.port:
                GPIO.output(self.port, GPIO.LOW)
        elif operation == 3:
            threading.Thread(target=lambda: TCP.sendData(f'{self.name}_toggle')).start()
            if self.port:
                GPIO.setup(self.port, GPIO.IN)
                tar = GPIO.input(self.port)
                print(tar)
                GPIO.setup(self.port, GPIO.OUT)
                if tar:
                    GPIO.output(self.port, GPIO.LOW)
                else:
                    GPIO.output(self.port, GPIO.HIGH)
        
        

if __name__ == '__main__':
    light = LIGHT(37)
    
        
    
    