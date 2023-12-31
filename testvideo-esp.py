import socket
import time
import cv2
import cv2.aruco

vid = cv2.VideoCapture(1)


HOST = "192.168.1.93"  # Adresse IP de l'ESP32
PORT = 8888  # Port utilisé pour la communication

connected = False  # Indicateur de connexion

# Fonction pour vérifier la connexion
def check_connection():
    global connected
    try:
        # Créez une socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            connected = True
    except ConnectionRefusedError:
        connected = False

# Attendez jusqu'à ce que la connexion soit établie
while not connected:
    print("En attente de la connexion à l'ESP32...")
    check_connection()
    time.sleep(1)  # Attendez 1 seconde avant de réessayer



while(connected == True):
    print("Connecté à l'ESP32. Le programme peut commencer.")
    ret, frame = vid.read()
    
    cv2.imshow('frame',frame)

    check_connection()
    if connected == False:
        print('connection perdue avec l\'ESP32')
        vid.release()
        cv2.destroyAllWindows()

    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break










