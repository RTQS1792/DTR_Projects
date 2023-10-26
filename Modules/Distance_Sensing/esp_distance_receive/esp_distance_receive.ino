/*
 * @Author       : Hanqing Qi
 * @Date         : 2023-10-20 17:22:06
 * @LastEditors  : Hanqing Qi
 * @LastEditTime : 2023-10-20 17:22:36
 * @FilePath     : /Distance_Sensing/esp_distance_receive/esp_distance_receive.ino
 * @Description  : Receive distance data from nicla
 */


#include <IBusBM.h>

IBusBM IBus; 
HardwareSerial MySerial0(0);

void setup() {
  // initialize serial port for debug
  Serial.begin(115200);
  // iBUS connected to MySerial0
  // Configure MySerial0 on pins TX=D6 and RX=D7 (-1, -1 means use the default)
  MySerial0.begin(115200, SERIAL_8N1, -1, -1);
  IBus.begin(MySerial0, IBUSBM_NOTIMER);
  Serial.println("Start iBUS sensor");
}

void loop() {
  IBus.loop();
	// print the value in each channel
  for (byte i = 0; i<14; i++) {
     int value = IBus.readChannel(i);
  }
  Serial.println();
  delay(20);                      // wait for a second
}