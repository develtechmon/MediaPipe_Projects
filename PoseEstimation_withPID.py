import cv2
import mediapipe as mp
import time
import numpy as np
from djitellopy import Tello

class poseDetectionModule():
    def __init__(self, mode=False, upBody=False, smooth=True,
                detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.upBody = upBody
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode, self.upBody, self.smooth, self.detectionCon, self.trackCon)

    def initialize(self):
        myDrone = Tello()
        myDrone.connect()
        myDrone.for_back_velocity = 0
        myDrone.left_right_velocity = 0
        myDrone.up_down_velocity = 0
        myDrone.yaw_velocity = 0
        myDrone.speed = 0
        print(myDrone.get_battery())
        myDrone.streamoff()
        myDrone.streamon()
        return myDrone

    def drawLine(self,img,w,h):
        cv2.line(img, (w // 2, 0), (w // 2, h), (0, 255, 0), 3)
        cv2.line(img, (0, h//2), (w, h//2), (0, 255, 0), 3)
        return img

    def findImage(self,cap, w, h):
        # success, img = cap.read()
        myFrame = cap.get_frame_read()
        myFrame = myFrame.frame
        img = cv2.resize(myFrame, (w, h))
        return img

    def findPose(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)
        return img

    def findPosition(self,img,draw=True):
        self.lmList = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h,w,c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmList.append([id, cx,cy, w, h])
                if draw:
                    cv2.circle(img, (cx, cy), 8, (0, 0, 255), cv2.FILLED)
        return self.lmList

    def findPID(self,img, lmList, pid, pError, detected, myDrone, draw=True):
        #print(lmList[0])
        if len(lmList[0]) !=0:
            posX_error = lmList[0][1] - lmList[0][3]//2
            posY_error = lmList[0][2] - lmList[0][4]//2

            speedX = pid[0] * posX_error + pid[1] * (posX_error - pError)
            speedY = pid[0] * posY_error + pid[1] * (posY_error - pError)

            speedX = int(np.clip(speedX, -100,100))
            speedY = int(np.clip(speedY, -100, 100))
            #print(posX, posY)

            print(speedX, -speedY)

        if detected == True:
            if lmList[0][1] !=0 | lmList[0][2] !=0:
                myDrone.yaw_velocity = speedX
                myDrone.up_down_velocity = -speedY
            else:
                myDrone.for_back_velocity = 0
                myDrone.left_right_velocity = 0
                myDrone.up_down_velocity = 0
                myDrone.yaw_velocity = 0

            if myDrone.send_rc_control:
                myDrone.send_rc_control(myDrone.left_right_velocity,
                                        myDrone.for_back_velocity,
                                        myDrone.up_down_velocity,
                                        myDrone.yaw_velocity)
        return speedX

    def Scanning(self,detected, speed):
        if detected == False:
            myDrone.up_down_velocity = speed
            myDrone.send_rc_control(myDrone.left_right_velocity,
                                        myDrone.for_back_velocity,
                                        myDrone.up_down_velocity,
                                        myDrone.yaw_velocity)
            print(0,speed)

def main():

    """Webcam"""
    cap = cv2.VideoCapture(0)

    detector = poseDetectionModule()
    w,h = 640,480
    pid = [0.1, 0.1, 0]
    pError = 0
    speed = 30
    startCounter = 0

    """Tello Webcam Return"""
    #return detector,pTime,w,h,pid,pError,speed, startCounter

    """WebCam Return"""
    return cap,detector,w,h,pid,pError,speed, startCounter

if __name__ == "__main__":

    """Tello WebCam"""
    #detector, pTime, w, h, pid, pError, speed, startCounter = main()

    """WebCam"""
    cap,detector,w,h,pid,pError,speed, startCounter = main()

    myDrone = detector.initialize()

    while True:

        if startCounter == 0:
            myDrone.takeoff()
            time.sleep(5)
        startCounter = 1

        success,img = cap.read()

        ## Step 0 - Find Image from Tello WebCam
        #img = detector.findImage(myDrone, w,h)

        ## Step 1 -Detect Pose
        img = detector.findPose(img)

        ## Step 2 - Find Position
        lmList = detector.findPosition(img)

        ## Step 3 - Draw Line
        img = detector.drawLine(img,w,h)

        ## Step 3 - Find PID speed
        if len(lmList) !=0:
            detected = True
            position = detector.findPID(img, lmList, pid, pError, detected, myDrone)

        #else:
            #myDrone.up_down_velocity = speed
            #myDrone.yaw_velocity = 0
            #myDrone.send_rc_control(myDrone.left_right_velocity,
            #                        myDrone.for_back_velocity,
            #                        myDrone.up_down_velocity,
            #                        myDrone.yaw_velocity)

        cv2.imshow("Result", img)
        if cv2.waitKey(1) & 0XFF == ord('q'):
            myDrone.land()
            time.sleep(1)
            break







