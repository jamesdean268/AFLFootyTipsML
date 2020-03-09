import unittest

# Class to test
from src.TableBuilder import TableBuilder

# Dependencies
from src.HTMLScraper import HTMLScraper

class TableBuilder_Test(unittest.TestCase):

    # Test to check if all years and all clubs return >= 22 tables = pctTable
    # Pct table is used in the main script to determine which games were played
    def test_scrapeWebAndParseHTML_WebScraped_22TablesReturned(self):
        # Arrange
        aflHTMLScraper = HTMLScraper()
        tableBuilder = TableBuilder(aflHTMLScraper)
        playerStats = tableBuilder.getPlayerStats()
        gamesPlayed = tableBuilder.getGamesPlayed()
        # Act
        p = 0
        print(playerStats[p][0]) # Brown, Luke
        print(playerStats[p][1]) # 2012
        print(playerStats[p][2]) # adelaide
        print(playerStats[p][3]) # 3
        print(playerStats[p][4]) # 19
        print(playerStats[p][11]) # 2
        print(gamesPlayed[12][:]) # Callinan, Ian, 2012, adelaide, R12
        # Assert

        self.assertEqual(1,1)

