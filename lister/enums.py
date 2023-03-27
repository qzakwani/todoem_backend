from enum import Enum

class ConnectionStatus(Enum):
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    SENT = "sent"
    RECEIVED = "received"
    PRIVATE = "private"