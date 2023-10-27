/*
 * @Author       : Hanqing Qi
 * @Date         : 2023-10-26 18:11:25
 * @LastEditors  : Hanqing Qi
 * @LastEditTime : 2023-10-27 14:43:43
 * @FilePath     : /Multi_Mac_Address_V2/espnowDataStruct.h
 * @Description  : The data structure to hold the information in espnow communication.
 */

#ifndef _ESP_NOW_DATA_STRUCT_H_
#define _ESP_NOW_DATA_STRUCT_H_

#include <Arduino.h>

#define MAX_PARAMS 16

typedef struct esp_now_data_struct {
    int paramCount;         // This int indicates the number of parameters in use
    int params[MAX_PARAMS]; // Array to hold 16 int parameters
    int flag;               // Flag that indicates which type of data is being sent
    /*
     * NOTE: Below is the list of flags and their corresponding data types
     * 0: regular control data
     * 1: BNP & barometer feedback
     * 2: nicla feedback
     * 3: wall sensor feedback
     */
} esp_now_data_struct;

#endif

void printEspnowData(const esp_now_data_struct& data){
    switch (data.flag) {}
    {
    case 0:
        Serial.print("Control data: ");
        break;
    case 1:
        Serial.print("BNP & baro feedback: ");
        break;
    case 2:
        Serial.print("Nicla feedback: ");
        break;
    case 3:
        Serial.print("Wall sensor feedback: ");
        break;
    default:
        Serial.print("Unknown flag: ");
        break;
    }
    for (int i = 0; i < data.paramCount; i++){
        Serial.print(data.params[i]);
        Serial.print(" ");
    }
}