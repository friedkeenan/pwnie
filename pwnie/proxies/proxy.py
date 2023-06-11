import asyncio
import importlib.resources
import io
import ssl
import pak

from public import public

from .. import resources

from ..packets import (
    ServerboundMasterPacket,
    ClientboundMasterPacket,
    ServerboundGamePacket,
    ClientboundGamePacket,
    master,
    game,
)

@public
class Proxy(pak.AsyncPacketHandler):
    class CommonConnection(pak.io.Connection):
        MAX_PACKET_LENGTH = 0x4000

        IS_MASTER = False

        _listen_sequentially = False

        def __init__(self, group, *, destination=None, ctx=None, **kwargs):
            self.group       = group
            self.destination = destination

            super().__init__(ctx=ctx, **kwargs)

        def is_closing(self):
            if self.destination is None:
                return pak.io.Connection.is_closing(self)

            return pak.io.Connection.is_closing(self) or pak.io.Connection.is_closing(self.destination)

        def close(self):
            self.group._remove_from_proxy()

            if self.destination is not None:
                pak.io.Connection.close(self.destination)

            pak.io.Connection.close(self)

        async def wait_closed(self):
            if self.destination is not None:
                await pak.io.Connection.wait_closed(self.destination)

            await pak.io.Connection.wait_closed(self)

        async def write_packet_instance(self, packet):
            await self.write_data(packet.pack(ctx=self.ctx))

    class MasterServerConnection(CommonConnection):
        IS_MASTER = True

        _listen_sequentially = True

        _UNSET_SERVERBOUND_PACKET = pak.util.UniqueSentinel()

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self._last_serverbound_packet = self._UNSET_SERVERBOUND_PACKET

        async def continuously_read_packets(self):
            data = await self.reader.read(self.MAX_PACKET_LENGTH)
            if len(data) <= 0:
                self.close()
                await self.wait_closed()

                return

            data = io.BytesIO(data)

            initial_header = master.clientbound.ServerInfoPacket.Header.unpack(data, ctx=self.ctx)
            if initial_header.magic != master.clientbound.ServerInfoPacket.magic:
                return

            yield master.clientbound.ServerInfoPacket.unpack(data, ctx=self.ctx)

            async for packet in super().continuously_read_packets():
                yield packet

        async def _read_next_packet(self):
            packet_data = await self.reader.read(self.MAX_PACKET_LENGTH)
            if len(packet_data) <= 0:
                return None

            if self._last_serverbound_packet.RESPONSE is None:
                raise ValueError(f"Unexpected response from '{self._last_serverbound_packet.__qualname__}")

            packet_cls = self._last_serverbound_packet.RESPONSE
            if packet_cls is ServerboundMasterPacket.UNKNOWN_RESPONSE:
                packet_cls = ClientboundMasterPacket.Generic

            self._last_serverbound_packet = self._UNSET_SERVERBOUND_PACKET

            return packet_cls.unpack(packet_data, ctx=self.ctx)

        async def write_packet_instance(self, packet):
            if (
                self._last_serverbound_packet is not self._UNSET_SERVERBOUND_PACKET and

                self._last_serverbound_packet.RESPONSE is not None and

                self._last_serverbound_packet.RESPONSE is not ServerboundMasterPacket.UNKNOWN_RESPONSE
            ):
                raise ValueError(
                    f"Attempted to write '{type(packet).__qualname__}' before reading "
                    f"response to '{type(self._last_serverbound_packet).__qualname__}'"
                )

            await self.write_data(packet.pack(ctx=self.ctx))

            self._last_serverbound_packet = packet

    class MasterClientConnection(CommonConnection):
        IS_MASTER = True

        _listen_sequentially = True

        async def _read_next_packet(self):
            data = await self.reader.read(self.MAX_PACKET_LENGTH)
            if len(data) <= 0:
                return None

            data = io.BytesIO(data)

            header = ServerboundMasterPacket.Header.unpack(data, ctx=self.ctx)

            packet_cls = ServerboundMasterPacket.subclass_with_id(header.id, ctx=self.ctx)
            if packet_cls is None:
                packet_cls = ServerboundMasterPacket.GenericWithID(header.id)

            return packet_cls.unpack(data, ctx=self.ctx)

    class GameServerConnection(CommonConnection):
        async def continuously_read_packets(self):
            data = await self.reader.read(self.MAX_PACKET_LENGTH)
            if len(data) <= 0:
                self.close()
                await self.wait_closed()

                return

            yield game.clientbound.InitialPlayerInfoPacket.unpack(data, ctx=self.ctx)

            async for packet in super().continuously_read_packets():
                yield packet

        async def _read_next_packet(self):
            data = await self.reader.read(self.MAX_PACKET_LENGTH)
            if len(data) <= 0:
                return None

            data = io.BytesIO(data)

            header = ClientboundGamePacket.Header.unpack(data, ctx=self.ctx)

            packet_cls = ClientboundGamePacket.subclass_with_id(header.id, ctx=self.ctx)
            if packet_cls is None:
                packet_cls = ClientboundGamePacket.GenericWithID(header.id)

            return packet_cls.unpack(data, ctx=self.ctx)

    class GameClientConnection(CommonConnection):
        async def continuously_read_packets(self):
            data = await self.reader.read(self.MAX_PACKET_LENGTH)
            if len(data) <= 0:
                self.close()
                await self.wait_closed()

                return

            yield game.serverbound.JoinGameServerPacket.unpack(data, ctx=self.ctx)

            async for packet in super().continuously_read_packets():
                yield packet

        async def _read_next_packet(self):
            data = await self.reader.read(self.MAX_PACKET_LENGTH)
            if len(data) <= 0:
                return None

            data = io.BytesIO(data)

            header = ServerboundGamePacket.Header.unpack(data, ctx=self.ctx)

            packet_cls = ServerboundGamePacket.subclass_with_id(header.id, ctx=self.ctx)
            if packet_cls is None:
                packet_cls = ServerboundGamePacket.GenericWithID(header.id)

            return packet_cls.unpack(data, ctx=self.ctx)

    class ConnectionGroup:
        class ServerAndClient:
            def __init__(self):
                self.server = None
                self.client = None

        def __init__(self, proxy):
            self.proxy = proxy

            self.master = self.ServerAndClient()
            self.game   = self.ServerAndClient()

        def _remove_from_proxy(self):
            try:
                self.proxy.connections.remove(self)

            # We may have already been removed.
            except ValueError:
                pass

    def __init__(
        self,
        *,
        host_address     = None,
        host_master_port = 3334,

        conveyed_game_address = "localhost",
        host_game_port        = 2999,

        host_certificate = None,
        host_keyfile     = None,

        master_server_address = "master.pwn3",
        master_server_port    = 3333,
    ):
        super().__init__()

        self.host_address     = host_address
        self.host_master_port = host_master_port

        self.conveyed_game_address = conveyed_game_address
        self.host_game_port        = host_game_port

        self.master_server_address = master_server_address
        self.master_server_port    = master_server_port

        self.master_srv = None
        self.game_srv   = None

        self.connections = []

        self._game_server_info = {}

        if host_certificate is None:
            resource_dir = importlib.resources.files(resources)

            with (
                importlib.resources.as_file(resource_dir / "server.crt") as builtin_certificate,
                importlib.resources.as_file(resource_dir / "server.key") as builtin_keyfile,
            ):
                self._setup_ssl(builtin_certificate, builtin_keyfile)

        else:
            self._setup_ssl(host_certificate, host_keyfile)

    def _setup_ssl(self, certificate, keyfile):
        # NOTE: Both the official client and official server
        # use old versions of OpenSSL, necessitating some
        # unfortunate settings we must use.

        self._server_ssl = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        self._server_ssl.minimum_version = ssl.TLSVersion.TLSv1
        self._server_ssl.set_ciphers("DEFAULT@SECLEVEL=0")

        self._server_ssl.load_cert_chain(certificate, keyfile)

        self._client_ssl = ssl.create_default_context()
        self._client_ssl.minimum_version = ssl.TLSVersion.TLSv1
        self._client_ssl.set_ciphers("DEFAULT@SECLEVEL=1")

        # We don't bother verifying the server's certificate.
        self._client_ssl.check_hostname = False
        self._client_ssl.verify_mode    = ssl.VerifyMode.CERT_NONE

    def is_serving(self):
        return (
            (self.master_srv is not None and self.master_srv.is_serving()) and

            (self.game_srv is not None and self.game_srv.is_serving())
        )

    def close(self):
        if self.master_srv is not None:
            self.master_srv.close()

        if self.game_srv is not None:
            self.game_srv.close()

    async def wait_closed(self):
        if self.master_srv is not None:
            await self.master_srv.wait_closed()

        if self.game_srv is not None:
            await self.game_srv.wait_closed()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, exc_tb):
        self.close()
        await self.wait_closed()

    async def _listen_to_packet(self, source_conn, packet):
        async with self.listener_task_group(listen_sequentially=source_conn._listen_sequentially) as group:
            listeners = self.listeners_for_packet(packet)

            async def proxy_wrapper():
                results = await asyncio.gather(*[listener(source_conn, packet) for listener in listeners])

                if False in results:
                    return

                await source_conn.destination.write_packet_instance(packet)

            group.create_task(proxy_wrapper())

    async def _listen_impl(self, source_conn):
        async for packet in source_conn.continuously_read_packets():
            packet.make_immutable()

            await self._listen_to_packet(source_conn, packet)

    async def listen(self, client):
        async with asyncio.TaskGroup() as tg:
            tg.create_task(
                self._listen_impl(client)
            )

            while client.destination is None:
                if client.is_closing():
                    return

                await pak.util.yield_exec()

            tg.create_task(
                self._listen_impl(client.destination)
            )

    async def open_streams(self, address, port, *, ssl=None):
        return await asyncio.open_connection(address, port, ssl=ssl)

    async def new_master_connection(self, client_reader, client_writer):
        server_reader, server_writer = await self.open_streams(self.master_server_address, self.master_server_port, ssl=self._client_ssl)

        group = self.ConnectionGroup(self)

        group.master.client = self.MasterClientConnection(group, reader=client_reader, writer=client_writer)
        group.master.server = self.MasterServerConnection(group, destination=group.master.client, reader=server_reader, writer=server_writer)

        group.master.client.destination = group.master.server

        self.connections.append(group)

        await self.listen(group.master.client)

    async def open_master_server(self):
        return await asyncio.start_server(self.new_master_connection, self.host_address, self.host_master_port, ssl=self._server_ssl)

    async def new_game_connection(self, client_reader, client_writer):
        # NOTE: Not added to 'self.connections' because
        # it is only used until we know the real group.
        group = self.ConnectionGroup(self)

        group.game.client = self.GameClientConnection(group, reader=client_reader, writer=client_writer)

        await self.listen(group.game.client)

    async def open_game_server(self):
        return await asyncio.start_server(self.new_game_connection, self.host_address, self.host_game_port)

    async def startup(self):
        self.master_srv = await self.open_master_server()
        self.game_srv   = await self.open_game_server()

    async def on_start(self):
        async with asyncio.TaskGroup() as tg:
            tg.create_task(
                self.master_srv.serve_forever()
            )

            tg.create_task(
                self.game_srv.serve_forever()
            )

    async def start(self):
        await self.startup()

        async with self:
            await self.on_start()

    def run(self):
        try:
            asyncio.run(self.start())

        except KeyboardInterrupt:
            pass

    @pak.packet_listener(master.clientbound.JoinGamePacket)
    async def _redirect_game_server(self, source, packet):
        if packet.game_info is None:
            return True

        self._game_server_info[packet.game_info.game_server_token] = (
            source.group,

            packet.game_info.game_server_address,
            packet.game_info.game_server_port
        )

        await source.destination.write_packet_instance(
            packet.copy(
                game_info = packet.game_info.copy(
                    game_server_address = self.conveyed_game_address,
                    game_server_port    = self.host_game_port,
                ),
            )
        )

        return False

    @pak.packet_listener(game.serverbound.JoinGameServerPacket)
    async def _attach_game_connection(self, source, packet):
        try:
            group, address, port = self._game_server_info.pop(packet.game_server_token)

        except KeyError:
            source.close()
            await source.wait_closed()

            return

        server_reader, server_writer = await self.open_streams(address, port)

        group.game.client = source
        group.game.server = self.GameServerConnection(group, destination=source, reader=server_reader, writer=server_writer)

        source.destination = group.game.server
