/*
 * @Author       : Hanqing Qi
 * @Date         : 2023-08-22 18:52:01
 * @LastEditors  : Hanqing Qi
 * @LastEditTime : 2023-09-29 17:42:02
 * @FilePath     : /Multi_Mac_Address_V1/Sender/Sender.ino
 * @Description  : This is a sender code for the ESP32. It receives data from the serial port and sends it to the receivers.
 */

#include <esp_now.h>
#include <WiFi.h>

const int NUM_PARAMS = 15;         // Number of parameters contained in the serial messages
const int NUM_CONTROL_PARAMS = 13; // Number of parameters used for control
const int MAX_RECEIVERS = 5;       // Maximum number of receiver addresses
const int MAC_LENGTH = 6;          // MAC address length

uint8_t broadcastAddresses[MAX_RECEIVERS][MAC_LENGTH] = {}; // The MAC addresses of the receivers
int numOfAddresses = 0;                                     // Number of addresses received

typedef struct ControlInput
{
  float params[NUM_CONTROL_PARAMS];
} ControlInput;

ControlInput controlParams;
bool receivingPackage = false; // If the serial port is receiving a package
bool completePackage = false;  // If the serial port has received a complete package to send
String inputData;
int selectedPeer = -1; // To store the selected peer from the extra parameters.
int brodcastMode = 0;  // To store the broadcast mode from the extra parameters.

esp_now_peer_info_t peerInfo; // The peer info structure

void OnDataSent(const uint8_t *mac_addr, esp_now_send_status_t status);
void processData(String &data);
int processAddress(String &data);
void parseAndStoreMac(int index, String &mac);
void print_params();

void setup()
{
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);
}

void loop()
{
  // Check if there is any data to be received
  while (Serial.available())
  {
    char c = Serial.read();
    if (c == '$') // The package contains the addresses of the receivers
    {
      // Toggle the receivingPackage flag to indicate the start or end of the address package
      receivingPackage = !receivingPackage;
      // If the flag is false, we have received the end of the address package
      if (!receivingPackage)
      {
        // Process the address package
        numOfAddresses = processAddress(inputData);
        if (numOfAddresses > 0) {
            initializeESPNowPeers();
        }
      }
    }
    else if (c == '<') // The beginning of the package containing the control parameters
    {
      // We are in the middle of processing a package, no complete package to send
      completePackage = false;
      receivingPackage = true;
    }
    else if (c == '>') // The end of the package containing the control parameters
    {
      // We have received a complete package to send
      completePackage = true;
      receivingPackage = false;
      processData(inputData);
    }
    else if (receivingPackage)
    {
      inputData += c;
    }
  }

  if (completePackage) // We have a complete package that has been processed
  {
    completePackage = false;
    esp_err_t result;

    if (selectedPeer >= 0 && selectedPeer < numOfAddresses)
    {
      result = esp_now_send(broadcastAddresses[selectedPeer], (uint8_t *)&controlParams, sizeof(ControlInput));
    }
    else
    {
      uint8_t defaultBroadcastMAC[] = {0x00, 0x00, 0x00, 0x00, 0x00, 0x00};
      result = esp_now_send(defaultBroadcastMAC, (uint8_t *)&controlParams, sizeof(ControlInput)); // Default sending behavior
    }
    // Consider handling the result here...
  }
}

/**
 * @description: Initialize the ESP-NOW peers
 * @return      {*} void
 */
void initializeESPNowPeers()
{
  esp_now_deinit();

  if (esp_now_init() != ESP_OK)
  {
    Serial.println("Error initializing ESP-NOW");
    return;
  }

  esp_now_register_send_cb(OnDataSent);

  for (int i = 0; i < numOfAddresses; i++) 
  {
    memcpy(peerInfo.peer_addr, broadcastAddresses[i], MAC_LENGTH);
    if (esp_now_add_peer(&peerInfo) != ESP_OK)
    {
      Serial.println("Failed to add peer");
    }
  }
}

