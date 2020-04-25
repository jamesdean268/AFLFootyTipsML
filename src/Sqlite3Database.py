# imports
import sqlite3
from sqlite3 import Error
import os

class Sqlite3Database:

    # Dependency injection of HTML scraper and variables
    def __init__(self, pathToDatabase):
        self.pathToDatabase = pathToDatabase

    def createSqlite3Tables(self):
        try:
            # Connect to database
            dbConnection = sqlite3.connect(self.pathToDatabase)
            # Create DB Cursor
            cursorObj = dbConnection.cursor()
            # Execute SQL to create tables
            cursorObj.execute("CREATE TABLE GAMES_PLAYED(player text, year text, team text, round text);")
            # Commit changes
            dbConnection.commit()
        except:
            print("Database already exists")

    def runSqlite3Query(self, query):
        # Connect to database
        dbConnection = sqlite3.connect(self.pathToDatabase)
        # Create DB Cursor
        cursorObj = dbConnection.cursor()
        # Execute SQL to run a query
        cursorObj.execute(query)
        # Commit changes
        dbConnection.commit()




# Execution of the class model for debugging purposes
if __name__ == '__main__':
    pwd = os.getcwd()
    pathToDatabase = pwd + '/data/AFLFootyTips.db'
    dbObj = Sqlite3Database(pathToDatabase)
    dbObj.createSqlite3Tables()

