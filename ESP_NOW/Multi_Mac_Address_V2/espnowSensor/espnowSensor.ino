/*
 * @Author       : Hanqing Qi
 * @Date         : 2023-10-26 18:32:19
 * @LastEditors  : Hanqing Qi
 * @LastEditTime : 2023-10-26 19:00:35
 * @FilePath     : /Multi_Mac_Address_V2/espnowSensor/espnowSensor.ino
 * @Description  : 
 */

#include <Arduino.h>
#include <esp_now.h>
#include <WiFi.h>

#define CHANNEL 1

#include "esp_now_data_struct.h"  // Include your data structure definition

uint8_t robotAddress[] = {0x24, 0x0A, 0xC4, 0x81, 0xA8, 0xAC};  // MAC address of the receiver

void debugLED(uint8_t pin, uint8_t errorType){
    if (errorType == 0){ // Error during setup
        while (true) {
            digitalWrite(pin, HIGH);
        }
    }
    else if (errorType == 1){ // Error during loop
        for (int i = 0; i < 2; i++) {
            digitalWrite(pin, LOW);
            delay(500);
            digitalWrite(pin, HIGH);
            delay(500);
        }
    }
}

void setup() {
    pinMode(LED_BUILTIN, OUTPUT); // Enable the LED_BUILTIN pin as an debug LED

    // Set device as a Wi-Fi Station
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
        return;
    }
    esp_now_register_send_cb(onDataSent);
}

void loop() {
    esp_now_data_struct data;
    data.paramCount = MAX_PARAMS;
    for (int i = 0; i < MAX_PARAMS; i++) {
        data.params[i] = i + 10;  // Just an example, populate with actual data
    }
    esp_now_send(robotAddress, (uint8_t *) &data, sizeof(data));
    delay(2000);  // Send data every 2 seconds
}

void onDataSent(const uint8_t *mac_addr, esp_now_send_status_t status) {
    Serial.println(status == ESP_NOW_SEND_SUCCESS ? "Delivery success" : "Delivery fail");
}