void processData(String &data)
{
  int paramIndex = 0;

  while (data.length() > 0 && paramIndex < NUM_PARAMS)
  {
    int split_position = data.indexOf('|');

    if (split_position == -1) // We are at the last parameter
    {
      if (paramIndex == NUM_PARAMS - 1) // If the last parameter is index NUM_PARAMS - 1, the package is complete
      {
        brodcastMode = data.toInt();
        paramIndex++;
      }
      else
      {
        Serial.println("Error: data is broken");
      }
      break;
    }

    String param = data.substring(0, split_position);

    if (paramIndex < NUM_CONTROL_PARAMS) // The first NUM_CONTROL_PARAMS - 1 parameters are control parameters
    {
      controlParams.params[paramIndex++] = param.toFloat();
    }
    else if (paramIndex == NUM_CONTROL_PARAMS) // The NUM_CONTROL_PARAMSth parameter is the selected peer
    {
      selectedPeer = param.toInt();
      paramIndex++;
    }
    else
    {
      Serial.println("Error: more floats than expected");
      break;
    }

    data = data.substring(split_position + 1);
  }

  if (paramIndex != NUM_PARAMS)
  {
    Serial.println("Error: data is broken");
  }
  else
  {
    print_params();
  }

}

/**
 * @description: Process the address package
 * @param       {String} &data: The address package
 * @return      {int} The number of addresses
 */
int processAddress(String &data)
{
  int numAddresses = data.substring(0, data.indexOf('#')).toInt();
  if (numAddresses > MAX_RECEIVERS)
  {
    Serial.print(data);
    Serial.print(" ");
    Serial.print(MAX_RECEIVERS);
    Serial.print(" ");
    Serial.println("Error: Too many MAC addresses provided");
    data = "";
    return 0;
  }

  data = data.substring(data.indexOf('#') + 1);
  for (int i = 0; i < numAddresses; i++)
  {
    int nextAddrEndPos = data.indexOf('#');
    String mac = nextAddrEndPos != -1 ? data.substring(0, nextAddrEndPos) : data;
    parseAndStoreMac(i, mac);
    data = data.substring(mac.length() + 1);
  }

  for (int i = numAddresses; i < MAX_RECEIVERS; i++)
  {
    memset(broadcastAddresses[i], 0, MAC_LENGTH); // clear out remaining addresses
  }

  Serial.print("Number of addresses: ");
  Serial.println(numAddresses);
  data = "";
  return numAddresses;
}

/**
 * @description: Parse the MAC address and store it in the broadcastAddresses array
 * @param       {int} index: The index of the address in the array
 * @param       {String} &mac: The MAC address
 * @return      {*} void
 */
void parseAndStoreMac(int index, String &mac)
{
  int prevPos = 0;
  for (int j = 0; j < MAC_LENGTH; j++)
  {
    int pos = mac.indexOf(':', prevPos);
    pos = (pos == -1) ? mac.length() : pos;
    broadcastAddresses[index][j] = strtol(mac.substring(prevPos, pos).c_str(), NULL, 16);
    prevPos = pos + 1;
  }
}

void OnDataSent(const uint8_t *mac_addr, esp_now_send_status_t status)
{
  char macStr[18];
  snprintf(macStr, sizeof(macStr), "%02x:%02x:%02x:%02x:%02x:%02x",
           mac_addr[0], mac_addr[1], mac_addr[2], mac_addr[3], mac_addr[4], mac_addr[5]);

  Serial.print("Packet to: ");
  Serial.print(macStr);
  Serial.print(" send status:\t");
  Serial.println(status == ESP_NOW_SEND_SUCCESS ? "Delivery Success" : "Delivery Fail");
}

/**
 * @description: Print the control params
 * @return      {*} void
 */
void print_params()
{
  for (int i = 0; i < NUM_CONTROL_PARAMS; i++)
  {
    Serial.print(controlParams.params[i]);
    if (i < NUM_CONTROL_PARAMS - 1)
    {
      Serial.print(", ");
    }
  }
  if (brodcastMode)
  {
    Serial.print(" ---- broadcast on channel: ");
    Serial.print(brodcastMode);
    selectedPeer = -1; // Reset the selected peer
  }
  else
  {
    Serial.print(" ---- to peer: ");
    Serial.print(selectedPeer);
  }
  Serial.print(" ----- ");
}
