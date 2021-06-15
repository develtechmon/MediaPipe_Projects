import cv2
import mediapipe as mp
import time

#from future.utils import lmap

cap = cv2.VideoCapture(0)

mFace = mp.solutions.face_detection
#face = mFace.FaceDetection()
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0
with mFace.FaceDetection(
    min_detection_confidence=0.5) as face:
    while True:
        success, image = cap.read()
        image.flags.writeable = True

        imgRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = face.process(imgRGB)

        if results.detections:
            for detections in results.detections:
                for id,lm in enumerate(results.detections):
                    h,w,c = image.shape
                    cv2.line(image, (w//2,0), (w//2,h), (0,255,0),3)
                mpDraw.draw_detection(image,detections)

        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime

        cv2.putText(image, str(int(fps)), (10,60), cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)
        cv2.imshow("Image Detection", image)
        
        if cv2.waitKey(1) & 0XFF == ord('q'):
            break
