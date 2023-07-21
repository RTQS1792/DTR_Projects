#define LED_BLUE Dy 
#define LED_RED Dx
#define SERVO_L D2
#define SERVO_R D3
#define THRUST_L D0
#define THRUST_R D1


#include <ESP32Servo.h>

Servo servo1;
Servo servo2;
Servo thrust1;
Servo thrust2;

void setup() {
  // pinMode(LED_BLUE, OUTPUT); // Initialize the LED_BUILTIN pin as an output
  // pinMode(LED_RED, OUTPUT); // Initialize the LED_BUILTIN pin as an output
  ESP32PWM::allocateTimer(0);
	ESP32PWM::allocateTimer(1);
	ESP32PWM::allocateTimer(2);
	ESP32PWM::allocateTimer(3);
  servo1.setPeriodHertz(50);// Standard 50hz servo
  servo2.setPeriodHertz(50);// Standard 50hz servo

  thrust1.setPeriodHertz(51);// Standard 50hz servo
  thrust2.setPeriodHertz(51);// Standard 50hz servo

  servo1.attach(SERVO_L, 600, 2400);
  servo2.attach(SERVO_R, 600, 2400);

  thrust1.attach(THRUST_L, 1000, 2000);
  thrust2.attach(THRUST_R, 1000, 2000);

  // ESC arm
  escarm();

}

// The loop function runs over and over again forever
void loop() {
  // digitalWrite(LED_BLUE, HIGH);
  // digitalWrite(LED_RED, LOW);
  for (int posVal = 1100; posVal <= 2000; posVal += 1) {
    thrust1.writeMicroseconds(posVal);
    thrust2.writeMicroseconds(posVal);
    delay(5);
  }

  for (int posVal = 2000; posVal >= 1100; posVal -= 1) {
    thrust1.writeMicroseconds(posVal);
    thrust2.writeMicroseconds(posVal);
    delay(5);
  }
  
  delay(1000);
  // digitalWrite(LED_BLUE, LOW);
  // digitalWrite(LED_RED, HIGH);
  // delay(1000);
  
  for (int posVal = 0; posVal <= 180; posVal++) {
    servo1.write(posVal);
    servo2.write(posVal);
    delay(5);
  }
  for (int posVal = 180; posVal >=0 ; posVal--) {
    servo1.write(posVal);
    servo2.write(posVal);
    delay(5);
  }
  servo1.write(90);
  servo2.write(90);
  while(1);
  //servo1.write(180);
  //servo2.write(180);
}


//Enter arming sequence for ESC
void escarm(){
  // ESC arming sequence for BLHeli S
  thrust1.writeMicroseconds(1000);
  delay(10);
  thrust2.writeMicroseconds(1000);
  delay(10);

  // Sweep up
  for(int i=1100; i<1500; i++) {
    thrust1.writeMicroseconds(i);
    delay(5);
    thrust2.writeMicroseconds(i);
    delay(5);
  }
  // Sweep down
  for(int i=1500; i<1100; i--) {
    thrust1.writeMicroseconds(i);
    delay(5);
    thrust2.writeMicroseconds(i);
    delay(5);
  }
  // Back to minimum value
  thrust1.writeMicroseconds(1100);
  delay(200);
  thrust2.writeMicroseconds(1100);
  delay(200);

}
