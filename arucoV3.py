import cv2 as cv
from cv2 import aruco
import numpy as np



marker_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
#param_markers = aruco.DetectorParameters()
param_markers = aruco.DetectorParameters_create()

camera_matrix = np.array([[275.48494487, 0, 307.36023929],
                         [0, 274.19034322, 248.29371074],
                         [0, 0, 1]])  
dist_coeffs = np.array([-0.32576806, 0.13293918, 0.00102543, -0.00083957, -0.02834439])

cap = cv.VideoCapture(1)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    marker_corners, marker_IDs, reject = aruco.detectMarkers(gray_frame, marker_dict, parameters=param_markers)
    if marker_corners:
        for ids, corners in zip(marker_IDs, marker_corners):
            cv.polylines(frame, [corners.astype(np.int32)], True, (0, 255, 255), 4, cv.LINE_AA)
            corners = corners.reshape(4, 2)
            corners = corners.astype(int)
            top_right = corners[0].ravel()

            font = cv.FONT_HERSHEY_PLAIN
            cv.putText(frame, f"id: {ids[0]}", tuple(top_right), font, 1, (0, 255, 0), 2, cv.LINE_AA)

            # Estimez la pose du marqueur
            rvecs, tvecs, _ = aruco.estimatePoseSingleMarkers(corners, 0.1, camera_matrix, dist_coeffs)

            if rvecs is not None and tvecs is not None:
                rvec = rvecs[0]  # Prenez le premier marqueur
                tvec = tvecs[0]

                # Convertissez les coordonnées du marqueur en position 3D
                marker_position_camera = -np.dot(np.linalg.inv(rvec), tvec)

                # Envoyez les coordonnées de la position à l'ESP32
                position_message = f"Position (x, y, z): ({marker_position_camera[0]}, {marker_position_camera[1]}, {marker_position_camera[2]})"
                print(position_message)

    cv.imshow("frame", frame)
    stop = cv.waitKey(1)
    if stop == ord("s"):
        break

cap.release()
cv.destroyAllWindows()
