#from lib.models.entity import Exit
from lib.models.enums import ExitType
from lib.models.room import Room, Exit
import sqlite3
from data import connection, cursor


def sql_command(command: str):
    cursor.execute(command)


def commit_data():
    connection.commit()


sql_command("PRAGMA foreign_keys = ON;")
sql_command('DROP TABLE IF EXISTS roomExitMap;')
sql_command('DROP TABLE IF EXISTS rooms;')
sql_command('DROP TABLE IF EXISTS exits;')


sql_command("""CREATE TABLE IF NOT EXISTS
exits(id INTEGER PRIMARY KEY, roomId INTEGER, destination TEXT);
""")


sql_command("""CREATE TABLE IF NOT EXISTS
rooms(id INTEGER PRIMARY KEY, name TEXT, description TEXT);""")

sql_command("""
CREATE TABLE IF NOT EXISTS
roomExitMap(
fromRoomKey INTEGER, 
toRoomKey INTEGER, 
exitKey INTEGER, 
FOREIGN KEY(fromRoomKey) REFERENCES rooms(id), 
FOREIGN KEY(toRoomKey) REFERENCES rooms(id), 
FOREIGN KEY(exitKey) REFERENCES exits(id));
""")

connection.commit()


def add_rooms(rooms):
    room_ids = dict()
    for room in rooms:
        command = f"INSERT INTO rooms(name,description) VALUES('{room.name}', '{room.description}');"
        cursor.execute(command)
        room_ids[room.name] = cursor.lastrowid

    for room in rooms:
        exit_ids = []
        for exit_name in room.get_exits():
            exit = room.get_exit(exit_name)
            command = f"INSERT INTO exits(roomId,destination) VALUES('{room_ids[exit.destination]}', '{exit.destination}');"
            cursor.execute(command)
            #exit_ids.append(cursor.lastrowid)
            command = f"INSERT INTO roomExitMap(fromRoomKey,toRoomKey,exitKey) VALUES('{room_ids[room.name]}', '{room_ids[exit.destination]}', '{cursor.lastrowid}');"
            cursor.execute(command)
    connection.commit()


def print_table(table_name):
    command = f"SELECT * FROM {table_name}"
    cursor.execute(command)
    for row in cursor.fetchall():
        print(row)
