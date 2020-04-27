
# Imports
import os
from src.Sqlite3Database import Sqlite3Database

# Main exeuction script

# Connect to SQLite3 database
pwd = os.getcwd()
pathToDatabase = pwd + '/data/AFLFootyTips.db'
aflSqlite3Database = Sqlite3Database(pathToDatabase)

# Build query
query_GamesPlayedWithStats =  ( "SELECT * FROM GAMES_PLAYED "
                                "OUTER JOIN PLAYER_STATS "
                                "ON " 
                                "GAMES_PLAYED.player = PLAYER_STATS.player,"
                                "GAMES_PLAYED.year = PLAYER_STATS.year,"
                                "GAMES_PLAYED.team = PLAYER_STATS.team;"
)

print(aflSqlite3Database.runSqlite3Query(query_GamesPlayedWithStats))



