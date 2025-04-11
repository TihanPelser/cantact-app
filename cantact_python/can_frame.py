class CanFrame:
    def __init__(self, can_id, data, is_extended=False, is_remote=False, is_error=False):
        self.can_id = can_id
        self.data = data
        self.is_extended = is_extended
        self.is_remote = is_remote 
        self.is_error = is_error 

    def __str__(self):
        """Returns a string representation of the CAN frame."""
        frame_type = "Extended" if self.is_extended else "Standard"  
        remote_flag = "Remote" if self.is_remote else "Data"  
        error_flag = "Error" if self.is_error else "No Error"  
        data_str = self.data.hex().upper()  
        return f"CAN Frame ({frame_type}, {remote_flag}, {error_flag}): ID = {self.can_id:#X}, Data = {data_str}"

    def to_bytes(self):
        """
        Converts the CAN frame to a byte array for transmission.
        """
        header_byte = 0  
        if self.is_extended:  
            header_byte |= 0x80  
        if self.is_remote:  
            header_byte |= 0x40  
        if self.is_error:  
            header_byte |= 0x20  
        
        if self.is_extended:  
            id_bytes = self.can_id.to_bytes(4, 'big')  
        else:  
            id_bytes = self.can_id.to_bytes(2, 'big')

        length_byte = len(self.data)  
        data_bytes = bytes(self.data)  
        return bytes([header_byte]) + id_bytes + bytes([length_byte]) + data_bytes  

    @staticmethod
    def from_bytes(frame_bytes):
        """
        Constructs a CAN frame object from a byte array received.
        """
        if len(frame_bytes) < 4:
            raise ValueError("Incomplete frame bytes provided.")

        header_byte = frame_bytes[0]  
        is_extended = (header_byte & 0x80) != 0  
        is_remote = (header_byte & 0x40) != 0  
        is_error = (header_byte & 0x20) != 0  

        if is_extended:  
            if len(frame_bytes) < 6:
                raise ValueError("Incomplete frame bytes provided for extended frame.")
            can_id = int.from_bytes(frame_bytes[1:5], 'big')  
            data_length_index = 5  
        else:  
            if len(frame_bytes) < 4:
                raise ValueError("Incomplete frame bytes provided for standard frame.")
            can_id = int.from_bytes(frame_bytes[1:3], 'big')  
            data_length_index = 3  

        data_length = frame_bytes[data_length_index]  
        data = frame_bytes[data_length_index + 1: data_length_index + 1 + data_length]  

        return CanFrame(can_id, data, is_extended, is_remote, is_error)  