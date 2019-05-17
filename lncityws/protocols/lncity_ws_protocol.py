
import asyncio
import json

from typing import Optional
from time import time
from uuid import uuid4

from autobahn.asyncio.websocket import WebSocketServerProtocol

from lncityapi.controllers.userscontroller import get_user_by_auth_token
from lncityapi.models import User
from lncityws.messages.message import WSMessage
from lncityws.pubsub.mem_pubsub import mem_pubsub


class LNCityWebsocketServerProtocol(WebSocketServerProtocol):

    def __init__(self):
        super().__init__()
        self.loop = asyncio.get_event_loop()

        self.authenticated: bool = False
        self.user: Optional[User] = None

        self.connected_at: float = time()

        self.closing: bool = False

        self.authentication_lock: asyncio.Lock = asyncio.Lock()

    ##########################################
    # Connection Handling
    ##########################################

    async def onConnect(self, request):
        await self.factory.on_connection_added(self)

    async def onOpen(self):
        pass

    async def onClose(self, _was_clean, code, reason):
        # Mark connection removed
        await self.factory.on_connection_removed(self)

        # Clean up resource handler
        if self.resource_handler is not None:
            await self.resource_handler.shutdown()

    async def force_close(self, code: int, reason: str):
        self.closing = True
        self.sendClose(code=code, reason=reason)

    ##########################################
    # Message Handling
    ##########################################

    def on_subscription_message(self, obj):
        message = WSMessage(uuid4(), 'subcription', obj)
        self.send_to_ws(message)

    async def onMessage(self, payload: bytes, is_binary: bool):
        if not self.closing:
            message: Optional[WSMessage] = self._parse_message(payload, is_binary)

            if message is None:
                await self.force_close(4000, 'invalid message')
                return

            if self.is_authenticated():
                await self._handle_message(message)
            else:
                with await self.authentication_lock:
                    if not self.is_authenticated():
                        self.user = await self._authenticate(message)
                        if self.user is None:
                            await self.force_close(4001, 'invalid login')
                    else:
                        success = await self._handle_message(message)
                        if not success:
                            await self.force_close(4000, 'invalid message')

    async def _handle_message(self, message: WSMessage):

        if message.action == 'publish':
            topic = message.parameters.get('topic')
            if topic is None:
                return False

            mem_pubsub.publish(topic, message.body)

        elif message.action == 'subscribe':
            topic = message.parameters.get('topic')
            if topic is None:
                return False

            mem_pubsub.subscribe(topic, self, 'on_subscription_message')

        self.send_ack(message)

    ##########################################
    # Parsing
    ##########################################

    @staticmethod
    def _parse_message(payload: bytes, is_binary: bool) -> Optional[WSMessage]:
        try:
            if is_binary:
                message_dict = json.loads(payload.decode('utf8'))
            else:
                message_dict = json.loads(payload)
        except Exception as ex:
            return None
        else:
            if not isinstance(message_dict, dict):
                return None

            message: WSMessage = WSMessage(**message_dict)
            if not message.is_valid():
                return None

            return message

    ##########################################
    # Send
    ##########################################

    def send_to_ws(self, message: WSMessage):
        self.sendMessage(json.dumps(message.serializable()).encode('utf-8'))

    def send_ack(self, message: WSMessage):
        message_ack = WSMessage(message.identifier, '_ack', {})
        self.send_to_ws(message_ack)

    ##########################################
    # Authentication
    ##########################################

    def is_authenticated(self) -> bool:
        return self.authenticated

    @staticmethod
    async def _authenticate(message: WSMessage) -> Optional[User]:

        if message.action != 'login':
            return None

        auth_token = message.body.get('auth_token')
        if auth_token is None:
            return None

        user = get_user_by_auth_token(auth_token)

        if user is None:
            return None

        return user
