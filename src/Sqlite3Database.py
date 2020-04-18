# imports
import sqlite3
from sqlite3 import Error
import os

class Sqlite3Database:

    # Tables
    GAMES_PLAYED = []
    PLAYER_STATS = []
    MATCH_DATA = []
    TEAM_DATA = []

    def connectToSqlite3DatabaseFile(self, pathToDatabase):
        conn = sqlite3.connect(pathToDatabase)
        return conn

    def createSqlite3Tables(self, dbConnection):
        # Create DB Cursor
        cursorObj = dbConnection.cursor()
        # Execute SQL to create tables
        cursorObj.execute("CREATE TABLE GAMES_PLAYED(player text, year text, team text, round text);")
        cursorObj.execute("INSERT INTO GAMES_PLAYED VALUES('James', '2020', 'James', 'R1');")
        # Commit changes
        dbConnection.commit()



# Execution of the class model for debugging purposes
if __name__ == '__main__':
    pwd = os.getcwd()
    pathToDatabase = pwd + '/data/AFLFootyTips.db'
    dbObj = Sqlite3Database()
    dbConnection = dbObj.connectToSqlite3DatabaseFile(pathToDatabase)
    dbObj.createSqlite3Tables(dbConnection)

