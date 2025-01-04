import enum
import pak

from public import public

from ..packets import master, game

from .proxy import Proxy

@public
class FlyProxy(Proxy):
    FLY_SPEED = 5000

    class FlyMode(enum.Enum):
        Disabled = 0
        Moving   = 1
        Hovering = 2

    @staticmethod
    async def _set_still_for_flying(client):
        await client.write_packet(
            game.clientbound.ActorPositionAndVelocityPacket,

            actor_id = client.actor_id,
            position = client.data.position,

            # Slight upward velocity to counteract gravity.
            velocity = [0, 0, 39],
        )

    @pak.packet_listener(master.clientbound.ServerInfoPacket)
    async def _init_flying(self, source, packet):
        source.data.fly_mode  = self.FlyMode.Disabled
        source.data.fly_speed = self.FLY_SPEED

        # Allow "flying" and then jumping off
        # the ground without activating hovering.
        source.data._previous_jumping_for_flying = False

    @pak.packet_listener(game.clientbound.InitialPlayerInfoPacket)
    async def _set_initial_position_for_flying(self, source, packet):
        source.data.position = packet.position

    @pak.packet_listener(game.serverbound.ChatPacket)
    async def _set_fly_speed(self, source, packet):
        if not packet.message.startswith("/flyspeed "):
            return True

        try:
            source.data.fly_speed = int(packet.message.split(" ", 1)[1])
        except ValueError:
            return True

        return False

    @pak.packet_listener(game.serverbound.SetSprintingPacket)
    async def _set_flying(self, source, packet):
        match source.data.fly_mode:
            case self.FlyMode.Disabled if not packet.is_sprinting:
                source.data.fly_mode = self.FlyMode.Moving

            case self.FlyMode.Moving if packet.is_sprinting:
                source.data.fly_mode = self.FlyMode.Disabled

                await self._set_still_for_flying(source)

    @pak.packet_listener(game.serverbound.SetJumpingPacket)
    async def _set_hovering(self, source, packet):
        match source.data.fly_mode:
            case self.FlyMode.Moving if not packet.is_jumping and not source.data._previous_jumping_for_flying:
                source.data.fly_mode = self.FlyMode.Hovering

                await self._set_still_for_flying(source)

            case self.FlyMode.Hovering:
                source.data.fly_mode = self.FlyMode.Disabled

        source.data._previous_jumping_for_flying = packet.is_jumping

    @pak.packet_listener(game.serverbound.MovePacket)
    async def _fly(self, source, packet):
        match source.data.fly_mode:
            case self.FlyMode.Disabled:
                source.data.position = packet.position

                return True

            case self.FlyMode.Moving:
                source.data.position = packet.position

                await source.write_packet(
                    game.clientbound.PlayerPositionPacket,

                    actor_id = source.actor_id,

                    position      = packet.position,
                    look_rotation = packet.look_rotation,

                    velocity = source.data.fly_speed * packet.look_rotation.direction(),

                    forward = packet.forward,
                    strafe  = packet.strafe,
                )

                return True

            case self.FlyMode.Hovering:
                await source.destination.write_packet_instance(
                    packet.copy(position=source.data.position)
                )

                await self._set_still_for_flying(source)

                return False
