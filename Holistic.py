import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)

mpHolistic = mp.solutions.holistic
holistic = mpHolistic.Holistic()
mpDraw = mp.solutions.drawing_utils

while True:
    success,img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = holistic.process(imgRGB)

    #if results.face_landmarks:
    #    print(results.face_landmarks.landmark)

    mpDraw.draw_landmarks(img, results.face_landmarks, mpHolistic.FACE_CONNECTIONS)
    mpDraw.draw_landmarks(img, results.left_hand_landmarks, mpHolistic.HAND_CONNECTIONS)
    mpDraw.draw_landmarks(img, results.right_hand_landmarks, mpHolistic.HAND_CONNECTIONS)
    mpDraw.draw_landmarks(img, results.pose_landmarks, mpHolistic.POSE_CONNECTIONS)

    cv2.imshow("Results",img)
    if cv2.waitKey(1) & 0XFF==ord('q'):
        break