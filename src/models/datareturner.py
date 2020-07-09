from src.common.database import Database

Database.initialize()


def findByKeyword(keyword):
    return [data for data in Database.find(collection="scraped_data", query={'keyword': keyword})]

def findByURL(url):
    return [ data for data in Database.find(collection="scraped_data", query={'url':url})]