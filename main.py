import cv2
import time
import math
import numpy as np
import HandTrackingModual as htm
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

detector = htm.handDetector(detectioCon=0.7)
pTime = 0

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))


# volume.GetMute()
# volume.GetMasterVolumeLevel()
volrange = volume.GetVolumeRange()
volume.SetMasterVolumeLevel(0, None)

print(volrange)
minvol = volrange[0]
maxvol = volrange[1]

while True:
    sucesses, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPositon(img, draw=False)
    if len(lmList) != 0:
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]

        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 2)
        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

        lenght = math.hypot(x2 - x1, y2 - y1)
        # print(lenght)
        if lenght < 45:
            cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)
        vol = np.interp(lenght, [45, 200], [minvol, maxvol])
        # print(vol)
        volume.SetMasterVolumeLevel(vol, None)
        cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
        cvol = np.interp(vol, (minvol, maxvol), (400, 150))
        cv2.rectangle(img, (50, int(cvol)), (85, 400), (255, 0, 0), cv2.FILLED)
        volpr = np.interp(lenght, [45, 200], [0, 100])
        cv2.putText(img, f'{int(volpr)} %', (35, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)

    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime

    cv2.putText(img, f'FPS : {int(fps)}', (50, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
    cv2.imshow("image", img)
    cv2.waitKey(1)