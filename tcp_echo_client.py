import asyncio

class EchoClientProtocol(asyncio.Protocol):
    def __init__(self, message, loop):
        self.message = message
        self.loop = loop

    def connection_made(self, transport):
        transport.write(self.message.encode())
        print('Data sent: {!r}'.format(self.message))

    def data_received(self, data):
        print('Data received: {!r}'.format(data.decode()))

    def connection_lost(self, exc):
        print('The server closed the connection')
        print('Stop the event loop')
        self.loop.stop()

loop = asyncio.get_event_loop()
message = 'Hello World!'

async def connect():
    while True:
        try:
            await loop.create_connection(lambda: EchoClientProtocol(message, loop), '127.0.0.1', 8888)
        except ConnectionRefusedError:
            print("Server is not up, retry in 1 second...")
            await asyncio.sleep(1)
        else:
            break

loop.run_until_complete(connect())
try:
    loop.run_forever()
except KeyboardInterrupt:
    print("exit")
loop.close()