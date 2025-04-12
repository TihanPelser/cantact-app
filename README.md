# CANtact Application

## Overview
The CANtact Application is a graphical user interface (GUI) tool for interacting with CAN (Controller Area Network) devices. It provides features for sending and receiving CAN messages, configuring devices, and performing diagnostics using the UDS (Unified Diagnostic Services) protocol.

## Features
- **Serial Port Management**: Automatically detects usable serial ports and allows users to connect to them. Hidden or unusable ports can be accessed via a "More" button.
- **CAN Communication**: Send and receive CAN messages using the CANtact device.
- **UDS Protocol Support**: Perform diagnostics using the UDS protocol.
- **User-Friendly Interface**: Intuitive GUI built with Python's Tkinter library.

## Requirements
- Python 3.10 or later
- Required Python packages:
  - `pyserial`
  - `cantact-python`

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/cantact-app.git
   cd cantact-app
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Run the application using the following command:
```bash
python main.py
```

## Recent Updates
- **11 April 2025**: Updated the serial port management to filter usable ports and hide the rest behind a "More" button.
- **11 April 2025**: Added logging functionality to save all sent messages and errors to a log file (`can_messages.log`).

## TODO List

### Planned Features
1. **Port Auto-Detection and Refresh**
   - Automatically refresh the list of available ports at regular intervals or when a new device is connected.

2. **Logging**
   - ~~Add a feature to log all sent and received CAN messages to a file for later analysis.~~

3. **Message Filtering**
   - ~~Allow users to filter received messages based on CAN IDs or data patterns.~~

4. **Customizable Message Templates**
   - Provide a way to save and reuse frequently sent CAN messages.

5. **Graphical Data Visualization**
   - Add a feature to plot CAN data in real-time, such as RPM, speed, or other sensor values.

6. **Error Handling and Diagnostics**
   - Display detailed error messages and diagnostics when communication issues occur.

7. **Multi-Device Support**
   - Allow simultaneous communication with multiple CANtact devices.

8. **Scripting Support**
   - Enable users to write and execute custom scripts for automated testing or diagnostics.

9. **Firmware Update Utility**
   - Add a feature to update the firmware of connected CANtact devices.

10. **Theme Customization**
    - ~~Provide light and dark mode options for the GUI.~~

11. **Protocol Support Expansion**
    - Add support for additional protocols like J1939 or CANopen.

12. **Export and Import Configurations**
    - Allow users to save and load their configurations, including port settings and message templates.

13. **Simulation Mode**
    - Add a mode to simulate CAN traffic for testing without requiring a physical device.

14. **Hotkey Support**
    - Add keyboard shortcuts for common actions like sending messages or refreshing the port list.

15. **Device Information Display**
    - Show detailed information about the connected CANtact device, such as firmware version and serial number.

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Submit a pull request with a detailed description of your changes.

## License
This project is licensed under the MIT License. See the `LICENSE.md` file for details.