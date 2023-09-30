import serial
import time

NULL_ADDRESS = ["00:00:00:00:00:00"]
DELIMITER = "|"

class ESPNOWControl:
    def __init__(self, serial_port: str, mac_addresses: list = NULL_ADDRESS) -> None:
        if(self._init_serial(serial_port)):
            print("Serial connection established")
        else:
            raise Exception("Serial connection failed")
        self._send_mac_addresses(mac_addresses)
        print("ESP-NOW Control Initialized Successfully")
        self.broadcast_mode = False
        if mac_addresses == NULL_ADDRESS:
            print("No MAC addresses provided, broadcast mode enabled")
            self.broadcast_mode = True

    def _init_serial(self, serial_port: str) -> bool:
        try:
            self.serial = serial.Serial(serial_port, 115200)
            print(f"Connected to port {serial_port}")
            # Empty the buffer
            while self.serial.in_waiting:
                self.serial.readline().decode(errors="ignore").strip()
            time.sleep(1)
            return True
        except serial.SerialException as e:
            print(f"Failed to connect to port {serial_port}. Error: {e}")
            return False
        
    def _send_mac_addresses(self, mac_addresses: list) -> None:
        print("Sending MAC addresses...")
        while True:
            mac_data = "${}#{}$".format(len(mac_addresses), "#".join(mac_addresses))
            self.serial.write(mac_data.encode())
            try:
                incoming = self.serial.readline().decode(errors="ignore").strip()
                if incoming == ("Number of addresses: " + str(len(mac_addresses))):
                    print("MAC addresses sent successfully!")
                    break
            except UnicodeDecodeError:
                print("Received malformed data!")
            time.sleep(0.5)

    def ESPNOW_send(self, control_params: list, brodcast_channel:int, slaveindex: int) -> bool:
        if len(control_params) != 13:
            raise ValueError("Expected 13 control parameters but got {}".format(len(control_params)))
        raw_massage = control_params
        if self.broadcast_mode or slaveindex == -1: # Broadcast mode
            raw_massage.append(brodcast_channel)
            raw_massage.append(-1)
        else:
            raw_massage.append(-1)
            raw_massage.append(slaveindex)
        # Format the message
        message = str("<" + DELIMITER.join(map(str, raw_massage)) + ">")
        self.serial.write(message.encode())
        try:
            incoming = self.serial.readline().decode(errors="ignore").strip()
            print("Received Data: " + incoming)
        except UnicodeDecodeError:
            print("Received malformed data!")

    def close(self) -> None:
        if self.serial.is_open:
            self.serial.close()
            print("Serial connection closed.")


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
