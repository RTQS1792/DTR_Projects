/*
 * @Author       : Hanqing Qi
 * @Date         : 2023-07-18 16:35:57
 * @LastEditors  : Hanqing Qi
 * @LastEditTime : 2023-07-21 14:45:04
 * @FilePath     : /ESP_NOW/Receiver/Receiver.ino
 * @Description  : This is the receiver of ESP-NOW
 */

#include <esp_now.h>
#include <WiFi.h>
#include <ESP32Servo.h>

#define SERVO_L D9
#define SERVO_R D10

Servo servo1;
Servo servo2;

//Structure example to receive data
//Must match the sender structure
typedef struct test_struct {
  int x;
  int y;
} test_struct;

//Create a struct_message called myData
test_struct myData;

//callback function that will be executed when data is received
void OnDataRecv(const uint8_t * mac, const uint8_t *incomingData, int len) {
  memcpy(&myData, incomingData, sizeof(myData));
  esp_now_recv_status_t status = ESP_NOW.getStatus();
  Serial.print("Received packet with RSSI: ");
  Serial.println(status.rssi);
  Serial.print("Bytes received: ");
  Serial.println(len);
  Serial.print("x: ");
  Serial.println(myData.x);
  Serial.print("y: ");
  Serial.println(myData.y);
  Serial.println();
  
  servo1.write(myData.x);
  servo2.write(myData.x);
}
 
void setup() {
  //Initialize Serial Monitor
  Serial.begin(115200);

  //Initialize Servo
  ESP32PWM::allocateTimer(0);
	ESP32PWM::allocateTimer(1);
	ESP32PWM::allocateTimer(2);
	ESP32PWM::allocateTimer(3);
  servo1.setPeriodHertz(50);// Standard 50hz servo
  servo2.setPeriodHertz(50);// Standard 50hz servo
  servo1.attach(SERVO_L, 600, 2400);
  servo2.attach(SERVO_R, 600, 2400);
  
  //Set device as a Wi-Fi Station
  WiFi.mode(WIFI_STA);

  //Init ESP-NOW
  if (esp_now_init() != ESP_OK) {
    Serial.println("Error initializing ESP-NOW");
    return;
  }
  
  // Once ESPNow is successfully Init, we will register for recv CB to
  // get recv packer info
  esp_now_register_recv_cb(OnDataRecv);
}
 
void loop() {

}
