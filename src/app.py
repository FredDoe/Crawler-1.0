__author__ = 'Godfred Doe'


from flask import Flask, render_template, request, session, make_response
from src.common.database import Database
from src.models.crawler import spider
from src.models.datareturner import findByKeyword

app = Flask(__name__)  # '__main__'
app.secret_key = "Godfred554433"



@app.route('/')
def homepage_template():
    return render_template("crawlnow.html")


@app.route('/crawl-pages', methods=['POST'])
def pageCrawler_template():
    url = request.form['url']
    keyword = request.form['keyword']
    number_of_pages = request.form['numberofpages']
    if number_of_pages =="":
        number_of_pages = 100
        maxPage = number_of_pages
    else:
        maxPage = int(number_of_pages)

    if url[0:3] == "www":
        url = "https://"+ url
    else:
        url = url

    status = spider(url, keyword, maxPage)
    keyword = keyword.split(",")
    return make_response( retrieveCrawledData(keyword, status))


@app.route('/crawled-pages/result')
def retrieveCrawledData(keyword, status):
    crawledData = findByKeyword(keyword)
    print(crawledData)
    if len(crawledData) > 0:
         return render_template("crawledResult.html", crawledData=crawledData, status=status, keyword=keyword)
    else:
        return render_template('failed.html', status=status)
@app.before_first_request
def initialize_database():
    Database.initialize()

if __name__ == '__main__':
    app.run(port=4009, debug=True)
