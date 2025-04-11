class UdsClient:
    def __init__(self, isotp_interface):
        """
        Initializes the UDS client with an ISO-TP interface.
        This class will implement the methods to interact with the UDS protocol
        It will need to send and receive UDS messages.
        It will use the IsotpInterface to send and receive frames

        Args:
            isotp_interface: An instance of the IsotpInterface class.
        """
        self.isotp_interface = isotp_interface

    def send_message(self, service_id, sub_function=None, data=None):
        """
        Sends a UDS message.

        Args:
            service_id (int): The UDS service ID.
            sub_function (int, optional): The UDS sub-function. Defaults to None.
            data (list, optional): The data payload. Defaults to None.

        Returns:
            bool: True if the message was sent, False otherwise.
        """
        message = [service_id]
        if sub_function is not None:
            message.append(sub_function)
        if data is not None:
            message.extend(data)

        return self.isotp_interface.send_frame(message)

    def receive_message(self, timeout=1.0):
        """
        Receives a UDS message.

        Args:
            timeout (float, optional): The timeout for receiving a message in seconds. Defaults to 1.0.

        Returns:
            list or None: The received message as a list of integers, or None if no message was received.
        """
        return self.isotp_interface.receive_frame(timeout)