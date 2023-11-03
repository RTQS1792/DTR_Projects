/*
 * @Author       : Hanqing Qi
 * @Date         : 2023-10-28 14:31:55
 * @LastEditors  : Hanqing Qi
 * @LastEditTime : 2023-10-28 19:52:09
 * @FilePath     : /ESP_NOW/Multi_Mac_Address_V2/espnowTranseiver/espnowTranseiver.ino
 * @Description  :
 */

#include <esp_now.h>
#include <WiFi.h>
#include "espnowDataStruct.h"

#define SOM 0x02               // Start of message
#define EOM 0x03               // End of message
#define MAX_MESSAGE_LENGTH 256 // Assuming a maximum message length
#define MAX_RECEIVERS 20       // Maximum number of receiver addresses
#define SERIAL_TIMEOUT 1000    // Timeout for serial communication in milliseconds

uint8_t macAddresses[MAX_RECEIVERS][6] = {}; // The MAC addresses of the receivers
uint8_t nullAddress[] = {0x00, 0x00, 0x00, 0x00, 0x00, 0x00};
uint8_t brodcastAddress[] = {0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF};
int numOfAddresses = 0; // Number of addresses received
int slaveIndex = 0;
int brodcastChannel = -1;
bool completePackage = false; // If the serial port has received a complete package to send

esp_now_data_struct dataToSend; // Create a struct to hold the data you will send
esp_now_data_struct dataReceived;
esp_now_peer_info_t peerInfo; // Create a struct to hold the peer information

void setup()
{
    Serial.begin(115200); // Initialize serial communication at 115200 bps
    WiFi.mode(WIFI_STA);  // Set WiFi mode to station
    Serial.print("ESP Sensor MAC Address:  ");
    Serial.println(WiFi.macAddress());
}

void loop()
{
    readSerialMessage(); // Call function to read serial message
    if (completePackage)
    {
        sendControlData();
    }
}

/**
 * @description: Initialize the ESP-NOW peers
 * @return      {*} None
 */
void initializeESPNowPeers()
{
    esp_now_deinit();

    if (esp_now_init() != ESP_OK)
    {
        Serial.println("Error initializing ESP-NOW");
        return;
    }
    esp_now_register_send_cb(onDataSent);
    esp_now_register_recv_cb(onDataRecv);
    for (int i = 0; i < numOfAddresses; i++)
    {
        memcpy(peerInfo.peer_addr, macAddresses[i], 6);
        if (esp_now_add_peer(&peerInfo) != ESP_OK)
        {
            Serial.println("Failed to add peer");
        }
    }
    memcpy(peerInfo.peer_addr, brodcastAddress, 6);
    if (esp_now_add_peer(&peerInfo) != ESP_OK)
    {
        Serial.println("Failed to add broadcast peer");
    }
}

/**
 * @description: Read a message from the serial port
 * @return      {*} None
 */
void readSerialMessage()
{
    if (Serial.available() > 0)
    {
        byte startMarker = Serial.read();
        if (startMarker == SOM) // If the message starts with SOM
        {
            byte msgLength = Serial.read(); // Read message length
            if (msgLength > MAX_MESSAGE_LENGTH || msgLength <= 0)
            {
                Serial.println("Invalid message length");
                return; // Exit function if message length is invalid
            }
            String messageBody = "";
            byte checksum = 0;
            for (int i = 0; i < msgLength; i++)
            {
                unsigned long startTime = millis();
                while (Serial.available() == 0 && millis() - startTime < SERIAL_TIMEOUT){}; // Wait for next character
                if (millis() - startTime >= SERIAL_TIMEOUT)
                {
                    Serial.println("Timeout waiting for data on serial port");
                    return; // Exit function if timeout
                }
                char c = Serial.read();
                messageBody += c;
                checksum ^= c; // Calculate checksum
            }
            while (Serial.available() < 2)
                ;                                  // Wait for checksum and EOM
            byte receivedChecksum = Serial.read(); // Read checksum from message
            byte endMarker = Serial.read();        // Read end of message marker
            if (endMarker == EOM && checksum == receivedChecksum)
            {
                processMessage(messageBody);
            }
            else
            {
                Serial.println("Message validation failed");
            }
        }
    }
}

/**
 * @description: Process the message received from the serial port
 * @param       {String} message: The message received from the serial port
 * @return      {*} None
 */
void processMessage(String message)
{
    char type = message.charAt(0);
    String data = message.substring(2);
    if (type == 'M')
    { // If the message is a MAC address list
        processMacAddresses(data);
    }
    else if (type == 'C')
    { // If the message is a control message
        processControlParameters(data);
    }
}

/**
 * @description: Process the MAC address list and store the addresses in the macAddresses array
 * @param       {String} macList: The MAC address list
 * @return      {*} None
 */
