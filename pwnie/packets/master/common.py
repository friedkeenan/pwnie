import pak

from public import public

from ... import types

@public
class AccountInfo(pak.SubPacket):
    user_id: pak.UInt32

    team_hash: types.String
    team_name: types.String

    admin: pak.Bool

@public
class Item(pak.SubPacket):
    name:        types.String
    count:       pak.UInt32
    loaded_ammo: pak.UInt16

@public
class Quest(pak.SubPacket):
    name:  types.String
    state: types.String
    count: pak.UInt32
