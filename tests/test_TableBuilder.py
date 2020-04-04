import unittest

# Class to test
from src.TableBuilder import TableBuilder

# Dependencies
from src.HTMLScraper import HTMLScraper

class TableBuilder_Test(unittest.TestCase):

    # Spot test of player Stats
    def test_getPlayerStats_TableCreated_ValuesExpected(self):
        # Arrange
        aflHTMLScraper = HTMLScraper()
        tableBuilder = TableBuilder(aflHTMLScraper)
        # Act
        playerStats = tableBuilder.getPlayerStats()
        # Assert
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

    # Spot test of player Stats
    def test_getGamesPlayed_TableCreated_ValuesExpected(self):
        # Arrange
        aflHTMLScraper = HTMLScraper()
        tableBuilder = TableBuilder(aflHTMLScraper)
        # Act
        gamesPlayed = tableBuilder.getGamesPlayed()
        # Assert
        print(gamesPlayed[12][3]) # R12
        self.assertEqual(gamesPlayed[12][3], 'R12')

    # Spot test of team data
    def test_getTeamData_TableCreated_ValuesExpected(self):
        # Arrange
        aflHTMLScraper = HTMLScraper()
        tableBuilder = TableBuilder(aflHTMLScraper)
        # Act
        teamData = tableBuilder.getTeamData()
        # Assert
        self.assertEqual(teamData[9][0], 'adelaide')
        self.assertEqual(teamData[9][1], 2012)
        self.assertEqual(teamData[9][2], 'R1')
        self.assertEqual(int(teamData[9][3]), int('137'))
        self.assertEqual(teamData[9][4], 'Away')


        # Spot test of match data
    def test_getMatchData_TableCreated_ValuesExpected(self):
        # Arrange
        aflHTMLScraper = HTMLScraper()
        tableBuilder = TableBuilder(aflHTMLScraper)
        # Act
        matchData = tableBuilder.getMatchData()
        # Assert
        self.assertEqual(matchData[0][0], 'gws_swans')
        self.assertEqual(matchData[0][1], 2012)
        self.assertEqual(matchData[0][2], 'R1')
        self.assertEqual(matchData[0][3], -63)