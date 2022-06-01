from data import connection, cursor
from lib.models import continent
from lib.models.continent import Continent
from lib.models.zone import Zone


def sql_command(command: str):
    cursor.execute(command)


def commit_data():
    connection.commit()


sql_command('DROP TABLE IF EXISTS world;')
sql_command('DROP TABLE IF EXISTS continents;')
sql_command("""CREATE TABLE IF NOT EXISTS
world(id INTEGER PRIMARY KEY, name TEXT, description TEXT, 
createdBy TEXT, createdOn TEXT);""")
sql_command("""CREATE TABLE IF NOT EXISTS
continents(id INTEGER PRIMARY KEY, name TEXT, description TEXT, 
createdBy TEXT, createdOn TEXT);""")


continent_ids = {Continent.name: Continent.id}
zone_ids = {Zone.name: Zone.id}


def add_continent(c: Continent):
    sql_command(f"INSERT INTO world(name,description,createdBy,createdOn) VALUES('{c.name}', '{c.description}','{c.createdBy}','{c.createdOn}');")
    continent_ids[c.name] = cursor.lastrowid
    commit_data()


def add_zone(z: Zone):
    sql_command(f"INSERT INTO continents(name,description,createdBy,createdOn) VALUES('{z.name}', '{z.description}','{z.createdBy}','{z.createdOn}');")
    zone_ids[z.name] = cursor.lastrowid
    commit_data()


def print_table(table_name):
    print(table_name)
    command = f"SELECT * FROM {table_name}"
    cursor.execute(command)
    for row in cursor.fetchall():
        print(row)

new_continent = Continent()
new_continent.name = "The Ethereal Plane"
add_continent(new_continent)

new_zone = Zone()
new_zone.name = "The Cloud City above Monte Thenas"

add_zone(new_zone)
