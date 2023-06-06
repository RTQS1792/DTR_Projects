#include "irrecvdata.h"

irGetCMD ir_receiver(15); // Creating instance of irGetCMD class. 2 is the GPIO number connected to the IR receiver.

void setup() {
    Serial.begin(115200); // Initialize serial communication at 115200 baud rate.
}

void loop() {
    String irValue = ir_receiver.my_irread(); // Read the IR signal.
    
    if (!irValue.isEmpty()) { // If a signal was received...
        Serial.println("Received: " + irValue); // Print the received value to the serial monitor.
    }else{
        Serial.println("No Signal");
    }
    
    delay(100); // Short delay before the next loop iteration.
}