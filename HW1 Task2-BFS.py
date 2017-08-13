import urllib2
import re
import time
from bs4 import BeautifulSoup
from urllib import urlretrieve


def spider(url, keyWord ,crawled,frontier,nextFrontier):
    newLinks = []
    html = urllib2.urlopen(url)
    # extract the data from the page
    soup = BeautifulSoup(html,'lxml')
    # only find the links in the bodyContent, ignore
    # Non-English articles, external links, main Wikipedia page, navigations and marginal links
    content = soup.find('div', id = 'bodyContent')
    # ignore those links in <li> tags
    ignoreList = content.find_all('li')
    for l in ignoreList:
        l.extract()
    # ignore those links in <a> tag that not lead to an article page
    ignoreLinks = content.find_all('a',href=re.compile(r"/wiki/.*:"))
    for link in ignoreLinks :
        link.extract()
    # ignore thumbinner link in article
    links = content.find_all('a', title=re.compile(keyWord, re.I), href=re.compile(r"^/wiki/"))

    for link in links :
        l = 'https://en.wikipedia.org' + link.get('href')
        if (l not in crawled) and (l not in frontier) \
                and (l not in nextFrontier) and (l not in newLinks):
            newLinks.append(l)
    return newLinks

def spiderControll(start , keyWord ,depth, numUrls):
    frontier = [start]
    crawled = []
    nextFrontier = []
    print 'your crawler starts working'
    # control the crawl depth
    for i in range(depth):
        # crawl when we still have urls to crawl in a depth
        while frontier :
            count = len(crawled)
            # if we have crawled maximum urls we should finish crawling
            if count >= numUrls :
                print 'already crawled' + str(numUrls) +'web pages \n crawler finished work'
                return
            # the first seed url not include keyword 'solar' we should ignore
            if i > 0 :
                crawled.append(frontier[0])
                # write the crawled url into file
                f = open("Task 2-A.txt", "a")
                link = frontier[0] + '\n'
                f.write(link)
                f.close()
                print 'depth: ' + str(i + 1) + frontier[0]
            print count
            print frontier[0]
            newLinks = spider(frontier.pop(0), keyWord ,crawled,frontier,nextFrontier)

            # be polite
            time.sleep(1)
            # update the frontier
            nextFrontier = nextFrontier + newLinks
        # when we finished crawling one layer we should crawl next layer
        frontier = nextFrontier
        nextFrontier = []
    print 'crawler finished work'


spiderControll('https://en.wikipedia.org/wiki/Sustainable_energy' , 'solar' ,5, 1000)