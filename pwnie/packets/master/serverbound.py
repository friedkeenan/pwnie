import pak

from public import public

from ... import types

from ..packet import ServerboundMasterPacket

from .clientbound import (
    LoginResultPacket,
    PlayerCountsPacket,
    CharacterListPacket,
    JoinGamePacket,
)

@public
class LoginPacket(ServerboundMasterPacket):
    id = 0x00

    RESPONSE = LoginResultPacket

    username: types.String
    password: types.String

@public
class GetPlayerCountsPacket(ServerboundMasterPacket):
    id = 0x02

    RESPONSE = PlayerCountsPacket

@public
class GetCharacterListPacket(ServerboundMasterPacket):
    id = 0x0A

    RESPONSE = CharacterListPacket

@public
class JoinGameServerPacket(ServerboundMasterPacket):
    id = 0x0D

    RESPONSE = JoinGamePacket

    character_id: pak.UInt32

@public
class HeartbeatPacket(ServerboundMasterPacket):
    id = 0x80

    RESPONSE = None

@public
class NotifyDisconnectPacket(ServerboundMasterPacket):
    id = 0x81

    RESPONSE = None
