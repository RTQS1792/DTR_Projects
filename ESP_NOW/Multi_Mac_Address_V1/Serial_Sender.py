import serial
import time
import sys

PORT = "/dev/cu.wchusbserial1140"
MAC_ADDRESSES = [
    "11:11:11:2b:11:11",
    "22:22:22:22:22:22",
    "33:33:33:33:33:33",
    "44:44:44:44:44:11",
    "54:4a:16:1a:1a:1a",
]
SLAVE_ID = 3
BRODCAST_MODE = 1
DELIMITER = "|"


# Class for control input
class ControlInput:
    def __init__(self, *args, slave_id: int = 0, broadcast_mode: int = 0) -> None:
        """
        @description: The constructor of ControlInput class
        @param       {*} self: -
        @param       {array} args: 13 parameters for ControlInput 
        @param       {int} slave_id: The id of the slave to control, default to 0
        @param       {int} broadcast_mode: The mode of broadcast, default to 0, no broadcast
        @return      {None}
        NOTE: broadcast_mode can override slave_id, if broadcast is enabled, slave_id will be ignored
        """
        if len(args) != 13:
            raise ValueError("Expected 13 parameters for ControlInput")
        self.params = args
        self.slave_id = slave_id
        self.broadcast_mode = broadcast_mode

    def __str__(self) -> str:
        """
        @description: Get the string representation of ControlInput class
        @param       {*} self: -
        @return      {str} The string representation
        """
        return (
            "<"
            + DELIMITER.join(map(str, self.params))
            + DELIMITER
            + str(self.slave_id)
            + DELIMITER
            + str(self.broadcast_mode)
            + ">"
        )


def espnow_init()->serial.Serial:
    """
    @description: Initialize the ESP-NOW connection
    @return      {serial.Serial} The serial connection
    """
    try:
        ser = serial.Serial(PORT, 115200)
        return ser
    except serial.SerialException as e:
        print(f"Failed to connect to port {PORT}. Error: {e}")
        sys.exit(1)


def send_mac_addresses(ser):
    print("Sending MAC addresses...")
    while True:
        mac_data = "${}#{}$".format(len(MAC_ADDRESSES), "#".join(MAC_ADDRESSES))
        ser.write(mac_data.encode())
        try:
            incoming = ser.readline().decode(errors="ignore").strip()
            if incoming == ("Number of addresses: " + str(len(MAC_ADDRESSES))):
                print("MAC addresses sent successfully!")
                break
        except UnicodeDecodeError:
            print("Received malformed data!")
        time.sleep(1)


def esp_now_send(ser, input):
    message = str(input)
    ser.write(message.encode())
    try:
        incoming = ser.readline().decode(errors="ignore").strip()
        print("Received Data: " + incoming)
    except UnicodeDecodeError:
        print("Received malformed data!")


if __name__ == "__main__":
    myserial = espnow_init()
    # Clear the buffer
    while myserial.in_waiting:
        print(myserial.readline().decode(errors="ignore").strip())
    time.sleep(2)
    send_mac_addresses(myserial)
    # sys.exit(0)
    try:
        while True:
            esp_now_input = ControlInput(
                0.12, 1.23, 2.34, 3.45, 4.56, 5.67, 6.78, 7.89, 8.9, 9.01, 10.12, 11.23, 12.34, slave_id=SLAVE_ID, broadcast_mode=BRODCAST_MODE
            )
            # print("Sending Data: " + str(esp_now_input))
            esp_now_send(myserial, esp_now_input)
            time.sleep(0.2)
    except KeyboardInterrupt:
        print("The end")
        myserial.close()
