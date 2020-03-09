# HTML Parser Class
import requests
import re
from bs4 import BeautifulSoup

class HTMLScraper:
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

	years = [2010, 2011]#, 2012, 2013, 2014, 2015, 2016, 2017, 2018]
	
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

	def getAllPlayerStats(self):
		cRow = 0
		rRow = 0
		arrSize = 100
		consolidatedTable = [['-1' for c in range(30)] for r in range(arrSize*100)]
		roundTable = [['-1' for c in range(4)] for r in range(arrSize*100)]
		for i in range(len(self.teams)):
			for j in range(len(self.years)):
				# Prepare afltables url
				webStr = "https://afltables.com/afl/stats/teams/" + self.teams[i] + "/" + str(self.years[j]) +"_gbg.html"
				# Get web page html content
				page = requests.get(webStr)
				contents = page.content
				# Parse html
				soup = BeautifulSoup(contents, 'html.parser')
				
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
							roundTable[rRow][0] = strTable[pctTable][r][0] # Player Name
							roundTable[rRow][1] = self.years[j] # Year
							roundTable[rRow][2] = self.teams[i] # Team
							roundTable[rRow][3] = headerArray[c] # Round Number
							gamesPlayed += 1
							rRow += 1
					strTable[pctTable][r][totCol + 1] = gamesPlayed
				
				# Add total features to consolidated table. Assumes all tables are the same size / shape
				for r in range(2, endRow):
					consolidatedTable[cRow][0] = strTable[pctTable][r][0] # Player Name
					consolidatedTable[cRow][1] = self.years[j] # Year
					consolidatedTable[cRow][2] = self.teams[i] # Team
					consolidatedTable[cRow][3] = strTable[pctTable][r][totCol + 1] # Games Played
					for t in range(len(tables)):
						consolidatedTable[cRow][4 + t] = strTable[t][r][totCol] # Total of feature
					cRow += 1


				'''
				# TODO: THIS
				print(strTable[0][2][2])
				print(strTable[0][2][24]) # Should be 9 games
				print(strTable[0][3][24]) # Should be 13 games
				print(strTable[0][6][24]) # Should be 19 games
				print(strTable[0][8][24]) # Should be 22 games
				'''

				# TODO: THIS
				p = 3 * (i + 2) * (j + 3)
				print(p)
				print(consolidatedTable[p][0]) # Armstrong, Tony
				print(consolidatedTable[p][1]) # 2010
				print(consolidatedTable[p][2]) # adelaide
				print(consolidatedTable[p][3]) # 9
				print(consolidatedTable[p][4]) # 140
				print(consolidatedTable[p][11]) # 14
				print(roundTable[12][:])

				


				# Extract table rows
				#tableRows = soup.find_all('tr')
				#for row in tableRows:
				#	row.a.contents


				#for row in tableRows:
				#	print(row)
				
				# Extract players list
				#playerLinks = soup.find_all(href=re.compile("players"))#('a')#re.compile('players'))
				
				# Extract table rows
				

				#for player in playerLinks:
				#	print(player.contents)
				
				#playersParsed = BeautifulSoup(playerLinks, 'html.parser')
				#print((str(playersParsed.a))
				#print(soup.prettify())


				


# Execution of the class model for debugging purposes
if __name__ == '__main__':
	aflHTML = HTMLScraper()
	print(aflHTML.teams[0])
	aflHTML.getAllPlayerStats()
	print(aflHTML.teams[0])