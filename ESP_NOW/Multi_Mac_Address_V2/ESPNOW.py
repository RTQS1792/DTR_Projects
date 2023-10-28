import serial
import time
import struct

# Serial Communication Parameters
SOM = 0x02  # Start of message
EOM = 0x03  # End of message

NULL_ADDRESS = ["00:00:00:00:00:00"]  # Default value for broadcast mode
DELIMITER = '|'  # Delimiter for the message


# ESP-NOW Control Class
class ESPNOWControl:
    def __init__(self, serial_port: str = "/dev/cu.wchusbserial1140" , mac_addresses: list = NULL_ADDRESS) -> None:
        """
        @description: Initialize the serial connection and send the MAC addresses
        @param       {*} self: -
        @param       {str} serial_port: The serial port to connect to
        @param       {list} mac_addresses: The list of MAC addresses to send
        @return      {*} None
        """
        if self._init_serial(serial_port):
            print("Serial connection established")
        else:
            raise Exception("Serial connection failed")
        print("ESP-NOW Control Initialized Successfully")
        if (
            mac_addresses == NULL_ADDRESS
        ): 
            print("No MAC addresses provided, broadcast mode enabled")
            self.broadcast_mode = True
            self._send_mac_addresses(NULL_ADDRESS) #TODO: Consider keeping the null address only in arduino
        else:
            self.broadcast_mode = False
            self._send_mac_addresses(mac_addresses)

    def _pack_message(self, raw_message: str) -> bytes:
        """
        @description: Pack the message with the SOM, EOM, and checksum
        @param       {*} self: -
        @param       {str} raw_message: The raw message as a string
        @return      {bytes} The packed message
        """
        message = struct.pack("B", SOM)  # Start of message
        message += struct.pack("B", len(raw_message))  # Length of message
        message += raw_message.encode() # Message body
        message += struct.pack("B", self._checksum(raw_message)) # Checksum
        message += struct.pack("B", EOM) # End of message
        return message

    def _checksum(self, raw_message: str) -> int:
        """
        @description: Calculate the checksum of the message
        @param       {*} self: -
        @param       {str} raw_message: The raw message as a string
        @return      {int} The checksum of the message
        """
        checksum = 0
        for char in raw_message:
            checksum ^= ord(char) # XOR
        return checksum
    
    def _send_mac_addresses(self, mac_addresses: list) -> None:
        print("Sending MAC addresses...")
        while True:
            raw_message = 'M|' + DELIMITER.join(mac_addresses)
            message = self._pack_message(raw_message)
            self.serial.write(message)
            # TODO: Implement feedback from the ESP32
            try:
                incoming = self.serial.readline().decode(errors="ignore").strip()
                print(incoming)
                if incoming == ("Received MAC addresses: " + str(len(mac_addresses))):
                    print("MAC addresses sent successfully!")
                    break
            except UnicodeDecodeError:
                print("Received malformed data!")
            time.sleep(0.5)

    def send(self, control_params: list, channel: int = 0, slave_index: int = -1) -> None:
        raw_massage = control_params.copy()
        if (
            self.broadcast_mode or slave_index == -1
        ):  # Empty mac_addresses or slaveindex is -1
            raw_massage.append(channel)
            raw_massage.append(-1)
        else:  # Mac addresses are provided and slaveindex is not -1
            raw_massage.append(-1)
            raw_massage.append(slave_index)
        # Format the message
        message = self._pack_message('C|' + DELIMITER.join(map(str, raw_massage)))
        self.serial.write(message)
        try:
            incoming = self.serial.readline().decode(errors="ignore").strip()
            print("Sending " + incoming)
        except UnicodeDecodeError:
            print("Received malformed data!")
            
    def _init_serial(self, serial_port: str) -> bool:
        """
        @description: Initialize the serial connection
        @param       {*} self: -
        @param       {str} serial_port: The serial port to connect to
        @return      {bool} True if the connection is successful, False otherwise
        """
        try:
            self.serial = serial.Serial(serial_port, 115200)
            print(f"Connected to port {serial_port}")
            while self.serial.in_waiting:  # Clear the buffer
                self.serial.read(self.serial.in_waiting)
            time.sleep(1)
            return True
        except serial.SerialException as e:
            print(f"Failed to connect to port {serial_port}. Error: {e}")
            return False
        
    def close(self) -> None:
        """
        @description: Close the serial connection
        @param       {*} self: -
        @return      {*} None
        """
        if self.serial.is_open:
            self.serial.close()
            print("Serial connection closed.")
