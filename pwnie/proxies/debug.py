import pak

from aioconsole import aprint

from public import public

from .proxy import Proxy

from ..packets import Packet, ServerboundPacket

@public
class LoggingProxy(Proxy):
    LOG_GENERIC_PACKETS = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.LOG_GENERIC_PACKETS:
            self.register_packet_listener(self._log_packet, Packet)
        else:
            self.register_packet_listener(self._log_specific_packets, Packet)

    async def _log_packet(self, source, packet):
        if isinstance(packet, ServerboundPacket):
            bound = "Serverbound"
        else:
            bound = "Clientbound"

        if source.IS_MASTER:
            server = "MASTER"
        else:
            server = "GAME"

        await aprint(f"{server}: {bound}: {packet}")

    async def _log_specific_packets(self, source, packet):
        if isinstance(packet, pak.GenericPacket):
            return

        await self._log_packet(source, packet)
