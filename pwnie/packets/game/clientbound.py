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
class PVPCountdownUpdatePacket(ClientboundGamePacket):
    id = 0x18E2

    enabled:   pak.Bool
    countdown: pak.Int32

@public
class NPCShopPacket(ClientboundGamePacket):
    id = 0x2424

    npc_actor_id: pak.UInt32

@public
class ChatPacket(ClientboundGamePacket):
    id = 0x2A23

    actor_id: pak.UInt32
    message:  types.String

@public
class FireBulletsPacket(ClientboundGamePacket):
    id = 0x2A2A

    actor_id: pak.UInt32

    item_name:    types.String
    target:       types.Vector
    count:        pak.UInt8
    spread_angle: pak.Float32

@public
class UpdateHealthPacket(ClientboundGamePacket):
    id = 0x2B2B

    actor_id: pak.UInt32

    health: pak.Int32

@public
class CircuitOutputPacket(ClientboundGamePacket):
    id = 0x3130

    name:    types.String
    inputs:  pak.UInt32 # TODO: Probably bit field.
    outputs: pak.Bool[pak.UInt16]

@public
class KillPacket(ClientboundGamePacket):
    id = 0x392D

    actor_id:  pak.UInt32
    killer_id: pak.UInt32
    item_name: types.String

@public
class EquipItemPacket(ClientboundGamePacket):
    id = 0x3D69

    slot: pak.UInt8
    name: types.String

@public
class SetCurrentQuestPacket(ClientboundGamePacket):
    id = 0x3D71

    name: types.String

@public
class SetCurrentSlotPacket(ClientboundGamePacket):
    id = 0x3D73

    slot: pak.UInt8

@public
class AdvanceQuestToStatePacket(ClientboundGamePacket):
    id = 0x3E71

    name:       types.String
    state_name: types.String

@public
class LoadAmmoPacket(ClientboundGamePacket):
    id = 0x616C

    item_name: types.String
    ammo:      pak.UInt32

@public
class UpdateManaPacket(ClientboundGamePacket):
    id = 0x616D

    mana: pak.UInt32

@public
class PlayerLeftPacket(ClientboundGamePacket):
    id = 0x635E

    actor_id: pak.UInt32

@public
class PlayerJoinedPacket(ClientboundGamePacket):
    id = 0x636E

    class State(pak.SubPacket):
        name:    types.String
        enabled: pak.Bool

    actor_id: pak.UInt32

    character_name: types.String
    team_name:      types.String

    avatar: pak.UInt8
    colors: pak.UInt32[4]

    position: types.Vector
    rotation: types.Rotation

    item_name: types.String

    health: pak.Int32

    states: State[pak.Int16]

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

@public
class DestroyActorPacket(ClientboundGamePacket):
    id = 0x7878

    actor_id: pak.UInt32
