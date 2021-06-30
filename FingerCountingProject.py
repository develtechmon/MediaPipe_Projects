import cv2
import time
import os
import HandTrackingModule as htm

#####################
wCam, hCam = 640, 480
#####################

cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
pTime = 0

folderPath = r"MediaPipe_Tutorial/FingerImage"
myList = os.listdir(folderPath)
overlayList = []

for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)
    #print ((f'{folderPath}/{imPath}'))

print(len(overlayList))

tipIds = [4, 8, 12, 16, 20]

detector = htm.handDetector()

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) !=0:
        fingers = []
        #print(lmList[tipIds[0]][1])

        if (lmList[tipIds[0]][1]) > lmList[tipIds[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        for id in range(1,5):
            if (lmList[tipIds[id]][2]) < (lmList[tipIds[id]-2][2]):
                fingers.append(1)
            else:
                fingers.append(0)
        print(fingers)
        totalFingers = fingers.count(1) # Counting 1
        #print(totalFingers)

        h,w,c = overlayList[totalFingers].shape
        img[0:h, 0:w] = overlayList[totalFingers]

        cv2.putText(img, str(int(totalFingers)), (50, 450), cv2.FONT_HERSHEY_PLAIN, 7, (225, 255, 0), 10)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    #cv2.putText(img, str(int(fps)), (550,40), cv2.FONT_HERSHEY_PLAIN,3, (225,0,255),4)

    cv2.imshow("Output", img)
    if cv2.waitKey(1) & 0XFF == ord('q'):
        break