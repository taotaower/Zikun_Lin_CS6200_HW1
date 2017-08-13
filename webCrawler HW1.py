import urllib2
import re
import time
from bs4 import BeautifulSoup
from urllib import urlretrieve


def spider(url,crawled,frontier,nextFrontier):
    newLinks = []
    html = urllib2.urlopen(url)
    # extract the data from the page
    # be polite
    time.sleep(0)
    soup = BeautifulSoup(html,'lxml')
    # get this link's url, since different urls may point to a same page,
    # we only store a page once
    thisLink = soup.find('link', rel = 'canonical').get('href')
    # only find the links in the bodyContent, ignore
    # Non-English articles, external links, main Wikipedia page, navigations and marginal links
    content = soup.find('div', id = 'bodyContent')
    # ignore those links in <li> tags
    ignoreList = content.find_all('li')
    for l in ignoreList:
        l.extract()
    # ignore those links in <a> tag that not lead to an article page
    ignoreLinks = content.find_all('a',href=re.compile(r"/wiki/.*:") )
    for link in ignoreLinks :
        link.extract()
    # ignore thumbinner link in article
    links = content.find_all('a', title=re.compile(r".*"), href=re.compile(r"^/wiki/"))
    for link in links :
        l = 'https://en.wikipedia.org' + link.get('href')
        if (l not in crawled) and (l not in frontier) \
                and (l not in nextFrontier) and (l not in newLinks):
            newLinks.append(l)
    return newLinks , thisLink

# store the crawled the page
def saveWebPage(url):
    try:
        webpage = urlretrieve(url)[0]
    except IOError:
        webpage = None
    if webpage:
        f = open(webpage)
        lines = f.readlines()
        f.close()
        # get the name of the download file
        u = re.match(r'(https://en.wikipedia.org/wiki/)(.*)',url)
        # let the file name reasonable
        fileName = u.group(2) + '.txt'
        # replace invalided character
        fileName = fileName.replace("/", "_")
        fobj = open(fileName, 'w')
        fobj.writelines(lines)
        fobj.close()

def spiderControll(start ,depth, numUrls):
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
                print 'already crawled   ' + str(numUrls) +'   web pages \n crawler finished work'
                return
            crawled.append(frontier[0])
            print len(crawled)
            print frontier[0]
            newLinks, thisLink = spider(frontier[0],crawled,frontier,nextFrontier)
            print 'depth: ' + str(i + 1) + thisLink
            saveWebPage(thisLink)
            # write the crawled url into file
            f = open("Task 1-E.txt", "a")
            link = frontier.pop(0) + '\n'
            f.write(link)
            f.close()
            # update the frontier
            nextFrontier = nextFrontier + newLinks
        # when we finished crawling one layer we should crawl next layer
        frontier = nextFrontier
        nextFrontier = []
    print 'crawler finished work'


spiderControll('https://en.wikipedia.org/wiki/Sustainable_energy', 5, 1000)
