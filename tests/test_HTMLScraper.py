import unittest

# Class to test
from src.HTMLScraper import HTMLScraper

class HTMLScraper_Test(unittest.TestCase):
    """
    The basic class that inherits unittest.TestCase
    """

    # Set team names based on afltables.com requirements
    teams = ['adelaide',
    'brisbanel']#,
    '''
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

    years = [2012, 2013]#, 2014, 2015, 2016, 2017, 2018, 2019]

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

    # Test to check if all years and all clubs return >= 22 tables = pctTable
    # Pct table is used in the main script to determine which games were played
    def test_scrapeWebAndParseHTML_WebScraped_22TablesReturned(self):
        # Arrange
        aflHTML = HTMLScraper()
        for i in range(len(self.teams)):
            for j in range(len(self.years)):
                url = "https://afltables.com/afl/stats/teams/" + self.teams[i] + "/" + str(self.years[j]) +"_gbg.html"
                # Act
                soup = aflHTML.scrapeWebAndParseHTML(url)
                tables = soup.find_all('table')
                # Assert
                key = "Year: " + str(self.years[j]) + " Team: " + self.teams[i]
                self.assertGreaterEqual(len(tables), 22, key)

