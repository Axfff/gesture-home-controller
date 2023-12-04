import RPi.GPIO as GPIO
from time import sleep

class SERVO:
    def __init__(self, port, startAngle, maxAngle=180):
        self.port = port
        self.maxAngle = maxAngle
        self.pwm = GPIO.PWM(port, 50)
        self.nowAngle = startAngle
        self.pwm.start(self.angleToDC(startAngle))

    def angleToDC(self, angle):
        return 2.5+10*(angle/self.maxAngle)

    def turnToAngle(self, angle):
        self.nowAngle = angle
        self.pwm.ChangeDutyCycle(self.angleToDC(angle))

    def addAngle(self, d_angle):
        self.nowAngle = min(max(self.nowAngle+d_angle, 0), self.maxAngle)
        self.pwm.ChangeDutyCycle(self.angleToDC(self.nowAngle))


if __name__ == '__main__':
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(40, GPIO.OUT)
    s1 = SERVO(40, 90)
    sleep(1)
    for i in range(3):
        s1.turnToAngle(0)
        sleep(1)
        s1.turnToAngle(60)
        sleep(1)
        s1.turnToAngle(120)
        sleep(1)
        s1.turnToAngle(180)
        sleep(1)

    for i in range(200):
        s1.addAngle(-1)
        sleep(0.1)
    for i in range(200):
        s1.addAngle(1)
        sleep(0.05)

