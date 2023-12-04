# from __future__ import division    # python2使用
from time import sleep
import Adafruit_PCA9685             # 调用PCA9685模块


class SERVO:
    def __init__(self, channel, startAngle, maxAngle=180):
        self.channel = channel
        # GPIO.setup(port, GPIO.OUT)
        self.maxAngle = maxAngle
        self.pwm = Adafruit_PCA9685.PCA9685()
        self.pwm.set_pwm_freq(50)
        self.nowAngle = startAngle
        self.turnToAngle(self.nowAngle)
        # self.pwm.set_pwm(channel, 0, self.angleToPulseLength(startAngle))

    def angleToPulseLength(self, angle):
        return int(75+(550-75)*(angle/self.maxAngle))

    def turnToAngle(self, angle):
        self.nowAngle = angle
        self.pwm.set_pwm(self.channel, 0, self.angleToPulseLength(angle))

    def addAngle(self, d_angle):
        self.nowAngle = min(max(self.nowAngle+d_angle, 0), self.maxAngle)
        self.turnToAngle(self.nowAngle)


if __name__ == '__main__':
    s1 = SERVO(1, 90)
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

    # GPIO.setup(37, GPIO.IN)
    # while True:
    #     if GPIO.input(37):
    #         s1.turnToAngle(60)
    #         print('high')
    #     else:
    #         s1.turnToAngle(120)
    #         print('low')

    # GPIO.cleanup()


