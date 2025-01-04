import pak

from public import public

from ... import types

from ..packet import ServerboundMasterPacket

from .common import Item

from .clientbound import (
    LoginResultPacket,
    RegisterResultPacket,
    PlayerCountsPacket,
    TeammatesPacket,
    CharacterListPacket,
    CreateCharacterResultPacket,
    DeleteCharacterResultPacket,
    JoinGamePacket,
    ValidateCharacterTokenResultPacket,
    CharacterRegionChangeResultPacket,
    GetFlagInfoResultPacket,
    SubmitFlagResultPacket,
    SubmitAnswerResultPacket,
)

@public
class LoginPacket(ServerboundMasterPacket):
    id = 0x00

    RESPONSE = LoginResultPacket

    username: types.String
    password: types.String

@public
class RegisterPacket(ServerboundMasterPacket):
    id = 0x01

    RESPONSE = RegisterResultPacket

    username:          types.String
    team_name_or_hash: types.String
    password:          types.String

@public
class GetPlayerCountsPacket(ServerboundMasterPacket):
    id = 0x02

    RESPONSE = PlayerCountsPacket

@public
class GetTeammatesPacket(ServerboundMasterPacket):
    id = 0x03

    RESPONSE = TeammatesPacket

@public
class GetCharacterListPacket(ServerboundMasterPacket):
    id = 0x0A

    RESPONSE = CharacterListPacket

@public
class CreateCharacterPacket(ServerboundMasterPacket):
    id = 0x0B

    RESPONSE = CreateCharacterResultPacket

    name:   types.String
    avatar: pak.UInt8
    colors: pak.UInt32[4]

@public
class DeleteCharacterPacket(ServerboundMasterPacket):
    id = 0x0C

    RESPONSE = DeleteCharacterResultPacket

    character_id: pak.Int32

@public
class JoinGameServerPacket(ServerboundMasterPacket):
    id = 0x0D

    RESPONSE = JoinGamePacket

    character_id: pak.Int32

@public
class ValidateCharacterTokenPacket(ServerboundMasterPacket):
    id = 0x14

    RESPONSE = ValidateCharacterTokenResultPacket

    character_id:    pak.Int32
    character_token: types.String # TODO: Same as 'game_server_token'?

@public
class AddServerToPoolPacket(ServerboundMasterPacket):
    id = 0x15

    RESPONSE = None

    host: types.String
    port: pak.UInt16

@public
class CharacterRegionChangePacket(ServerboundMasterPacket):
    id = 0x16

    RESPONSE = CharacterRegionChangeResultPacket

    character_id:   pak.Int32
    character_name: types.String
    position:       types.Vector
    health:         pak.Int32
    mana:           pak.Int32
    pvp:            pak.Bool

@public
class StartQuestPacket(ServerboundMasterPacket):
    id = 0x1E

    RESPONSE = None

    character_id: pak.Int32
    quest_name:   types.String

    state: types.String
    count: pak.UInt32

@public
class UpdateQuestPacket(ServerboundMasterPacket):
    id = 0x1F

    RESPONSE = None

    character_id: pak.Int32
    quest_name: types.String

    state: types.String
    count: pak.UInt32

@public
class CompleteQuestPacket(ServerboundMasterPacket):
    id = 0x20

    RESPONSE = None

    character_id: pak.Int32
    quest_name:   types.String

@public
class SetActiveQuestPacket(ServerboundMasterPacket):
    id = 0x21

    RESPONSE = None

    character_id: pak.Int32
    quest_name:   types.String

@public
class UpdateItemsPacket(ServerboundMasterPacket):
    id = 0x22

    RESPONSE = None

    character_id: pak.Int32
    items:        Item[pak.UInt16]
    equipped:     types.String[10]
    active_slot:  pak.UInt8

@public
class GetPickupPacket(ServerboundMasterPacket):
    id = 0x23

    RESPONSE = None

    character_id: pak.Int32
    pickup_name:  types.String
    items:        Item[pak.UInt16]
    equipped:     types.String[10]
    active_slot:  pak.UInt8

@public
class GetFlagInfoPacket(ServerboundMasterPacket):
    id = 0x28

    RESPONSE = GetFlagInfoResultPacket

    name: types.String

@public
class SubmitFlagPacket(ServerboundMasterPacket):
    id = 0x29

    RESPONSE = SubmitFlagResultPacket

    name: types.String

@public
class SubmitAnswerPacket(ServerboundMasterPacket):
    id = 0x2A

    RESPONSE = SubmitAnswerResultPacket

    # TODO: Better names?
    name: types.String
    text: types.String

@public
class HeartbeatPacket(ServerboundMasterPacket):
    id = 0x80

    RESPONSE = None

@public
class NotifyDisconnectPacket(ServerboundMasterPacket):
    id = 0x81

    RESPONSE = None
