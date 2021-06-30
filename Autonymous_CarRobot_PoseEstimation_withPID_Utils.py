from Autonymous_CarRobot_PoseEstimation_withPID_Function import *

if __name__ == "__main__":
    detector = AutonymousCarRobotPoseEstimation()
    while True:
        img = detector.findImage()
        img = detector.findPose(img)
        lmList = detector.findPosition(img)

        if len(lmList) != 0:
            detected = True
            position = detector.findPID(lmList,detected)

        cv2.imshow("Result",img)
        if cv2.waitKey(1) & 0XFF == ord('q'):
            break




