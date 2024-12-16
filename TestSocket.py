import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
from CommonAssit import TimeControl

def connect(host, port):
    sock.connect((host, port))

if __name__ == '__main__':
    connect("192.168.3.10", 2100)
    TimeControl.sleep(100000)