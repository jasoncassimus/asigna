from dataclasses import dataclass
from datetime import date
from typing import Dict, List

from lib.models.entity import Exit, Inventory
from lib.models.enums import Obscuration, LightLevel


@dataclass()
class Room:
    id: int = None
    name: str = "A New Zone"
    description: str = "This zone has not been set up yet."
    createdBy: str = "None"
    createdOn: str = date.today().__str__()

    exits: List[Exit] = None
    light_level: LightLevel = LightLevel.BRIGHT
    obscuration: Obscuration = Obscuration.NONE
    inventory = Inventory()

    def add_exit(self, ex: Exit):
        self.exits.add(ex)

    def get_exits(self) -> Dict[str, Exit]:
        exits = {}
        for ex in self.exits:
            exits[ex.name] = ex
        return exits

    def get_exit(self, ex) -> Exit:
        return self.get_exits()[ex]

    def has_exit(self, ex: str) -> bool:
        if ex in self.get_exits().keys():
            return True
        return False
