from Connection.SocketManager import SocketClientManager

class PLCEthernetClient(SocketClientManager):

    def __init__(self, mainWindow):
        SocketClientManager.__init__(self, mainWindow, "PLCEthernetClient")