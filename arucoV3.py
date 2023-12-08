import cv2 as cv
from cv2 import aruco
import numpy as np
from picamera2 import Picamera2



marker_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
param_markers = aruco.DetectorParameters()
#param_markers = aruco.DetectorParameters_create()


matrix2kcam = np.array([[878.95170188, 0, 993.89589179],
                        [0           ,876.72068118, 775.53981922],
                        [0           ,0           ,1           ]])
coeff2kcam = np.array([[-0.29467958 , 0.08874286 , 0.00187015, -0.00062744, -0.01134761]])
camera_matrix = matrix2kcam
dist_coeffs = coeff2kcam

cap = cv.VideoCapture(0)



picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888',"size":(maxh,maxl)}))
picam2.start()

while True:
    #ret, frame = cap.read()
    frame = picam2.capture_array()
    #if not ret:
    #    break
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

#cap.release()
picam2.stop()
cv.destroyAllWindows()
