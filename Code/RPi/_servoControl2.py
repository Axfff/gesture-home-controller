# from __future__ import division    # python2使用
from time import sleep
import Adafruit_PCA9685             # 调用PCA9685模块

from luma.core.interface.serial import i2c, spi
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1325, ssd1331, sh1106
from luma.core.virtual import viewport

# # 初始化端口
# serial = i2c(port=1, address=0x3C)
# # 初始化设备，这里改ssd1306, ssd1325, ssd1331, sh1106
# device = ssd1306(serial, width=128, height=32)

# pwm = Adafruit_PCA9685.PCA9685()
# # 设置最大最小脉冲长度
# servo_min = 75  # 4096的最小脉冲长度
# servo_max = 550  # 4096的最大脉冲长度
# servo_mid = 365  # 4096的中间脉冲长度
# 设置频率为60
# pwm.set_pwm_freq(50)
# print('Moving servo on, press Ctrl-C to quit...')
# for off in range(0, 731):
#     pwm.set_pwm(0, 0, off)
#     print(off)
#     with canvas(device) as draw:
#         draw.rectangle(device.bounding_box, outline="white", fill="black")
#         draw.text((30, 10), str(off), fill="white")
#     sleep(0.05)
# while True:
#     pwm.set_pwm(1, 0, servo_min)
#     sleep(1)
#     pwm.set_pwm(1, 0, servo_max)
#     sleep(1)


class SERVO:
    def __init__(self, channel, startAngle, maxAngle=180):
        self.channel = channel
        # GPIO.setup(port, GPIO.OUT)
        self.maxAngle = maxAngle
        self.pwm = Adafruit_PCA9685.PCA9685()
        self.pwm.set_pwm_freq(50)
        self.nowAngle = startAngle
        self.pwm.set_pwm(channel, 0, self.angleToPulseLength(startAngle))

        # with canvas(device) as draw:
        #     draw.rectangle(device.bounding_box, outline="white", fill="black")
        #     draw.text((30, 10), str(self.nowAngle), fill="white")

    def angleToPulseLength(self, angle):
        return int(75+(550-75)*(angle/self.maxAngle))

    def turnToAngle(self, angle):
        self.nowAngle = angle
        self.pwm.set_pwm(self.channel, 0, self.angleToPulseLength(angle))
        
        # with canvas(device) as draw:
        #     draw.rectangle(device.bounding_box, outline="white", fill="black")
        #     draw.text((30, 10), str(self.nowAngle), fill="white")

    def addAngle(self, d_angle):
        self.nowAngle = min(max(self.nowAngle+d_angle, 0), self.maxAngle)
        self.turnToAngle(self.nowAngle)
        
        # with canvas(device) as draw:
        #     draw.rectangle(device.bounding_box, outline="white", fill="black")
        #     draw.text((30, 10), str(self.nowAngle), fill="white")


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

    # import RPi.GPIO as GPIO
    
    # GPIO.setmode(GPIO.BOARD)
    # # GPIO.setup(40, GPIO.OUT)

    # GPIO.setup(37, GPIO.IN)
    # while True:
    #     if GPIO.input(37):
    #         # s1.turnToAngle(60)
    #         print('high')
    #     else:
    #         # s1.turnToAngle(120)
    #         print('low')

    # GPIO.cleanup()


