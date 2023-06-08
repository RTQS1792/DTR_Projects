/*
 * IRremoteESP8266: IRrecvDemo - demonstrates receiving IR codes with IRrecv
 * This is very simple teaching code to show you how to use the library.
 * If you are trying to decode your Infra-Red remote(s) for later replay,
 * use the IRrecvDumpV2.ino (or later) example code instead of this.
 * An IR detector/demodulator must be connected to the input kRecvPin.
 * Copyright 2009 Ken Shirriff, http://arcfn.com
 * Example circuit diagram:
 *  https://github.com/crankyoldgit/IRremoteESP8266/wiki#ir-receiving
 * Changes:
 *   Version 0.2 June, 2017
 *     Changed GPIO pin to the same as other examples.
 *     Used our own method for printing a uint64_t.
 *     Changed the baud rate to 115200.
 *   Version 0.1 Sept, 2015
 *     Based on Ken Shirriff's IrsendDemo Version 0.1 July, 2009
 */

#include <Arduino.h>
#include <IRremoteESP8266.h>
#include <IRrecv.h>
#include <IRutils.h>

// An IR detector/demodulator is connected to GPIO pin 14(D5 on a NodeMCU
// board).
// Note: GPIO 16 won't work on the ESP8266 as it does not have interrupts.
const uint16_t kRecvPin = 14;
const uint16_t kRecvPin2 = 15;
int total = 0;
int success = 0;
int Flag1 = 0;
int Flag2 = 0;

IRrecv irrecv(kRecvPin);
IRrecv irrecv2(kRecvPin2);

decode_results results;

void setup() {
  Serial.begin(115200);
  irrecv.enableIRIn();  // Start the receiver
  irrecv2.enableIRIn();  // Start the receiver
  while (!Serial)  // Wait for the serial connection to be establised.
    delay(50);
  Serial.println();
  Serial.print("IRrecvDemo is now running and waiting for IR message on Pin ");
  Serial.println(kRecvPin);
}

void loop() {
  if (irrecv.decode(&results)) {
    Total++;
    // print() & println() can't handle printing long longs. (uint64_t)
    Serial.print("1 ");
    serialPrintUint64(results.value, HEX);
    Serial.println("");
    if(results.value == 0x807F08F7 || results.value == 0x97CB7FD4 ||results.value == 0xE4F2D735){
      Serial.println("Traget");

    }
    irrecv.resume();  // Receive the next value
  }
  
  if (irrecv2.decode(&results)) {
    // print() & println() can't handle printing long longs. (uint64_t)
    Serial.print("2 ");
    serialPrintUint64(results.value, HEX);
    Serial.println("");
    if(results.value == 0x807F08F7){
      Serial.println("Traget");
    }
    irrecv2.resume();  // Receive the next value
  }
  
  delay(100);
}
