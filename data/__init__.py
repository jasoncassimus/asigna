import sqlite3
from data.player_data import *
from data.room_data import *
from data.world_data import *


connection = sqlite3.connect('data/game_data.db')
cursor = connection.cursor()
sql_command("PRAGMA foreign_keys = ON;")
