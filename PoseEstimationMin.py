import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)

mPose = mp.solutions.pose
pose = mPose.Pose()
mpDraw = mp.solutions.drawing_utils

pTime = 0


while True:
    success,img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB)
    #print(results.pose_landmarks)

    if results.pose_landmarks:
        lmList = []
        for id, lm in enumerate(results.pose_landmarks.landmark):
            h,w,c = img.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            #print(id,lm)
            lmList.append([id,cx,cy])
            print(lmList)

            cv2.circle(img, (cx,cy),5, (255,0,0), 4)

        mpDraw.draw_landmarks(img, results.pose_landmarks, mPose.POSE_CONNECTIONS)

    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (70,50), cv2.FONT_HERSHEY_PLAIN,3,(0,255,0), 3)

    cv2.imshow("Results",img)
    if cv2.waitKey(1) & 0XFF == ord('q'):
        break