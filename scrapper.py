import urllib.request
from bs4 import BeautifulSoup


class Scraper:
    def __init__(self, site, language, number, letter):
        self.site = site  # The page to get the info
        self.language = language  # The language to extract the words
        self.number = number  # The maximum number of words to extract
        self.letter = letter  # The letter from which to start the scrapping

    def scrape(self):
        r = urllib.request.urlopen(self.site)  # Get the page
        html = r.read()  # Transform the page into an html doc
        parser = "html.parser"
        soup = BeautifulSoup(html, parser)

        table_head = soup.find(summary="Contents")
        index = []
        for link in table_head.td.find_all('a'):  # Looks for the first td found
            letter = link.string
            href = link.get('href')
            index.append([href, letter])

        print(index)


site = "https://en.wiktionary.org/w/index.php?title=Category:English_idioms"
language = "english"
number = 200
letter = 'A'
Scraper(site, language, number).scrape()
