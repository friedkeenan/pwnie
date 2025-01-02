import pak

from public import public

from ... import types

from ..packet import ServerboundGamePacket

@public
class JoinGameServerPacket(ServerboundGamePacket):
    Header = pak.Packet.Header

    id = None

    character_id:      pak.UInt32
    game_server_token: types.String

@public
class NotifyDisconnectPacket(ServerboundGamePacket):
    id = 0x0000

@public
class ChatPacket(ServerboundGamePacket):
    id = 0x2A23

    message: types.String

@public
class SetSprintingPacket(ServerboundGamePacket):
    id = 0x6E72

    is_sprinting: pak.Bool

@public
class SetJumpingPacket(ServerboundGamePacket):
    id = 0x706A

    is_jumping: pak.Bool

@public
class MovePacket(ServerboundGamePacket):
    id = 0x766D

    position:      types.Vector
    look_rotation: types.Rotation

    forward_velocity: types.SignedFraction
    strafe_velocity:  types.SignedFraction
