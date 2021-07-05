import os
import sqlite3
import json

class CacheProcessor:
    """Saves and retrives the internal cache of program which has data related to file attributes."""

    def __init__(self):
        self.__cache_dir__ = os.path.abspath(os.path.join(
            os.path.pardir, 'cache'))
        self.__cache_f__ = os.path.abspath(os.path.join(
            self.__cache_dir__, 'attributes.db'))

        if not os.path.exists(self.__cache_dir__) : os.mkdir(self.__cache_dir__)

        self.table = "FileAttributes"
        self.conn = sqlite3.connect(self.__cache_f__)
        self.cursor = self.conn.cursor()
        self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS {self.table}
         (FILE TEXT  PRIMARY KEY NOT NULL,
         OBJECT_COL  TEXT        NOT NULL,
         SPACE_COL   TEXT        NOT NULL,
         ST_TIME_COL TEXT        NOT NULL,
         ND_TIME_COL TEXT        NOT NULL);''')
        self.conn.commit()


    def file_cache_exists(self, filepath: str) -> bool:
        """Checks if the given file has any previous recorded settigns in database."""
        self.cursor.execute(f"SELECT * FROM {self.table} WHERE FILE={filepath};")
        got = self.cursor.fetchall()
        if len(got) == 0:
            return False
        return True


    def insert_cache(self, data:dict):
        """Inserts a new record into the database."""
        # Get all the data from dictionary
        fname = data['file']
        object_col  = data['object_col']
        space_col   = data['space_col']
        st_time_col = data['st_time_col']
        nd_time_col = data['nd_time_col']
        # Insert the above record into database.
        self.cursor.execute(f"INSERT INTO {self.table} (FILE, OBJECT_COL, SPACE_COL, ST_TIME_COL, ND_TIME_COL) VALUES (?,?,?,?,?)",
            (fname, object_col, space_col, st_time_col, nd_time_col))
        # Commit the changes
        self.conn.commit()


    def update_cache(self, data:dict):
        """Updates the existing cache."""
        # Get all the data from dictionary
        fname = data['file']
        object_col  = data['object_col']
        space_col   = data['space_col']
        st_time_col = data['st_time_col']
        nd_time_col = data['nd_time_col']
        # Update the database with the above data.
        query = f"""UPDATE {self.table} 
                    SET OBJECT_COL = ?, 
                    SPACE_COL = ?, 
                    ST_TIME_COL = ?, 
                    ND_TIME_COL = ?
                WHERE FILE = ?""",
        self.cursor.execute(query, (object_col, space_col, st_time_col, nd_time_col, fname))
        # Commit the changes
        self.conn.commit()


    def retrieve_cache(self, filepath):
        """Returns the file settings from database."""
        self.cursor.execute(f"SELECT * FROM {self.table} WHERE FILE={filepath};")
        got = self.cursor.fetchall()
        return got


class CacheSaver:
    """Saves Cache of the application."""
    def __init__(self):
        self.__cache_dir__ = os.path.abspath(os.path.join(
            os.path.pardir, 'cache'))
        self.__cache_f__ = os.path.abspath(os.path.join(
            self.__cache_dir__, 'attributes.json'))

        if not os.path.exists(self.__cache_dir__) : os.mkdir(self.__cache_dir__)

    def save_cache(self, cache: dict) -> None:
        with open(self.__cache_f__, "w") as f:
            json.dump(cache, f)


class CacheRetriever:
    def __init__(self):
        self.__cache_dir__ = os.path.abspath(os.path.join(
            os.path.pardir, 'cache'))
        self.__cache_f__ = os.path.abspath(os.path.join(
            self.__cache_dir__, 'attributes.json'))

        if not os.path.exists(self.__cache_dir__) : os.mkdir(self.__cache_dir__)

    def retrieve_cache(self) -> dict:
        cache: dict = {}
        with open(self.__cache_f__, "r") as f:
            cache = json.load(f)
        return cache

if __name__ == "__main__":
    retriever = CacheRetriever()
    cache = retriever.retrieve_cache()
    print(cache)