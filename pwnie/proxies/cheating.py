import pak

from public import public

from ..packets import game

from .tracking import TrackMovementProxy

@public
class FlyProxy(TrackMovementProxy):
    FLY_SPEED = 2500

    @pak.packet_listener(game.clientbound.InitialPlayerInfoPacket)
    async def _init_flying(self, source, packet):
        source.data.flying = False

    @pak.packet_listener(game.serverbound.SetSprintingPacket)
    async def _set_flying(self, source, packet):
        source.data.flying = not packet.is_sprinting

        if not source.data.flying:
            # Reset the player's velocity when they stop flying.

            await source.write_packet(
                game.clientbound.PlayerPositionPacket,

                actor_id = source.actor_id,

                position      = source.data.position,
                look_rotation = source.data.look_rotation,

                velocity = [0, 0, 0],

                forward = source.data.forward,
                strafe  = source.data.strafe,
            )

    @pak.packet_listener(game.serverbound.MovePacket)
    async def _fly(self, source, packet):
        if not source.data.flying:
            return

        # It would be kinda nice to use the
        # information from 'TrackMovementProxy'
        # but it's not worth it to make sure that
        # that listener gets executed before this one.

        await source.write_packet(
            game.clientbound.PlayerPositionPacket,

            actor_id = source.actor_id,

            position      = packet.position,
            look_rotation = packet.look_rotation,

            velocity = self.FLY_SPEED * packet.look_rotation.direction(),

            forward = packet.forward,
            strafe  = packet.strafe,
        )
