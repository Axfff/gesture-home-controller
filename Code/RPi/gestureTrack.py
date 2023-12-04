import cv2
import mediapipe as mp
import RPi.GPIO as GPIO
from servoControl2 import SERVO
from PID import PID
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands



# GPIO.setmode(GPIO.BOARD)
# GPIO.setup(40, GPIO.OUT)
# GPIO.setup(38, GPIO.OUT)
s_yaw = SERVO(0, 90)
pid_yaw = PID(-0.9, -0.06, -0.6)
s_pitch = SERVO(1, 80)
pid_pitch = PID(-0.9, -0.06, -0.6)



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
    # print(pos1_x, pos1_y, pos2_x, pos2_y)
    # print(imgSize[1])
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
    # delta = nowPos[0] - centerPos_x
    # alpha = 0.02
    print(f'target pos: {centerPos_x}; now pos: {nowPos[0]}')
    pid_yaw.update(nowPos[0])
    s_yaw.addAngle(pid_yaw.output*0.01)
    # s_yaw.turnToAngle(pid_yaw.output)

def track_y(nowPos, imgSize):
    centerPos_y = imgSize[0]/2
    pid_pitch.SetPoint = centerPos_y
    # delta = nowPos[1] - centerPos_y
    # alpha = 0.02
    print(f'target pos: {centerPos_y}; now pos: {nowPos[1]}')
    pid_pitch.update(nowPos[1])
    s_pitch.addAngle(pid_pitch.output*0.01)
    # s_pitch.turnToAngle(pid_pitch.output)


if __name__ == '__main__':
    from luma.core.interface.serial import i2c
    from luma.core.render import canvas
    from luma.oled.device import ssd1306
    serial = i2c(port=1, address=0x3C)
    # 初始化设备，这里改ssd1306, ssd1325, ssd1331, sh1106
    device = ssd1306(serial, width=128, height=32)

    # For webcam input:
    cap = cv2.VideoCapture(0)
    with mp_hands.Hands(
            # model_complexity=0,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as hands:

        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                # If loading a video, use 'break' instead of 'continue'.
                continue

            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = hands.process(image)

            # Draw the hand annotations on the image.
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            if results.multi_hand_landmarks:
                # with canvas(device) as draw:
                #     draw.rectangle(device.bounding_box, outline="white", fill="black")
                #     draw.text((30, 10), 'found hand', fill="white")

                for ind, hand_landmarks in enumerate(results.multi_hand_landmarks):
                    # show
                    mp_drawing.draw_landmarks(
                        image,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style())

                    x1, y1, x2, y2 = findBox(hand_landmarks.landmark, image.shape[:2])
                    cx, cy = findCenter(hand_landmarks.landmark, image.shape[:2])
                    print(x1, y1, x2, y2)
                    print(cx, cy)
                    image = cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 255), 2)
                    image = cv2.circle(image, (cx, cy), 2, (255, 0, 255), -1)
                    track_x(findCenter(hand_landmarks.landmark, image.shape[:2]), image.shape[:2])
                    track_y(findCenter(hand_landmarks.landmark, image.shape[:2]), image.shape[:2])

            # else:
            #     with canvas(device) as draw:
            #         draw.rectangle(device.bounding_box, outline="white", fill="black")
            #         draw.text((30, 10), 'no hand', fill="white")

                # # record
                # with open('datas/five.txt', 'a') as f:
                #     f.write('123')

            # Flip the image horizontally for a selfie-view display.
            # cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
            # if cv2.waitKey(5) & 0xFF == 27:
            #     break

    cap.release()
    # GPIO.cleanup()
