/*
 * @Author       : Hanqing Qi
 * @Date         : 2023-10-26 18:11:25
 * @LastEditors  : Hanqing Qi
 * @LastEditTime : 2023-10-26 18:26:50
 * @FilePath     : /Multi_Mac_Address_V2/espnowDataStruct.h
 * @Description  : The data structure to hold the information in espnow communication.
 */

#ifndef _ESP_NOW_DATA_STRUCT_H_
#define _ESP_NOW_DATA_STRUCT_H_

#include <Arduino.h>

#define MAX_PARAMS 16

typedef struct esp_now_data_struct
{
    int paramCount;  // This int indicates the number of parameters in use
    int params[MAX_PARAMS];  // Array to hold 16 int parameters
} esp_now_data_struct;

#endif