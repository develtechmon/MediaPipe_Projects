import cv2
import mediapipe as mp

class AutonymousCarRobotPoseEstimation():
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
        self.pid = [0.1, 0.1, 0]
        self.PError = 0
        self.speed = 30
        self.speedRight = 0
        self.speedForwardBackward = 0
        self.cap = cv2.VideoCapture(0)
        self.w, self.h = 640, 480

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
                h,w,c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmList.append([id,cx,cy,w,h])
                if draw:
                    cv2.circle(img, (cx,cy), 8 , (0,0,255), cv2.FILLED)
        return self.lmList

    def findPID(self,lmList, detected):
        print((lmList[0][0]))

        # Detect Nose and Track
        if len(lmList[0]) != 0 & lmList[0][0] == 0:
            posX_error = lmList[0][1] - lmList[0][3] // 2
            posY_error = lmList[0][2] - lmList[0][4] // 2

            speedX = self.pid[0] * posX_error + self.pid[1] * (posX_error)
            speedY = self.pid[0] * posY_error + self.pid[1] * (posY_error)
            print(str(speedX) + "----" + str(speedY))
if __name__ == "__main__":
    # Step 0 - Create an Object
    detector = AutonymousCarRobotPoseEstimation()

    while True:
        # Step 1 - FindImage
        img = detector.findImage()

        # Step 2 - DetectPose
        img = detector.findPose(img)

        # Step 3 - Find Position
        lmList = detector.findPosition(img)

        # Step 4 - Find PID
        if len(lmList) != 0:
            detected = True
            position = detector.findPID(lmList,detected)

        cv2.imshow("Result",img)
        if cv2.waitKey(1) & 0XFF == ord('q'):
            break






