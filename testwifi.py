import socket
import time 

# Paramètres du serveur
HOST = "192.168.1.25"
PORT = 8888

# Créez une socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Connectez-vous à l'ESP32
    s.connect((HOST, PORT))



    while True:
        # Envoyez des données à l'ESP32
        message = input("Envoyer à l'ESP32 : ")
        s.sendall(message.encode('utf-8'))

        # Recevez des données de l'ESP32
        data = s.recv(1024).decode('utf-8')
        print(f"Reçu de l'ESP32 : {data}")

