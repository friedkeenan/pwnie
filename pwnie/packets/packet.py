import pak

from public import public

@public
class Packet(pak.Packet):
    pass

@public
class ClientboundPacket(Packet):
    pass

@public
class ServerboundPacket(Packet):
    pass

@public
class MasterPacket(Packet):
    @classmethod
    @pak.util.cache
    def GenericWithID(cls, id):
        return type(f"{cls.__qualname__}.GenericWithID(0x{id:02X})", (pak.GenericPacket, cls), dict(
            id = id,

            __module__ = cls.__module__,
        ))

@public
class ClientboundMasterPacket(MasterPacket, ClientboundPacket):
    # To later be replaced with a class which inherits from 'ClientboundMasterPacket'.
    class Generic:
        pass

class _GenericClientboundMasterPacket(ClientboundMasterPacket):
    data: pak.RawByte[None]

_GenericClientboundMasterPacket.__name__     = "Generic"
_GenericClientboundMasterPacket.__qualname__ = "ClientboundMasterPacket.Generic"
ClientboundMasterPacket.Generic              = _GenericClientboundMasterPacket

del _GenericClientboundMasterPacket

@public
class ServerboundMasterPacket(MasterPacket, ServerboundPacket):
    class Header(MasterPacket.Header):
        id: pak.UInt8

    # Could be no response, could be generic response.
    UNKNOWN_RESPONSE = pak.util.UniqueSentinel("UNKNOWN_RESPONSE")

    RESPONSE = UNKNOWN_RESPONSE

@public
class GamePacket(Packet):
    class Header(Packet.Header):
        id: pak.UInt16

    @classmethod
    @pak.util.cache
    def GenericWithID(cls, id):
        return type(f"{cls.__qualname__}.GenericWithID(0x{id:04X})", (pak.GenericPacket, cls), dict(
            id = id,

            __module__ = cls.__module__,
        ))

@public
class ClientboundGamePacket(GamePacket, ClientboundPacket):
    pass

@public
class ServerboundGamePacket(GamePacket, ServerboundPacket):
    pass
