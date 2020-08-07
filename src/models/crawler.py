__author__='Godfred Doe'


from bs4 import BeautifulSoup
from src.common.database import Database
from src.models.linkparser import LinkParser
from src.models.theClassifier import predict_from_text

# The spider function takes a URL, a word to find,and the number of pages to search through
def spider(url, keyword, maxPages):
    pagesToVisit = [url]
    numberVisited = 0
    visitedPages = []
    foundKeywords = []
    foundWord = False
    keyFrequency = {}
    sum = 0
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
                        foundKeywords.append(keyword)
                if len(foundKeywords) > 0:
                    foundWord = True
                    strippedData = stripper(data)
                    # predict data category and return the probability of the catgory
                    category, probability = predict_from_text(strippedData)
                    category = category[0].upper() + category[1:]
                    probability = probability.round(2)
                    for word in foundKeywords:
                        frequency = strippedData.count(word)
                        if frequency > 0 :
                            keyFrequency[word] = frequency
                            sum = sum + frequency
                    pagesToVisit = pagesToVisit + links
                    print("The word", foundKeywords, "was found at", url)
                    if len(keyFrequency)>0:
                        foundData = {
                            'searchedKeywords': keywords,
                            'keywordWithFrequency': keyFrequency,
                            'summedFrequency': sum,
                            'url': url,
                            'data': strippedData,
                            'category': category,
                            'certainty': probability
                        }
                        Database.insert(collection="scraped_data", data=foundData)

            except:
                print(" **Failed!**")
        visitedPages.append(url)
        foundKeywords = []
        keyFrequency.clear()
        sum = 0
    if foundWord:
        return{
            'status':'Success',
            'message':'The keywords were found '
        }
    else:
        return{
            'status': 'failed',
            'message': 'No keyword was not found on any of the pages visited'
        }



def stripper(html):
    soup = BeautifulSoup(html, "html.parser")
    for script in soup(["script", "style"]):
        script.extract()
    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)

    return text




# spider("https://www.dreamhost.com/", "secure,data,host,url", 3)


