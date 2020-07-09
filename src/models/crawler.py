__author__='Godfred Doe'

from bs4 import BeautifulSoup

from src.common.database import Database
from src.models.linkparser import LinkParser

# The spider function takes a URL, a word to find,and the number of pages to search through
def spider(url, keyword, maxPages):
    pagesToVisit = [url]
    numberVisited = 0
    visitedPages = []
    foundWord = False
    # Create a LinkParser and get all the links on the page.Search the page for the keyword(string)
    while numberVisited < maxPages and pagesToVisit != []:
        numberVisited = numberVisited + 1
        # Start from the beginning of the collection of pages to visit:
        url = pagesToVisit[0]
        pagesToVisit = pagesToVisit[1:]
        # My to do: Fix the bug here which prevents further crawling when word is not found on the first page
        try:
            print(numberVisited, "Visiting:", url)
            parser = LinkParser()
            data, links = parser.getLinks(url)
            if data.find(keyword) > -1:
                foundWord = True
                #strip the html tags off
                strippedData = stripper(data)
                # Add the urls we found to the end of our collection of pages to visit:
                pagesToVisit = pagesToVisit + links
                if foundWord:
                    print("The word", keyword, "was found at", url)
                    #determine frequency of keyword in stripped data
                    frequency = strippedData.count(keyword)
                    foundData = {
                        'keyword': keyword,
                        'frequency':frequency,
                        'url': url,
                        'data': strippedData
                    }
                    # save the json file to database
                    Database.insert(collection="scraped_data", data=foundData)
        except:
            print(" **Failed!**")
    if foundWord:
        return{
            'status':'Success',
            'message':'The keyword \" %s \" was found '%keyword
        }
    else:
        return{
            'status': 'failed',
            'message': 'The keyword \" %s \" was not found on any oof the pages visited'%keyword
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
