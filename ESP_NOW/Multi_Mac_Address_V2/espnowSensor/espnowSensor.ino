/*
 * @Author       : Hanqing Qi
 * @Date         : 2023-10-26 18:32:19
 * @LastEditors  : Hanqing Qi
 * @LastEditTime : 2023-10-27 14:58:24
 * @FilePath     : /Multi_Mac_Address_V2/espnowSensor/espnowSensor.ino
 * @Description  : 
 */

#include <Arduino.h>
#include <esp_now.h>
#include <WiFi.h>

#define CHANNEL 1 // Choose a channel between 1 and 13

#include "esp_now_data_struct.h"  // Include your data structure definition

uint8_t robotAddress[] = {0x24, 0x0A, 0xC4, 0x81, 0xA8, 0xAC};  // MAC address of the receiver
esp_now_data_struct dataToSend;  // Create a struct to hold the data you will send

void debugLED(uint8_t pin, uint8_t errorType) {
    pinMode(pin, OUTPUT);  // Ensure the pin is set as OUTPUT
    if (errorType == 0) {  // Error during setup
        while (true) {
            digitalWrite(pin, LOW); // NOTE: The led control is reversed, LOW will enable the LED and HIGH will disable it
        }
    } 
    else if (errorType == 1) {  // Error during loop
        for (int i = 0; i < 3; i++) {  // Blink 3 times to indicate error
            digitalWrite(pin, LOW);
            delay(200);  // Faster blink
            digitalWrite(pin, HIGH);
            delay(200);
        }
    }
}

void setup() {
    pinMode(LED_BUILTIN, OUTPUT); // Enable the LED_BUILTIN pin as an debug LED
    Serial.begin(115200);
    WiFi.mode(WIFI_STA);
    if (esp_now_init() != ESP_OK) {
        Serial.println("Error initializing ESP-NOW");
        debugLED(LED_BUILTIN, 0); // Error Initializing ESP-NOW
        return;
    }
    esp_now_peer_info_t peerInfo;
    memcpy(peerInfo.peer_addr, robotAddress, 6);
    peerInfo.channel = CHANNEL;
    peerInfo.encrypt = false;
    if (esp_now_add_peer(&peerInfo) != ESP_OK){
        Serial.println("Failed to add peer");
        debugLED(LED_BUILTIN, 0); // Error Adding Peer
        return;
    }
    esp_now_register_send_cb(onDataSent);
}

void loop() {
    esp_now_data_struct data;
    data.paramCount = 1; // Only need one parameter for wall sensor feedback
    data.params[0] = 99; // TODO: Change this to the actual wall sensor feedback
    data.flag = 3; // Flag for wall sensor feedback
    lastSentData = data;  // Store the data before sending
    esp_now_send(robotAddress, (uint8_t *) &data, sizeof(data));
    delay(2000);  // Send data every 2 seconds
}


void onDataSent(const uint8_t *mac_addr, esp_now_send_status_t status, const uint8_t *data, int len) {
    Serial.print("Sent to: ");
    for (int i = 0; i < 6; i++) {
        Serial.print(mac_addr[i], HEX);
        if (i < 5) Serial.print(":");
    }
    Serial.print(", Status: ");
    Serial.println(status == ESP_NOW_SEND_SUCCESS ? "Success" : "Fail    ");

    printEspnowData(lastSentData);  // Print the data that was sent
}
