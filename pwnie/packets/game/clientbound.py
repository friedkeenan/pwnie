import pak

from public import public

from ... import types

from ..packet import ClientboundGamePacket

@public
class InitialPlayerInfoPacket(ClientboundGamePacket):
    Header = pak.Packet.Header

    id = None

    actor_id: pak.UInt32
    location: types.Vector
    rotation: types.Rotation

@public
class TickCompletedPacket(ClientboundGamePacket):
    id = 0x0000
