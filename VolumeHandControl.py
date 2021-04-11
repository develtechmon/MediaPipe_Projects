import cv2
import mediapipe as mp
import time

###########################
wCam, hcam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hcam)

#mpHands = mp.solutions.hands
#hands = mpHands.Hands()
pTime = 0

while True:
    success, img = cap.read()

    cTime = time.time()
    fps = 1 /(cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)),(10,60), cv2.FONT_HERSHEY_PLAIN,3, (255,0,255),4)

    cv2.imshow("Img",img)
    cv2.waitKey(1)