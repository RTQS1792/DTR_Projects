void callBack(void)
{
  int level = digitalRead(15); //读取GPIO_13上的电平
  Serial.printf("触发了中断，当前电平是： %d\n", level);
}

void setup()
{
  Serial.begin(115200);
  Serial.println();
  
  pinMode(15,OUTPUT);    //GPIO_13,输出模式
  attachInterrupt(15, callBack, CHANGE);  //当电平发生变化时，触发中断


  for (int i = 0; i < 30; i++)
  {
    delay(1000);
    Serial.println(digitalRead(15));
  }

  detachInterrupt(15); //关闭中断
}

void loop()
{
}