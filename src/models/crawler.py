__author__='Godfred Doe'

from bs4 import BeautifulSoup

from src.common.database import Database
from src.models.linkparser import LinkParser

# The spider function takes a URL, a word to find,and the number of pages to search through
def spider(url, keyword, maxPages):
    pagesToVisit = [url]
    numberVisited = 0
    visitedPages = []
    foundKeywords = []
    foundWord = False
    keyFrequency = {}
    keywords = keyword.split(",")
    # Create a LinkParser and get all the links on the page.Search the page for the keyword(string)
    while numberVisited < maxPages and pagesToVisit != []:
        numberVisited = numberVisited + 1
        # Start from the beginning of the collection of pages to visit:
        url = pagesToVisit[0]
        pagesToVisit = pagesToVisit[1:]
        if url in visitedPages:
            continue
        else:
            try:
                print(numberVisited, "Visiting:", url)
                parser = LinkParser()
                data, links = parser.getLinks(url)
                for keyword in keywords:
                    if data.find(keyword) > -1:
                        frequency = data.count(keyword)
                        foundKeywords.append(keyword)
                        keyFrequency.update({'keyword':keyword,'frequency':frequency})
                if len(foundKeywords) > 0:
                    foundWord = True
                    strippedData = stripper(data)
                    pagesToVisit = pagesToVisit + links
                    print("The word", foundKeywords, "was found at", url)
                    #frequency = strippedData.count(keyword)
                    foundData = {
                        'searchedKeywords': keywords,
                        'foundKeywords':{
                            'keyword':keyFrequency['keyword'],
                            'frequency':keyFrequency['frequency']
                        },
                        'url': url,
                        'data': strippedData
                    }
                    Database.insert(collection="scraped_data", data=foundData)

            except:
                print(" **Failed!**")
        visitedPages.append(url)
        foundKeywords = []
        keyFrequency ={}
    if foundWord:
        return{
            'status':'Success',
            'message':'The keyword was found '
        }
    else:
        return{
            'status': 'failed',
            'message': 'The keyword was not found on any of the pages visited'
        }



def stripper(html):
    soup = BeautifulSoup(html, 'lxml')
    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()  # rip it out
    # get text
    text = soup.get_text()
    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)

    return text
