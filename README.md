Finding Philosophy
===================

Requirements
-------------
To run the script, you need [Python 2.7](https://www.python.org/download/releases/2.7/).
The other dependencies required are BeautifulSoup for HTML parsing and Requests making for HTTP requests.

To install these dependencies, use [pip](https://pip.pypa.io/en/latest/installing.html). After installing pip, just run
```
$ pip install requests
$ pip install beautifulsoup4
```

To run the script run the following
```
$ python find_philosophy.py "Art"
Found 11 pages from Art to Philosophy

Articles:
- Art
- Human_Behavior
- Behavior
- Organism
- Biology
- Natural_Science
- Science
- Knowledge
- Awareness
- Conscious
- Quality_(Philosophy)

$ python find_philosophy.py "Special:Random"
Found 5 pages from Trigamma_Function to Philosophy

Articles:
- Trigamma_Function
- Mathematics
- Quantity
- Property_(Philosophy)
- Modern_Philosophy
```

_"Special:Random" allows for the Wikipedia server to serve a random page_
