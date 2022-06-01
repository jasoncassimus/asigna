from dataclasses import dataclass
from datetime import date


@dataclass()
class Zone:
    id: int = None
    name: str = "A New Zone"
    description: str = "This zone has not been set up yet."
    createdBy: str = "None"
    createdOn: str = date.today().__str__()