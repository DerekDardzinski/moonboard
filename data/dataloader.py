import sqlite3
from sqlite3 import Error
import numpy as np
import time

class DataLoader(object):
    """
    Class for accessing the data from the database file
    """

    def __init__(self, file):
        """TODO: to be defined. """
        self.connection = self.create_connection(file)

    def create_connection(self, file):
        """
        Creates a database connection to the SQLite database specified
        by the file path.

        Parameters:
            file (str): File path to local database file

        Returns:
            Database connection
        """
        conn = None
        try:
            conn = sqlite3.connect(file)
        except Error as e:
            print(e)

        return conn


    def get_moves_from_Id(self, Id):
        """
        Get the moves of a route given a route Id.

        Parameters:
            Id (int): Id of a given route.

        Returns:
            List of moves.
        """
        cur = self.connection.cursor()
        cur.execute(
            """
            SELECT GROUP_CONCAT(Position, ',') FROM problemMoves
            WHERE Problem = ?
            GROUP BY Problem
            """,
            (Id, )
        )

        moves = cur.fetchone()[0]

        return moves


    def get_all_data(self, max_grade=10):
        """
        Load all the data from the database

        Parameters:
            Max grade (int): Maximum grade to load in from a database.

        Returns:
            The Id's, Grades, and Moves of all routes
        """
        cursor = self.connection.cursor()
        cursor.execute(
            """
            SELECT
                Problem,
                CAST(Grade as INTEGER),
                GROUP_CONCAT(Position, ','),
                GROUP_CONCAT(IsStart, ','),
                GROUP_CONCAT(IsEnd, ',')
            FROM problemMoves
            INNER JOIN problems on problemMoves.Problem = problems.Id
            WHERE Problem IN (
                SELECT Id FROM problems
                WHERE CAST(Grade as INTEGER) < ?
            )
            GROUP BY Problem
            """,
            (max_grade, )
        )
        data = cursor.fetchall()
        cursor.close()

        return data

        


loader = DataLoader('./moonboard_data.db')
data = loader.get_all_data()
name, grades, positions, start, end = list(zip(*data))
print(loader.get_moves_from_Id(Id=name[0]))
