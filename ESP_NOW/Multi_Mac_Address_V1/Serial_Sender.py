import serial
import time

NULL_ADDRESS = ["00:00:00:00:00:00"]
DELIMITER = "|"


class ESPNOWControl:
    def __init__(self, serial_port: str, mac_addresses: list = NULL_ADDRESS) -> None:
        if self._init_serial(serial_port):
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

    def send(
        self, control_params: list, brodcast_channel: int, slaveindex: int
    ) -> bool:
        if len(control_params) != 13:
            raise ValueError(
                "Expected 13 control parameters but got {}".format(len(control_params))
            )
        raw_massage = control_params.copy()
        if self.broadcast_mode or slaveindex == -1:  # Broadcast mode
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
            print("Sending " + incoming)
        except UnicodeDecodeError:
            print("Received malformed data!")

    def close(self) -> None:
        if self.serial.is_open:
            self.serial.close()
            print("Serial connection closed.")
