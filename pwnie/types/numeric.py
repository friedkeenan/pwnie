import math
import pak

from public import public

@public
class SignedFraction(pak.Type):
    # NOTE: This type is basically equivalent
    # to 'pak.ScaledInteger(pak.Int8, 127)'
    # but with additional clamping to handle imprecision.

    _default = 0.0
    _size    = 1

    @classmethod
    def _unpack(cls, buf, *, ctx):
        return pak.Int8.unpack(buf, ctx=ctx) / 127

    @classmethod
    async def _unpack_async(cls, reader, *, ctx):
        return await pak.Int8.unpack_async(reader, ctx=ctx) / 127

    @classmethod
    def _pack(cls, value, *, ctx):
        if value <= -1:
            return b"\x81"

        if value >= 1:
            return b"\x7F"

        return pak.Int8.pack(int(value * 127), ctx=ctx)

@public
class Saturated16(pak.Type):
    _default = 0.0
    _size    = 2

    @classmethod
    def _unpack(cls, buf, *, ctx):
        return float(pak.Int16.unpack(buf, ctx=ctx))

    @classmethod
    async def _unpack_async(cls, reader, *, ctx):
        return float(await pak.Int16.unpack_async(reader, ctx=ctx))

    @classmethod
    def _pack(cls, value, *, ctx):
        if value < -32768:
            return b"\x00\x80"

        if value > 32767:
            return b"\xFF\x7F"

        value = math.floor(value + 0.5)

        return pak.Int16.pack(value, ctx=ctx)
