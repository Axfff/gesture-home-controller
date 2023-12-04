import RPi.GPIO as GPIO
from time import sleep

class SERVO:
    def __init__(self, port, startAngle, maxAngle=180):
        self.port = port
        GPIO.setup(port, GPIO.OUT)
        self.maxAngle = maxAngle
        self.pwm = GPIO.PWM(port, 50)
        self.nowAngle = startAngle
        self.pwm.start(self.angleToDC(startAngle))

    def angleToDC(self, angle):
        return 2.5+10*(angle/self.maxAngle)

    def turnToAngle(self, angle):
        delta = abs(self.nowAngle-angle)
        self.nowAngle = angle
        self.pwm.ChangeDutyCycle(self.angleToDC(angle))
        # sleep(0.02*delta)
        # sleep(0.02)
        # self.pwm.ChangeDutyCycle(0)

    def addAngle(self, d_angle):
        self.nowAngle = min(max(self.nowAngle+d_angle, 0), self.maxAngle)
        self.turnToAngle(self.nowAngle)
        # sleep(0.002*abs(d_angle))
        # sleep(0.02)
        # self.pwm.ChangeDutyCycle(0)


# class SERVO:
#     def __init__(self, port, startAngle, maxAngle=180):
#         self.port = port
#         GPIO.setup(port, GPIO.OUT)
#         self.maxAngle = maxAngle
#         self.pwm = GPIO.PWM(port, 50)
#         self.nowAngle = startAngle
#         self.pwm.start(self.angleToDC(startAngle))
#         sleep(0.5)
#         self.pwm.stop()
#         print('stop')

#     def setServo(self, DC):
#         # self.pwm = GPIO.PWM(self.port, 50)
#         self.pwm.start(DC)
#         sleep(0.5)
#         self.pwm.stop()
#         print('stop')

#     def angleToDC(self, angle):
#         return 2.5+10*(angle/self.maxAngle)

#     def turnToAngle(self, angle):
#         self.nowAngle = angle
#         self.setServo(self.angleToDC(angle))

#     def addAngle(self, d_angle):
#         self.nowAngle = min(max(self.nowAngle+d_angle, 0), self.maxAngle)
#         self.setServo(self.angleToDC(self.nowAngle))


if __name__ == '__main__':
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(40, GPIO.OUT)
    s1 = SERVO(40, 90)
    sleep(1)
    # for i in range(3):
    #     s1.turnToAngle(0)
    #     sleep(1)
    #     s1.turnToAngle(60)
    #     sleep(1)
    #     s1.turnToAngle(120)
    #     sleep(1)
    #     s1.turnToAngle(180)
    #     sleep(1)

    # for i in range(200):
    #     s1.addAngle(-1)
    #     sleep(0.1)
    # for i in range(200):
    #     s1.addAngle(1)
    #     sleep(0.05)

    GPIO.setup(37, GPIO.IN)
    while True:
        if GPIO.input(37):
            s1.turnToAngle(60)
            print('high')
        else:
            s1.turnToAngle(120)
            print('low')

    GPIO.cleanup()

