# -------- Imports ---------
# Dependencies
import os
import sqlite3
import pandas as pd
import numpy as np

# Web
import requests
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from requests_html import HTMLSession
from bs4 import BeautifulSoup

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

def toLastnameFirstname(nameStr):
    nameStr = nameStr.replace(',','')
    nameArray = nameStr.split(' ')
    return nameArray[-2] + ', ' + nameArray[1]

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
statsYear = 2019

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


# -------------- Scrape afl.com to get team line-ups ------------
# Build URL
webStr = "https://www.afl.com.au/matches/team-lineups"
#webStr = "https://www.afl.com.au/matches/team-lineups?GameWeeks=5"

# Test
#page = requests.get(webStr)
#contents = page.content
#driver = webdriver.PhantomJS()
#driver.get(webStr)

'''
# create an HTML Session object
session = HTMLSession()
# Use the object above to connect to needed webpage
resp = session.get(webStr)
# Run JavaScript code on webpage
resp.html.render()
soup = BeautifulSoup(resp.html.html, "lxml")
'''

# Using Selenium

chrome_options = Options()
chrome_options.add_argument("--headless")
#driver = webdriver.Chrome(options=chrome_options)

from webdriver_manager.chrome import ChromeDriverManager
#driver = webdriver.Chrome(ChromeDriverManager().install())
driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
#driver = webdriver.Chrome(options=chrome_options)

driver.get(webStr)

# Create that beautiful soup
soup = BeautifulSoup(driver.page_source, "lxml")

# Connect to database
pwd = os.getcwd()
pathToDatabase = pwd + '/data/AFLFootyTips.db'
aflSqlite3Database = Sqlite3Database(pathToDatabase)

# Drop the previous weeks tables
try:
    aflSqlite3Database.runSqlite3Query("DROP TABLE CURRENT_TEAM_DATA")
    aflSqlite3Database.runSqlite3Query("DROP TABLE CURRENT_GAMES_PLAYED")
except:
    print("Tables Created")

# Create the tables
aflSqlite3Database.runSqlite3Query("CREATE TABLE CURRENT_TEAM_DATA(team text, year text, round text, score real, home_away text);")
aflSqlite3Database.runSqlite3Query("CREATE TABLE CURRENT_GAMES_PLAYED(player text, year text, team text, round text);")

# Extract teams and matches
teamPlayersArray = [['-1' for c in range(2)] for r in range(500)]
rP = 0

matchWrapperHTML = soup.find_all("div", "team-lineups__wrapper")
for matchHTML in matchWrapperHTML:
    # Get Team names
    teamsHTMLParsed = matchHTML.find_all("div", "team-lineups__team")
    teamsHTML = teamsHTMLParsed[0]
    # --------------- HOME TEAM -----------
    homeTeam = teamsHTML.contents[1].contents[4]
    # SQL Table
    insertQuery = "INSERT INTO CURRENT_TEAM_DATA VALUES ("
    insertQuery += "'" + str(homeTeam) + "', " # Team Name
    insertQuery += "'" + str(statsYear) + "', " # Year
    insertQuery += "'" + str('RX') + "', " # Round
    insertQuery += "'" + str(0) + "'," # Score
    insertQuery += "'" + "Home" + "'"
    insertQuery += ");"
    aflSqlite3Database.runSqlite3Query(insertQuery)
    # --------------- AWAY TEAM -----------
    awayTeam = teamsHTML.contents[5].contents[4]
    # SQL Table
    insertQuery = "INSERT INTO CURRENT_TEAM_DATA VALUES ("
    insertQuery += "'" + str(awayTeam) + "', " # Team Name
    insertQuery += "'" + str(statsYear) + "', " # Year
    insertQuery += "'" + str('RX') + "', " # Round
    insertQuery += "'" + str(0) + "'," # Score
    insertQuery += "'" + "Away" + "'"
    insertQuery += ");"
    aflSqlite3Database.runSqlite3Query(insertQuery)
    # Get Team Players
    playerRowsHTMLParsed = matchHTML.find_all("div", "team-lineups__positions-row")
    for playerRow in playerRowsHTMLParsed:
        homePlayersContainer = playerRow.contents[1]
        awayPlayersContainer = playerRow.contents[3]
        homePlayers = homePlayersContainer.find_all("span", "team-lineups__player")
        awayPlayers = awayPlayersContainer.find_all("span", "team-lineups__player")
        for homePlayer in homePlayers:
            teamPlayersArray[rP][0] = homeTeam
            # Strip out , and turn into lastname, firstname
            playerString = homePlayer.contents[2]
            playerName = toLastnameFirstname(playerString)
            teamPlayersArray[rP][1] = playerName
            rP += 1
            # ------------ SQL ------------
            insertQuery = "INSERT INTO CURRENT_GAMES_PLAYED VALUES ("
            insertQuery += '"' + str(playerName) + '", ' # Player Name
            insertQuery += "'" + str(statsYear) + "', " # Year
            insertQuery += "'" + str(homeTeam) + "', " # Team
            insertQuery += "'" + str('RX') + "'" # Round Number
            insertQuery += ");"
            aflSqlite3Database.runSqlite3Query(insertQuery)

        for awayPlayer in awayPlayers:
            teamPlayersArray[rP][0] = awayTeam
            # Strip out , and turn into lastname, firstname
            playerString = awayPlayer.contents[2]
            playerName = toLastnameFirstname(playerString)
            teamPlayersArray[rP][1] = playerName
            rP += 1
            # ------------ SQL ------------
            insertQuery = "INSERT INTO CURRENT_GAMES_PLAYED VALUES ("
            insertQuery += '"' + str(playerName) + '", ' # Player Name
            insertQuery += "'" + str(statsYear) + "', " # Year
            insertQuery += "'" + str(awayTeam) + "', " # Team
            insertQuery += "'" + str('RX') + "'" # Round Number
            insertQuery += ");"
            aflSqlite3Database.runSqlite3Query(insertQuery)




