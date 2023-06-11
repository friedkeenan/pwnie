import pak

from public import public

from ... import types

from ..packet import ClientboundMasterPacket

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
    class AccountInfo(pak.SubPacket):
        user_id: pak.UInt32

        team_hash: types.String
        team_name: types.String

        admin: pak.Bool

    account_info: pak.Optional(AccountInfo, pak.Bool)

@public
class PlayerCountsPacket(ClientboundMasterPacket):
    num_team_players:  pak.UInt32
    num_total_players: pak.UInt32

@public
class CharacterListPacket(ClientboundMasterPacket):
    class CharacterInfo(pak.SubPacket):
        character_id: pak.UInt32
        name:         types.String
        location:     types.String

        avatar: pak.UInt8
        colors: pak.UInt32[4]

        unk_uint32_6: pak.UInt32 # Number of flags?

        transitioning: pak.Bool

    characters: CharacterInfo[pak.UInt16]

@public
class JoinGamePacket(ClientboundMasterPacket):
    class GameInfo(pak.SubPacket):
        class Quest(pak.SubPacket):
            name:  types.String
            state: types.String

            # Count?
            unk_uint32_3: pak.UInt32

        class Item(pak.SubPacket):
            name:     types.String
            item_id:  pak.UInt32
            quantity: pak.UInt16

        game_server_address: types.String
        game_server_port:    pak.UInt16
        game_server_token:   types.String

        character_name: types.String
        team_name:      types.String

        transitioning: pak.Bool

        quests:            Quest[pak.UInt16]
        active_quest_name: types.String

        items:  Item[pak.UInt16]
        hotbar: types.String[10]

        unk_uint8_11: pak.UInt8
        unk_array_12: types.String[pak.UInt16]

    access_granted: pak.Bool
    servers_free:   pak.Optional(pak.Bool, "access_granted")

    game_info: pak.Optional(GameInfo, lambda packet: packet.access_granted and packet.servers_free)
