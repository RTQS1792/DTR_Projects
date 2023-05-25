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
 
//#define DECODE_DENON        // Includes Sharp
//#define DECODE_JVC
//#define DECODE_KASEIKYO
//#define DECODE_PANASONIC    // alias for DECODE_KASEIKYO
//#define DECODE_LG
#define DECODE_NEC  // Includes Apple and Onkyo
//#define DECODE_SAMSUNG
//#define DECODE_SONY
//#define DECODE_RC5
//#define DECODE_RC6

//#define DECODE_BOSEWAVE
//#define DECODE_LEGO_PF
//#define DECODE_MAGIQUEST
//#define DECODE_WHYNTER
//#define DECODE_FAST

//#define DECODE_DISTANCE_WIDTH // Universal decoder for pulse distance width protocols
//#define DECODE_HASH         // special decoder for all protocols

//#define DECODE_BEO          // This protocol must always be enabled manually, i.e. it is NOT enabled if no protocol is defined. It prevents decoding of SONY!

//#define DEBUG               // Activate this for lots of lovely debug output from the decoders.

//#define RAW_BUFFER_LENGTH  180  // Default is 112 if DECODE_MAGIQUEST is enabled, otherwise 100.

#include <Arduino.h>
#include "PinDefinitionsAndMore.h"  // Define macros for input and output pin etc.
#include <IRremote.hpp>

// WIFI ----------------------------------------------------
#include <WiFi.h>
const char* ssid = "AIRLab-BigLab"; // Wifi name
const char* password = "Airlabrocks2022"; // Wifi Password
const char* host = "192.168.0.41";  // Host IP
const int httpPort = 80;            // Port
WiFiClient client;
// END WIFI ------------------------------------------------

void setup() {
  Serial.begin(115200);
  // SET UP THE RECEIVER ----------------------------------------------------
  // Just to know which program is running on my Arduino
  Serial.println(F("START " __FILE__ " from " __DATE__ "\r\nUsing library version " VERSION_IRREMOTE));

  // For ESP32 the IR_Reveiver pin is defined in the PinDefinitionsAndMore.h to be 15
  IrReceiver.begin(IR_RECEIVE_PIN, ENABLE_LED_FEEDBACK);

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
  /*
     * Check if received data is available and if yes, try to decode it.
     * Decoded result is in the IrReceiver.decodedIRData structure.
     *
     * E.g. command is in IrReceiver.decodedIRData.command
     * address is in command is in IrReceiver.decodedIRData.address
     * and up to 32 bit raw data in IrReceiver.decodedIRData.decodedRawData
     */
  if (IrReceiver.decode()) {
    /*
    * Print a short summary of received data
    */
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
    // Keeps searching for connecting
        if (!client.connect(host, httpPort)) {
          Serial.printf("\n No connection");
          delay(500);
          return;
        }
        Serial.printf("\n Connected");
    if (IrReceiver.decodedIRData.command == 0x10 && IrReceiver.decodedIRData.address == 0x01) {
        client.write("1");
        client.flush();
        delay(100);
    } else{
      Serial.printf("\n Noise");
      client.write("0");
      client.flush();
      delay(100);
    }
  }
}
