import cv2 as cv
from cv2 import aruco
import numpy as np
import socket




#marker_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
marker_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
param_markers = aruco.DetectorParameters_create() # sur la tour
#param_markers = aruco.DetectorParameters() #sur le pc portable

cap = cv.VideoCapture(0)


while True:
    ret,frame = cap.read()
    if not ret:
        break
    gray_frame = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
    marker_corners, marker_IDs,reject = aruco.detectMarkers(gray_frame,marker_dict,parameters=param_markers)
    if marker_corners:
        for ids,corners in zip(marker_IDs,marker_corners):
            cv.polylines(frame, [corners.astype(np.int32)],True, (0,255,255),4,cv.LINE_AA)
            #print (ids)
            corners = corners.reshape(4,2)
            corners = corners.astype(int)
            #top_right = corners[0].ravel()
            (topLeft, topRight, bottomRight, bottomLeft) = corners
            topRight = (int(topRight[0]), int(topRight[1]))
            bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
            topLeft = (int(topLeft[0]), int(topLeft[1]))
            bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))

            # contour du tag 
            cv.line(frame, topLeft, topRight, (0, 255, 0), 2)
            cv.line(frame, topRight, bottomRight, (0, 255, 0), 2)
            cv.line(frame, bottomRight, bottomLeft, (0, 255, 0), 2)
            cv.line(frame, bottomLeft, topLeft, (0, 255, 0), 2)

            cx = int((topLeft[0] + bottomRight[0]) / 2.0)
            cy = int((topLeft[1] + bottomRight[1]) / 2.0)
            cv.circle(frame, (cx, cy), 4, (0, 0, 255), -1)
            
            #affichage de la détection sur l'image
            cv.putText(frame,str(marker_IDs),(topLeft[0],topLeft[1]-15),cv.FONT_HERSHEY_SIMPLEX,0.5,(0,255,0),2)



            
            #font = cv.FONT_HERSHEY_PLAIN
            #print(top_right, 'id = ',ids)
            #cv.putText(frame,f"id: {ids[0]}",tuple(top_right),font,1, (0,255,0),2,cv.LINE_AA)





    cv.imshow("frame",frame)
    stop  = cv.waitKey(1)
    if stop == ord("s"):
        break
cap.release()
cv.destroyAllWindows()
