import tkinter as tk
import serial.tools.list_ports
from cantact_python.cantact_device import CantactDevice
from cantact_python.isotp_interface import IsotpInterface
from cantact_python.uds_client import UdsClient
from datetime import datetime

class MainWindow:
    def __init__(self, master):
        self.master = master
        master.title("CANtact Application")
        
        self.master.geometry("600x400")
        
        self.cantact_device = CantactDevice()
        self.isotp_interface = IsotpInterface(self.cantact_device)
        self.uds_client = UdsClient(self.isotp_interface)
        log_filename = datetime.now().strftime("can_messages_%Y-%m-%d_%H-%M-%S.log")
        self.log_file = log_filename

        self.is_dark_mode = False
        self.theme_button = tk.Button(master, text="Toggle Theme", command=self.toggle_theme)
        self.theme_button.pack(pady=10)
        
        # Serial ports Listbox
        self.ports_label = tk.Label(master, text="Serial Ports:")
        self.ports_label.pack()

        self.ports_listbox = tk.Listbox(master)
        self.ports_listbox.pack()
        self.ports_listbox.bind('<<ListboxSelect>>', self.on_port_select)
        self.update_ports_list()
        
        # Message frame
        self.message_frame = tk.Frame(master)
        self.message_frame.pack(fill=tk.BOTH, expand=True)

        self.can_message_label = tk.Label(self.message_frame, text="CAN Messages:")
        self.can_message_label.grid(row=0, column=0, sticky="w")

        self.can_message_text = tk.Text(self.message_frame, height=10, width=50)
        self.can_message_text.grid(row=1, column=0, padx=5, pady=5)

        self.log_message_label = tk.Label(self.message_frame, text="Log Messages:")
        self.log_message_label.grid(row=0, column=1, sticky="w")

        self.log_message_text = tk.Text(self.message_frame, height=10, width=50)
        self.log_message_text.grid(row=1, column=1, padx=5, pady=5)

        # Text box to write messages to send
        self.send_message_label = tk.Label(master, text="Message to Send:")
        self.send_message_label.pack()

        self.send_message_entry = tk.Entry(master, width=50)
        self.send_message_entry.pack()

        # Send button
        self.send_button = tk.Button(master, text="Send", command=self.send_message)
        self.send_button.pack(pady=10)

        # Filter entry and buttons
        self.filter_entry = tk.Entry(master, width=50)
        self.filter_entry.pack()
        self.filter_button = tk.Button(master, text="Apply Filter", command=self.apply_filter)
        self.filter_button.pack(pady=5)
        self.clear_filter_button = tk.Button(master, text="Clear Filter", command=self.clear_filter)
        self.clear_filter_button.pack(pady=5)
        self.message_filter = None

        # Clear Output button
        self.clear_output_button = tk.Button(master, text="Clear Output", command=self.clear_output)
        self.clear_output_button.pack(pady=5)

        self.seen_messages = set()
    
    def update_ports_list(self):
        """Updates the listbox with available serial ports."""
        self.ports_listbox.delete(0, tk.END)
        ports = serial.tools.list_ports.comports()
        usable_ports = []
        hidden_ports = []

        for port, desc, hwid in sorted(ports):
            try:
                test_device = CantactDevice(port=port)
                test_device.open()
                test_device.close()
                usable_ports.append(f"{port} - {desc}")
            except Exception:
                hidden_ports.append(f"{port} - {desc}")

        for port in usable_ports:
            self.ports_listbox.insert(tk.END, port)

        if hidden_ports:
            self.more_button = tk.Button(self.master, text="More", command=lambda: self.show_hidden_ports(hidden_ports))
            self.more_button.pack()

    def show_hidden_ports(self, hidden_ports):
        """Displays hidden ports in a new window."""
        hidden_window = tk.Toplevel(self.master)
        hidden_window.title("Hidden Ports")

        hidden_listbox = tk.Listbox(hidden_window)
        hidden_listbox.pack()

        for port in hidden_ports:
            hidden_listbox.insert(tk.END, port)
            
    def on_port_select(self, event):
        """Opens the selected serial port."""
        selection = self.ports_listbox.curselection()
        if selection:
            selected_port = self.ports_listbox.get(selection[0]).split(" - ")[0]
            try:
                self.cantact_device.open(selected_port)
                self.add_message(f"Port {selected_port} opened.", is_can_message=False)
                self.start_receiving()
            except Exception as e:
                self.add_message(f"Error opening port: {e}", is_can_message=False)
    
    def start_receiving(self):
        """Starts a loop to receive messages."""
        try:
            received_data = self.cantact_device.receive()
            if received_data:
                message = received_data.hex()
                if not self.message_filter or self.message_filter in message:
                    if message in self.seen_messages:
                        self.add_message(f"Repeated: {message}", is_can_message=True)
                    else:
                        self.add_message(f"New: {message}", is_can_message=True)
                        self.seen_messages.add(message)
        except Exception as e:
            self.add_message(f"Error receiving: {e}", is_can_message=False)
        
        self.master.after(100, self.start_receiving)
            
    def send_message(self):
        """Sends a message to the CAN bus and logs it."""
        message = self.send_message_entry.get()
        try:
            self.uds_client.send(bytes.fromhex(message))
            self.add_message(f"Sent: {message}", is_can_message=False)
            self.log_message(f"Sent: {message}")
        except Exception as e:
            error_message = f"Error sending: {e}"
            self.add_message(error_message, is_can_message=False)
            self.log_message(error_message)

    def log_message(self, message):
        """Logs a message to the log file."""
        with open(self.log_file, "a") as log:
            log.write(message + "\n")

    def add_message(self, message, is_can_message=False):
        """Adds a message to the appropriate text box."""
        if is_can_message:
            self.can_message_text.insert(tk.END, message + "\n")
            self.can_message_text.see(tk.END)
        else:
            self.log_message_text.insert(tk.END, message + "\n")
            self.log_message_text.see(tk.END)

    def toggle_theme(self):
        """Toggles between light and dark themes."""
        if self.is_dark_mode:
            self.master.configure(bg="white")
            self.ports_label.configure(bg="white", fg="black")
            self.can_message_label.configure(bg="white", fg="black")
            self.log_message_label.configure(bg="white", fg="black")
            self.send_message_label.configure(bg="white", fg="black")
            self.can_message_text.configure(bg="white", fg="black")
            self.log_message_text.configure(bg="white", fg="black")
            self.send_message_entry.configure(bg="white", fg="black")
            self.theme_button.configure(bg="white", fg="black")
            self.is_dark_mode = False
        else:
            dark_grey = "#2E2E2E"
            self.master.configure(bg=dark_grey)
            self.ports_label.configure(bg=dark_grey, fg="white")
            self.can_message_label.configure(bg=dark_grey, fg="white")
            self.log_message_label.configure(bg=dark_grey, fg="white")
            self.send_message_label.configure(bg=dark_grey, fg="white")
            self.can_message_text.configure(bg=dark_grey, fg="white")
            self.log_message_text.configure(bg=dark_grey, fg="white")
            self.send_message_entry.configure(bg=dark_grey, fg="white")
            self.theme_button.configure(bg=dark_grey, fg="white")
            self.is_dark_mode = True

    def apply_filter(self):
        """Applies a filter to the received messages."""
        filter_text = self.filter_entry.get()
        if filter_text:
            self.message_filter = filter_text
            self.add_message(f"Filter applied: {filter_text}", is_can_message=False)
        else:
            self.message_filter = None
            self.add_message("Filter cleared.", is_can_message=False)

    def clear_filter(self):
        """Clears the current message filter."""
        self.message_filter = None
        self.filter_entry.delete(0, tk.END)
        self.add_message("Filter cleared.", is_can_message=False)

    def clear_output(self):
        """Clears the output terminal."""
        self.can_message_text.delete(1.0, tk.END)
        self.log_message_text.delete(1.0, tk.END)

def main():
    root = tk.Tk()
    ui = MainWindow(root)
    root.mainloop()

