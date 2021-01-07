import urllib.request, csv
from bs4 import BeautifulSoup
from wiktionaryparser import WiktionaryParser


class Scraper:
    def __init__(self, site, language):
        self.site = site  # The page from which get the info
        self.language = language  # The language in which to extract the words

    def main(self):
        result = []
        result = self.scrape(result, self.site, 1)
        item = result[0][0]
        print(item['etymology'])
        return result

    def scrape(self, result, nextsite, count):
        print("Iteration " + str(count) + "/41")
        wikparser = WiktionaryParser()

        start_r = urllib.request.urlopen(nextsite)
        html = start_r.read()
        parser = "html.parser"
        soup = BeautifulSoup(html, parser)
        categories = soup.find_all(class_="mw-category-group")  # Returns a list of the categories
        for category in categories:
            for item in category.find_all("li"):
                entry = item.get_text()
                wikentry = wikparser.fetch(entry, self.language)
                result.append(wikentry)
        page = soup.find(id="mw-pages")
        try:  # Checks if there is more pages to load
            link = page.find(string="next page").parent.get('href')
            count += 1
            next_link = "https://en.wiktionary.org"+link
            self.scrape(result, next_link, count)
        except:
            print("End")
            return result


site = "https://en.wiktionary.org/w/index.php?title=Category:English_idioms&from=Y"
language = "english"
Scraper(site, language).main()
