import cv2
import mediapipe as mp
import HandTrackingModule as htm

class NoseHandTracking():
    def __init__(self, mode=False, upBody=False, smooth=True, detection=0.5, trackCon=0.5):
        self.cap = cv2.VideoCapture(0)
        self.landmark = [0,7,8]
        self.mode = mode
        self.upBody = upBody
        self.smooth = smooth
        self.detectionCon = detection
        self.trackCon = trackCon
        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        #self.pose = self.mpPose.Pose(self.mode, self.upBody, self.smooth, self.detectionCon, self.trackCon)
        self.pose = self.mpPose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)


    def findImage(self, img, draw=False):     
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)

        if draw:
            if self.results.pose_landmarks:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)

        return img

    def findPosition(self,img):
        idList = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h,w,c = img.shape
                cx,cy = int(lm.x * w), int(lm.y * h)

                idList.append([id,cx,cy,w,h])

                if id in self.landmark:
                    cv2.circle(img, (cx,cy), 8, (0,0,255),cv2.FILLED)
        
if __name__ == "__main__":
    detect = NoseHandTracking()
    detector = htm.handDetector()

    while True:
        success, img = detect.cap.read()

        # Step 1 - Find Nose and Hand
        Nose = detect.findImage(img)
        Hand = detector.findHands(img)

        # Step 2 - Find Position
        position = detect.findPosition(img)

        cv2.imshow("Results",img )
        if cv2.waitKey(1) & 0XFF == ord('q'):
            break

    cv2.destroyAllWindows()


    
    
