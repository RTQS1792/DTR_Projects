/*
 * File: Final_Sender.cpp
 * Author: Hanqing Qi
 * Date Modified: 06/01/2023
 * Description: This file is used to send the signal to the receiver.
 * NOTE - The signal sent by the sender is not the same as the signal received by the receiver, the signal decomposed by the receiver is not the same as the signal sent by the sender.
 */
#include <Arduino.h>
#include "PinDefinitionsAndMore.h" // Define macros for input and output pin etc.
#include <IRremote.hpp>

/*
 * FUNCTION - Setup Function
 * Define the IR sender object
 */
void setup()
{
    // pinMode(2, OUTPUT);

    Serial.begin(115200);

    // Just to know which program is running on my Arduino
    Serial.println(F("START " __FILE__ " from " __DATE__ "\r\nUsing library version " VERSION_IRREMOTE));
    Serial.print(F("Send IR signals at pin "));
    Serial.println(IR_SEND_PIN);          // On ESP32 the default send PIN is 4
    IrSender.begin(DISABLE_LED_FEEDBACK); // Start with IR_SEND_PIN as send pin and disable feedback LED at default feedback LED pin
}

// Setiup the data to be send
uint8_t sCommand = 0x11; // Command is 0x10
uint8_t sRepeats = 1;    // The signal is send only once

/*
 * FUNCTION - Loop Function
 * Send the signal to the receiver
 */
void loop()
{
    Serial.println();
    Serial.print(F("Send now: address=0x00, command=0x"));
    Serial.print(sCommand, HEX);
    // Serial.print(F(", repeats="));
    // Serial.print(sRepeats);
    Serial.println();

    // Serial.println(F("Send standard NEC with 8 bit address"));
    Serial.flush();

    // Adress is 0x01
    IrSender.sendNEC(0x11, sCommand, sRepeats);
    // NOTE - This delay is related to the receive function. If the delay is too short, the receiver recognizes everything as one long signal or the signal will failed to pass the peak length filter.
    // Delay 300 is much better than 150
    delay(827);
}
