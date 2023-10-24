import cv2
import cv2.aruco
import time 

vid = cv2.VideoCapture(1)

    #vid.set(3,2028)
    #vid.set(4,1080)
#vid.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
#vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 1520)


while(True):

    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
    ret, frame = vid.read()
    small_frame = cv2.resize(frame, (600, 400)) 
    
    
    #cv2.imshow('frame',small_frame)
    cv2.imshow('frame',frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
vid.release()
cv2.destroyAllWindows()

