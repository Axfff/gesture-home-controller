import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands


# def translateScientificNotation(numStr):
#     if 'e' not in numStr:
#         return float(numStr)
#     base, exponent = numStr.split('e')
#     return str(float(base)*(10**int(exponent)))


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
        print()
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


# For webcam input:
cap = cv2.VideoCapture(0)
with mp_hands.Hands(
        model_complexity=0,
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

                x1, y1, x2, y2 = findBox(hand_landmarks.landmark, image.shape[:2])
                cx, cy = findCenter(hand_landmarks.landmark, image.shape[:2])
                print(x1, y1, x2, y2)
                image = cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 255), 2)
                image = cv2.circle(image, (cx, cy), 2, (255, 0, 255), -1)

            # # record
            # with open('datas/five.txt', 'a') as f:
            #     f.write('123')

        # Flip the image horizontally for a selfie-view display.
        cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
        if cv2.waitKey(5) & 0xFF == 27:
            break

cap.release()


