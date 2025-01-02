import pak

from public import public

from ... import types

@public
class AccountInfo(pak.SubPacket):
    user_id: pak.UInt32

    team_hash: types.String
    team_name: types.String

    admin: pak.Bool
