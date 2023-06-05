/*
 * SimpleReceiver.cpp
 * Description: This prgram demonstrates receiving NEC IR codes with IRremote
 * This file is part of Arduino-IRremote https://github.com/Arduino-IRremote/Arduino-IRremote.
 */

/*
 * Specify which protocol(s) should be used for decoding.
 * If no protocol is defined, all protocols (except Bang&Olufsen) are active.
 * This must be done before the #include <IRremote.hpp>
 */


#define DECODE_NEC  // Includes Apple and Onkyo
#include <Arduino.h>
#include "PinDefinitionsAndMore.h"  // Define macros for input and output pin etc.
#include <IRremote.hpp>

// WIFI ----------------------------------------------------
#include <WiFi.h>
const char* ssid = "AIRLab-BigLab";        // Wifi name
const char* password = "Airlabrocks2022";  // Wifi Password
const char* host = "192.168.0.41";         // Host IP
const int httpPort = 8848;                   // Port
WiFiClient client;
// END WIFI ------------------------------------------------

void setup() {
  Serial.begin(115200);
  // SET UP THE RECEIVER ----------------------------------------------------
  // Just to know which program is running on my Arduino
  Serial.println(F("START " __FILE__ " from " __DATE__ "\r\nUsing library version " VERSION_IRREMOTE));

  // For ESP32 the IR_Reveiver pin is defined in the PinDefinitionsAndMore.h to be 15
  IrReceiver.begin(15, ENABLE_LED_FEEDBACK);

  Serial.print(F("Ready to receive IR signals of protocols: "));
  printActiveIRProtocols(&Serial);
  Serial.println(F("at pin " STR(IR_RECEIVE_PIN)));
  // SET UP THE CLIENT ----------------------------------------------------
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

void loop() {
  IrReceiver.setReceivePin(15);
  delay(100);
  if (IrReceiver.decode()) {
    Serial.println("L");
    IrReceiver.printIRResultShort(&Serial);
    IrReceiver.printIRSendUsage(&Serial);
    if (IrReceiver.decodedIRData.protocol == UNKNOWN) {
      Serial.println(F("Received noise or an unknown (or not yet enabled) protocol"));
      // We have an unknown protocol here, print more info
      IrReceiver.printIRResultRawFormatted(&Serial, true);
    }
    Serial.println();

    /*
         * !!!Important!!! Enable receiving of the next value,
         * since receiving has stopped after the end of the current received data packet.
         */
    IrReceiver.resume();  // Enable receiving of the next value

    /*
         * Finally, check the received data and perform actions according to the received command
         */
  } else {
    Serial.println("xL");
  }
  IrReceiver.setReceivePin(13);
  delay(100);
  if (IrReceiver.decode()) {
    Serial.println("R");
    IrReceiver.printIRResultShort(&Serial);
    IrReceiver.printIRSendUsage(&Serial);
    if (IrReceiver.decodedIRData.protocol == UNKNOWN) {
      Serial.println(F("Received noise or an unknown (or not yet enabled) protocol"));
      // We have an unknown protocol here, print more info
      IrReceiver.printIRResultRawFormatted(&Serial, true);
    }
    Serial.println();

    /*
         * !!!Important!!! Enable receiving of the next value,
         * since receiving has stopped after the end of the current received data packet.
         */
    IrReceiver.resume();  // Enable receiving of the next value

    /*
         * Finally, check the received data and perform actions according to the received command
         */
  } else {
    Serial.println("xR");
  }
  delay(1000);
}
