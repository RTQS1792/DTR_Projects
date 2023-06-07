/*
 * @Author       : Hanqing Qi
 * @Date         : 2023-06-06 18:10:31
 * @LastEditors  : Hanqing Qi
 * @LastEditTime : 2023-06-06 18:10:35
 * @FilePath     : /Blimps_Team/C_Receiver/irrecvdata.h
 * @Description  : This is the header file for the IR receiver library
 */

#ifndef IRGETCMD_H
#define IRGETCMD_H

#include <Arduino.h>
#include <vector>
#include <unordered_map>

class irGetCMD {
public:
    irGetCMD(int gpioNum);
    void ICACHE_RAM_ATTR logHandler();
    String my_irread();

private:
    volatile uint32_t start;
    volatile uint32_t index;
    volatile uint32_t dictKeyNum;
    volatile uint32_t irValue;
    volatile std::vector<uint32_t> logList;
    std::unordered_map<uint32_t, uint32_t> irDict;
};

#endif // IRGETCMD_H

