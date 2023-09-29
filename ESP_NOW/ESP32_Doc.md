# ESP32 Wrover Python Document

## ESP32_NOW

- [ESP32 Official Link](https://docs.espressif.com/projects/esp-idf/zh_CN/release-v5.0/esp32/get-started/linux-macos-setup.html#get-started-linux-macos-first-steps)
- [ESP-IDF Tutorial with VSCode](https://github.com/espressif/vscode-esp-idf-extension/blob/master/docs/tutorial/install.md)

### Tutorial 1

1. Getting Mac Address

   ```c
   // Complete Instructions to Get and Change ESP MAC Address: https://RandomNerdTutorials.com/get-change-esp32-esp8266-mac-address-arduino/
   
   #ifdef ESP32
     #include <WiFi.h>
   #else
     #include <ESP8266WiFi.h>
   #endif
   
   void setup(){
     Serial.begin(115200);
     Serial.println();
     Serial.print("ESP Board MAC Address:  ");
     Serial.println(WiFi.macAddress());
   }
    
   void loop(){
   
   }
   ```

   Output: 

   ```
   Old ESP Board MAC Address:  B4:8A:0A:61:20:0C
   New ESP Board MAC Address:  C0:49:EF:FB:FD:14
   ```

2. Sender Code

   ```c
   #include <esp_now.h>
   #include <WiFi.h>
   
   // REPLACE WITH YOUR ESP RECEIVER'S MAC ADDRESS
   uint8_t broadcastAddress1[] = {0xC0, 0x49, 0xEF, 0xFB, 0xFD, 0x14};
   // uint8_t broadcastAddress2[] = {0xFF, , , , , };
   // uint8_t broadcastAddress3[] = {0xFF, , , , , };
   
   typedef struct test_struct {
     int x;
     int y;
   } test_struct;
   
   test_struct test;
   
   esp_now_peer_info_t peerInfo;
   
   // callback when data is sent
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
     Serial.begin(115200);
    
     WiFi.mode(WIFI_STA);
    
     if (esp_now_init() != ESP_OK) {
       Serial.println("Error initializing ESP-NOW");
       return;
     }
     
     esp_now_register_send_cb(OnDataSent);
      
     // register peer
     peerInfo.channel = 0;  
     peerInfo.encrypt = false;
     // register first peer  
     memcpy(peerInfo.peer_addr, broadcastAddress1, 6);
     if (esp_now_add_peer(&peerInfo) != ESP_OK){
       Serial.println("Failed to add peer");
       return;
     }
   }
    
   void loop() {
     test.x = random(0,20);
     test.y = random(0,20);
    
     esp_err_t result = esp_now_send(0, (uint8_t *) &test, sizeof(test_struct));
      
     if (result == ESP_OK) {
       Serial.println("Sent with success");
     }
     else {
       Serial.println("Error sending the data");
     }
     delay(2000);
   }
   ```

   **IMPORTANT**: In arduino, go to tools and make sure the upload speed is 115200, or the flush will fail!

3. Reciever Code

   ```c
   #include <esp_now.h>
   #include <WiFi.h>
   
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
     Serial.print("Bytes received: ");
     Serial.println(len);
     Serial.print("x: ");
     Serial.println(myData.x);
     Serial.print("y: ");
     Serial.println(myData.y);
     Serial.println();
   }
    
   void setup() {
     //Initialize Serial Monitor
     Serial.begin(115200);
     
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
   ```

## ESP_IDF Commands

- Set up the environment

  ```shell
  alias get_idf='. $HOME/esp/esp-idf/export.sh'
  ```

- Check ports information

  ```shell
  ls /dev/cu.*
  # Sample output
  /dev/cu.Bluetooth-Incoming-Port			/dev/cu.usbserial-2120
  /dev/cu.Ditoo-Plus-audio						/dev/cu.wchusbserial2120
  /dev/cu.HanqingsPowerbeatsPro
  ```

- Configure a project

  ```shell
  cd ~/esp/hello_world				# Make sure you are in the working directory
  idf.py set-target esp32 		# Set target device
  idf.py menuconfig 					# Open config menu
  ```

- Building

  ```shell
  idf.py build
  ```

- Burn to device

  ```shell
  idf.py -p /dev/cu.wchusbserial2120 -b BAUD flash # BAUD is suggeted to be 460800
  ```
