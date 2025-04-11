import tkinter as tk
import serial.tools.list_ports
from .cantact_device import CantactDevice
from .isotp_interface import IsotpInterface
from .uds_client import UdsClient

class MainWindow:
    def __init__(self, master):
        self.master = master
        master.title("CANtact Application")
        
        self.master.geometry("600x400")
        
        self.cantact_device = CantactDevice()
        self.isotp_interface = IsotpInterface(self.cantact_device)
        self.uds_client = UdsClient(self.isotp_interface)

        
        # Serial ports Listbox
        self.ports_label = tk.Label(master, text="Serial Ports:")
        self.ports_label.pack()

        self.ports_listbox = tk.Listbox(master)
        self.ports_listbox.pack()
        self.ports_listbox.bind('<<ListboxSelect>>', self.on_port_select)
        self.update_ports_list()
        
        # Text box to show received messages
        self.received_messages_label = tk.Label(master, text="Received Messages:")
        self.received_messages_label.pack()

        self.received_messages_text = tk.Text(master, height=10, width=50)
        self.received_messages_text.pack()

        # Text box to write messages to send
        self.send_message_label = tk.Label(master, text="Message to Send:")
        self.send_message_label.pack()

        self.send_message_entry = tk.Entry(master, width=50)
        self.send_message_entry.pack()

        # Send button
        self.send_button = tk.Button(master, text="Send", command=self.send_message)
        self.send_button.pack(pady=10)
    
        
    def update_ports_list(self):
        """Updates the listbox with available serial ports."""
        self.ports_listbox.delete(0, tk.END)
        ports = serial.tools.list_ports.comports()
        for port, desc, hwid in sorted(ports):
            self.ports_listbox.insert(tk.END, f"{port} - {desc}")
            
    def on_port_select(self, event):
        """Opens the selected serial port."""
        selection = self.ports_listbox.curselection()
        if selection:
            selected_port = self.ports_listbox.get(selection[0]).split(" - ")[0]
            try:
                self.cantact_device.open(selected_port)
                self.add_message(f"Port {selected_port} opened.")
                self.start_receiving()
            except Exception as e:
                self.add_message(f"Error opening port: {e}")
    
    def start_receiving(self):
        """Starts a loop to receive messages."""
        try:
            received_data = self.cantact_device.receive()
            if received_data:
                self.add_message(f"Received: {received_data.hex()}")
        except Exception as e:
            self.add_message(f"Error receiving: {e}")
        
        self.master.after(100, self.start_receiving)
            
    def send_message(self):
        """Sends a message to the CAN bus."""
        message = self.send_message_entry.get()
        try:
            self.uds_client.send(bytes.fromhex(message))
            self.add_message(f"Sent: {message}")
        except Exception as e:
            self.add_message(f"Error sending: {e}")

    def add_message(self, message):
        """Adds a message to the output text box."""
        self.received_messages_text.insert(tk.END, message + "\n")
        self.received_messages_text.see(tk.END)

def main():
    root = tk.Tk()
    ui = MainWindow(root)
    root.mainloop()

