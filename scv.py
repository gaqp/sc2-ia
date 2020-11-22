import sc2
from sc2 import units
from sc2.bot_ai import BotAI
from sc2.player import Bot, Computer
from sc2.ids.unit_typeid import UnitTypeId


class SCV_AI(BotAI):
    async def on_step(self, iteration: int):
        await self.distribute_workers()
        await self.build_vespene()
        await self.build_supplyDepot()
        await self.build_barracks()
        await self.build_bunker()
        await self.build_engineering_bay()
    async def build_supplyDepot(self):
        if self.supply_left < 5 and not self.already_pending(UnitTypeId.SUPPLYDEPOT):
            commandCenter = self.townhalls(UnitTypeId.COMMANDCENTER).ready
            if commandCenter.exists:
                if self.can_afford(UnitTypeId.SUPPLYDEPOT):
                    await self.build(UnitTypeId.SUPPLYDEPOT, near=commandCenter.random.position.towards(self.game_info.map_center, 5))

    async def build_vespene(self):
        for commandCenter in self.townhalls(UnitTypeId.COMMANDCENTER).ready:
            vespenos = self.vespene_geyser.closer_than(25, commandCenter)
            for vespeno in vespenos:
                if self.can_afford(UnitTypeId.REFINERY):
                    await self.build(UnitTypeId.REFINERY, vespeno)

    async def build_barracks(self):
        for commandCenter in self.townhalls(UnitTypeId.COMMANDCENTER).ready:
            if(self.can_afford(UnitTypeId.BARRACKS)):
                if(self.already_pending(UnitTypeId.BARRACKS) + self.structures(UnitTypeId.BARRACKS).amount < self.townhalls(UnitTypeId.COMMANDCENTER).amount * 2):
                    await self.build(UnitTypeId.BARRACKS, near=commandCenter.position.towards(self.game_info.map_center, 9))

    async def build_bunker(self):
        for commandCenter in self.townhalls(UnitTypeId.COMMANDCENTER).ready:
            if(self.can_afford(UnitTypeId.BUNKER)):
                if(self.already_pending(UnitTypeId.BUNKER) + self.structures(UnitTypeId.BUNKER).amount < self.townhalls(UnitTypeId.COMMANDCENTER).amount * 3):
                    await self.build(UnitTypeId.BUNKER, near=commandCenter.position.towards(self.enemy_start_locations[0], 14))

    async def build_engineering_bay(self):
        if(self.can_afford(UnitTypeId.ENGINEERINGBAY)):
            if(self.already_pending(UnitTypeId.ENGINEERINGBAY) + self.structures(UnitTypeId.ENGINEERINGBAY).amount < 1):
                await self.build(UnitTypeId.ENGINEERINGBAY, near=self.game_info.player_start_location)


sc2.run_game(
    sc2.maps.get("(2)CatalystLE"),
    [Bot(sc2.Race.Terran, SCV_AI()), Computer(
        sc2.Race.Zerg, sc2.Difficulty.Easy)],
    realtime=False,
)
