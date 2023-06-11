import pak

from public import public

from ... import types

from ..packet import ServerboundGamePacket

@public
class JoinGameServerPacket(ServerboundGamePacket):
    Header = pak.Packet.Header

    id = None

    character_id: pak.UInt32
    game_server_token: types.String

@public
class NotifyDisconnectPacket(ServerboundGamePacket):
    id = 0x0000
