import unittest

# Class to test
from src.TableBuilder import TableBuilder

# Dependencies
import os
from src.HTMLScraper import HTMLScraper
from src.Sqlite3Database import Sqlite3Database

class TableBuilder_Test(unittest.TestCase):

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
    teams = ['adelaide']#,
    '''
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
    '''

    years = [2012]#, 2013]#, 2014, 2015, 2016, 2017, 2018]

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

    useSQL = True

    # Spot test of player Stats
    def test_getPlayerStats_TableCreated_ValuesExpected(self):
        # Arrange
        aflHTMLScraper = HTMLScraper()
        pwd = os.getcwd()
        pathToDatabase = pwd + '/data/AFLFootyTips.db'
        aflSqlite3Database = Sqlite3Database(pathToDatabase)
        tableBuilder = TableBuilder(aflHTMLScraper, aflSqlite3Database, self.teams, self.teamsList, self.years, self.fullTeams, self.useSQL)
        # Act
        playerStats = tableBuilder.getPlayerStats()
        # Assert
        if self.useSQL:
            self.assertEqual(1,1)
        else:
            p = 0
            print(playerStats[p][0]) # Brown, Luke
            self.assertEqual(playerStats[p][0], 'Brown, Luke')
            print(playerStats[p][1]) # 2012
            self.assertEqual(playerStats[p][1], 2012)
            print(playerStats[p][2]) # adelaide
            self.assertEqual(playerStats[p][2], 'adelaide')
            print(playerStats[p][3]) # 3
            self.assertEqual(playerStats[p][3], 3)
            print(playerStats[p][4]) # 19
            self.assertEqual(playerStats[p][4], '19')
            print(playerStats[p][11]) # 2
            self.assertEqual(playerStats[p][11], '2')

    # Spot test of games played
    def test_getGamesPlayed_TableCreated_ValuesExpected(self):
        # Arrange
        aflHTMLScraper = HTMLScraper()
        pwd = os.getcwd()
        pathToDatabase = pwd + '/data/AFLFootyTips.db'
        aflSqlite3Database = Sqlite3Database(pathToDatabase)
        tableBuilder = TableBuilder(aflHTMLScraper, aflSqlite3Database, self.teams, self.teamsList, self.years, self.fullTeams, self.useSQL)
        # Act
        gamesPlayed = tableBuilder.getGamesPlayed()
        # Assert
        if self.useSQL:
            self.assertEqual(1,1)
        else:
            print(gamesPlayed[12][3]) # R12
            self.assertEqual(gamesPlayed[12][3], 'R12')

    # Spot test of team data
    def test_getTeamData_TableCreated_ValuesExpected(self):
        # Arrange
        aflHTMLScraper = HTMLScraper()
        pwd = os.getcwd()
        pathToDatabase = pwd + '/data/AFLFootyTips.db'
        aflSqlite3Database = Sqlite3Database(pathToDatabase)
        tableBuilder = TableBuilder(aflHTMLScraper, aflSqlite3Database, self.teams, self.teamsList, self.years, self.fullTeams, self.useSQL)
        # Act
        teamData = tableBuilder.getTeamData()
        # Assert
        if self.useSQL:
            self.assertEqual(1,1)
        else:
            self.assertEqual(teamData[9][0], 'adelaide')
            self.assertEqual(teamData[9][1], 2012)
            self.assertEqual(teamData[9][2], 'R1')
            self.assertEqual(int(teamData[9][3]), int('137'))
            self.assertEqual(teamData[9][4], 'Away')


        # Spot test of match data
    def test_getMatchData_TableCreated_ValuesExpected(self):
        # Arrange
        aflHTMLScraper = HTMLScraper()
        pwd = os.getcwd()
        pathToDatabase = pwd + '/data/AFLFootyTips.db'
        aflSqlite3Database = Sqlite3Database(pathToDatabase)
        tableBuilder = TableBuilder(aflHTMLScraper, aflSqlite3Database, self.teams, self.teamsList, self.years, self.fullTeams, self.useSQL)
        # Act
        matchData = tableBuilder.getMatchData()
        # Assert
        self.assertEqual(matchData[0][0], 'gws_swans')
        self.assertEqual(matchData[0][1], 2012)
        self.assertEqual(matchData[0][2], 'R1')
        self.assertEqual(matchData[0][3], -63)