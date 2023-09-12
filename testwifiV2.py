import socket
import time

HOST = "192.168.1.25"  # Adresse IP de l'ESP32
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

print("Connecté à l'ESP32. Vous pouvez maintenant exécuter votre code.")



with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        message = input("Envoyer à l'ESP32 : ")
        s.sendall(message.encode('utf-8'))
