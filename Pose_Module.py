import math

import cv2
import mediapipe as mp
import numpy as np
import time

class poseDetectorModule():
    def __init__(self, mode=False, upBody=False, smooth=True,
                 detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.upBody = upBody
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode, self.upBody, self.smooth,
                                     self.detectionCon, self.trackCon)

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
                # print(id,lm)
                self.lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 8, (0, 0, 255), cv2.FILLED)
        return self.lmList

    def findAngle(self, img, points,check):
        x1, y1 = self.lmList[points[0]][1:]
        x2, y2 = self.lmList[points[1]][1:]
        x3, y3 = self.lmList[points[2]][1:]

        """Calculate the Angle - 2D dimension space with inverse tan trigonometry law."""
        angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))

        """Use Acceleration Vector - 3D space dimension vectors"""
        """u.v/ ||u||||v||"""
        uv = (x1*x3) + (y1*y3)
        u = math.sqrt(pow(x1,2) + pow(y1,2))
        v = math.sqrt(pow(x3,2) + pow(y3,2))

        vectorAngle = math.degrees(math.acos(uv/(u*v)))
        # print(vectorAngle)

        if angle < 0:
            angle += 360

        if check:
            angle = np.interp(angle, (180, 360), (180, 0))

        if angle >= 140:
            cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 3)
            cv2.line(img, (x3, y3), (x2, y2), (0, 255, 0), 3)

            cv2.circle(img, (x1, y1), 10, (0, 255, 0), cv2.FILLED)
            cv2.circle(img, (x1, y1), 20, (0, 255, 0), 3)

            cv2.circle(img, (x2, y2), 10, (0, 255, 0), cv2.FILLED)
            cv2.circle(img, (x2, y2), 20, (0, 255, 0), 3)

            cv2.circle(img, (x3, y3), 10, (0, 255, 0), cv2.FILLED)
            cv2.circle(img, (x3, y3), 20, (0, 255, 0), 3)

        else:
            cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
            cv2.line(img, (x3, y3), (x2, y2), (255, 255, 255), 3)

            cv2.circle(img, (x1, y1), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x1, y1), 20, (0, 0, 255), 3)

            cv2.circle(img, (x2, y2), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 20, (0, 0, 255), 3)

            cv2.circle(img, (x3, y3), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x3, y3), 20, (0, 0, 255), 3)

        cv2.putText(img, str(int(angle)), (x2 + 30, y2 - 30), cv2.FONT_HERSHEY_PLAIN, 4, (0, 255, 0), 2)

        return angle


def main():
    cap = cv2.VideoCapture(0)
    detector = poseDetectorModule()
    pTime = 0
    count = 0
    dir = 0

    while True:
        success, img = cap.read()
        img = detector.findPose(img, draw=False)
        lmList = detector.findPosition(img, draw=False)
        points = [12, 14, 16]
        if len(lmList) != 0:

            if count > 5:
                angle = detector.findAngle(img, points,check=True)
                per = np.interp(angle, (80, 155), (0, 100))
                bar = np.interp(per, (0, 100), (400, 100))

            else:
                angle = detector.findAngle(img, points,check=False)
                per = np.interp(angle, (75, 135), (100, 0))
                bar = np.interp(per, (0, 100), (400, 100))

            if angle >= 170:
                bar = 400
                per = 0

            color = (255, 0, 255)
            if per == 100:
                color = (0, 255, 0)
                if dir == 0:
                    count += 0.5
                    dir = 1

            if per == 0:
                color = (0, 255, 0)
                if dir == 1:
                    count += 0.5
                    dir = 0

            print(count)

            # Draw Bar
            cv2.rectangle(img, (550, 100), (600, 400), color, 3)
            cv2.rectangle(img, (550, int(bar)), (600, 400), color, cv2.FILLED)
            cv2.putText(img, f'{int(per)}%', (530, 80), cv2.FONT_HERSHEY_PLAIN, 2,
                        color, 3)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.imshow("Result", img)
        #cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

        if cv2.waitKey(1) & 0XFF == ord('q'):
            break


if __name__ == "__main__":
    main()
