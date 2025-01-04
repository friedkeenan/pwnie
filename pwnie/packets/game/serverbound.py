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
class SetCircuitInputsPacket(ServerboundGamePacket):
    id = 0x3130

    name: types.String

    # TODO: Probably a bit field.
    inputs: pak.UInt32

@public
class EquipItemPacket(ServerboundGamePacket):
    id = 0x3D69

    slot: pak.UInt8
    name: types.String

@public
class SetCurrentQuestPacket(ServerboundGamePacket):
    id = 0x3D71

    name: types.String

@public
class SetCurrentSlotPacket(ServerboundGamePacket):
    id = 0x3D73

    slot: pak.UInt8

@public
class TransitionToNPCStatePacket(ServerboundGamePacket):
    id = 0x3E23

    state: types.String

@public
class BuyItemPacket(ServerboundGamePacket):
    id = 0x6224

    npc_actor_id: pak.UInt32
    name:         types.String
    count:        pak.UInt32

@public
class UsePacket(ServerboundGamePacket):
    # TODO: Better name?

    id = 0x6565

    actor_id: pak.UInt32

@public
class ActivatePacket(ServerboundGamePacket):
    # TODO: Better name?

    id = 0x692A

    name:          types.String
    look_rotation: types.PrecisionRotation

@public
class ReloadWeaponPacket(ServerboundGamePacket):
    id = 0x6C72

@public
class SetSprintingPacket(ServerboundGamePacket):
    id = 0x6E72

    is_sprinting: pak.Bool

@public
class SetJumpingPacket(ServerboundGamePacket):
    id = 0x706A

    is_jumping: pak.Bool

@public
class TeleportPacket(ServerboundGamePacket):
    id = 0x7074

    name: types.String

@public
class FireRequestPacket(ServerboundGamePacket):
    # TODO: Better names.

    id = 0x7266

    state: pak.Bool

@public
class SellItem(ServerboundGamePacket):
    id = 0x7324

    npc_actor_id: pak.UInt32
    name:         types.String
    count:        pak.UInt32

@public
class RespawnPacket(ServerboundGamePacket):
    id = 0x7372

@public
class FastTravelPacket(ServerboundGamePacket):
    id = 0x7466

    origin:      types.String
    destination: types.String

@public
class MovePacket(ServerboundGamePacket):
    id = 0x766D

    position:      types.Vector
    look_rotation: types.Rotation

    forward: types.SignedFraction
    strafe:  types.SignedFraction

@public
class SetPVPDesiredPacket(ServerboundGamePacket):
    id = 0x7670

    desired: pak.Bool

@public
class SubmitDLCKeyPacket(ServerboundGamePacket):
    id = 0x796B

    key: types.String
