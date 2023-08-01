#include <string>

void setup() {
  Serial.begin(115200); // Begin the Serial at 9600 Baud
}

void loop() {
  String incoming = ""; // String to hold incoming message
  
  while (Serial.available()) {
    // delay(10); // Delay to make sure all data is received
    char c = Serial.read();
    incoming += c;
  }
  
  if (incoming.length() > 0) {
    // Serial.println("Received from PC: " + incoming);
    // Echo the message back to PC
    int number = incoming.toInt();
    Serial.println(number);

  }
}