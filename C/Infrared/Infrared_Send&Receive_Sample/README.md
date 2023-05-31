# Infrared Sender and Receiver Sample

*Last updated by Hanqing on 05/30/2023*

## 📁Files

- SimpleReviever - A receiver using the NEC protocal for singel sensor.
- SimpleSender - A sender using the NEC protocal.
- TinyRecv - A proto receiver for two sensors. (**⚠️Bug⚠️**: either two sensors catch the signal at the same time or both of them failed to see the signal)
- TinyRecvV2 - An updated protol with the same problem as above.

## 🔗Source

SimpleSender and SimpleReciever are both examples in the library **IRremote** form **Arduino**.

## Description

These program uses the NEC communication protocal. Each message contains an **Adreess** and a **Command** both in HEX 16 format. The actual sending happens in the **IrSender**. When sending message, call :

```c
IrSender.sendNEC(0x01, sCommand, sRepeats);
// Parameters: (Adress, Command, Repeats)
```

The repeats is an *int* represents how many times the message will be sent. 

e.g If the repeat is 4 the the message will be send four times.

## Pinout

The default pinout is defined in the *PinDefinitionsAndMore.h* file with Sender PIN **4** and Receiver PIN **15**.