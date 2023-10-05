/*
 * @Author       : Hanqing Qi
 * @Date         : 2023-10-03 15:41:43
 * @LastEditors  : Hanqing Qi
 * @LastEditTime : 2023-10-03 15:41:43
 * @FilePath     : /DTR_Projects/Modules/Voltage_Measurement/getVoltage/getVoltage.ino
 * @Description  : Get the voltage of the battery
 */

#include "driver/adc.h"
#include "esp_adc_cal.h"

void setup(){
  Serial.begin(115200);
}

void loop(){
  Serial.print("VCC Voltage: ");
  Serial.print(readVcc(), 2);
  Serial.println("V");
  delay(1000);
}

float readVcc() {
  // Read 1100mV voltage reference against AVDD
  // set all-in-one command ADC_V_REF_TO_GPIO
  adc_dac_vref_to_gpio(GPIO_NUM_25); 
  adc1_config_channel_atten(ADC1_CHANNEL_6, ADC_ATTEN_DB_0);
  adc1_config_width(ADC_WIDTH_BIT_12);

  int sum = 0;                  // sum of samples taken
  int reading_count = 32;       // number of samples taken
  float average = 0;            // average of samples taken

  for (int i = 0; i < reading_count; i++) {
    sum += adc1_get_raw(ADC1_CHANNEL_6);
    delay(1);
  }
  average = sum / reading_count;

  // Convert ADC reading to voltage
  float VCC = 1100 / average;
  VCC = VCC * 1000;  // Convert millivolt to volt
  return VCC;
}


