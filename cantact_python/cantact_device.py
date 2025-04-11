import serial
import time
import serial.tools.list_ports

class CantactDevice:
    def __init__(self, port=None, baudrate=115200, timeout=1):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial_connection = None

    def open(self):
        """Opens the serial connection."""
        if self.serial_connection is not None and self.serial_connection.is_open:
            print("Serial port is already open.")
            return

        try:
            if self.port is None:
                pass
                #available_ports = [port.device for port in serial.tools.list_ports.comports()]
                #if not available_ports:
                #    raise Exception("No serial ports available.")
                #self.port = available_ports[0]

            #self.serial_connection = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
            #time.sleep(2) # wait for the device to be ready
            #print(f"Serial connection opened on {self.port} at {self.baudrate} baud.")
        except Exception as e:
            self.serial_connection = None
            raise Exception(f"Failed to open serial port {self.port}: {e}")

    def close(self):
        """Closes the serial connection."""
        if self.serial_connection is not None and self.serial_connection.is_open:
            self.serial_connection.close()
            print("Serial connection closed.")
        else:
            print("No serial connection to close.")
        self.serial_connection = None

    def send(self, data):
        """Sends data through the serial connection."""
        if self.serial_connection is None or not self.serial_connection.is_open:
            raise Exception("Serial connection is not open.")

        try:
            self.serial_connection.write(data)
            print(f"Sent: {data.hex()}")
        except Exception as e:
            
            raise Exception(f"Failed to send data: {e}")

    def receive(self):
        """Receives data from the serial connection."""
        if self.serial_connection is None or not self.serial_connection.is_open:
            raise Exception("Serial connection is not open.")

        try:
            data = bytes()
            time_out = 1
            start_time = time.time()
            while True:
                if self.serial_connection.in_waiting > 0:
                    data += self.serial_connection.read(1)
                if time.time() - start_time > time_out:
                    break
            if len(data) > 0:
                print(f"Received: {data.hex()}")
            return data
        except Exception as e:
            raise Exception(f"Failed to receive data: {e}")