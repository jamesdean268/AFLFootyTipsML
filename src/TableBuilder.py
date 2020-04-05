

class TableBuilder:

    # Tables
    GAMES_PLAYED = []
    PLAYER_STATS = []
    MATCH_DATA = []
    TEAM_DATA = []

    # Variables (now injected!)
    teamsList = []    
    teams = [] # Set team names based on afltables.com requirements
    years = []
    fullTeams = []

    # Dependency injection of HTML scraper and variables
    def __init__(self, HTMLScraper, teams, teamsList, years, fullTeams):
        self._HTMLScraper = HTMLScraper
        self.teams = teams
        self.teamsList = teamsList
        self.years = years
        self.fullTeams = fullTeams

    # Get in-memory array of player stats
    def getPlayerStats(self):
        if self.PLAYER_STATS == []:
            self.calculateGamesPlayedAndPlayerStats()
        return self.PLAYER_STATS
    
    # Get in-memory array of games played
    def getGamesPlayed(self):
        if self.GAMES_PLAYED == []:
            self.calculateGamesPlayedAndPlayerStats()
        return self.GAMES_PLAYED
    
    # Get in-memory array of team data
    def getTeamData(self):
        if self.TEAM_DATA == []:
            self.calculateTeamAndMatchData()
        return self.TEAM_DATA
    
    # Get in-memory array of match data
    def getMatchData(self):
        if self.MATCH_DATA == []:
            self.calculateTeamAndMatchData()
        return self.MATCH_DATA

    # Use the HTML scraper to calculate player stats and games played
    def calculateGamesPlayedAndPlayerStats(self):

        # Initialise internal variables and arrays
        cRow = 0
        rRow = 0
        arrSize = 1000
        self.PLAYER_STATS = [['-1' for c in range(30)] for r in range(arrSize)]
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

    # Use the HTML scraper to calculate the team data and match data
    def calculateTeamAndMatchData(self):

        # Initialise internal variables and arrays
        tRow = 0
        mRow = 0
        arrSize = 10000
        self.MATCH_DATA = [['-1' for c in range(4)] for r in range(arrSize*100)]
        self.TEAM_DATA = [['-1' for c in range(5)] for r in range(arrSize*100)]

        # Loop through each team and each year to get all the data
        for j in range(len(self.years)):

            # Build URL
            webStr = "https://afltables.com/afl/seas/" + str(self.years[j]) + ".html"
            
            # Get parsed HTML
            #htmlScraper = HTMLScraper()
            #soup = htmlScraper.scrapeWebAndParseHTML(webStr)
            soup = self._HTMLScraper.scrapeWebAndParseHTML(webStr)

            # Extract tables
            tables = soup.find_all('table')

            # Extract rounds, scores, and teams
            t = 0
            for table in tables:
                # Extract Round Number
                if ('border' in table.attrs):
                    if (table.attrs['border'] == '2'):
                        boldText = table.find_all('b')
                        roundNum = boldText[0].get_text()
                        if "Round" in roundNum:
                            roundText = "R" + roundNum.split(" ")[1]

                            # Extract team names and scores
                            roundTable = tables[t + 1]
                            teamNames = roundTable.find_all(width="16%")

                            # Extract team scores
                            teamScores = roundTable.find_all(width="5%")

                            # Populate TEAM_DATA
                            for i in range(0,len(teamScores)):
                                fullTeamName = teamNames[i].get_text()
                                teamIdx = self.fullTeams.index(fullTeamName)
                                self.TEAM_DATA[tRow][0] = self.teamsList[teamIdx] # Team Name
                                self.TEAM_DATA[tRow][1] = self.years[j] # Year
                                self.TEAM_DATA[tRow][2] = roundText # Round
                                self.TEAM_DATA[tRow][3] = teamScores[i].get_text() # Score
                                if i % 2 == 0:
                                    self.TEAM_DATA[tRow][4] = "Home"
                                else:
                                    self.TEAM_DATA[tRow][4] = "Away"
                                tRow += 1
                               
                # Increment table
                t += 1

            # Populate MATCH_DATA
            endRow = 0
            while not(self.TEAM_DATA[endRow][0] == '-1'):
                endRow += 1
            
            for i in range(0, endRow, 2):
                self.MATCH_DATA[mRow][0] = self.TEAM_DATA[i][0] + "_" + self.TEAM_DATA[i + 1][0] # HomeTeam_AwayTeam
                self.MATCH_DATA[mRow][1] = self.TEAM_DATA[i][1] # Year
                self.MATCH_DATA[mRow][2] = self.TEAM_DATA[i][2] # Round
                self.MATCH_DATA[mRow][3] = int(self.TEAM_DATA[i][3]) - int(self.TEAM_DATA[i + 1][3]) # Home Score - Away Score
                mRow += 1

            


# Execution of the class model for debugging purposes
if __name__ == '__main__':
    placeholder = 0

