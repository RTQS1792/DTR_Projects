/*
 * @Author       : Hanqing Qi
 * @Date         : 2023-06-06 18:10:09
 * @LastEditors  : Hanqing Qi
 * @LastEditTime : 2023-06-06 18:57:14
 * @FilePath     : /Blimps_Team/C_Receiver/irrecvdata.cpp
 * @Description  : This is the source file for the IR receiver library
 */
#include <Arduino.h>
#include <vector>

class irGetCMD {
  public:
    irGetCMD(int gpioNum);
    String my_irread();

  private:
    int irRecvPin;
    volatile uint32_t start;
    volatile int index;
    std::vector<uint32_t> logList;
    void IRAM_ATTR handleInterrupt();
    static void IRAM_ATTR isrstatic(void* arg) {
      static_cast<irGetCMD*>(arg)->handleInterrupt();
    }
};

irGetCMD::irGetCMD(int gpioNum) {
  irRecvPin = gpioNum;
  pinMode(irRecvPin, INPUT_PULLUP);
  attachInterruptArg(digitalPinToInterrupt(irRecvPin), isrstatic, this, CHANGE);
  index = 0;
  start = 0;
}

// FIXME - The handleInterrupt() function is not being called.
void irGetCMD::handleInterrupt() {
  Serial.println("Triggered");
  uint32_t now = micros();
  if (start == 0) {
    start = now;
    index = 0;
    return;
  }
  logList.push_back(now - start);
  start = now;
  index++;
}

String irGetCMD::my_irread() {
  // Serial.println(start);
  if ((micros() - start) > 100000 && index > 0) {
    if (logList.size() < 66) {
      return "Signal Length Too Short";
    }

    std::vector<int> ir_buffer;
    for (int i = 3; i < 66; i += 2) {
      if (logList[i] > 800) {
        ir_buffer.push_back(1);
      } else {
        ir_buffer.push_back(0);
      }
    }

    uint32_t irValue = 0;
    for (int i = 0; i < 4; i++) {
      for (int j = 0; j < 8; j++) {
        if (ir_buffer[i * 8 + j] == 1) {
          irValue = irValue << 1;
          irValue |= 0x01;
        } else {
          irValue = irValue << 1;
          irValue &= 0xFFFFFFFE;
        }
      }
    }

    logList.clear();
    index = 0;
    start = 0;

    char buffer[10];
    sprintf(buffer, "%x", irValue);
    return buffer;
  }
  return "";
}