# -------------- Run queries to build training data -------------

def getFeatureSet(rows):
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
    
    return featureSet


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

# Run the SQL query to nearly build the feature set
sqlFile = open(pwd + '/data/CURRENT_TEAM_STATS_PER_ROUND_WITH_SCORE.sql')
sqlAsString = sqlFile.read()
c.execute(sqlAsString)
currentRows=c.fetchall()

featureSet = getFeatureSet(rows)
currentFeatureSet = getFeatureSet(currentRows)


# Output currentFeatureSet to csv
pathToCurrentFeatureSet = pwd + '/data/currentFeatureSet.csv'
fs = np.asarray(currentFeatureSet)  
np.savetxt(pathToCurrentFeatureSet, fs, fmt='%10.5f', delimiter=",")

# Add header
headerString = "DI_Avg,KI_Avg,MK_Avg,HB_Avg,GL_Avg,BH_Avg,HO_Avg,TK_Avg,RB_Avg,I5_Avg,CL_Avg,target"
with open(pathToCurrentFeatureSet, 'r+') as f:
    content = f.read()
    f.seek(0, 0)
    f.write(headerString.rstrip('\r\n') + '\n' + content)

# -------------------- TRAINING FEATURE SET ----------------

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




# -------------- Run tensorflow to extract predictions ----------
# Source: https://hackernoon.com/build-your-first-neural-network-to-predict-house-prices-with-keras-3fb0839680f4

# Use Pandas to create a dataframe
#dataframe = pd.read_csv(pathToFeatureSet)
df = pd.read_csv(pathToFeatureSet)
dataset = df.values

# Current data
currentDf = pd.read_csv(pathToCurrentFeatureSet)
currentDataset = currentDf.values
# Scale inputs
current_X = currentDataset[:,0:11]
min_max_scaler = preprocessing.MinMaxScaler()
current_X_scale = min_max_scaler.fit_transform(current_X)

# Features
X = dataset[:,0:11]
# Outputs (score classifier)
Y = dataset[:,11]

# Scale inputs
min_max_scaler = preprocessing.MinMaxScaler()
X_scale = min_max_scaler.fit_transform(X)


# --------------- DEBUG ----------------
# Split into test and train datasets
X_train, X_val_and_test, Y_train, Y_val_and_test = train_test_split(X_scale, Y, test_size=0.05)
X_val, X_test, Y_val, Y_test = train_test_split(X_val_and_test, Y_val_and_test, test_size=0.5)


# X_train (11 input features, 70% of full dataset)
# X_val (11 input features, 15% of full dataset)
# X_test (11 input features, 15% of full dataset)
# Y_train (1 label, 70% of full dataset)
# Y_val (1 label, 15% of full dataset)
# Y_test (1 label, 15% of full dataset)

print(X_train.shape, X_val.shape, X_test.shape, Y_train.shape, Y_val.shape, Y_test.shape)
print(current_X_scale.shape)

# Build model placeholder 11 inputs, two layers each with 32 nodes, one output
model = Sequential([
    Dense(32, activation='relu', input_shape=(11,)),
    #Dense(16, activation='relu'),
    Dense(1, activation='sigmoid'),
])

# Compile the model
model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

# Train the model
hist = model.fit(X_train, Y_train,
          batch_size=32, epochs=200,
          validation_data=(X_val, Y_val))

#print(Y_test)
model.evaluate(X_test, Y_test)[1]


# ------- PREDICTION ----
y_out = model.predict_classes(current_X_scale)
print(y_out)



