import re
import nltk
from urllib.parse import urlparse
from bs4 import BeautifulSoup


UniqueUrlSet = set() #Set of URLs checked already and for deliverable Q1
PageWithMostWords = "" #Deliverable Q2
MostCommonWordsList = list() #Deliverable Q3
SubDomainsFoundDict = dict() #Deliverable Q4


def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]

def extract_next_links(url, resp):
    # Implementation required.
    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content
    
    if(resp.status == 200 and resp.raw_response.content != None): #Check if we got onto the page and if it has content
        _soupHtml = BeautifulSoup(resp.raw_response.content, 'html.parser')
        _urlTokenList = tokenize(_soupHtml.getText())
    else:
        print("resp.status code: ", resp.status, "\nError of: ", resp.error)
        return list()
    
    _urlList =  list()
    #TODO Fill the List and update any deliverable vars

    
    return _urlList

def tokenize(resp):
    #Tokenize urls
    _urlTokens = list()
    tokenizer = re('TODO')
    _urlTokens.extend( [_reObject.lower() for _reObject in re.split(r'\W+', resp) if _reObject.isalnum()])
    return _urlTokens

def is_valid(url):
    global UniqueUrlSet
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        parsed = urlparse(url)
        if parsed.hostname == None or parsed.netloc == None: #Check if hostname is not None
            return False
        if parsed.scheme not in set(["http", "https"]):
            return False
        if any(_domainName in parsed.hostname for _domainName in [".ics.uci.edu","cs.uci.edu",".informatics.uci.edu",".stat.uci.edu"]): #Only check for certain domains (Assignemnt)
            if not re.match(
                r".*\.(css|js|bmp|gif|jpe?g|ico"
                + r"|png|tiff?|mid|mp2|mp3|mp4"
                + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
                + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
                + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
                + r"|epub|dll|cnf|tgz|sha1"
                + r"|thmx|mso|arff|rtf|jar|csv"
                + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower()):
                if url not in UniqueUrlSet: 
                    UniqueUrlSet.add(url)
                    return True
        return False

    except TypeError:
        print ("TypeError for ", parsed)
        raise
