/*
 * @Author       : Hanqing Qi
 * @Date         : 2023-10-26 18:32:19
 * @LastEditors  : Hanqing Qi
 * @LastEditTime : 2023-10-27 15:23:48
 * @FilePath     : /Multi_Mac_Address_V2/espnowSensor/espnowSensor.ino
 * @Description  :
 */

#include <Arduino.h>
#include <esp_now.h>
#include <WiFi.h>

#include "espnowDataStruct.h" // Include your data structure definition

uint8_t robotAddress[] = {0x00, 0x00, 0x00, 0x00, 0x00, 0x00}; // MAC address of the receiver
esp_now_data_struct dataToSend;                                // Create a struct to hold the data you will send
esp_now_peer_info_t peerInfo;

void setup()
{
    pinMode(LED_BUILTIN, OUTPUT); // Enable the LED_BUILTIN pin as an debug LED
    digitalWrite(LED_BUILTIN, LOW);
    Serial.begin(115200);
    WiFi.mode(WIFI_STA);
    Serial.print("ESP Sensor MAC Address:  ");
    Serial.println(WiFi.macAddress());
    if (esp_now_init() != ESP_OK)
    {
        Serial.println("Error initializing ESP-NOW");
        return;
    }
    esp_now_register_send_cb(onDataSent);
    memcpy(peerInfo.peer_addr, robotAddress, 6);
    peerInfo.encrypt = false;
    if (esp_now_add_peer(&peerInfo) != ESP_OK)
    {
        Serial.println("Failed to add peer");
        return;
    }
  digitalWrite(LED_BUILTIN, HIGH);
}

void loop()
{
    esp_now_data_struct data;
    data.paramCount = 1; // Only need one parameter for wall sensor feedback
    data.params[0] = 99; // TODO: Change this to the actual wall sensor feedback
    data.flag = 3;       // Flag for wall sensor feedback
    dataToSend = data; // Store the data before sending
    esp_now_send(robotAddress, (uint8_t *)&data, sizeof(data));
}

void onDataSent(const uint8_t *mac_addr, esp_now_send_status_t status)
{
    printEspnowData(dataToSend); // Print the data that was sent
    Serial.print("Sent to: ");
    for (int i = 0; i < 6; i++)
    {
        Serial.print(mac_addr[i], HEX);
        if (i < 5)
            Serial.print(":");
    }
    Serial.print(", Status: ");
    Serial.println(status == ESP_NOW_SEND_SUCCESS ? "Success" : "Fail    ");
}
