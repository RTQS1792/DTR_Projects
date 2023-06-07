//接收到的红外信号
struct RX_signal
{
    uint32_t item_num;  //item数量
    uint32_t lowlevel;  //低电平时间 us
    uint32_t highlevel_1;   //高电平1的时间
    uint32_t highlevel_0;   //高电平0的时间
    uint32_t encode;    //由0和1组成的编码
};
/*
 * 红外接收任务 rmt_rx_start()执行后才会接收数据
 * 接收的数据以item的数据结构存放到nvs
*/
void rmt_ir_rxTask(void *agr)
{
    size_t rx_size = 0;

    RingbufHandle_t rb = NULL;
    rmt_get_ringbuf_handle(rx_channel, &rb); //获取红外接收器接收的数据 放在ringbuff中

    rmt_rx_stop(rx_channel); //暂停接收
    while (rb)
    {

        //从ringbuff读取items 会进入阻塞 直到ringbuff中有新的数据
        rmt_item32_t *item = (rmt_item32_t *)xRingbufferReceive(rb, &rx_size, portMAX_DELAY);
        if (item)
        {
            ESP_LOGI(TAG, "rx_size = %u", rx_size);

            //!红外线接收器有干扰，需要滤波
            if (rx_size > 30)
            {
                struct RX_signal sig;   //接收信号结构体
                size_t item_num = rx_size / 4;  //一个item32bit
                sig.item_num = item_num;
                sig.highlevel_1 = 0;
                sig.highlevel_0 = 0;
                sig.encode = 0;

                //解析item
                parse_items(item, item_num, &sig);

                ir_code_lib_update(&sig); //更新ac_handle
                rmt_rx_stop(rx_channel);  //暂停接收
                xSemaphoreGive(IR_sem);   //释放信号量
            }

            //解析出数据后释放ringbuff的空间
            vRingbufferReturnItem(rb, (void *)item);
        }
    }
    vTaskDelete(NULL);
}

