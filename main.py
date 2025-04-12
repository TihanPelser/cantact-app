from cantact_python.cantact_device import CantactDevice
from cantact_python.can_frame import CanFrame
from cantact_python.isotp_interface import IsotpInterface
from cantact_python.uds_client import UdsClient
from cantact_python.ui import MainWindow
import tkinter as tk


def main():
    """Main function to run the application."""
    root = tk.Tk()
    window = MainWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()