import urllib.request, csv
from bs4 import BeautifulSoup
from wiktionaryparser import WiktionaryParser


class Scraper:
    def __init__(self, language):
        self.site = "https://en.wiktionary.org/w/index.php?title=Category:English_idioms&from=0"  # The page from which get the info
        self.language = language  # The language in which to extract the words

    def main(self):
        initial = []
        result = self.scrape(initial, self.site, 1)
        with open('english_idioms.csv', 'w') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',')
            filewriter.writerow(['link',
                                 'pronunciation:text',
                                 'pronunciation:audio (link)',
                                 'etymology',
                                 'definition:text',
                                 'definition:examples'
                                 ])
            for word_pre in result:
                link = word_pre[0]
                # An empty list has falsiness
                try:
                    word = word_pre[1][0]  # The format of the result from WikiParser is hella weird and has some
                # pesky nested[{}]
                except Exception as e:
                    print("Line not included due to ", str(e))
                    continue
                pronunciation_text = word['pronunciations']['text']
                pronunciation_audio_link = word['pronunciations']['audio']
                etymology = word['etymology'].strip().replace("\n", "")
                # Wiktionary entries are not 100% filled, so we have to deal with some nulls
                try:
                    definition_text = word['definitions'][0]['text']
                except:
                    definition_text = ""
                examples = []
                try:
                    for example in word['definitions'][0]['examples']:
                        examples.append(example.strip().replace("\n", ""))
                except:
                    examples = []
                filewriter.writerow(
                    [link, pronunciation_text, pronunciation_audio_link, etymology, definition_text, examples])
        print("All done!")

    def scrape(self, result, nextsite, count):
        if nextsite == "":
            return result
        print("Iteration " + str(count) + "/41")
        newresult = result
        wikparser = WiktionaryParser()

        start_r = urllib.request.urlopen(nextsite)
        html = start_r.read()
        parser = "html.parser"
        soup = BeautifulSoup(html, parser)
        categories = soup.find_all(class_="mw-category-group")  # Returns a list of the categories
        for category in categories:
            second_count = 0
            for item in category.find_all("li"):
                print("Progress: " + str(int(second_count/len(category.find_all('li'))*100)) + "%", end='\r')
                link = "https://en.wiktionary.org" + item.a['href']
                entry = item.get_text()
                try:
                    wikentry = wikparser.fetch(entry, self.language)
                except:
                    print("fail: ", entry)
                    continue
                newresult.append([link, wikentry])
                second_count += 1
        try:  # Checks if there is more pages to load
            page = soup.find(id="mw-pages")
            link = page.find(string="next page").parent.get('href')
            link = "https://en.wiktionary.org" + link
        except Exception as e:
            link = ""
        count += 1
        return self.scrape(newresult, link, count)


language = "english"
Scraper(language).main()
