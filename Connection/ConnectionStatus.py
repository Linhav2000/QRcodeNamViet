import enum

class ConnectionStatus(enum.Enum):
    connected = "Connected"
    disconnected = "Disconnected"
    reconnecting = "Reconnecting"
    waiting = "Waiting"