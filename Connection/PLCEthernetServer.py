from Connection.SocketManager import SocketServerManager

class PLCEthernetServer(SocketServerManager):

    def __init__(self, mainWindow):
        SocketServerManager.__init__(self, mainWindow, "PLCEthernetServer")