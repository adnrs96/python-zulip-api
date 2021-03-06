"""This module is used for managing, storing, and operating certain
functions to said data. Almost every action of the data is wrapped with the
connection opening and closing. This module is supplied with a default name
for the database. If the user is not satisfied with the name, the user can
change it with their own database name for convenience.

Essentially, this database is used for storing static matches that hasn't
finished yet so any matches that are finished will be removed.
"""

import json

from .constants import EMPTY_BOARD


class MerelsStorage():
    def __init__(self, storage):
        """Instantiate storage field.

        The current database has this form:
            TOPIC_NAME (UNIQUE)
                +----> TURN
                +----> X_TAKEN
                +----> O_TAKEN
                +----> BOARD
                +----> HILL_UID
                +----> TAKE_MODE

        :param name: Name of the storage
        """
        self.storage = storage

    def create_new_game(self, topic_name):
        """ Creates a new merels game if it doesn't exists yet.

        :param topic_name: Name of the topic
        :return: True, if the game is successfully created, False if otherwise.
        """

        parameters = ("X", 0, 0, EMPTY_BOARD, "", 0)

        # Checks whether the game exists yet
        # If it exists

        try:
            if not self.storage.contains(topic_name) or self.storage.get(
                    topic_name) == "":
                self.storage.put(topic_name, json.dumps(parameters))
                return True
            else:
                return False
        except KeyError:
            self.storage.put(topic_name, json.dumps(parameters))
            return True

    def update_game(self, topic_name, turn, x_taken, o_taken, board, hill_uid,
                    take_mode):
        """ Updates the current status of the game to the database.

        :param topic_name: The name of the topic
        :param turn: "X" or "O"
        :param x_taken: How many X's are taken from the board during the
                        gameplay by O
        :param o_taken: How many O's are taken from the board during the
                        gameplay by X
        :param board: A compact representation of the grid
        :param hill_uid: Unique hill id
        :param take_mode: Whether the game is in take mode, which "turn" has
                        to take a piece
        :return: None
        """

        parameters = (
            turn, x_taken, o_taken, board, hill_uid, take_mode)

        self.storage.put(topic_name, json.dumps(parameters))

    def remove_game(self, topic_name):
        """ Removes the game from the database by setting it to an empty
        string. An empty string marks an empty match.

        :param topic_name: The name of the topic
        :return: None
        """

        self.storage.put(topic_name, "")

    def get_game_data(self, topic_name):
        """Gets the game data

        :param topic_name: The name of the topic
        :return: A tuple containing the data
        """

        try:
            select = json.loads(self.storage.get(topic_name))
        except (json.decoder.JSONDecodeError, KeyError):
            select = ""

        if select == "":
            return None
        else:
            res = (topic_name, select[0], select[1], select[2], select[3],
                   select[4], select[5])

            return res
