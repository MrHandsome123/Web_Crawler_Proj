import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup as BS

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
    found_urls = []
    #status 404 going in. 
    if(resp.status == 200):
        info = BS(resp.raw_response.content, 'html.parser')
        all_urls = info.find_all('a')
        for found_url in all_urls:
            url_to_add = found_url.get('href')
            if(url_to_add != url):
                found_urls.append(url_to_add)
        return found_urls
        

    return list()

def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        parsed = urlparse(url)
        #or parsed.hostname not in set(["www.ics.uci.edu","www.cs.uci.edu/","www.informatics.uci.edu/", "www.stat.uci.edu/" ])
        if parsed.scheme not in set(["http", "https"]) or parsed.hostname not in set(["www.ics.uci.edu","www.cs.uci.edu","www.informatics.uci.edu", "www.stat.uci.edu" ]):
            return False
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise
