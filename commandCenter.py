import sc2
from sc2 import units
from sc2.bot_ai import BotAI
from sc2.player import Bot, Computer
from sc2.ids.unit_typeid import UnitTypeId


class commandCenter_AI(BotAI):
    async def on_step(self, iteration: int):
        await self.buildWorkers()

    async def buildWorkers(self):
        print("TENTANDO FAZER SCV")
        if(self.can_afford(UnitTypeId.SCV) and self.units(UnitTypeId.SCV).amount + self.already_pending(UnitTypeId.SCV) < self.townhalls().ready.amount * 22):
                commandCenter.build(UnitTypeId.SCV)
