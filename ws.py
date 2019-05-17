import asyncio
import signal

from lncityws.factories import LNCityWebsocketServerFactory
from lncityws.protocols import LNCityWebsocketServerProtocol

if __name__ == '__main__':

    # Get loop
    loop = asyncio.get_event_loop()

    # Create factory and set WS protocol
    factory = LNCityWebsocketServerFactory(loop=loop)
    factory.protocol = LNCityWebsocketServerProtocol
    factory.setProtocolOptions(autoPingInterval=10, maxConnections=10)

    # Start server
    loop.run_until_complete(factory.start())
    coro = loop.create_server(factory, '127.0.0.1', 9000)
    server = loop.run_until_complete(asyncio.wait_for(coro, timeout=5))

    # Add signal handling
    async def shutdown():
        await factory.stop()
        server.close()

        # Wait for all tasks to finish
        await asyncio.sleep(5)

        loop.stop()

    # To run on Windows machines we need to catch NotImplementedError exception
    # add_signal_handler is not supported on Windows OS
    try:
        loop.add_signal_handler(signal.SIGINT, lambda: asyncio.ensure_future(shutdown()))
        loop.add_signal_handler(signal.SIGTERM, lambda: asyncio.ensure_future(shutdown()))
    except NotImplementedError:
        pass

    # Run forever
    try:
        loop.run_forever()
    finally:
        loop.close()
