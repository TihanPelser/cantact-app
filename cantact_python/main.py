from cantact_device import CantactDevice
from can_frame import CanFrame
from isotp_interface import IsotpInterface
from uds_client import UdsClient
from ui import MainWindow


def main():
    """Main function to run the application."""
    window = MainWindow()
    window.mainloop()


if __name__ == "__main__":
    main()