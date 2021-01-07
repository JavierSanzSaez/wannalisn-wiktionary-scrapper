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
        with open('english_idioms.csv', 'w') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',')
            filewriter.writerow(['pronunciation:text',
                                 'pronunciation:audio (link)',
                                 'etymology',
                                 'definition:text',
                                 'definition:examples'
                                 ])
            for word_pre in result:
                word = word_pre[0]  # The format of the result from WikiParser is hella weird and has some pesky nested[{}]
                pronunciation_text = word['pronunciations']['text']  # There may be more than one text pronunciation, we only care for the RP, which is the first one
                pronunciation_audio_link = word['pronunciations']['audio'][0]  # Idem
                etymology = word['etymology']
                definition_text = word['definitions'][0]['text']
                examples = []
                for example in word['definitions'][0]['examples']:
                    examples.append(example)
                filewriter.writerow([pronunciation_text,pronunciation_audio_link,etymology,definition_text,examples])
                print(pronunciation_text, pronunciation_audio_link, etymology, definition_text, examples)
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
