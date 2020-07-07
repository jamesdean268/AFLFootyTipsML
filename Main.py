# -------- Imports ---------
# Dependencies
import os
import sqlite3
import pandas as pd
import numpy as np

import tensorflow as tf
from tensorflow import feature_column
#from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.model_selection import train_test_split
from sklearn import preprocessing

# Classes
from src.Sqlite3Database import Sqlite3Database
from src.HTMLScraper import HTMLScraper
from src.TableBuilder import TableBuilder

'''
# A utility method to create a tf.data dataset from a Pandas Dataframe
def df_to_dataset(dataframe, shuffle=True, batch_size=32):
    dataframe = dataframe.copy()
    labels = dataframe.pop('target')
    ds = tf.data.Dataset.from_tensor_slices((dict(dataframe), labels))
    if shuffle:
        ds = ds.shuffle(buffer_size=len(dataframe))
    ds = ds.batch(batch_size)
    return ds
'''

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

years = [2012]#, 2013, 2014, 2015, 2016, 2017, 2018, 2019]

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
# clearTables = False
# currentYear = [2020]

# # Create objects
# aflHTMLScraper = HTMLScraper()
# pwd = os.getcwd()
# pathToDatabase = pwd + '/data/AFLFootyTips.db'
# aflSqlite3Database = Sqlite3Database(pathToDatabase)
# tableBuilder = TableBuilder(aflHTMLScraper, aflSqlite3Database, teams, teamsList, currentYear, fullTeams, useSQL, clearTables)

# # Remove all previous references to the current year
# deleteQuery = "DELETE FROM GAMES_PLAYED WHERE year = " + str(currentYear[0]) + ";"
# aflSqlite3Database.runSqlite3Query(deleteQuery)
# deleteQuery = "DELETE FROM MATCH_DATA WHERE year = " + str(currentYear[0]) + ";"
# aflSqlite3Database.runSqlite3Query(deleteQuery)
# deleteQuery = "DELETE FROM PLAYER_STATS WHERE year = " + str(currentYear[0]) + ";"
# aflSqlite3Database.runSqlite3Query(deleteQuery)
# deleteQuery = "DELETE FROM TEAM_DATA WHERE year = " + str(currentYear[0]) + ";"
# aflSqlite3Database.runSqlite3Query(deleteQuery)

# # Add in new table lines for the current year
# tableBuilder.calculateGamesPlayedAndPlayerStats()
# tableBuilder.calculateTeamAndMatchData()

# -------------- Run queries to build training data -------------

# Connect to the database
pwd = os.getcwd()
pathToDatabase = pwd + '/data/AFLFootyTips.db'
conn = sqlite3.connect(pathToDatabase, isolation_level=None, detect_types=sqlite3.PARSE_COLNAMES)
c = conn.cursor()

# Run the SQL query to nearly build the feature set
sqlFile = open(pwd + '/data/TEAM_STATS_PER_ROUND_WITH_SCORE.sql')
sqlAsString = sqlFile.read()
c.execute(sqlAsString)
rows=c.fetchall()

# Read the query contents into an array
numCols = 16
teamStatsPerRoundArray = [['-1' for c in range(numCols)] for r in range(len(rows))]
r = 0
for row in rows:
    for c in range(len(row)):
        teamStatsPerRoundArray[r][c] = str(row[c])
    r += 1

# Finish building the feature set in an array, then dump to CSV
featureSet = [['-1' for c in range(12)] for r in range(int(len(rows)/2))]
fr = 0
for r in range(0, len(rows), 2):
    fc = 0
    for c in range(3, 15):
        featureSet[fr][fc] = float(teamStatsPerRoundArray[r][c]) - float(teamStatsPerRoundArray[r+1][c]) 
        fc += 1
    fr += 1

# Use 5 classifiers:
# Home team wins > 50 = 2
# Home team wins > 20 = 1
# Home team wins or Away team wins < 20 = 0
# Away team wins > 20 = -1
# Away team wins > 50 = -2
scoreCol = 11
'''
for r in range(len(featureSet)):
    score = featureSet[r][scoreCol]
    if score > 29:
        featureSet[r][scoreCol] = 2
    elif score > 11:
        featureSet[r][scoreCol] = 1
    elif score < -29:
        featureSet[r][scoreCol] = -2
    elif score < -11:
        featureSet[r][scoreCol] = -1
    else:
        featureSet[r][scoreCol] = 0
'''


for r in range(len(featureSet)):
    score = featureSet[r][scoreCol]
    if score >= 0:
        featureSet[r][scoreCol] = 1
    else:
        featureSet[r][scoreCol] = 0


'''
for r in range(len(featureSet)):
    score = featureSet[r][scoreCol]
    if score > 23:
        featureSet[r][scoreCol] = 1
    elif score < -23:
        featureSet[r][scoreCol] = -1
    else:
        featureSet[r][scoreCol] = 0
'''


# Output to csv
pathToFeatureSet = pwd + '/data/featureSet.csv'
fs = np.asarray(featureSet)  
np.savetxt(pathToFeatureSet, fs, fmt='%10.5f', delimiter=",")

# Add header
headerString = "DI_Avg,KI_Avg,MK_Avg,HB_Avg,GL_Avg,BH_Avg,HO_Avg,TK_Avg,RB_Avg,I5_Avg,CL_Avg,target"
with open(pathToFeatureSet, 'r+') as f:
    content = f.read()
    f.seek(0, 0)
    f.write(headerString.rstrip('\r\n') + '\n' + content)

# -------------- Scrape afl.com to get team line-ups ------------




