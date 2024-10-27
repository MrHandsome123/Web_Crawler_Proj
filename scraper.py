import re
from urllib.parse import urlparse
from urllib.parse import urljoin
from bs4 import BeautifulSoup

def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]

def extract_next_links(url, resp):
	if resp.status == 200: 
		soup = BeautifulSoup(resp.raw_response.content, 'html.parser')
		robots_meta_tag = soup.find("meta", attrs={"name": "robots"})
		if robots_meta_tag and "content" in robots_meta_tag and "nofollow" in robots_meta_tag["content"].lower():
			return []
		links = [link.get("href") for link in soup.find_all('a') if "nofollow" not in link.get("rel", [])]
		de_fragmented_links = []
		for link in links:
			if link:
				full_url = urljoin(url, link)
				full_url = full_url.split('#')[0]
				de_fragmented_links.append(full_url)

		return de_fragmented_links
	else:
		return []

def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
        elif not is_in_domain(parsed): #filtering out the hosts
            return False
        elif bool(re.search(r'\b\d{4}-\d{2}-\d{2}\b', url)) or bool(re.search(r'\b\d{4}-\d{2}\b', url)): 
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


def is_in_domain(parsed):
    # Detect whether or not the parsed url is in the domains that we set
    # returns True if it's in the scheme, False otherwise
    if re.match(r"^([a-zA-Z0-9-]+\.)?(ics|cs|informatics|stat)\.uci\.edu$", parsed.hostname):
        return True
    elif parsed.hostname == "today.uci.edu" and parsed.path.startswith("/department/information_computer_sciences/"):
        return True
    return False
