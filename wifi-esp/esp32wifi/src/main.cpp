#include <WiFi.h>
#include <WiFiClient.h>

const char* ssid = "Freebox-49A6CF"; // Remplacez par le nom de votre réseau Wi-Fi
const char* password = "italici2.-ejurat-adsertivum7-clematidas!"; // Remplacez par le mot de passe de votre réseau Wi-Fi
const int port = 8888; // Port pour la communication

WiFiServer server(port);

void setup() {
  Serial.begin(115200);
  delay(1000);

  // Connexion au réseau Wi-Fi
  Serial.println();
  Serial.print("Connexion à ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connecté");
  Serial.println("Adresse IP: " + WiFi.localIP().toString());

  // Démarrez le serveur
  server.begin();
}

void loop() {
  WiFiClient client = server.available();

  if (client) {
    Serial.println("Nouvelle connexion");

    while (client.connected()) {
      if (client.available()) {
        String command = client.readStringUntil('\n');
        Serial.print("Commande reçue: ");
        Serial.println(command);

        // Traitez la commande ici
        // Par exemple, vous pouvez renvoyer une réponse au client
        client.println("Commande reçue avec succès!");
      }
    }

    client.stop();
    Serial.println("Client déconnecté");
  }
}
