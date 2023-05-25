/*
Author: Hanqing Qi
Date: 05/25/2023 
Description: This is the client on the ESP32 that sends data to the server
*/

#include <WiFi.h>

const char* ssid = "AIRLab-BigLab"; // Wifi name
const char* password = "Airlabrocks2022"; // Wifi Password

const char* host = "192.168.0.41";  // Host IP
const int httpPort = 80;            // Port

WiFiClient client;

void setup() {
  Serial.begin(115200);
  while (!Serial) { delay(100); }
  // Connect to wifi network
  Serial.println();
  Serial.println("******************************************************");
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

/*
This function is used to read the reponds from the server.
We do not need this for now.
*/
/*
  void readResponse(WiFiClient* client) {
    unsigned long timeout = millis();
    while (client->available() == 0) {
      if (millis() - timeout > 5000) {
        Serial.println(">>> Client Timeout !");
        client->stop();
        return;
      }
    }


    // Read all the lines of the reply from server and print them to Serial
    while (client->available()) {
      String line = client->readStringUntil('\r');
      Serial.print(line);
    }

    Serial.printf("\nClosing connection\n\n");
  }
*/

/*
Description: This function executes when setup is finished and keeps sending message
*/
void loop() {
  // Keeps searching for connecting
  if (!client.connect(host, httpPort)) {
    Serial.printf("\n No connection");
    delay(1000);
    return;
  }
  Serial.printf("\n alive");
  String readRequest = "Hi";
  client.write(255);
  client.write(125);
  client.flush();
  delay(1000);
}