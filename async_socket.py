import asyncio


class EchoClientProtocol(asyncio.Protocol):
    def __init__(self, message, on_con_lost):
        self.message = message
        self.on_con_lost = on_con_lost

    def connection_made(self, transport):
        transport.write(self.message.encode())
        print(f'Data sent: {self.message}')

    def data_received(self, data):
        print(f'Data received: {data.decode()}')

    def connection_lost(self, exc):
        print('The server closed the connection')
        self.on_con_lost.set_result(True)


async def main():
    loop = asyncio.get_running_loop()
    on_con_lost = loop.create_future()
    message = 'Hello World!'

    transport_one, protocol = await loop.create_connection(
        lambda: EchoClientProtocol(message, on_con_lost),
        '127.0.0.1', 50007)

    transport_two, protocol2 = await loop.create_connection(
        lambda: EchoClientProtocol(message, on_con_lost),
        '127.0.0.1', 50008)


    try:
        await on_con_lost
    finally:
        transport_one.close()
        transport_two.close()


asyncio.run(main())
