/*
 * @Author       : Hanqing Qi
 * @Date         : 2023-09-29 15:39:01
 * @LastEditors  : Hanqing Qi
 * @LastEditTime : 2023-09-29 15:39:20
 * @FilePath     : /Multi_Mac_Address_V1/Sender/Sender_Old.ino
 * @Description  : Old version of the sender code
 */

#include <esp_now.h>
#include <WiFi.h>

const int NUM_PARAMS = 15; // Number of parameters contained in the serial messages
const int NUM_CONTROL_PARAMS = 13; // Number of parameters used for control
const int MAX_ADDRESSES = 5; // Maximum number of receiver addresses
const int MAC_ADRESS_LENGTH = 6; // MAC address length

uint8_t broadcastAddresses[MAX_RECEIVERS][MAC_LENGTH] = {}; // The MAC addresses of the receivers
int NUM_ADDRESSES = 0; // Number of addresses received

// The data structure of the control parameters
typedef struct ControlInput
{
  float params[NUM_CONTROL_PARAMS];
} ControlInput;

esp_now_peer_info_t peerInfo; // The peer info structure

void OnDataSent(const uint8_t *mac_addr, esp_now_send_status_t status);

void setup()
{
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);
}

ControlInput params;
bool isDataStarted = false;
bool HaveData = false;
bool isAddressStarted = false;
String inputData;
int selectedPeer = -1; // To store the selected peer from the extra parameter.

void loop()
{
  while (Serial.available())
  {
    char c = Serial.read();
    if (c == '$')
    {
      isDataStarted = !isDataStarted;
      isAddressStarted = false;
      if (!isDataStarted)
      {
        numOfAddresses = process_address(inputData);
      }
    }
    else if (c == '<')
    {
      HaveData = false;
      isDataStarted = true;
      inputData = "";
    }
    else if (c == '>')
    {
      HaveData = true;
      isDataStarted = false;
      process_data(inputData);
    }
    else if (isDataStarted)
    {
      inputData += c;
    }
  }

  if (HaveData)
  {
    HaveData = false;
    esp_err_t result;

    if (!isAddressStarted)
    {
      isAddressStarted = true;
      initializeESPNowPeers();
    }

    if (selectedPeer >= 0 && selectedPeer < numOfAddresses)
    {
      result = esp_now_send(broadcastAddresses[selectedPeer], (uint8_t *)&params, sizeof(ControlInput));
    }
    else
    {
      result = esp_now_send(0, (uint8_t *)&params, sizeof(ControlInput)); // Default sending behavior
    }

    // Handling the result remains unchanged...
  }
}

bool allMACAddressesCollected()
{
  if (numOfAddresses == 0)
  {
    return false;
  }

  for (int i = 0; i < numOfAddresses; i++)
  {
    bool isAddressEmpty = true;
    for (int j = 0; j < MAC_LENGTH; j++)
    {
      if (broadcastAddresses[i][j] != 0)
      {
        isAddressEmpty = false;
        break;
      }
    }
    if (isAddressEmpty)
      return false;
  }

  return true;
}

void initializeESPNowPeers()
{
  if (esp_now_init() != ESP_OK)
  {
    Serial.println("Error initializing ESP-NOW");
    return;
  }
  esp_now_register_send_cb(OnDataSent);

  // Register peer
  memcpy(peerInfo.peer_addr, broadcastAddresses[selectedPeer], MAC_LENGTH);
  if (esp_now_add_peer(&peerInfo) != ESP_OK)
  {
    Serial.println("Failed to add peer");
    return;
  }

  // for (int i = 0; i < numOfAddresses; i++)
  // {
  //   memcpy(peerInfo.peer_addr, broadcastAddresses[i], MAC_LENGTH);
  //   if (esp_now_add_peer(&peerInfo) != ESP_OK)
  //   {
  //     Serial.println("Failed to add peer");
  //     return;
  //   }
  // }
}

void process_data(String &data)
{
  int paramIndex = 0;
  int lastSplitPosition = 0;

  while (data.length() > 0 && paramIndex < TOTAL_PARAMS)
  {
    int split_position = data.indexOf('|');

    if (split_position == -1)
    { // Last parameter
      if (paramIndex == TOTAL_PARAMS - 1)
      {
        selectedPeer = data.toInt(); // The 14th parameter determines the selected peer.
        paramIndex++;
      }
      else
      {
        Serial.println("Error: data is broken");
      }
      break;
    }

    // Extracting a parameter
    String param = data.substring(0, split_position);

    if (paramIndex < MAX_PARAMS)
    {
      params.params[paramIndex++] = param.toFloat();
    }
    else
    {
      Serial.println("Error: more floats than expected");
      break;
    }

    // Move to the next parameter in the data strings
    data = data.substring(split_position + 1);
  }

  if (paramIndex != TOTAL_PARAMS)
  {
    Serial.println("Error: data is broken");
  }
  else
  {
    print_params();
  }
}

int process_address(String &data)
{
  int numAddresses = data.substring(0, data.indexOf('#')).toInt();
  if (numAddresses > MAX_RECEIVERS)
  {
    Serial.print(data);
    Serial.print(" ");
    Serial.print(MAX_RECEIVERS);
    Serial.print(" ");
    Serial.println("Error: Too many MAC addresses provided");
    // Clear the data
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

void print_params()
{
  for (int i = 0; i < MAX_PARAMS; i++)
  {
    Serial.print(params.params[i]);
    if (i < MAX_PARAMS - 1)
    {
      Serial.print(", ");
    }
  }
  Serial.print(" -- to peer: ");
  Serial.print(selectedPeer);
  Serial.print(" ----- ");
}
