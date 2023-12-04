#!/usr/bin/python3
# -*- coding: utf-8 -*-
from luma.core.interface.serial import i2c, spi
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1325, ssd1331, sh1106
from luma.core.virtual import viewport
from time import sleep
from PIL import ImageFont
"""
OLED luma 驱动库测试程序
功能：显示 几何图形 持续10秒
"""
__version__ = 1.0
# 初始化端口
serial = i2c(port=1, address=0x3C)
# 初始化设备，这里改ssd1306, ssd1325, ssd1331, sh1106
device = ssd1306(serial, width=128, height=32)
print("当前版本：", __version__)
font = ImageFont.truetype('/home/pi/Desktop/controlSystem/tests/alibabapuhui.otf', 12) # fm.findfont(fm.FontProperties('jiangchenghei500w.ttf'))

# 调用显示函数
with canvas(device) as draw:
    draw.rectangle(device.bounding_box, outline="white", fill="black")
    draw.text((30, 10), "Hello World", fill="white")
# 延时显示10s
sleep(3)

# 调用显示函数
with canvas(device) as draw:
    draw.rectangle(device.bounding_box, outline="white", fill="black")
    draw.text((5, 10), "古诗一首", fill="white", font=font)
    draw.text((5, 24), "白日依山尽，", fill="white", font=font)
    draw.text((5, 38), "黄河入海流。", fill="white", font=font)
# 延时显示10s
sleep(3)

# 调用显示函数
with canvas(device) as draw:
    draw.rectangle(device.bounding_box, outline="white", fill="black")
    # Draw an ellipse.
    draw.ellipse((2, 2, 20, 28), outline="white", fill="black")
    # Draw a rectangle.
    draw.rectangle((24, 2, 42, 28), outline="blue", fill="black")
    # Draw a triangle.
    draw.polygon([(44, 28), (54, 2), (64, 28)], outline="green", fill="black")
    # Draw an X.
    draw.line((66, 28, 86, 2), fill="yellow")
    draw.line((66, 2, 86, 28), fill="yellow")
    # 延时显示10s
sleep(3)


txt = """
将进酒
李白
君不见黄河之水天上来，
奔流到海不复回。
君不见高堂明镜悲白发，
朝如青丝暮成雪。
人生得意须尽欢，
莫使金樽空对月。
天生我材必有用，
千金散尽还复来。
 
"""
 
txt2 = """将进酒 君不见黄河之水天上来，奔流到海不复回。君不见高堂明镜悲白发，朝如青丝暮成雪。
李白   人生得意须尽欢，莫使金樽空对月。天生我材必有用，千金散尽还复来。
""" 
 
 
virtual = viewport(device, width=500, height=768)
 
def horizontal_scroll():
    with canvas(virtual) as draw:
        for i, line in enumerate(txt2.split("\n")):
            draw.text((0, (i * 16)), text=line, fill="white", font=font)
 
    sleep(2)
 
    # update the viewport one position below, causing a refresh,
    # giving a rolling up scroll effect when done repeatedly
    y = 0
    for x in range(240):
        virtual.set_position((x, y))
        sleep(0.01)
 
def vertical_scroll():
    with canvas(virtual) as draw:
        for i, line in enumerate(txt.split("\n")):
            draw.text((0, 20 + (i * 16)), text=line, fill="white", font=font)
 
    sleep(2)
 
    # update the viewport one position below, causing a refresh,
    # giving a rolling up scroll effect when done repeatedly
    x = 0
    for y in range(240):
        virtual.set_position((x, y))
        sleep(0.01)
 
 
def main():
    print("当前版本：", __version__)
    horizontal_scroll()
    vertical_scroll()

main()
