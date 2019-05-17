
import asyncio

from time import time
from typing import Dict

from autobahn.asyncio.websocket import WebSocketServerFactory

from lncityws.protocols import LNCityWebsocketServerProtocol


class LNCityWebsocketServerFactory(WebSocketServerFactory):
    MAX_UNAUTHENTICATED_TIME = 30

    def __init__(self, loop: asyncio.AbstractEventLoop, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._loop: asyncio.AbstractEventLoop = loop
        self._connections_lock = asyncio.Lock()
        self._connections: Dict[LNCityWebsocketServerProtocol, float] = {}

    def start(self):
        pass

    def stop(self):
        pass

    async def on_connection_added(self, connection: LNCityWebsocketServerProtocol):
        async with self._connections_lock:
            self._connections[connection] = time()

    async def on_connection_removed(self, connection: LNCityWebsocketServerProtocol):
        async with self._connections_lock:
            if connection in self._connections:
                del self._connections[connection]