void processMacAddresses(String macList)
{
    // Reset the macAddresses array and the dataToSend struct
    memset(macAddresses, 0, sizeof(macAddresses));
    memset(&dataToSend, 0, sizeof(dataToSend));

    int addressIndex = 0;         // Index to keep track of where to store the next address
    int startPos = 0, endPos = 0; // Positions to help in substring operation

    while ((endPos = macList.indexOf('|', startPos)) != -1 && addressIndex < MAX_RECEIVERS)
    {
        String macStr = macList.substring(startPos, endPos);
        convertMacStrToBytes(macStr, macAddresses[addressIndex]);
        addressIndex++;
        startPos = endPos + 1; // Update startPos for next iteration
    }

    // Process the last address if any
    if (startPos < macList.length() && addressIndex < MAX_RECEIVERS)
    {
        String macStr = macList.substring(startPos);
        convertMacStrToBytes(macStr, macAddresses[addressIndex]);
        addressIndex++;
    }
    numOfAddresses = addressIndex; // Update numOfAddresses with the number of valid addresses
    Serial.println("Received MAC addresses: " + String(numOfAddresses));
    initializeESPNowPeers();
}

/**
 * @description: Convert a MAC address string to a byte array
 * @param       {String} macStr: The MAC address string
 * @param       {uint8_t*} macBytes: The byte array to store the MAC address
 * @return      {*} None
 */
void convertMacStrToBytes(String macStr, uint8_t *macBytes)
{
    if (macStr.length() != 17)
    { // Check if the MAC address is 17 characters long
        Serial.println("Invalid MAC address format");
        return;
    }
    for (int i = 0; i < 6; i++)
    {
        if (macStr.charAt(i * 3 + 2) != ':' && i < 5)
        { // Check if the MAC address has colons at the right places
            Serial.println("Invalid MAC address format");
            return;
        }
        String byteStr = macStr.substring(i * 3, i * 3 + 2); // Extract the byte string
        char *endptr;
        long byteValue = strtol(byteStr.c_str(), &endptr, 16); // Convert the byte string to a number
        if (*endptr != '\0')
        { // Check if the conversion was successful
            Serial.println("Invalid byte in MAC address");
            return;
        }
        macBytes[i] = (uint8_t)byteValue;
    }

    // // Print the processed MAC address
    for (int i = 0; i < 5; i++)
    {
        Serial.print(macBytes[i], HEX);
        Serial.print(":");
    }
    Serial.println(macBytes[5], HEX);
}

void processControlParameters(String controlParams)
{
    int paramIndex = 0;
    int startPos = 0, endPos = 0;

    esp_now_data_struct tempData; // Temporary data structure to hold new data

    while ((endPos = controlParams.indexOf('|', startPos)) != -1 && paramIndex < MAX_PARAMS)
    {
        String paramStr = controlParams.substring(startPos, endPos);
        float paramValue = paramStr.toFloat();
        if (paramValue == 0 && paramStr != "0")
        { // Invalid control parameter value
            Serial.println("Invalid control parameter value");
            return;
        }
        tempData.params[paramIndex] = paramValue;
        paramIndex++;
        startPos = endPos + 1; // Update startPos for next iteration
    }

    // Process the last parameter if any
    if (startPos < controlParams.length() && paramIndex < MAX_PARAMS)
    {
        String paramStr = controlParams.substring(startPos);
        float paramValue = paramStr.toFloat();
        if (paramValue == 0 && paramStr != "0")
        {
            Serial.println("Invalid control parameter value");
            return;
        }
        tempData.params[paramIndex] = paramValue;
    }

    tempData.paramCount = paramIndex + 1; // Update paramCount in the temporary data structure
    tempData.flag = 0;                    // Set the flag to indicate that this is a control message

    dataToSend = tempData; // Update dataToSend with the new valid data
    completePackage = true;
    Serial.print("Sent ");
    printEspnowData(dataToSend);
}

void onDataSent(const uint8_t *mac_addr, esp_now_send_status_t status)
{
    Serial.println(status == ESP_NOW_SEND_SUCCESS ? " S " : " F111 ");
}

void sendControlData()
{
    if (dataToSend.paramCount > 0 && dataToSend.flag == 0)
    { // If there is control data to send
        Serial.print("Still sending");
        esp_err_t result;
        slaveIndex = dataToSend.params[dataToSend.paramCount - 1];
        brodcastChannel = dataToSend.params[dataToSend.paramCount - 2];
        if (slaveIndex < numOfAddresses && slaveIndex >= 0)
        {
            result = esp_now_send(macAddresses[slaveIndex], (uint8_t *)&dataToSend, sizeof(dataToSend));
        }
        else if (slaveIndex == -1)
        {
            result = esp_now_send(brodcastAddress, (uint8_t *)&dataToSend, sizeof(dataToSend));
        }
        else
        {
            Serial.println("Receiver index out of range");
        }
        completePackage = false;
    }
}

void onDataRecv(const uint8_t *mac_addr, const uint8_t *data, int len)
{
    Serial.println("Data received:");
    esp_now_data_struct *dataReceived = (esp_now_data_struct *)data;
    printEspnowData(*dataReceived);
}
