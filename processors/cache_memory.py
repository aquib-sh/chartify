import os
import sqlite3
import json


class CacheProcessor:
    """Saves and retrives the internal cache of program which has data related to file attributes."""

    def __init__(self, basefile, table):
        self.__cache_dir__ = "cache"
        self.__cache_f__ = os.path.abspath(os.path.join(self.__cache_dir__, basefile))

        if not os.path.exists(self.__cache_dir__):
            os.mkdir(self.__cache_dir__)

        self.table = table
        self.conn = sqlite3.connect(self.__cache_f__)
        # print(f"[+] Connected to database in {self.__cache_f__}")
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            f"""CREATE TABLE IF NOT EXISTS {self.table}
            (COLOR TEXT PRIMARY KEY NOT NULL,
             RED   REAL             NOT NULL,
             GREEN REAL             NOT NULL,
             BLUE  REAL             NOT NULL,
             ALPHA REAL             NOT NULL);"""
        )
        self.conn.commit()

    def file_cache_exists(self, filepath: str) -> bool:
        """Checks if the given file has any previous recorded settigns in database."""
        self.cursor.execute(f"SELECT * FROM {self.table} WHERE FILE={filepath};")
        got = self.cursor.fetchall()
        if len(got) == 0:
            return False
        return True

    def insert_cache(self, colorname: str, rgba: tuple[float, float, float, float]):
        """Inserts a new record into the database.

        Parameters
        ----------
        colorname: str
            Colorname to save it as.

        data: tuple[float, float, float, float]
            RGBA float values must be passed as a tuple
            (red_value, green_value, blue_value, alpha_value)
        """
        if colorname == None or type(colorname) != str or len(colorname) <= 1:
            raise Exception(
                "InvalidColorNameError", "colorname must be a string with length > 1"
            )
        if len(rgba) != 4:
            raise Exception(
                "InvalidParameterError",
                "data: tuple must have only 4 elements, (red_value, green_value, blue_value, alpha_value)",
            )

        # Get all the data from dictionary
        red, green, blue, alpha = rgba
        # Insert the above record into database.
        self.cursor.execute(
            f"INSERT INTO {self.table} (COLOR, RED, GREEN, BLUE, ALPHA) VALUES (?,?,?,?,?)",
            (colorname, red, green, blue, alpha),
        )
        # Commit the changes
        self.conn.commit()

    def update_cache(self, colorname: str, rgba: tuple[float, float, float, float]):
        """Updates the existing cache.

        Parameters
        ----------
        colorname: str
            Colorname to save it as.

        data: tuple[float, float, float, float]
            RGBA float values must be passed as a tuple
            (red_value, green_value, blue_value, alpha_value)
        """
        # Get all the data from dictionary
        if colorname == None or type(colorname) != str or len(colorname) <= 1:
            raise Exception(
                "InvalidColorNameError", "colorname must be a string with length > 1"
            )
        if len(rgba) != 4:
            raise Exception(
                "InvalidParameterError",
                "data: tuple must have only 4 elements, (red_value, green_value, blue_value, alpha_value)",
            )

        # Get all the data from dictionary
        red, green, blue, alpha = rgba
        # Update the database with the above data.
        query = (
            f"""UPDATE {self.table} 
                    RED = ?, 
                    GREEN = ?, 
                    BLUE = ?, 
                    ALPHA = ?,
                WHERE COLOR = ?""",
        )
        self.cursor.execute(query, (colorname, red, green, blue, alpha))
        # Commit the changes
        self.conn.commit()

    def retrieve_cache(self) -> dict:
        """Returns data from database as a dictionary."""
        self.cursor.execute(f"SELECT * FROM {self.table};")
        retrieved_data: list = self.cursor.fetchall()
        data: dict = {}

        for row in retrieved_data:
            data[row[0]] = row[1:]

        return data


class CacheSaver:
    """Saves Cache of the application."""

    def __init__(self):
        self.__cache_dir__ = os.path.abspath("cache")
        self.__cache_f__ = os.path.abspath(
            os.path.join(self.__cache_dir__, "attributes.json")
        )

        if not os.path.exists(self.__cache_dir__):
            os.mkdir(self.__cache_dir__)

    def save_cache(self, cache: dict) -> None:
        with open(self.__cache_f__, "w") as f:
            json.dump(cache, f, indent=4)


class CacheRetriever:
    def __init__(self):
        self.__cache_dir__ = os.path.abspath("cache")
        self.__cache_f__ = os.path.abspath(
            os.path.join(self.__cache_dir__, "attributes.json")
        )
        if not os.path.exists(self.__cache_dir__):
            os.mkdir(self.__cache_dir__)

    def cache_exists(self):
        return os.path.exists(self.__cache_f__)

    def retrieve_cache(self) -> dict:
        cache: dict = {}
        with open(self.__cache_f__, "r") as f:
            cache = json.load(f)
        return cache
