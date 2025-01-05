import enum
import pak

from public import public

from ..packets import master, game

from .proxy import Proxy

@public
class AutoLootProxy(Proxy):
    AUTOLOOT_DROPS = [
        "WhiteDrop",
        "GreenDrop",
        "BlueDrop",
        "PurpleDrop",
    ]

    @pak.packet_listener(game.clientbound.SpawnActorPacket)
    async def _perform_autoloot(self, source, packet):
        if packet.blueprint_name not in self.AUTOLOOT_DROPS:
            return

        await source.write_packet(
            game.serverbound.UsePacket,

            actor_id = packet.actor_id,
        )

@public
class QuickReloadProxy(Proxy):
    @pak.packet_listener(game.clientbound.ReloadWeaponPacket)
    async def _perform_quick_reload(self, source, packet):
        await source.destination.write_packet(
            game.clientbound.SetAmmoPacket,

            item_name = packet.weapon_name,
            ammo      = packet.ammo,
        )

        await source.destination.write_packet(
            game.clientbound.RemoveItemPacket,

            name  = packet.ammo_name,
            count = packet.ammo,
        )

        return False

@public
class FlyProxy(Proxy):
    FLY_SPEED = 5000

    class FlyMode(enum.Enum):
        Disabled = 0
        Moving   = 1
        Hovering = 2

    async def _set_still_for_flying(self, client):
        await client.write_packet(
            game.clientbound.ActorPositionAndVelocityPacket,

            actor_id = client.actor_id,
            position = client.data.position,
        )

    @pak.packet_listener(master.clientbound.ServerInfoPacket)
    async def _init_flying(self, source, packet):
        source.data.fly_mode  = self.FlyMode.Disabled
        source.data.fly_speed = self.FLY_SPEED

        # Allow "flying" and then jumping off
        # the ground without activating hovering.
        source.data._previous_jumping_for_flying = False

        source.data._track_position_for_hovering = False

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

                source.data._track_position_for_hovering = True

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
                if source.data._track_position_for_hovering:
                    source.data.position = packet.position

                    source.data._track_position_for_hovering = False

                await source.destination.write_packet_instance(
                    packet.copy(position=2*source.data.position - packet.position)
                )

                await source.write_packet(
                    game.clientbound.ActorPositionAndVelocityPacket,

                    actor_id = source.actor_id,

                    position = source.data.position,
                    velocity = source.data.position - packet.position,
                )

                return False
