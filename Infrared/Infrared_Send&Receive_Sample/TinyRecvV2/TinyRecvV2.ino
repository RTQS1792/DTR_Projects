#include <Arduino.h>
#include <IRremoteESP8266.h>
#include <IRrecv.h>
#include <IRutils.h>

const uint16_t Left_Eye = 14;
const uint16_t Right_Eye = 15;
IRrecv Lirrecv(Left_Eye, kRawBuf, kTimeoutMs, true);
IRrecv Rirrecv(Right_Eye, kRawBuf, kTimeoutMs, true);
decode_results Left_Vision;
decode_results Right_Vision;

void setup() {
  Serial.begin(115200);
  while (!Serial)
    delay(50);
  // Initialize the serial port and set the baud rate to 115200 // Start the receiver // Wait for the serial connection to be established.
}

void loop() {
  Lirrecv..enableIRIn();
  //Serial.println("L online");
  delay(100);
  if (Lirrecv.decode(&Left_Vision)) {            // Waiting for decoding
    Serial.print("Left eye: ");
    serialPrintUint64(Left_Vision.value, HEX);  // Print out the decoded results
    Serial.println("");
    if (Left_Vision.value == 0x807F08F7)
      Serial.println("Left eye on target");
    Serial.println("");
    Lirrecv.resume();  // Release the IRremote. Receive the next value
    
  }else{
    // Serial.println("Left eye blind");
  }
  Lirrecv.pause();
  Lirrecv.disableIRIn();
  Rirrecv.enableIRIn();
  //Serial.println("R online");
  delay(100);
  if (Rirrecv.decode(&Right_Vision)) {            // Waiting for decoding
    Serial.print("Right eye: ");
    serialPrintUint64(Right_Vision.value, HEX);  // Print out the decoded results
    Serial.println("");
    if (Right_Vision.value == 0x807F08F7)
      Serial.println("Right eye on target");
    Serial.println("");
    Rirrecv.resume();  // Release the IRremote. Receive the next value
    
  }else{
    // Serial.println("Right eye blind");
  }
  Rirrecv.pause();
  Rirrecv.disableIRIn();
  delay(500);
}