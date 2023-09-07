import numpy as np
import cv2
import cv2.aruco as aruco

marker_size = 100




aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_250)
cap = cv2.VideoCapture(0)

ret,frame = cap.read()

gray_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

corners,ids, rejected = aruco.detectMarkers(gray_frame,aruco_dict)
if ids is not None:
    aruco.drawDetectedMarkers(frame, corners)
    rvec,tvec,_objPoints = aruco.estimatePoseSingleMarkers(corners,marker_size)
    
    for marker in range(len(ids)):
        aruco.drawAxis(frame, rvec[marker],tvec[marker],100)
        cv2.putText(frame,str(ids([marker][0]),(int(corners[marker][0][0][0]) -  30,int(corners([marker][0][0][1])),cv2.FONT_HERSHEY_PLAIN, 3, (255,0,0),2,cv2.LINE_AA)))

cv2.imshow('frame',frame)
cv2.waitKey(0)
cap.release()
cv2.destroyAllWindows()

