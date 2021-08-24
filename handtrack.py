import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)

# (1) hand gotva mate niche mujab nu lakhavu pade j..
mpHands = mp.solutions.hands
hands = mpHands.Hands()
# (6) line dorva mate (jevi ke terva vache ni line (21 point vali))
mpDra = mp.solutions.drawing_utils

# (8) fps print karava mate
pTime = 0
cTime = 0         # baki no code nichhe chhe fps mate

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # (2) result hand ne pridict kare chhe.  result ma hand na attribute(x, y, z axis hoy chhe) hoy chhe
    result = hands.process(imgRGB)
    # print(result.multi_hand_landmarks)

    # (3) jo hand hoy to j prosses thay aana mate
    if result.multi_hand_landmarks:
        # (4) 2 hand pan hoe sake atle bane hand mate for loop lagayu chhe
        for handLms in result.multi_hand_landmarks:

            # (11) id number and landmark gotva mate
            # id number 1 to 21 valu and land marks id ni posion batave x, y and z cordinet
            for id, lm in enumerate(handLms.landmark):
                # print(id, lm)

                # (12) land marks pixel ma nathi fream retio ma chhe atle have aane pixal ma convert kariyu
                # pixel ma karva mate hight and widht joye
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                # print(id, cx, cy)

                # (13) id number uper circle dorva mate
                if id == 4:
                    # cv2.circle(image, x and y co-ordinate, )
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

            # (7) hand ma tapka drow karva mate
            # mpDra.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
            # hand ma line drow karva mate
            mpDra.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    # (9) fps mate
    cTime = time.time()   # time.time() current time aape
    fps = 1/(cTime - pTime)
    pTime = cTime

    # (10) fps print karava mate
    # cv2.putText(image, je lakhva nu hoy a text, jiya dekhadvu hoy aa point, font style, scale, color, thinkness)
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_SCRIPT_COMPLEX, 3, (0, 0, 0), 3)

    cv2.imshow("image", img)
    cv2.waitKey(1)