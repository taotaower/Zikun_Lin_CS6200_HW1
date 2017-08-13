import urllib2
import re
import time
from bs4 import BeautifulSoup
from urllib import urlretrieve

crawled = []
frontier = []
nextFrontier = []

def spider(url, keyWord):
    newLinks = []
    # be polite
    time.sleep(1)
    html = urllib2.urlopen(url)
    # extract the data from the page
    soup = BeautifulSoup(html,'lxml')
    # only find the links in the bodyContent, ignore
    # Non-English articles, external links, main Wikipedia page, navigations and marginal links
    content = soup.find('div', id='bodyContent')
    # ignore those links in <li> tags
    ignoreList = content.find_all('li')
    for l in ignoreList:
        l.extract()
    # ignore those links in <a> tag that not lead to an article page
    ignoreLinks = content.find_all('a',href=re.compile(r"/wiki/.*:") )
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

def spiderControll(start , count ,keyWord ,depth, numUrls):
    frontier = [start]

    # crawl when when there is still url in frontier to crawl, and it is a valid depth
    while frontier and depth > 0:
        # if we have crawled maximum urls we should finish crawling
        if len(crawled) >= numUrls :
            print 'already crawled' + str(numUrls) +'web pages \n crawler finished work'
            return
        # we store the link when it is not crawled and
        # we should ignore first seed url that not include keyword 'solar'
        if frontier[0] not in crawled and 5 - depth > 0:
            crawled.append(frontier[0])
            f = open("Task 2-B.txt", "a")
            link = frontier[0] + '\n'
            f.write(link)
            f.close()
        # get the next layer to crawler
        nextFrontier = spider(frontier[0], keyWord)
        # when we have links in next layer we should crawl it first
        while nextFrontier :
            # use recursion to finish the DFC, every time we decrease the left depth
            # And let the leftmost node be the first crawled one
            spiderControll(nextFrontier[0], count ,keyWord, depth - 1 , numUrls)
            # after we crawled the leftmost one, we should remove it in the nextFrontier
            nextFrontier.pop(0)
        frontier.pop(0)

print 'your crawler starts working'
spiderControll('https://en.wikipedia.org/wiki/Sustainable_energy' ,[0],'solar' ,5, 1000)
print 'your crawler finished working'

