from lib.models.creature import Creature
import json
import pprint
import dataclasses

@dataclasses.dataclass
class Foo:
    bar:int = 0

    def serialize(self):
        return [self.bar]


x = Foo()

test_creature = Creature()
test_creature.name = "Bob"
test_json = json.dumps(test_creature.serialize())

def creature_creator(creature_dict) -> Creature:
    result = Creature()
    result.name = creature_dict['name']
    return result

another_test_creature = json.loads(test_json, object_hook=creature_creator)
pprint.pprint(another_test_creature)