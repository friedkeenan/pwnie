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
    pass

@public
class ClientboundMasterPacket(MasterPacket, ClientboundPacket):
    pass

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

@public
class ClientboundGamePacket(GamePacket, ClientboundPacket):
    pass

@public
class ServerboundGamePacket(GamePacket, ServerboundPacket):
    pass
