from View.Setting.EthernetSettingWindow import EthernetSettingView
import socket
import select
import tkinter.messagebox as messagebox
from CommonAssit.FileManager import CsvFile
from CommonAssit import TimeControl
import threading
from Connection.ConnectionStatus import ConnectionStatus

class SocketClientManager:
    retryTime = 0
    SEND_DATA_TIME_OUT = 3000
    ready = False
    sock = None

    def __init__(self, mainWindow, name="socketClient"):
        from MainWindow import MainWindow
        self.mainWindow:MainWindow = mainWindow
        self.name = name
        self.sockInfo = SocketInfo(name)

        # r, w, e = select.select([self.sock,], [self.sock,], (), 0)
        # # print(r, w, e)
        # # return True
        # if len(r) > 0:
        #     print(r,w,e)
        #     return False
        # else:
        #     return True

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.settimeout(0.2)
            self.sock.connect((self.sockInfo.host, self.sockInfo.port))
            self.ready = True
            return True
        except Exception as error:
            self.mainWindow.runningTab.insertLog("ERROR Ethernet connect: {}".format(error))
            return False

    def check_connection(self):
        if self.sock is None:
            return
        try:
            self.sock.send(b" ")
        except Exception as error:
            self.sock.close()
            self.isConnected = False
            self.mainWindow.workingThread.plcReadingFlag = False

    def setting(self):
        plcEthernetSetting = EthernetSettingView(self.mainWindow,self.sockInfo, title="{} Socket Setting".format(self.name))

    def sendData(self, data):
        if self.ready:
            try:
                self.sock.sendall(data.encode('utf-8'))
            except:
                pass
        else:
            messagebox.showerror("Server Connection", "Server connection is lost!")
            self.mainWindow.runningTab.insertLog("Server connection is lost!")

    def readData(self):
        if not self.ready:
            # messagebox.showerror("Server Connection", "Server connection is lost!")
            self.mainWindow.runningTab.insertLog("Server connection is lost!")
            return ""
        ret = ""
        try:
            data = self.sock.recv(4096)
            if data == b"":
                self.disconnect()
            ret = data.decode('utf-8')
        except:
            pass
        return ret

    def disconnect(self):
        if not hasattr(self, 'sock'):
            self.ready = False
            return
        else:
            try:
                self.ready = False
                self.sock.close()
            except:
                pass


class SocketServerManager:
    isOpened = False
    isConnected = False
    # isWaitingConnection = False
    sock = None
    connection = None

    def __init__(self, mainWindow, name="socketServer"):
        from MainWindow import MainWindow
        self.mainWindow:MainWindow = mainWindow
        self.name = name
        self.sockInfo = SocketInfo(name)

    def open(self):
        if self.isOpened:
            self.mainWindow.runningTab.insertLog("Tcp/ip server is already open")
            return True

        try:
            # Create a TCP/IP socket
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Bind the socket to the port
            server_address = (self.sockInfo.host, self.sockInfo.port)
            print("starting up on port {}".format(server_address))
            self.sock.bind(server_address)
            self.sock.settimeout(0.5)
            # Listen for incoming connections
            self.sock.listen(1)
            self.isOpened = True
            thread = threading.Thread(target=self.acceptThread, args=())
            thread.start()
            return True
        except Exception as error:
            self.mainWindow.runningTab.insertLog("ERROR Open Tcp/ip server: {}".format(error))
            return False

    def acceptThread(self):
        while self.isOpened:

            if not self.isConnected:
                # Wait for a connection
                try:
                    self.mainWindow.runningTab.setPLCStatus(ConnectionStatus.waiting)
                    self.mainWindow.runningTab.insertLog("TCP/IP server waiting for a connection")
                    self.connection, client_address = self.sock.accept()
                    self.connection.settimeout(0.2)
                    self.mainWindow.runningTab.insertLog("TCP/IP server connected to {} successfully!".format(client_address))
                    self.isConnected = True
                    self.mainWindow.runningTab.setPLCStatus(ConnectionStatus.connected)
                except:
                    pass
            else:
                self.checkConnection()
            TimeControl.sleep(3)

    def checkConnection(self):
        if self.connection is None:
            return
        try:
            self.connection.send(b"")
        except Exception as error:
            self.connection.close()
            self.isConnected = False
            # self.mainWindow.workingThread.plcReadingFlag = False

        # return True
        # if len(r) > 0:
        #     print(r,w,e)
        #     return False
        # else:
        #     return True

    def close(self):
        self.isOpened = False
        self.isConnected = False
        try:
            self.connection.close()
        except:
            pass
        try:
            self.sock.close()
        except:
            pass


    def setting(self):
        plcEthernetSetting = EthernetSettingView(self.mainWindow,self.sockInfo, title="{} Socket Setting".format(self.name))

    def sendAsciiData(self, data):
        if self.isConnected:
            try:
                self.connection.sendall(data.encode("utf-8"))
                self.mainWindow.runningTab.insertLog("Tcp/ip server send : {}".format(data))
            except Exception as error:
                self.isConnected = False
                self.connection.close()
                self.mainWindow.runningTab.insertLog("ERROR Tcp/ip server send data: {}".format(error))
        else:
            self.mainWindow.runningTab.insertLog("Send data: Tcp/ip server is not connected")

    def readAsciiData(self):
        recv = ""
        if self.isConnected:
            try:
                data = self.connection.recv(4096)
                if data == b"":
                    self.connection.close()
                    self.isConnected = False
                recv += data.decode("utf-8")
            except:
                pass
        return recv

class SocketInfo:
    HOST_IDX = 0
    PORT_IDX = 1

    host = "192.16.1.1"
    port = 1000

    filePath = "./config/PLCEthernet.csv"

    def __init__(self, name):
        self.filePath = "./config/{0}.csv".format(name)
        self.getInfo()

    def save(self):
        fileManager = CsvFile(filePath=self.filePath)

        fileManager.readFile()
        if len(fileManager.dataList) < 1:
            fileManager.dataList.append([0])
        fileManager.dataList[0] = ([self.host, self.port])
        fileManager.saveFile()

    def getInfo(self):
        fileManager = CsvFile(self.filePath)
        dataList = fileManager.readFile()

        if len(dataList) < 1:
            return
        data = dataList[0]
        if len(data) < 2:
            return

        self.host = data[self.HOST_IDX]
        self.port = int(data[self.PORT_IDX])

        return