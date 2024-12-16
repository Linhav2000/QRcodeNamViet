from Connection.SocketManager import SocketClientManager
from Connection.ConnectionStatus import ConnectionStatus

class ServerClientManager(SocketClientManager):

    def __init__(self, mainWindow):
        SocketClientManager.__init__(self, mainWindow, "TCPServer")

    def connectServer(self):
        if self.connect():
            self.mainWindow.runningTab.setServerStatus(ConnectionStatus.connected)

    def disconnectSever(self):
        self.disconnect()
        self.mainWindow.runningTab.setServerStatus(ConnectionStatus.disconnected)

    def test(self):
        self.sendData("Test")

