/*
 * @Author       : Hanqing Qi
 * @Date         : 2023-10-13 16:19:06
 * @LastEditors  : Hanqing Qi
 * @LastEditTime : 2023-10-13 16:20:48
 * @FilePath     : /Modules/Servo_Test/Servo_Test.ino
 * @Description  : Code to test the servos independently
 */

#define SERVO_L D9
#define SERVO_R D10

#include <ESP32Servo.h>

Servo servo1;
Servo servo2;

void setup()
{
    // pinMode(LED_BLUE, OUTPUT); // Initialize the LED_BUILTIN pin as an output
    // pinMode(LED_RED, OUTPUT); // Initialize the LED_BUILTIN pin as an output
    ESP32PWM::allocateTimer(0);
    ESP32PWM::allocateTimer(1);
    ESP32PWM::allocateTimer(2);
    ESP32PWM::allocateTimer(3);
    servo1.setPeriodHertz(50); // Standard 50hz servo
    servo2.setPeriodHertz(50); // Standard 50hz servo

    servo1.attach(SERVO_L, 500, 2450);
    servo2.attach(SERVO_R, 500, 2450);
}

// The loop function runs over and over again forever
void loop()
{
    servo1.write(90);
    servo2.write(90);
    delay(5000);
    // Sweep servos from 0 to 180 degrees and increase thrust from 1100 to 2000
    for (int posVal = 0; posVal <= 180; posVal++)
    {
        servo1.write(posVal);
        servo2.write(posVal);
        delay(20);
    }

    delay(1000);

    // Sweep servos from 180 to 0 degrees and decrease thrust from 2000 to 1100
    for (int posVal = 180; posVal >= 0; posVal--)
    {
        servo1.write(posVal);
        servo2.write(posVal);
        delay(20);
    }
    delay(1000);
}