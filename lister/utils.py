from .enums import ConnectionStatus
from .models import ConnectedLister, ConnectionRequest

def check_connection_status(user: int, lister: int):
    conn_status = ConnectionStatus.DISCONNECTED
    if ConnectedLister.objects.filter(user_id=user, lister_id=lister).exists():
        conn_status = ConnectionStatus.CONNECTED
    elif ConnectionRequest.objects.filter(sender_id=lister, receiver_id=user).exists():
        conn_status = ConnectionStatus.RECEIVED
    elif ConnectionRequest.objects.filter(sender_id=user, receiver_id=lister).exists():
        conn_status = ConnectionStatus.SENT
    
    return conn_status


def is_lister(me: int, lister: int) -> bool:
    return ConnectedLister.objects.filter(user=me, lister=lister).exists()


async def ais_lister(me: int, lister: int):
    return await ConnectedLister.objects.filter(user=me, lister=lister).aexists()