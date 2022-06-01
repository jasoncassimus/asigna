from lib.models.entity import Exit, DescriptionItem
from lib.models.enums import ExitType
from lib.models.room import Room
rooms = {}


def add_room(room: Room):
    rooms[room.name] = room


# This is unpleasant to work with.

add_room(
    Room(name = 'tavern',
        description = "You're in a cozy tavern warmed by an open fire.",
        exits = [
            Exit(name = 'outside',
                description = 'A door leading to the outside.',
                destination = 'outside',
                exit_type = ExitType.DOOR)
        ]
    )
)


add_room(
    Room(name = 'outside',
        description = "You're standing outside a tavern. It's raining.",
        exits = [
            Exit(
                name = 'inside',
                description = 'A door leading back inside.',
                destination = 'tavern',
                exit_type = ExitType.DOOR)
        ]
    )
)