/*
 * @Author       : Hanqing Qi
 * @Date         : 2023-07-18 16:35:57
 * @LastEditors  : Hanqing Qi
 * @LastEditTime : 2023-07-28 14:37:54
 * @FilePath     : /ESP_NOW/Receiver/Receiver.ino
 * @Description  : This is the receiver of ESP-NOW
 */

#include <esp_now.h>
#include <WiFi.h>
#include <ESP32Servo.h>

// #define SERVO_L D9
// #define SERVO_R D10

// Servo servo1;
// Servo servo2;

// Structure example to receive data
// Must match the sender structure
typedef struct Control_Input
{
  float p1;
  float p2;
  float p3;
  float p4;
  float p5;
  float p6;
  float p7;
  float p8;
  float p9;
  float p10;
  float p11;
  float p12;
  float p13;
} Control_Input;

// Create a struct_message called myData
Control_Input myData;

// callback function that will be executed when data is received
void OnDataRecv(const uint8_t *mac, const uint8_t *incomingData, int len)
{
  memcpy(&myData, incomingData, sizeof(myData));
  Serial.print("Bytes received: ");
  Serial.println(len);
  Serial.print("Data: ");
  Serial.print(myData.p1);
  Serial.print("|");
  Serial.print(myData.p2);
  Serial.print("|");
  Serial.print(myData.p3);
  Serial.print("|");
  Serial.print(myData.p4);
  Serial.print("|");
  Serial.print(myData.p5);
  Serial.print("|");
  Serial.print(myData.p6);
  Serial.print("|");
  Serial.print(myData.p7);
  Serial.print("|");
  Serial.print(myData.p8);
  Serial.print("|");
  Serial.print(myData.p9);
  Serial.print("|");
  Serial.print(myData.p10);
  Serial.print("|");
  Serial.print(myData.p11);
  Serial.print("|");
  Serial.print(myData.p12);
  Serial.print("|");
  Serial.print(myData.p13);
  Serial.println();

  // servo1.write(myData.x);
  // servo2.write(myData.x);
}

void setup()
{
  // Initialize Serial Monitor
  Serial.begin(115200);

  // Initialize Servo
  //  ESP32PWM::allocateTimer(0);
  //  ESP32PWM::allocateTimer(1);
  //  ESP32PWM::allocateTimer(2);
  //  ESP32PWM::allocateTimer(3);
  //  servo1.setPeriodHertz(50);// Standard 50hz servo
  //  servo2.setPeriodHertz(50);// Standard 50hz servo
  //  servo1.attach(SERVO_L, 600, 2400);
  //  servo2.attach(SERVO_R, 600, 2400);

  // Set device as a Wi-Fi Station
  WiFi.mode(WIFI_STA);

  // Init ESP-NOW
  if (esp_now_init() != ESP_OK)
  {
    Serial.println("Error initializing ESP-NOW");
    return;
  }

  // Once ESPNow is successfully Init, we will register for recv CB to
  // get recv packer info
  esp_now_register_recv_cb(OnDataRecv);
}

void loop()
{
}
