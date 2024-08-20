import cv2
import mediapipe as mp
import numpy as np
import keyboard

class Pose_Keyboard_Control():
    def __init__(self, mode=False, upBody=False, smooth=True, detectionCon=0.5, trackCon=0.5):
        
        self.mode = mode
        self.upBody = upBody
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        
        #self.pose = self.mpPose.Pose(self.mode, self.upBody, self.smooth, self.detectionCon, self.trackCon)
        self.pose = self.mpPose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

        self.cap = cv2.VideoCapture(0)
        self.cap.set(3,1920)
        self.cap.set(4,1440)
        
        self.command = None

    def findImage(self):
        success,img = self.cap.read()
        return img
    
    def findPose(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)
        return img
    
    def findPosition(self, img, draw=True):
        self.lmList = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmList.append([id, cx, cy, w, h])
                if draw:
                    cv2.circle(img, (cx, cy), 8, (0, 0, 255), cv2.FILLED)
        return self.lmList
    
    def actionpose(self, img, lmList, detected, draw=True):
        """ Detect Nose And Track"""
        if len(lmList[0]) !=0 & lmList[0][0] == 0:
            if (lmList[16][2] > lmList[12][2]) & (lmList[15][2] > lmList[11][2]): #& (lmList[16][2] > lmList[0][2]) & (lmList[15][2] > lmList[0][2]):
                self.command = "down"
                print("Stop")
                
            """Detect Nose, Right Arm, Left Arm Shoulders and Track, Jump"""
            if (lmList[16][2] < lmList[0][2]) & (lmList[15][2] < lmList[0][2]):
                self.command = "up"
                print("Jump !")
                
            # """Detect Nose, Left Arm, Right Arm, Shoulders and Track, Move Left"""
            # if (lmList[16][2] < lmList[0][2]) & (lmList[15][2] > lmList[0][2]) & (lmList[15][2] > lmList[11][2]):
            #     self.command = "left"
            #     print("Move Left !")

            # """Detect Nose, Right Arm, Left Arm, Shoulders and Track, Move Right"""
            # if (lmList[15][2] < lmList[0][2]) & (lmList[16][2] > lmList[0][2]) & (lmList[16][2] > lmList[12][2]):
            #     self.command = "right"
            #     print("Move Right !")
            
            """Detect Nose, Left Arm, Right Arm, Shoulders and Track, Move Left"""
            if (lmList[20][2] < lmList[12][2]) & (lmList[15][2] > lmList[0][2]) & (lmList[15][2] > lmList[11][2]) & (lmList[15][2] > lmList[13][2]):
                self.command = "left"
                print("Move Left !")

            """Detect Nose, Right Arm, Left Arm, Shoulders and Track, Move Right"""
            if (lmList[19][2] < lmList[11][2]) & (lmList[16][2] > lmList[0][2]) & (lmList[16][2] > lmList[12][2]) & (lmList[16][2] > lmList[14][2]):
                self.command = "right"
                print("Move Right !")
                
            """Detect Nose, Left Arm, Right Arm, Shoulders and Track, Move Left"""
            if (lmList[16][2] < lmList[0][2]) & (lmList[14][2] < lmList[0][2]) & (lmList[15][2] > lmList[0][2]): #& (lmList[15][2] < lmList[11][2]):
                self.command = "jump left"
                print("Jump and Move Left !")
                
            """Detect Nose, Right Arm, Left Arm, Shoulders and Track, Move Right"""
            if (lmList[15][2] < lmList[0][2]) & (lmList[13][2] < lmList[0][2]) & (lmList[16][2] > lmList[0][2]): #& (lmList[16][2] < lmList[12][2]):
                self.command = "jump right"
                print("Jump and Move Right !")
                
            # """Detect Nose, Left Arm, Right Arm, Shoulders and Track, Move Left"""
            # if (lmList[16][2] < lmList[0][2]) & (lmList[15][2] > lmList[0][2]) & (lmList[15][2] < lmList[11][2]):
            #     self.command = "jump left"
            #     #print("Jump and Move Left !")
                
            # """Detect Nose, Right Arm, Left Arm, Shoulders and Track, Move Right"""
            # if (lmList[15][2] < lmList[0][2]) & (lmList[16][2] > lmList[0][2]) & (lmList[16][2] < lmList[12][2]):
            #     self.command = "jump right"
                #print("Jump and Move Right !")
                
            # else:
            #     self.command = "down"
            #     print("Stop")
                
        self.executeCommand()        
        
    def executeCommand(self):
        # Release all arrow keys first
        keyboard.release("k")
        keyboard.release("l")
        keyboard.release("h")
        #keyboard.release("right")

        # Press the corresponding key
        if self.command == "up":
            keyboard.press("k")
            print("Jump !")
            
        elif self.command == "left":
            keyboard.press("h")
            print("Move Left !")
            
        elif self.command == "right":
            keyboard.press("l")
            print("Move Right !")
            
        elif self.command == "jump right":
            keyboard.press("k")
            keyboard.press("l")
            print("Jump and Move Right !")
            
        elif self.command == "jump left":
            keyboard.press("k")
            keyboard.press("h")
            print("Jump and Move Left !")
            
        elif self.command == "down":
            keyboard.release("k")
            keyboard.release("l")
            keyboard.release("h")  
            print("Stop")
                
if __name__ == "__main__":
    detect = Pose_Keyboard_Control()
    
    while True:
        
        # Step 1 - Find Image
        img = detect.findImage()
        
        # Step 2 - Find Pose
        img = detect.findPose(img)
        
        # Step 3 - Find Position
        lmList = detect.findPosition(img)
        
        # Step 4 - Find Jump, Left, Right, Jump Left, Jump Right Pose
        if len(lmList) != 0:
            detected = True
            position = detect.actionpose(img, lmList, detected)

        cv2.imshow("Results",img)
        if cv2.waitKey(1) & 0XFF == ord('q'):
            break
        
    
        