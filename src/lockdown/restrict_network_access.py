import socket
import logging
from lockdown.no_internet_socket import NoInternetSocket
from lockdown.singleton import Singleton


class RestrictNetworkAccess(metaclass=Singleton):
    def __init__(self):
        self.__init_logger()
        self.original_socket = socket.socket
        self.original_socket_type = socket.SocketType

    def __init_logger(self):
        """
        Initializes the logger with a file handler and a specific format.
        """
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        # handler = logging.FileHandler('network_access_attempts.log')
        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)  # Set the handler's level to INFO
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def activate(self):
        self.logger.info("Installing network restrictions.")
        self.original_socket = socket.socket
        self.original_socket_type = socket.SocketType
        socket.socket = NoInternetSocket
        socket.SocketType = NoInternetSocket

    def deactivate(self):
        self.logger.info("Uninstalling network restrictions.")
        socket.socket = self.original_socket
        socket.SocketType = self.original_socket_type
