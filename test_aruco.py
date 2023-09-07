import numpy as np
import cv2 as cv
import sys


tag = np.zeros((300, 300, 1), dtype="uint8")
cv.aruco.drawMarker(cv.aruco.Dictionary_get(cv.aruco.DICT_4X4_50), 1, 300, tag)
# write the generated ArUCo tag to disk and then display it 
cv.imwrite("tags/DICT_5X5_100_id24.png" , tag)
cv.imshow("Aruco Tag", tag)
cv.waitKey(0)