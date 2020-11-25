from scv import SCV_AI
import sc2
from sc2 import units
from sc2.bot_ai import BotAI
from sc2.player import Bot, Computer
from sc2.ids.unit_typeid import UnitTypeId
from scv import SCV_AI
from commandCenter import commandCenter_AI

CC = commandCenter_AI
SCV = SCV_AI

sc2.run_game(
    sc2.maps.get("(2)CatalystLE"),
    [Bot(sc2.Race.Terran, SCV_AI()), Computer(
        sc2.Race.Zerg, sc2.Difficulty.Easy)],
    realtime=False,
)
