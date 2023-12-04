import RPi.GPIO as GPIO
import numpy as np
import time


def read_data(port):
    
    GPIO.setup(port, GPIO.OUT)
    GPIO.output(port, GPIO.HIGH)
    #给信号提示传感器开始工作,并保持低电平18ms以上
    # time.sleep(0.02)                #这里保持20ms   
    GPIO.output(port, GPIO.LOW)
    # GPIO.output(port, GPIO.HIGH)  #然后输出高电平
    
    GPIO.setup(port, GPIO.IN)    
    # 发送完开始信号后得把输出模式换成输入模式，不然信号线上电平始终被拉高
 
    while GPIO.input(port) == GPIO.LOW:
        continue
    #DHT11发出应答信号，输出 80 微秒的低电平
    
    while GPIO.input(port) == GPIO.HIGH:
        continue
    #紧接着输出 80 微秒的高电平通知外设准备接收数据
    
    
    #开始接收数据
    j = 0               #计数器
    data = []           #收到的二进制数据
    kk=[]               #存放每次高电平结束后的k值的列表
    while j < 50:
        k = 0
        while GPIO.input(port) == GPIO.LOW:  # 先是 50 微秒的低电平
            continue

        t1 = time.time()
        # print(t1)
        while GPIO.input(port) == GPIO.HIGH: # 接着是26-28微秒的高电平，或者 70 微秒的高电平
            k += 1
            if k > 1000:
                break
            time.sleep(0.0001)
            # time.sleep(0.000001)
        k = int((time.time()-t1)*10000)
        # print(t1)
        kk.append(k)
        if k < 15:       #26-28 微秒时高电平时通常k等于5或6
            data.append(0)      #在数据列表后面添加一位新的二进制数据“0”
        else:           #70 微秒时高电平时通常k等于17或18
            data.append(1)      #在数据列表后面添加一位新的二进制数据“1”
        
        j += 1
 
    print("sensor is working.")
    print('初始数据高低电平:\n',data)    #输出初始数据高低电平
    print('参数k的列表内容：\n',kk)      #输出高电平结束后的k值
    
    m = np.logspace(9,0,10,base=2,dtype=int) #logspace()函数用于创建一个于等比数列的数组
    #即[512 256 128 64 32 16 8 4 2 1]，8位二进制数各位的权值
    data_array = np.array(data) #将data列表转换为数组

    #dot()函数对于两个一维的数组，计算的是这两个数组对应下标元素的乘积和(数学上称之为内积)
    temperature = m.dot(data_array[0:10])           #用前8位二进制数据计算湿度的十进制值
    brightness = m.dot(data_array[10:20])
    air_quality = m.dot(data_array[20:30])
    humanity = m.dot(data_array[30:40])
    check = m.dot(data_array[40:50])
    
    print(temperature,brightness,air_quality,humanity,check)
    
    tmp = (temperature + brightness + air_quality + humanity)%1024
    #十进制的数据相加

    # return temperature, air_quality
    if check == tmp:    #数据校验，相等则输出
        return temperature, brightness, air_quality, humanity
    else:               #错误输出错误信息
        return False


if __name__ == "__main__":
    GPIO.setmode(GPIO.BOARD)
    while True:
        # input()
        print(read_data(11))
        time.sleep(5)

