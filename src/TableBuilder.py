

class TableBuilder:

    # Tables
    GAMES_PLAYED = []
    PLAYER_STATS = []

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

    years = [2012, 2013]#, 2014, 2015, 2016, 2017, 2018]

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

    # Dependency injection of HTML scraper
    def __init__(self, HTMLScraper):
        self._HTMLScraper = HTMLScraper

    def getPlayerStats(self):
        if self.PLAYER_STATS == []:
            self.calculateGamesPlayedAndPlayerStats()
        return self.PLAYER_STATS
    
    def getGamesPlayed(self):
        if self.GAMES_PLAYED == []:
            self.calculateGamesPlayedAndPlayerStats()
        return self.GAMES_PLAYED

    def calculateGamesPlayedAndPlayerStats(self):

        # Initialise internal variables and arrays
        cRow = 0
        rRow = 0
        arrSize = 100
        self.PLAYER_STATS = [['-1' for c in range(30)] for r in range(arrSize*100)]
        self.GAMES_PLAYED = [['-1' for c in range(4)] for r in range(arrSize*100)]

        # Loop through each team and each year to get all the data
        for i in range(len(self.teams)):
            for j in range(len(self.years)):

                # Build URL
                webStr = "https://afltables.com/afl/stats/teams/" + self.teams[i] + "/" + str(self.years[j]) +"_gbg.html"
                
                # Get parsed HTML
                #htmlScraper = HTMLScraper()
                #soup = htmlScraper.scrapeWebAndParseHTML(webStr)
                soup = self._HTMLScraper.scrapeWebAndParseHTML(webStr)

                # Extract tables
                tables = soup.find_all('table')

                # Store all tables in 3D array
                strTable = [[['-1' for c in range(arrSize)] for r in range(arrSize*10)] for t in range(len(tables))]
                t = 0
                for table in tables:
                    r = 0
                    for row in table.find_all('tr'):
                        c = 0
                        for col in row.find_all('td'):
                            strTable[t][r][c] = col.get_text()
                            c += 1
                        r += 1
                    t += 1
                        
                # Loop through each player, capture tot column idx and value, and add number of games played
                # To guarantee 'isnumeric' works to calculate number of games played, we use the pct played table
                pctTable = 22

                # Extract round data
                headerArray = ['-1' for t in range(arrSize)]
                headerTable = tables[pctTable]
                headers = headerTable.find_all('thead')
                roundHeaders = headers[0].contents
                roundHeader = roundHeaders[1]
                c = 0
                for col in roundHeader.find_all('th'):
                    headerArray[c] = col.get_text()
                    c += 1

                # Extract max row index
                r = 2
                while not(strTable[pctTable][r][0] == '-1'):
                    r += 1
                endRow = r - 1
                # Extract max col index
                c = 1
                while not(strTable[pctTable][2][c] == '-1'):
                    c += 1
                totCol = c - 1
                # Calculate number of games played and add to additional column
                for r in range (2, endRow): # First player row index
                    gamesPlayed = 0
                    for c in range(1, totCol):
                        if str.isnumeric(strTable[pctTable][r][c]):
                            self.GAMES_PLAYED[rRow][0] = strTable[pctTable][r][0] # Player Name
                            self.GAMES_PLAYED[rRow][1] = self.years[j] # Year
                            self.GAMES_PLAYED[rRow][2] = self.teams[i] # Team
                            self.GAMES_PLAYED[rRow][3] = headerArray[c] # Round Number
                            gamesPlayed += 1
                            rRow += 1
                    strTable[pctTable][r][totCol + 1] = gamesPlayed
                
                # Add total features to consolidated table. Assumes all tables are the same size / shape
                for r in range(2, endRow):
                    self.PLAYER_STATS[cRow][0] = strTable[pctTable][r][0] # Player Name
                    self.PLAYER_STATS[cRow][1] = self.years[j] # Year
                    self.PLAYER_STATS[cRow][2] = self.teams[i] # Team
                    self.PLAYER_STATS[cRow][3] = strTable[pctTable][r][totCol + 1] # Games Played
                    for t in range(len(tables)):
                        self.PLAYER_STATS[cRow][4 + t] = strTable[t][r][totCol] # Total of feature
                    cRow += 1



# Execution of the class model for debugging purposes
if __name__ == '__main__':
    placeholder = 0
