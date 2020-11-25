import sc2
from sc2 import units
from sc2.bot_ai import BotAI
from sc2.player import Bot, Computer
from sc2.ids.unit_typeid import UnitTypeId


class SCV_AI(BotAI):
    async def on_step(self, iteration: int):
        await self.build_workers();
        await self.distribute_workers()
        await self.build_vespene()
        await self.build_supplyDepot()
        await self.build_barracks()
        await self.build_bunker()
        await self.build_engineering_bay()
        await self.build_missle_tower()
        await self.build_factory()
        await self.build_armory()
        await self.expand()

    async def expand(self):
        if self.townhalls().amount < 2 and self.can_afford(UnitTypeId.COMMANDCENTER):
            await self.expand_now()

    async def build_supplyDepot(self):
        if self.supply_left < 6 and not self.already_pending(UnitTypeId.SUPPLYDEPOT):
            for commandCenter in self.townhalls().ready:
                if self.can_afford(UnitTypeId.SUPPLYDEPOT):
                    position_towards_map_center = commandCenter.position.towards(
                        self.game_info.map_center, distance=8)
                    await self.build(UnitTypeId.SUPPLYDEPOT, position_towards_map_center)

    async def build_vespene(self):
        for commandCenter in self.townhalls().ready:
            vespenos = self.vespene_geyser.closer_than(10, commandCenter)
            for vespeno in vespenos:
                if self.can_afford(UnitTypeId.REFINERY):
                    await self.build(UnitTypeId.REFINERY, vespeno)

    async def build_barracks(self):
        for commandCenter in self.townhalls().ready:
            if(self.can_afford(UnitTypeId.BARRACKS)):
                if(self.already_pending(UnitTypeId.BARRACKS) + self.structures(UnitTypeId.BARRACKS).amount < self.townhalls().ready.amount * 2):
                    if(self.structures.closer_than(15, commandCenter.position).filter(lambda structure: structure.type_id == UnitTypeId.BARRACKS).amount < 2):
                        position_towards_map_center=commandCenter.position.towards(
                            self.game_info.map_center, distance=12)
                        await self.build(UnitTypeId.BARRACKS, position_towards_map_center)

    async def build_bunker(self):
        for commandCenter in self.townhalls().ready:
            if(self.can_afford(UnitTypeId.BUNKER)):
                if(self.structures.closer_than(18, commandCenter.position).filter(lambda structure: structure.type_id == UnitTypeId.BUNKER).amount < 3):
                    if(self.already_pending(UnitTypeId.BUNKER) + self.structures(UnitTypeId.BUNKER).amount < self.townhalls().ready.amount * 3):
                        await self.build(UnitTypeId.BUNKER, near=commandCenter.position.towards(self.enemy_start_locations[0], 18))

    async def build_engineering_bay(self):
        for commandCenter in self.townhalls().ready:
            if(self.can_afford(UnitTypeId.ENGINEERINGBAY)):
                if(self.already_pending(UnitTypeId.ENGINEERINGBAY) + self.structures(UnitTypeId.ENGINEERINGBAY).amount < 1):
                    position_towards_map_center=commandCenter.position.towards(
                        self.game_info.map_center, distance=8)
                    await self.build(UnitTypeId.ENGINEERINGBAY, position_towards_map_center)

    async def build_missle_tower(self):
        for commandCenter in self.townhalls().ready:
            if(self.can_afford(UnitTypeId.MISSILETURRET)):
                if(self.structures.closer_than(20, commandCenter.position).filter(lambda structure: structure.type_id == UnitTypeId.MISSILETURRET).amount < 3):
                    if(self.already_pending(UnitTypeId.MISSILETURRET) + self.structures(UnitTypeId.MISSILETURRET).amount < self.townhalls().ready.amount*3):
                        await self.build(UnitTypeId.MISSILETURRET, near=commandCenter.position.towards(self.enemy_start_locations[0], 20))

    async def build_factory(self):
        for commandCenter in self.townhalls().ready:
            if(self.can_afford(UnitTypeId.FACTORY)):
                if(self.structures.closer_than(12, commandCenter.position).filter(lambda structure: structure.type_id == UnitTypeId.FACTORY).amount < 2):
                    if(self.already_pending(UnitTypeId.FACTORY) + self.structures(UnitTypeId.FACTORY).amount < self.townhalls().amount * 2):
                        position_towards_map_center=commandCenter.position.towards(
                            self.game_info.map_center, distance=12)
                        await self.build(UnitTypeId.FACTORY, position_towards_map_center)

    async def build_armory(self):
        for commandCenter in self.townhalls().ready:
            if self.can_afford(UnitTypeId.ARMORY):
                if(self.already_pending(UnitTypeId.ARMORY) + self.structures(UnitTypeId.ARMORY).amount < 1):
                    position_towards_map_center=commandCenter.position.towards(
                        self.game_info.map_center, distance=8)
                    await self.build(UnitTypeId.ARMORY, position_towards_map_center)

    async def build_workers(self):
        if(self.can_afford(UnitTypeId.SCV) and self.units(UnitTypeId.SCV).amount + self.already_pending(UnitTypeId.SCV) < self.townhalls().ready.amount * 22):
            for commandCenter in self.townhalls().ready:
                if commandCenter.is_idle:
                    commandCenter.build(UnitTypeId.SCV)
    
