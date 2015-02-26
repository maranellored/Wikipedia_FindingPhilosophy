#!/usr/bin/env python

################################################################################
##  A Wikipedia parser that tries to follow the first link in each article
##  starting from the specified article and tries to reach the wikipedia page on
##  Philosophy.
##
##  The rules on following a link are -
##      - If a link is italicized, do not follow it
##      - If a link is enclosed in parantheses, do not follow it
##
##  ** Note **
##      - This version doesn't do anything special with redirects. It follows a
##        a redirect blindly.
##      - Also follows links to wiktionary blindly.
################################################################################

import sys
import requests
from bs4 import BeautifulSoup
from collections import OrderedDict

WIKIPEDIA_BASE_URL = "http://en.wikipedia.org/wiki/"


def usage():
    print "Usage:\n{} \"<Wikipedia Article>\"\nEnclose the name of the article "\
        " in quotes".format(sys.argv[0])
    sys.exit(1)


# Parses the given URL to check if it can be followed.
#
# Valid URLs are not enclosed in parantheses. The italicized URLs have already
# been factored out before this method call.
# Any files or images that have been uploaded usually have a ':' in their
# URL and are thus factored out.
def is_valid_link(url, para):
    if ':' in url:
        return False

    # ensure that we only follow links to wikipedia articles
    if '/wiki/' not in url:
        return False

    # Wiktionary links are not allowed.
    if '.wiktionary.org' in url:
        return False

    # url is usable. Ensure that it is not inside a parantheses
    # if this url is inside a parantheses, then the count of open
    # parantheses, '(', will not be equal to that of close parantheses ')'
    search_text = para.split(url)[0]
    if search_text.count('(') != search_text.count(')'):
        return False

    return True


# Return only p or the ul tags
# the ul tags are required for pages that have no lead sections or are search
# result pages
def valid_tag_selector(tag):
    return tag.name == 'p' or tag.name == 'ul'


# Use the requests library to perform a get request for the page.
# The wikipedia base URL is constant
def retrieve_page(article):
    wikipedia_url = WIKIPEDIA_BASE_URL + article
    # use requests to perform a http get
    response = requests.get(wikipedia_url)
    # Parse the http response
    if response.status_code != 200:
        # TODO: Add error message from response?
        # response.reason
        print "Cannot fetch article {} from wikipedia. " \
            "Status code: {}, Reason: {}" \
            .format(article, response.status_code, response.reason)

    return response


# Parse the HTML text with BeautifulSoup and remove the unwanted links
# Unwanted links are italicized or are enclosed in parantheses
def get_first_linked_article(html_text):

    # parse the html text
    soup = BeautifulSoup(html_text)
    content_div = soup.find('div', id='mw-content-text')

    # Find all valid tags using the valid_tag_selector method.
    # We need to find either the 'p' or the 'ul' tags.
    # Also, we need only the direct children of the mw-content-text div
    # element
    for p in content_div.find_all(valid_tag_selector, recursive=False):
        # Assuming that italicized links are surrounded by <i> </i> tags
        for i in p.find_all('i'):
            i.replace_with("")

        # Find all child links in the current paragraph element
        # need recursive searching because links can be nested under a li tag
        # under a ul tag.
        links = p.find_all('a')

        # Also convert the entire paragraph element into a unicode string to
        # make it easier to search through it
        unicode_para = unicode(p)

        for link in links:
            linked_article = link.get('href')
            # Check if link is valid and not in parantheses
            if is_valid_link(linked_article, unicode_para):
                return linked_article.split('/')[-1]


def run():
    # We need to check if we have an argument to parse
    if len(sys.argv) != 2:
        usage()

    # Print the arguments
    article = sys.argv[1]
    visited_articles = OrderedDict()

    while article.lower() != "philosophy":

        # check if we've already visited this article's page
        if article.lower() in visited_articles:
            print "Already visited this page. Found a loop. Quitting. " \
                "Current page: {}".format(article)
            sys.exit(1)

        response = retrieve_page(article)

        if article == 'Special:Random':
            # Replace the random string with the URL of the page
            article = response.url.split('/')[-1]

        # add the page to our visited section
        visited_articles[article.lower()] = None
        article = get_first_linked_article(response.text)

    # Finished finding all the pages till Philosophy.
    print "Found {} pages from {} to Philosophy\n" \
        .format(len(visited_articles), visited_articles.keys()[0].title())

    print "Articles: "
    for a in visited_articles.keys():
        # use the title method to create upper case words for better
        # presentation
        print "- {}".format(a.title())

if __name__ == '__main__':
    run()
