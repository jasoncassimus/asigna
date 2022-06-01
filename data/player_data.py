
import sqlite3
#import lib.models.player

connection = sqlite3.connect('data/game_data.db')
cursor = connection.cursor()

# Drop Players Table
command = 'DROP TABLE IF EXISTS players;'
cursor.execute(command)

command = """CREATE TABLE IF NOT EXISTS
players(id INTEGER PRIMARY KEY, name TEXT, password TEXT);"""

cursor.execute(command)

command = """INSERT INTO players(name,password)
VALUES('Jason', 'cassimus');"""
cursor.execute(command)
connection.commit()


def add_player(name: str, password: str):
    command = f"INSERT INTO players(name,password) VALUES('{name}', '{password}');"
    cursor.execute(command)
    connection.commit()


def execute():
    cursor.execute(command)


def player_exists(name):
    cursor.execute("SELECT * FROM players WHERE name=?", (name,))
    rows = cursor.fetchall()
    if rows is None or len(rows) == 0:
        return False
    else:
        return True


def player_password(name):
    cursor.execute("SELECT password FROM players WHERE name=?", (name,))
    row = cursor.fetchone()
    if row is None:
        pass
    else:
        return row[0].__str__()
