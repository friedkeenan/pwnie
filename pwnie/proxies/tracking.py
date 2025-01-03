import numpy as np
import pak

from public import public

from ..packets import game

from .proxy import Proxy

@public
class TrackMovementProxy(Proxy):
    @pak.packet_listener(game.clientbound.InitialPlayerInfoPacket)
    async def _track_initial_position(self, source, packet):
        source.data.position      = packet.position
        source.data.look_rotation = np.array([0.0, 0.0, 0.0])
        source.data.forward       = 0.0
        source.data.strafe        = 0.0

    @pak.packet_listener(game.serverbound.MovePacket)
    async def _track_movement(self, source, packet):
        source.data.position      = packet.position
        source.data.look_rotation = packet.look_rotation
        source.data.forward       = packet.forward
        source.data.strafe        = packet.strafe
