import numpy as np
import pak

from public import public

from ..packets import game

from .proxy import Proxy

@public
class TrackMovementProxy(Proxy):
    @pak.packet_listener(game.clientbound.InitialPlayerInfoPacket)
    async def _track_initial_position(self, source, packet):
        source.meta.position      = packet.position
        source.meta.look_rotation = np.array([0.0, 0.0, 0.0])
        source.meta.forward       = 0.0
        source.meta.strafe        = 0.0

    @pak.packet_listener(game.serverbound.MovePacket)
    async def _track_movement(self, source, packet):
        source.meta.position      = packet.position
        source.meta.look_rotation = packet.look_rotation
        source.meta.forward       = packet.forward
        source.meta.strafe        = packet.strafe
