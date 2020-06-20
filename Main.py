# -------- Imports ---------
# Dependencies
import os
import sqlite3
import pandas as pd

# Classes
from src.Sqlite3Database import Sqlite3Database
from src.HTMLScraper import HTMLScraper
from src.TableBuilder import TableBuilder

# Teams and years
# Set team names based on afltables.com requirements
teamsList = ['adelaide',
'brisbanel',
'carlton',
'collingwood',
'essendon',
'fremantle',
'geelong',
'goldcoast',
'gws',
'hawthorn',
'melbourne',
'kangaroos',
'padelaide',
'richmond',
'stkilda',
'swans',
'westcoast',
'bullldogs']    

# Set team names based on afltables.com requirements
teams = ['adelaide',
'brisbanel',
'carlton',
'collingwood',
'essendon',
'fremantle',
'geelong',
'goldcoast',
'gws',
'hawthorn',
'melbourne',
'kangaroos',
'padelaide',
'richmond',
'stkilda',
'swans',
'westcoast',
'bullldogs']

years = [2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019]

# Set full team names based on afl.com.au requirements
fullTeams = ['Adelaide',
'Brisbane Lions',
'Carlton',
'Collingwood',
'Essendon',
'Fremantle',
'Geelong',
'Gold Coast',
'Greater Western Sydney',
'Hawthorn',
'Melbourne',
'North Melbourne',
'Port Adelaide',
'Richmond',
'St Kilda',
'Sydney',
'West Coast',
'Western Bulldogs'
]  

# Main exeuction script
generateDatabase = False
generateCSVs = False
useSQL = True

# ------------------- Data preparation thread -------------------
if generateDatabase:

    # Clear tables if generating database from scratch
    clearTables = True

    # Create objects
    aflHTMLScraper = HTMLScraper()
    pwd = os.getcwd()
    pathToDatabase = pwd + '/data/AFLFootyTips.db'
    aflSqlite3Database = Sqlite3Database(pathToDatabase)
    tableBuilder = TableBuilder(aflHTMLScraper, aflSqlite3Database, teams, teamsList, years, fullTeams, useSQL, clearTables)

    # Build all SQL Database
    tableBuilder.calculateGamesPlayedAndPlayerStats()
    tableBuilder.calculateTeamAndMatchData()

if generateCSVs:
    # Get path to database
    pwd = os.getcwd()
    pathToDatabase = pwd + '/data/AFLFootyTips.db'
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

# ------------------- Main execution thread -------------------
# Get latest data from website and update tables, scrape afl.com for players, do ML

# --------------- Populate current years data -----------------
clearTables = False
currentYear = 2020

# Create objects
aflHTMLScraper = HTMLScraper()
pwd = os.getcwd()
pathToDatabase = pwd + '/data/AFLFootyTips.db'
aflSqlite3Database = Sqlite3Database(pathToDatabase)
tableBuilder = TableBuilder(aflHTMLScraper, aflSqlite3Database, teams, teamsList, currentYear, fullTeams, useSQL, clearTables)

# Remove all previous references to the current year
deleteQuery = "DELETE FROM GAMES_PLAYED WHERE year = " + currentYear + ";"
aflSqlite3Database.runSqlite3Query(deleteQuery)
deleteQuery = "DELETE FROM MATCH_DATA WHERE year = " + currentYear + ";"
aflSqlite3Database.runSqlite3Query(deleteQuery)
deleteQuery = "DELETE FROM PLAYER_STATS WHERE year = " + currentYear + ";"
aflSqlite3Database.runSqlite3Query(deleteQuery)
deleteQuery = "DELETE FROM TEAM_DATA WHERE year = " + currentYear + ";"
aflSqlite3Database.runSqlite3Query(deleteQuery)

# Add in new table lines for the current year
tableBuilder.calculateGamesPlayedAndPlayerStats()
tableBuilder.calculateTeamAndMatchData()

# -------------- Run queries to build training data -------------



# -------------- Scrape afl.com to get team line-ups ------------


# -------------- Run tensorflow to extract predictions ----------


