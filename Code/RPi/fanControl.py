import RPi.GPIO as GPIO
import time

import Adafruit_PCA9685
pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(50)


# pin = 7                    # 使用8号引脚
# GPIO.setmode(GPIO.BOARD)    # 使用BOARD引脚编号，此外还有 GPIO.BCM
# GPIO.setup(pin, GPIO.OUT)   # 设置7号引脚输出
def get_cup_tem():
    with open("/sys/class/thermal/thermal_zone0/temp","r") as fp:
        return int(fp.readline())/1000

def main(channel):
    running = 0         #设置一个变量记录风扇状态，策略是：
                        #当风扇启动时，要降温到45度
    while True:
        print(f'board temperature: {get_cup_tem()}')
        if(get_cup_tem()>60):
            # GPIO.output(port, GPIO.HIGH) ## 打开 GPIO 引脚（HIGH）
            pwm.set_pwm(channel, 0, 700)
            running = 1
        elif running:
            if(get_cup_tem()<45):
                pwm.set_pwm(channel, 0, 0)  ## 关闭 GPIO 引脚（LOW)
                running = 0
        time.sleep(5) #睡眠5s

if __name__ == '__main__':
    main(15)

