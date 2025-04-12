from cantact_python.can_frame import CanFrame

class IsotpInterface:
    def __init__(self, can_interface):
        """
        Initializes the ISO-TP interface.

        Args:
            can_interface: An object that implements send and receive methods for CAN frames.
        """
        self.can_interface = can_interface

    def send_isotp_frame(self, can_id, data):
        """
        Sends an ISO-TP frame.

        Args:
            can_id (int): The CAN ID for the frame.
            data (bytes): The data to be sent.

        Returns:
            bool: True if the frame was sent successfully, False otherwise.
        """
        if not isinstance(data, bytes):
            raise ValueError("Data must be bytes")

        data_length_bytes = len(data)

        if data_length_bytes <= 7:  # Single Frame (SF)
            sf_header = data_length_bytes & 0x0F
            sf_data = bytes([sf_header]) + data + bytes(7 - data_length_bytes)
            can_frame = CanFrame(can_id, sf_data)
            
            self.can_interface.send(can_frame)
            return True
        else:  # Multi-Frame (FF, CF)
            # First Frame (FF)
            ff_header = 0x10 | ((data_length_bytes >> 8) & 0x0F)
            ff_header2 = data_length_bytes & 0xFF
            ff_data = bytes([ff_header, ff_header2]) + data[:6]
            ff_data += bytes(6 - len(data[:6]))
            
            can_frame = CanFrame(can_id, ff_data)
            self.can_interface.send(can_frame)

            # Consecutive Frames (CF)
            sequence_number = 1
            for i in range(6, data_length_bytes, 7):
                cf_header = 0x20 | (sequence_number & 0x0F)
                cf_data = bytes([cf_header]) + data[i:i + 7]
                cf_data += bytes(7 - len(data[i:i + 7]))
                can_frame = CanFrame(can_id, cf_data)
                self.can_interface.send(can_frame)
                sequence_number += 1
                sequence_number %= 16  # Sequence number wraps around at 15
            return True

    def receive_isotp_frame(self, expected_can_id, timeout=5.0):
        """
        Receives an ISO-TP frame.

        Args:
            expected_can_id (int): The expected CAN ID for the frame.
            timeout: The timeout for receiving frames.

        Returns:
            bytes: The received data if successful, None otherwise.
        """
        received_data = b''
        total_data_length = 0
        consecutive_frame_counter = 1
        while True:
            received_can_frame = self.can_interface.receive(expected_can_id, timeout)
            if received_can_frame is None:
                return None
            can_frame = received_can_frame.data
            header = can_frame[0]            
            if (header & 0xF0) == 0x00:
                 #Single frame
                received_data += can_frame[1:1+ (header & 0x0F)]
                return received_data

            elif (header & 0xF0) == 0x10:  # First Frame (FF)
                if first_frame_received:
                    return None
                total_data_length = ((header & 0x0F) << 8) + can_frame[1]
                received_data += can_frame[2:8]
            
            elif (header & 0xF0) == 0x20:  # Consecutive Frame (CF)
                if total_data_length == 0:
                    return None
                current_sequence_number = header & 0x0F
                if current_sequence_number != consecutive_frame_counter:
                    return None
                consecutive_frame_counter += 1
                consecutive_frame_counter %= 16
                received_data += can_frame[1:8]
                
                if len(received_data) >= total_data_length:
                    received_data = received_data[:total_data_length]
                    return received_data
        return None