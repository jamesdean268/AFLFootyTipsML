# HTML Parser Class
import requests
import re
from bs4 import BeautifulSoup

class HTMLScraper:

	__soup = ''

	def scrapeWebAndParseHTML(self, url):
		# Get web page html content
		page = requests.get(url)
		contents = page.content
		# Parse html
		self.__soup = BeautifulSoup(contents, 'html.parser')
		return self.__soup

# Execution of the class model for debugging purposes
if __name__ == '__main__':
	aflHTML = HTMLScraper()
	url = "https://afltables.com/afl/stats/teams/adelaide/2010_gbg.html"
	soup = aflHTML.scrapeWebAndParseHTML(url)
	print(soup)