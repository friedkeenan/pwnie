import pak
import numpy as np

from public import public

@public
class Vector(pak.Type):
    _num_floats = 3

    _default = np.array([0.0] * _num_floats)

    @classmethod
    def _size(cls, value, *, ctx):
        return pak.Float32.size(ctx=ctx) * cls._num_floats

    @classmethod
    def _unpack(cls, buf, *, ctx):
        return np.array([pak.Float32.unpack(buf, ctx=ctx) for _ in range(cls._num_floats)])

    @classmethod
    async def _unpack_async(cls, reader, *, ctx):
        return np.array([await pak.Float32.unpack_async(reader, ctx=ctx) for _ in range(cls._num_floats)])

    @classmethod
    def _pack(cls, value, *, ctx):
        return b"".join(pak.Float32.pack(coord, ctx=ctx) for coord in value[:cls._num_floats])

@public
class Rotation(pak.SubPacket):
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
