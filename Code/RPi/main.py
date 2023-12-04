import time

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(37, GPIO.IN)

import temperatureControl

# ======================OLED=======================
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
# 初始化端口
serial = i2c(port=1, address=0x3C)
# 初始化设备，这里改ssd1306, ssd1325, ssd1331, sh1106
device = ssd1306(serial, width=128, height=32)
# ======================OLED========================

# =======================PTZ=======================
with canvas(device) as draw:
    draw.text((20, 10), f'ptz init...', fill="white")

from PID import PID
pid_yaw = PID(-1.6, -0.0, -0.9)
pid_pitch = PID(-2.9, -0.0, -0.9)

from servoControl2 import SERVO
s_yaw = SERVO(0, 90)
s_pitch = SERVO(1, 100)
# =======================PTZ=======================

# ====================gesture=======================
with canvas(device) as draw:
    draw.text((20, 10), f'cv init...', fill="white")
import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands


with canvas(device) as draw:
    draw.text((10, 10), f'loading model...', fill="white")
import numpy as np
from keras.models import Sequential
from keras.layers import Dense

model = Sequential()
model.add(Dense(units=64, activation='relu', input_dim=65))
model.add(Dense(units=128, activation='relu'))
model.add(Dense(units=64, activation='relu'))
model.add(Dense(units=32, activation='relu'))
model.add(Dense(units=13, activation='softmax'))
model.load_weights('/home/pi/Desktop/controlSystem/main/my_model_weights.h5')


def translateData(landmarks, handedness):
    # record
    res = '['

    for landmark in landmarks:
        x = str(landmark).split('\n')[0][3:]
        y = str(landmark).split('\n')[1][3:]
        z = str(landmark).split('\n')[2][3:]
        # print()
        res += f'{x}, {y}, {z}, '

    handType = '0' if str(handedness).split('\n')[3][10:-1] == 'Left' else '1'
    score = str(handedness).split('\n')[2][9:]
    # print(handType, score)
    res += f'{handType}, '
    res += f'{score}'

    res += ']'
    return np.array(eval(res))


def findBox(landmarks, imgSize):
    # print(imgSize)
    pos1_x = str(landmarks[0]).split('\n')[0][3:]
    pos1_y = str(landmarks[0]).split('\n')[1][3:]
    pos2_x = str(landmarks[0]).split('\n')[0][3:]
    pos2_y = str(landmarks[0]).split('\n')[1][3:]
    for landmark in landmarks:
        pos1_x = min(str(landmark).split('\n')[0][3:], pos1_x)
        pos2_x = max(str(landmark).split('\n')[0][3:], pos2_x)
        pos1_y = min(str(landmark).split('\n')[1][3:], pos1_y)
        pos2_y = max(str(landmark).split('\n')[1][3:], pos2_y)
    pos1_x = int(float(pos1_x) * imgSize[1])
    pos1_y = int(float(pos1_y) * imgSize[0])
    pos2_x = int(float(pos2_x) * imgSize[1])
    pos2_y = int(float(pos2_y) * imgSize[0])

    return pos1_x, pos1_y, pos2_x, pos2_y


def findCenter(landmarks, imgSize):
    x1, y1, x2, y2 = findBox(landmarks, imgSize)
    cx = int((x1+x2)/2)
    cy = int((y1+y2)/2)
    return cx, cy


def track_x(nowPos, imgSize):
    centerPos_x = imgSize[1]/2
    pid_yaw.SetPoint = centerPos_x
    print(f'target pos: {centerPos_x}; now pos: {nowPos[0]}')
    pid_yaw.update(nowPos[0])
    s_yaw.addAngle(pid_yaw.output*0.01)
    # s_yaw.turnToAngle(pid_yaw.output)

def track_y(nowPos, imgSize):
    centerPos_y = imgSize[0]/2
    pid_pitch.SetPoint = centerPos_y
    print(f'target pos: {centerPos_y}; now pos: {nowPos[1]}')
    pid_pitch.update(nowPos[1])
    s_pitch.addAngle(pid_pitch.output*0.01)
    # s_pitch.turnToAngle(pid_pitch.output)

isDetect = False
humanUndetectedCount = 0
# ====================gesture=======================

# ====================threads=======================
import threading

def HumanExistingThread_func():
    global isDetect, humanUndetectedCount
    humanExistingState = 0
    judgeCount = 30
    while True:
        if GPIO.input(37):
            print('high')
            humanExistingState = 1
            isDetect = True

        else:
            if humanExistingState == 0:
                pass
            elif humanExistingState == 1:
                humanExistingState = 2
            elif humanExistingState == 2:
                if humanUndetectedCount < judgeCount:
                    humanUndetectedCount += 1
                else:
                    humanUndetectedCount = 0
                    humanExistingState = 1
                    isDetect = False
            # s1.turnToAngle(120)
            print('low')

        time.sleep(1)

HumanExistingThread = threading.Thread(target=HumanExistingThread_func)
HumanExistingThread.setDaemon(True)
HumanExistingThread.start()
# ====================threads=======================


if __name__ == '__main__':
    while True:
        if isDetect:
            # Cam input:
            cap = cv2.VideoCapture(0)
            hands = mp_hands.Hands(
                            min_detection_confidence=0.5,
                            min_tracking_confidence=0.5)

            lastTime = time.time()
            nowTime = lastTime
            fps = 0

            while cap.isOpened():
                success, image = cap.read()
                if not success:
                    print("Ignoring empty camera frame.")
                    continue

                image.flags.writeable = False
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                results = hands.process(image)

                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                if results.multi_hand_landmarks:
                    humanUndetectedCount = 0
                    for ind, hand_landmarks in enumerate(results.multi_hand_landmarks):
                        # gesture tracking
                        track_x(findCenter(hand_landmarks.landmark, image.shape[:2]), image.shape[:2])
                        track_y(findCenter(hand_landmarks.landmark, image.shape[:2]), image.shape[:2])

                        # gesture recognization
                        x = translateData(hand_landmarks.landmark, results.multi_handedness[ind])
                        x.resize((1, 65))
                        prediction = model.predict(x)
                        prediction = np.argmax(prediction)
                        print(prediction)
                    
                    with canvas(device) as draw:
                        draw.text((15, 10), f'found hand: type{prediction}', fill="white")

                else:
                    if not isDetect:
                        break

                    with canvas(device) as draw:
                        draw.text((10, 10), f'board tem: {temperatureControl.get_cup_tem()}', fill="white")
                
                # calculate frame per sec
                nowTime = time.time()
                fps = 1/(nowTime - lastTime)
                lastTime = nowTime
                # with canvas(device) as draw:
                #         draw.text((10, 10), f'FPS: {fps}', fill="white")
                    

            cap.release()
        
        else:
            with canvas(device) as draw:
                draw.text((20, 10), f'not detecting', fill="white")






