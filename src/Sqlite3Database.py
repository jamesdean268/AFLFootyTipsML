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
            cursorObj.execute("CREATE TABLE PLAYER_STATS(player text, year text, team text, games_played integer, DI real, KI real, MK real, HB real, GL real, BH real, HO real, TK real, RB real, I5 real, CL real, DI_Avg real, KI_Avg real, MK_Avg real, HB_Avg real, GL_Avg real, BH_Avg real, HO_Avg real, TK_Avg real, RB_Avg real, I5_Avg real, CL_Avg real);")
            cursorObj.execute("CREATE TABLE TEAM_DATA(team text, year text, round text, score real, home_away text);")
            cursorObj.execute("CREATE TABLE MATCH_DATA(hometeam_awayteam text, year text, round text, match_score real);")
            # Current Rounds
            cursorObj.execute("CREATE TABLE CURRENT_TEAM_DATA(team text, year text, round text, score real, home_away text);")
            cursorObj.execute("CREATE TABLE CURRENT_GAMES_PLAYED(player text, year text, team text, round text);")
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

