import pak

from public import public

from ... import types

from ..packet import ClientboundGamePacket

@public
class InitialPlayerInfoPacket(ClientboundGamePacket):
    Header = pak.Packet.Header

    id = None

    actor_id: pak.UInt32
    position: types.Vector
    rotation: types.Rotation

@public
class TickCompletedPacket(ClientboundGamePacket):
    id = 0x0000

@public
class ChatPacket(ClientboundGamePacket):
    id = 0x2A23

    actor_id: pak.UInt32
    message:  types.String

@public
class SpawnActorPacket(ClientboundGamePacket):
    id = 0x6B6D

    actor_id: pak.UInt32

    owner_id: pak.UInt32

    is_character: pak.Bool

    blueprint_name: types.String

    position: types.Vector
    rotation: types.Rotation

    health: pak.Int32

@public
class PlayerPositionPacket(ClientboundGamePacket):
    id = 0x7070

    actor_id: pak.UInt32

    position:      types.Vector
    look_rotation: types.Rotation
    velocity:      types.Vector16

    forward: types.SignedFraction
    strafe:  types.SignedFraction

@public
class ActorPositionAndVelocityPacket(ClientboundGamePacket):
    id = 0x7370

    actor_id: pak.UInt32

    position: types.Vector
    rotation: types.Rotation
    velocity: types.Vector16

@public
class ActorPositionPacket(ClientboundGamePacket):
    id = 0x766D

    actor_id: pak.UInt32

    position: types.Vector
    rotation: types.Rotation

@public
class TeleportPacket(ClientboundGamePacket):
    id = 0x7074

    actor_id: pak.UInt32

    position: types.Vector
    rotation: types.Rotation
