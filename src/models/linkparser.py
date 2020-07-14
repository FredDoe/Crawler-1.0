__author__ = 'Godfred Doe'

from html.parser import HTMLParser
from urllib.request import urlopen
from urllib import parse


# Class LinkParser inherits some methods from HTMLParser
class LinkParser(HTMLParser):

    # This is a function that HTMLParser normally has but a few functionality are added to it
    def handle_starttag(self, tag, attrs):
        # Looking for the beginning of a link.
        if tag == 'a':
            for (key, value) in attrs:
                if key == 'href':
                    # Grab the new URL and add the base URL to it.
                    newUrl = parse.urljoin(self.baseUrl, value)
                    # Add it to our collection of links:
                    self.links = self.links + [newUrl]

    # A funtion that the spider() function will call to get links
    def getLinks(self, url):
        self.links = []
        # Store base url for creating absolute urls
        self.baseUrl = url
        # Use the urlopen function from the standard Python 3 library
        response = urlopen(url)
        # We are looking for HTML and not data floating around the page such as JavaScript files, CSS, or .PDFs
        #if response.getheader('Content-Type') == 'text/html':
        htmlBytes = response.read()
        htmlString = htmlBytes.decode("utf-8")
        self.feed(htmlString)
        return htmlString, self.links
        # else:
        #     return "", []