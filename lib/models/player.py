from abc import ABC

from data.player_data import add_player, player_exists, player_password
from game_data import rooms
from lib.models.client import Client
from lib.models.creature import Creature
from mudserver import MudServer
from lib.constants import DEFAULT_START_LOCATION


class Player(Creature, ABC):

    def __init__(self, client: Client, server: MudServer, creature: Creature = None):
        self.client = client
        self.server = server
        self.login = None
        self.password = None

        self.__login_state = self.__new_connection

        if creature:
            super().__init__(
                 creature.name,
                 creature.description,
                 creature.character_class,
                 creature.level,
                 creature.background,
                 creature.race,
                 creature.alignment,
                 creature.xp,
                 creature.abilities,
                 creature.skills,
                 creature.max_hp, 
                 creature.armor_class,
                 creature.hd_value,
                 creature.hd_total,
                 creature.inventory
            )

        super().__init__()

    def advance_login_state(self, player_input, params, commands, game):
        self.__login_state = self.__login_state(player_input, params, commands, game)

    def __new_connection(self, player_input, params, commands, game):
        clean_input = str(player_input).lstrip().rstrip()
        if len(clean_input) == 0 or not clean_input.isalpha():
            return self.__new_connection
        else:
            self.login = player_input.capitalize()
            if player_exists(self.login):
                self.message("Enter your password:")
                return self.__wait_for_existing_pw
            else:
                self.message("Welcome new player, please enter a password to create your account!")
                return self.__wait_for_new_pw

    def __wait_for_new_pw(self, player_input, params, commands, game):
        clean_input = str(player_input).lstrip().rstrip()
        if len(clean_input) > 0 or clean_input.isalnum():
            self.name = self.login
            self.password = player_input
            add_player(self.name, self.password)
            self.__just_logged_on(player_input, params, commands, game)
            return self.__logged_on
        else:
            self.message("This password is no good! Try again.")
            return self.__wait_for_new_pw

    def __wait_for_existing_pw(self, player_input, params, commands, game):
        clean_input = str(player_input).lstrip().rstrip()
        if len(clean_input) > 0 or clean_input.isalnum():
            self.password = player_password(self.login)
            if clean_input == self.password:
                self.__just_logged_on(player_input, params, commands, game)
                return self.__logged_on
            else:
                self.message("Password is no good! Please try again.")
                return self.__wait_for_existing_pw

    def __just_logged_on(self, player_input, params, commands, game):
        self.name = self.login
        game.broadcast(f"{self.name} entered the game.")
        self.message(f"Asigna has awaited your return, {self.name}!")
        self.message("Type 'help' for a list of commands. Have fun!")
        self.move(DEFAULT_START_LOCATION)
        return self.__logged_on

    def __logged_on(self, player_input, params, commands, game):
        commands.execute_command(self, player_input, params)
        return self.__logged_on

    def message(self, message):
        self.server.send_message(self.client.uuid, message)

    def move(self, destination):
        super().move(destination)
        self.message(f"You arrive at '{self._location}'")
        self.message(rooms[self._location].description)
