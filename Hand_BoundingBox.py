import cv2
import time
from HandTrackingModule import handDetector
from djitellopy import tello

cap = cv2.VideoCapture(0)
cap.set(3,1920)
cap.set(4,1440)

# me = tello.Tello()
# me.connect()
# print(me.get_battery())
# me.streamon()

def webcamVideo():
    detector = handDetector(detectionCon=0.5, maxHands=2)
    startCounter = 0
    while True:
        success, img = cap.read()
        height, width, centre = img.shape
        hands, img = detector.findAllHands(img)

        # droneImg = me.get_frame_read().frame
        # droneImg = cv2.resize(droneImg, (640, 480))

        ## Draw Middle Line
        #cv2.line(img,(width//2,0),(width//2,height-24), (255,0,255),3)
        #cv2.line(img,(0,height//2),(width-24,height//2), (255,0,255),3)

        ## Draw Circle in the Middle Line
        cv2.circle(img, (width//2, height//2), 8, (0, 0, 255), cv2.FILLED)
        cv2.rectangle(img, (0, height-24), (width,height), (0,0,0), -1)
        cv2.rectangle(img, (width, 0), (0,60), (0,0,0), -1)
        if hands:
            ## Dictionary index start at index 0 for Left
            hand1 = hands[0]
            lmList1 = hand1["lmList"]
            bbox1 = hand1["bbox"]
            centerPoint1 = hand1["center"]
            handType1 = hand1["type"]

            fingers1 = detector.fingersUp(hand1)
            
            if len(hands) == 2:
                ## Dictionary index start at index 1 for Right
                hand2 = hands[1]
                lmList2 = hand2["lmList"]
                bbox2 = hand2["bbox"]
                centerPoint2 = hand2["center"]
                handType2 = hand2["type"]

                fingers2 = detector.fingersUp(hand2)
                length, info, img = detector.findDistance(lmList1[4], lmList2[4],img)

                # Drone Take Off
                if startCounter == 0:
                    if (fingers1[1] == 1 and fingers2[1] == 1):
                        #me.takeoff()
                        #message = "Drone TakeOff"
                        #time.sleep(1)
                        startCounter = 1
                    else:
                        message = "Waiting to Take Off"
                cv2.putText(img,message, (width//2 - 100, 50),cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)

                if startCounter == 1:
                    lr, fb, ud, yv = 0,0,0,0
                    speed = 30

                    # Check if Right or Left in the Front
                    if (info[5] > 480):
                        if (info[4] < 640) and (fingers1[1] == 0 & fingers2[1] == 0) :
                            message = "Move Left"
                            lr = -speed

                        if (info[4] > 640) and (fingers1[1] == 0 & fingers2[1] == 0) :
                            message = "Move Right"
                            lr = speed

                        if (info[4] < 640) and (fingers1[1] == 1 & fingers2[1] == 1):
                            message = "Tilt Left"
                            yv = -30

                        if (info[4] > 640) and (fingers1[1] == 1 & fingers2[1] == 1) :
                            message = "Tilt Right"
                            yv = 30

                    if (info[5] < 480):
                        if (info[4] < 640) and (fingers1[1] == 0 & fingers2[1] == 0):
                            message = "Move Backward"
                            fb = -speed

                        if (info[4] > 640) and (fingers1[1] == 0 & fingers2[1] == 0):
                            message = "Move Forward"
                            fb = speed

                        if (info[4] < 640) and (fingers1[1] == 1 & fingers2[1] == 1):
                            message = "Move Downward"
                            ud = -speed

                        if (info[4] > 640) and (fingers1[1] == 1 & fingers2[1] == 1):
                            message = "Move Upward"
                            ud = speed

                    if (info[5] == 480):
                        message = "Stop"
                        #me.land()
                        startCounter = 0

                    cv2.putText(img,message, (width//2 - 100, 50),cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
                    #me.send_rc_control(lr, fb, ud, yv)

        #cv2.imshow("Drone View", droneImg)
        cv2.imshow("Result",img)
        if cv2.waitKey(1) & 0XFF == ord('q'):
            #me.land()
            time.sleep(1)
            break

if __name__ == "__main__":
    webcamVideo()


