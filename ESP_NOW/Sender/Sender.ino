/*
 * @Author       : Hanqing Qi
 * @Date         : 2023-07-18 16:29:47
 * @LastEditors  : Hanqing Qi
 * @LastEditTime : 2023-07-21 14:24:36
 * @FilePath     : /ESP_NOW/Sender/Sender.ino
 * @Description  : This is the sender of ESP-NOW.
 */

#include <esp_now.h>
#include <WiFi.h>

// Mac address of the receivers
uint8_t broadcastAddress1[] = {0x34, 0x85, 0x18, 0x91, 0x49, 0xC0};

// Add more receivers here
// uint8_t broadcastAddress2[] = {0xFF, , , , , }; 
// uint8_t broadcastAddress3[] = {0xFF, , , , , };

// Structure example to send data
// NOTE - The structure of the data must match the receiver structure
typedef struct test_struct {
  int x;
  int y;
} test_struct;

test_struct test;

esp_now_peer_info_t peerInfo;

/**
 * @description: Callback when data is sent
 * @param       {uint8_t} *mac_addr: Mac address of the receiver
 * @param       {esp_now_send_status_t} status: Status of the sent message
 * @return      {void} -
 */
void OnDataSent(const uint8_t *mac_addr, esp_now_send_status_t status) {
  char macStr[18];
  Serial.print("Packet to: ");
  // Copies the sender mac address to a string
  snprintf(macStr, sizeof(macStr), "%02x:%02x:%02x:%02x:%02x:%02x",
           mac_addr[0], mac_addr[1], mac_addr[2], mac_addr[3], mac_addr[4], mac_addr[5]);
  Serial.print(macStr);
  Serial.print(" send status:\t");
  Serial.println(status == ESP_NOW_SEND_SUCCESS ? "Delivery Success" : "Delivery Fail");
}
 
void setup() {
  // Set up
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);
 
  if (esp_now_init() != ESP_OK) {
    Serial.println("Error initializing ESP-NOW");
    return;
  }
  
  esp_now_register_send_cb(OnDataSent);
   
  // Register peer
  peerInfo.channel = 0;  
  peerInfo.encrypt = false;
  // Register first peer  
  memcpy(peerInfo.peer_addr, broadcastAddress1, 6);
  if (esp_now_add_peer(&peerInfo) != ESP_OK){
    Serial.println("Failed to add peer");
    return;
  }
  // Register second peer  
  // memcpy(peerInfo.peer_addr, broadcastAddress2, 6);
  // if (esp_now_add_peer(&peerInfo) != ESP_OK){
  //   Serial.println("Failed to add peer");
  //   return;
  // }
  // Register third peer
  // memcpy(peerInfo.peer_addr, broadcastAddress3, 6);
  // if (esp_now_add_peer(&peerInfo) != ESP_OK){
  //   Serial.println("Failed to add peer");
  //   return;
  // }
}
 
void loop() {
  String incoming = ""; // String to hold incoming message from PC
  
  while (Serial.available()) {
    // delay(10); // Delay to make sure all data is received
    char c = Serial.read();
    incoming += c;
  }
  
  if (incoming.length() > 0) {
    int number = incoming.toInt();
    Serial.println(number);
    test.x = incoming.toInt();
    test.y = incoming.toInt()+5;
  }
 
  esp_err_t result = esp_now_send(0, (uint8_t *) &test, sizeof(test_struct));
   
  if (result == ESP_OK) {
    Serial.println("Sent with success");
  }
  else {
    Serial.println("Error sending the data");
  }
  delay(50); 
  // NOTE - The delay time here need to match the time.sleep() of the serial sender on PC. Or multiple data will be sent in one packet.
}
