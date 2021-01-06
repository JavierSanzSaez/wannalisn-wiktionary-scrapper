import urllib.request
from bs4 import BeautifulSoup


class Scraper:
    def __init__(self, site, language, number, letter):
        self.site = site  # The page from which get the info
        self.language = language  # The language in which to extract the words
        self.number = number  # The maximum number of words to extract
        self.letter = letter  # The letter from which to start the scrapping

    def create_index(self):
        # Returns a dictionary that serves as an search index

        r = urllib.request.urlopen(self.site)  # Get the page
        html = r.read()  # Transform the page into an html doc
        parser = "html.parser"
        soup = BeautifulSoup(html, parser)

        table_head = soup.find(summary="Contents")
        index = {}
        for link in table_head.td.find_all('a'):  # Looks for the first td found
            initial = link.string
            href = link.get('href')
            index.update({initial: href})
        return index

    def scrape(self):
        index = self.create_index()  # Get the search index
        start_point = index[self.letter]

        start_r = urllib.request.urlopen(start_point)
        html = start_r.read()
        parser = "html.parser"
        soup = BeautifulSoup(html, parser)
        page = soup.find_all(class_="mw-category-group")  # Returns a list of the categories

        count = 0
        for category in page:
            pass  # TODO Iterate and get the words


site = "https://en.wiktionary.org/w/index.php?title=Category:English_idioms"
language = "english"
number = 200
letter = 'Y'
Scraper(site, language, number, letter).scrape()
