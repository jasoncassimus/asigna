#!/usr/bin/env python3
"""A simple Multi-User Dungeon (MUD) game.
author: Mark Frimston - mfrimston@gmail.com
    Additional code added by:
author: Jason Cassimus - jasoncassimus@gmail.com
author: Nathan Robertson - absnathanr@gmail.com
"""
import threading
import time

import data
#from game_data import rooms
from mudserver import MudServer
from lib.constants import DEFAULT_START_LOCATION
from lib.command import Commands
from lib.models.game_state import GameState
from os import environ

from data import *

import socket
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
        print("Running test server")
    finally:
        s.close()
    return IP

print(f"My IP:{get_ip()}")

if 'PRODUCTION' in environ:
    print("Running production server")
    interface=get_ip()
else:
    interface="0.0.0.0"
game = GameState(MudServer(interface=interface))
commands = Commands(game)

my_rooms = [
    Room(name='tavern',
         description="Youre in a cozy tavern warmed by an open fire",
         exits=[
             Exit(name='outside',
                  description='A door leading to the outside',
                  destination='outside',
                  exit_type=ExitType.DOOR),
             Exit(name='to wonderland',
                  description='A door leading to wonderland',
                  destination='Wonderland',
                  exit_type=ExitType.ROAD)
         ]
         ),
    Room(name='outside',
         description="Youre standing outside a tavern. Its raining",
         exits=[
             Exit(
                 name='inside',
                 description='A door leading back inside',
                 destination='tavern',
                 exit_type=ExitType.DOOR)
         ]
         ),
    Room(name='Wonderland',
         description='A great time',
         exits=[
             Exit(
                 name='inside',
                 description='A door leading back to freedom',
                 destination='tavern',
                 exit_type=ExitType.ROAD
             )
         ])
]

add_rooms(my_rooms)

print_table("rooms")

print_table("exits")
print_table("roomExitMap")

print_table("world")

print_table("continents")

while True:
    time.sleep(0.2)
    game.update()

    # go through any newly connected players
    new_players = game.handle_player_join()

    # go through any recently disconnected players
    game.handle_player_leave()

    # go through any new commands sent from players
    for event in game.server.get_commands():
        client = event.client
        command = event.command
        params = event.params
        
        player = game.find_player_by_client_id(client.uuid)

        # if for any reason the player isn't in the player map, skip them and
        # move on to the next one
        if not player:
            continue

        player.advance_login_state(command, params, commands, game)