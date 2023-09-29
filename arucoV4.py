import cv2
import numpy as np


camera_matrix = np.array([[275.48494487, 0, 307.36023929],
                         [0, 274.19034322, 248.29371074],
                         [0, 0, 1]])  
dist_coeffs = np.array([-0.32576806, 0.13293918, 0.00102543, -0.00083957, -0.02834439])



# Créez un objet de capture vidéo en utilisant la caméra par défaut (0 pour la première caméra).
cap = cv2.VideoCapture(0)
# Assurez-vous que la caméra est ouverte avec succès.
if not cap.isOpened():
    print("Erreur: Impossible d'ouvrir la caméra.")
    exit()

# Créez un détecteur ArUco.
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)

# Définissez les paramètres du détecteur ArUco.
parameters = cv2.aruco.DetectorParameters_create()

while True:
    # Capturez une image depuis la caméra.
    ret, frame = cap.read()

    if not ret:
        print("Erreur: Impossible de lire l'image depuis la caméra.")
        break

    # Appliquez la correction de distorsion à l'image.
    corrected_frame = cv2.undistort(frame, camera_matrix, dist_coeffs)

    # Convertissez l'image corrigée en niveaux de gris (pour la détection ArUco).
    gray = cv2.cvtColor(corrected_frame, cv2.COLOR_BGR2GRAY)

    # Détectez les marqueurs ArUco.
    corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

    if ids is not None:
        # Dessinez les marqueurs détectés sur l'image en direct.
        cv2.aruco.drawDetectedMarkers(corrected_frame, corners, ids)

        # Affichez les identifiants des marqueurs et leurs positions.
        for i in range(len(ids)):
            print(f"Marqueur ID {ids[i]} trouvé à la position : {corners[i][0]}")

    # Affichez l'image en direct avec les marqueurs détectés.
    cv2.imshow('Detection ArUco', corrected_frame)

    # Quittez la boucle si la touche 'q' est enfoncée.
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libérez les ressources et fermez la fenêtre vidéo.
cap.release()
cv2.destroyAllWindows()
