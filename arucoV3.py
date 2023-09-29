import cv2 as cv
from cv2 import aruco
import numpy as np
import socket

HOST = "192.168.1.93"
PORT = 8888

connected = False

while not connected:
    try:
        # Créez une socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Connectez-vous à l'ESP32
            s.connect((HOST, PORT))
            connected = True
    except ConnectionRefusedError:
        print("En attente de la connexion à l'ESP32...")
        time.sleep(1)  # Attendre 1 seconde avant de réessayer

print("Connecté à l'ESP32. Le programme peut commencer.")

marker_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
param_markers = aruco.DetectorParameters()

# Supposons que vous ayez calibré votre caméra et obtenu les matrices de calibration suivantes
#cameraMatrix = np.array([[fx, 0, cx],
                       #  [0, fy, cy],
                       #  [0, 0, 1]], dtype=np.float32)  # Remplacez fx, fy, cx, cy par les valeurs de votre calibration
#distCoeffs = np.array([k1, k2, p1, p2, k3], dtype=np.float32)  # Remplacez par les valeurs de votre calibration

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
            rvecs, tvecs, _ = aruco.estimatePoseSingleMarkers(corners, 0.1, cameraMatrix, distCoeffs)

            if rvecs is not None and tvecs is not None:
                rvec = rvecs[0]  # Prenez le premier marqueur
                tvec = tvecs[0]

                # Convertissez les coordonnées du marqueur en position 3D
                marker_position_camera = -np.dot(np.linalg.inv(rvec), tvec)

                # Envoyez les coordonnées de la position à l'ESP32
                position_message = f"Position (x, y, z): ({marker_position_camera[0]}, {marker_position_camera[1]}, {marker_position_camera[2]})"
                s.sendall(position_message.encode('utf-8'))

    cv.imshow("frame", frame)
    stop = cv.waitKey(1)
    if stop == ord("s"):
        break

cap.release()
cv.destroyAllWindows()
