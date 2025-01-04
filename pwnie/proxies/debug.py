import pak

from aioconsole import aprint

from public import public

from .proxy import Proxy

from ..packets import Packet, ServerboundPacket, game

@public
class LoggingProxy(Proxy):
    LOG_NOISY_PACKETS = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.LOG_NOISY_PACKETS:
            self.register_packet_listener(self._log_packet, Packet)
        else:
            self.register_packet_listener(self._log_quiet_packets, Packet)

    @staticmethod
    def is_noisy_packet(packet):
        if isinstance(packet, game.serverbound.MovePacket):
            return True

        if isinstance(packet, game.clientbound.TickCompletedPacket):
            return True

        if isinstance(packet, game.clientbound.ActorPositionAndVelocityPacket):
            return True

        return False

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

    async def _log_quiet_packets(self, source, packet):
        if self.is_noisy_packet(packet):
            return

        await self._log_packet(source, packet)
