import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
from CommonAssit import TimeControl

def connect(host, port):
    sock.connect((host, port))


if __name__ == '__main__':
    connect("192.168.1.126", 23)
    TimeControl.sleep(20000)