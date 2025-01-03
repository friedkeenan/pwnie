import pak
import numpy as np

from public import public

from .numeric import Saturated16

@public
class Vector(pak.Type):
    underlying = pak.Float32

    num_elems = 3

    @classmethod
    def _size(cls, value, *, ctx):
        return cls.underlying.size(ctx=ctx) * cls.num_elems

    @classmethod
    def _default(cls, *, ctx):
        return [cls.underlying.default(ctx=ctx)] * cls.num_elems

    @classmethod
    def _unpack(cls, buf, *, ctx):
        return np.array([cls.underlying.unpack(buf, ctx=ctx) for _ in range(cls.num_elems)])

    @classmethod
    async def _unpack_async(cls, reader, *, ctx):
        return np.array([await cls.underlying.unpack_async(reader, ctx=ctx) for _ in range(cls.num_elems)])

    @classmethod
    def _pack(cls, value, *, ctx):
        return b"".join(cls.underlying.pack(coord, ctx=ctx) for coord in value[:cls.num_elems])

@public
class Vector16(Vector):
    underlying = Saturated16

class _Rotation:
    def direction(self):
        pitch = np.deg2rad(self.pitch)
        yaw   = np.deg2rad(self.yaw)

        return np.array([
            np.cos(yaw),

            np.sin(yaw),

            np.sin(pitch),
        ])

@public
class Rotation(pak.SubPacket, _Rotation):
    class _Angle(pak.Type):
        _default = 0.0

        @classmethod
        def _size(cls, value, *, ctx):
            return pak.UInt16.size(ctx=ctx)

        @classmethod
        def _unpack(cls, buf, *, ctx):
            return 360 * (pak.UInt16.unpack(buf, ctx=ctx) / 0xFFFF)

        @classmethod
        async def _unpack_async(cls, reader, *, ctx):
            return 360 * (await pak.UInt16.unpack_async(reader, ctx=ctx) / 0xFFFF)

        @classmethod
        def _pack(cls, value, *, ctx):
            return pak.UInt16.pack(int(0xFFFF * (value / 360)), ctx=ctx)

    pitch: _Angle
    yaw:   _Angle
    roll:  _Angle

@public
class PrecisionRotation(pak.SubPacket, _Rotation):
    pitch: pak.Float32
    yaw:   pak.Float32
    roll:  pak.Float32
