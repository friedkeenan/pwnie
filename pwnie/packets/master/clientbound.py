import pak

from public import public

from ... import types

from ..packet import ClientboundMasterPacket

from .common import AccountInfo, Item, Quest

@public
class ServerInfoPacket(ClientboundMasterPacket):
    class Header(ClientboundMasterPacket.Header):
        magic: pak.RawByte[4]

    magic = b"PWN3"

    protocol_version: pak.UInt16
    server_name:      types.String
    login_text:       types.String

@public
class LoginResultPacket(ClientboundMasterPacket):
    account_info: pak.Optional(AccountInfo, pak.Bool)

    @property
    def succeeded(self):
        return self.account_info is not None

@public
class RegisterResultPacket(ClientboundMasterPacket):
    account_info: pak.Optional(AccountInfo, pak.Bool)

    error_message: pak.Optional(types.String, lambda packet: not packet.succeeded)

    @property
    def succeeded(self):
        return self.account_info is not None

@public
class PlayerCountsPacket(ClientboundMasterPacket):
    num_team_players:  pak.UInt32
    num_total_players: pak.UInt32

@public
class TeammatesPacket(ClientboundMasterPacket):
    class Teammate(pak.SubPacket):
        name:     types.String
        location: types.String

    teammates: Teammate[pak.UInt16]

@public
class CharacterListPacket(ClientboundMasterPacket):
    class CharacterInfo(pak.SubPacket):
        character_id: pak.Int32
        name:         types.String
        location:     types.String

        avatar: pak.UInt8
        colors: pak.UInt32[4]

        num_flags: pak.UInt32

        admin: pak.Bool

    characters: CharacterInfo[pak.UInt16]

@public
class CreateCharacterResultPacket(ClientboundMasterPacket):
    character_id: pak.Optional(pak.Int32, pak.Bool)

    error_message: pak.Optional(types.String, lambda packet: not packet.succeeded)

    @property
    def succeeded(self):
        return self.character_id is not None

@public
class DeleteCharacterResultPacket(ClientboundMasterPacket):
    succeeded: pak.Bool

@public
class JoinGamePacket(ClientboundMasterPacket):
    class GameInfo(pak.SubPacket):
        game_server_address: types.String
        game_server_port:    pak.UInt16
        game_server_token:   types.String

        character_name: types.String
        team_name:      types.String

        admin: pak.Bool

        quests:            Quest[pak.UInt16]
        active_quest_name: types.String

        items:       Item[pak.UInt16]
        equipped:    types.String[10]
        active_slot: pak.UInt8

        pickups: types.String[pak.UInt16]

    access_granted: pak.Bool
    servers_free:   pak.Optional(pak.Bool, "access_granted")

    game_info: pak.Optional(GameInfo, lambda packet: packet.access_granted and packet.servers_free)

@public
class ValidateCharacterTokenResultPacket(ClientboundMasterPacket):
    class CharacterInfo(pak.SubPacket):
        character_name: types.String
        team_name:      types.String
        location:       types.String

        avatar: pak.UInt8
        colors: pak.UInt32[4]

        transitioning:       pak.Bool
        transition_position: types.Vector
        transition_health:   pak.Int32
        transition_mana:     pak.Int32
        transition_pvp:      pak.Bool

        admin: pak.Bool

        quests:            Quest[pak.UInt16]
        active_quest_name: types.String

        items:       Item[pak.UInt16]
        equipped:    types.String[10]
        active_slot: pak.UInt8

        pickups: types.String[pak.UInt16]

    character_info: pak.Optional(CharacterInfo, pak.Bool)

    @property
    def succeeded(self):
        return self.character_info is not None

@public
class CharacterRegionChangeResultPacket(ClientboundMasterPacket):
    succeeded: pak.Bool

@public
class GetFlagInfoResultPacket(ClientboundMasterPacket):
    succeeded: pak.Bool

    message: types.String

    submitted: pak.Optional(pak.Bool, "succeeded")

@public
class SubmitFlagResultPacket(ClientboundMasterPacket):
    succeeded: pak.Bool

    message: types.String

@public
class SubmitAnswerResultPacket(ClientboundMasterPacket):
    succeeded: pak.Bool

    message: types.String
