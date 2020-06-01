
# Imports
import os
import sqlite3
import pandas as pd
from src.Sqlite3Database import Sqlite3Database

# Main exeuction script

# Connect to SQLite3 database
pwd = os.getcwd()
pathToDatabase = pwd + '/data/AFLFootyTips.db'
aflSqlite3Database = Sqlite3Database(pathToDatabase)

'''
# Build query
query_GamesPlayedWithStats =  ( "SELECT * FROM GAMES_PLAYED "
                                "LEFT JOIN PLAYER_STATS "
                                "ON " 
                                "GAMES_PLAYED.player = PLAYER_STATS.player AND"
                                "GAMES_PLAYED.year = PLAYER_STATS.year AND"
                                "GAMES_PLAYED.team = PLAYER_STATS.team;"
)

print(aflSqlite3Database.runSqlite3Query(query_GamesPlayedWithStats))
'''

# Export tables to csv
conn = sqlite3.connect(pathToDatabase, isolation_level=None, detect_types=sqlite3.PARSE_COLNAMES)
# Export PLAYER_STATS
db_df = pd.read_sql_query("SELECT * FROM PLAYER_STATS", conn)
db_df.to_csv(pwd + '/data/PLAYER_STATS.csv', index=False)
# Export GAMES_PLAYED
db_df = pd.read_sql_query("SELECT * FROM GAMES_PLAYED", conn)
db_df.to_csv(pwd + '/data/GAMES_PLAYED.csv', index=False)
# Export MATCH_DATA
db_df = pd.read_sql_query("SELECT * FROM MATCH_DATA", conn)
db_df.to_csv(pwd + '/data/MATCH_DATA.csv', index=False)
# Export TEAM_DATA
db_df = pd.read_sql_query("SELECT * FROM TEAM_DATA", conn)
db_df.to_csv(pwd + '/data/TEAM_DATA.csv', index=False)

