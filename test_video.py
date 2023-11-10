import cv2
import cv2.aruco
import time
from picamera2 import Picamera2 

maxh=2028
maxl=1520
midh=2028
midl=1080
minl=1332
minh=990

picam2 = Picamera2()
picam2.configure(picam.create_preview_configuration(main={"format": 'XRGB8888',"size":(maxh,maxl)}))
picam2.start()

while(True):

    frame= picam2.capture_array()
    
    cv2.imshow('frame',frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cv2.destroyAllWindows()

