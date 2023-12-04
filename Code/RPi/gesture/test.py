import cv2
import mediapipe as mp
import numpy as np
# from tensorflow.keras.models import load_model
from keras.models import Sequential
from keras.layers import Dense
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands


# def translateScientificNotation(numStr):
#     if 'e' not in numStr:
#         return float(numStr)
#     base, exponent = numStr.split('e')
#     return str(float(base)*(10**int(exponent)))


def translateData(landmarks, handedness):
    # record
    res = '['

    # print(landmarks)
    # print(str(handedness).split('\n')[3][10:-1])
    # print(str(handedness).split('\n')[2][9:])

    for landmark in landmarks:
        # print(str(landmark).split('\n')[0][3:])
        # print(str(landmark).split('\n')[1][3:])
        # print(str(landmark).split('\n')[2][3:])
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


# For webcam input:
cap = cv2.VideoCapture(0)

# model = load_model('/home/pi/Desktop/controlSystem/gesture/128x128x64x64_1024epochs_0.967.keras')
model = Sequential()
model.add(Dense(units=64, activation='relu', input_dim=65))
model.add(Dense(units=128, activation='relu'))
model.add(Dense(units=64, activation='relu'))
model.add(Dense(units=32, activation='relu'))
model.add(Dense(units=13, activation='softmax'))
model.load_weights('/home/pi/Desktop/controlSystem/gesture/my_model_weights.h5')

with mp_hands.Hands(
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
            for ind, hand_landmarks in enumerate(results.multi_hand_landmarks):
                # show
                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())

                x = translateData(hand_landmarks.landmark, results.multi_handedness[ind])
                x.resize((1, 65))
                # print(x)
                # print(type(x))
                # print(x.shape)
                prediction = model.predict(x)
                prediction = np.argmax(prediction)
                print(prediction)

            # # record
            # with open('datas/five.txt', 'a') as f:
            #     f.write('123')

        # Flip the image horizontally for a selfie-view display.
        # cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
        if cv2.waitKey(5) & 0xFF == 27:
            break

cap.release()


