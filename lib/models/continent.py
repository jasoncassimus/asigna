from dataclasses import dataclass
from datetime import date


@dataclass()
class Continent:
    id: int = None
    name: str = "A New Continent"
    description: str = "This continent has not been set up yet."
    recall: int = None
    createdBy: str = None
    createdOn: str = date.today().__str__()

