from collections import Counter, defaultdict
import re
from urllib.parse import urlparse, urlunparse
from bs4 import BeautifulSoup
import datetime
import nltk


unique_pages=set()
longest_page=None
longest_page_number=0
word_counts=Counter()
subdomain_counts=defaultdict(int)

def update_unique_pages(url):
    global unique_pages
    parsed = urlparse(url)
    cleaned_url = urlunparse((parsed.scheme, parsed.netloc, parsed.path, '', '', ''))
    unique_pages.add(cleaned_url)

def update_longest_page(url,  content):
    global longest_page
    global longest_page_number
    
    words=[]
    try:
        soup = BeautifulSoup(content, "html.parser")
        words.extend(re.findall(r'\w+', soup.get_text()))
        word_count = len(words)

        if word_count > longest_page_number:
            longest_page = url
            longest_page_number = word_count
    except (UnicodeDecodeError, AttributeError) as e:
        print(f"Skipping URL due to decoding error: {url}")
        
def update_most_common_words(url, content, top_n=50):
    nltk.download('stopwords')
    stop_words = set(nltk.stopwords.words("english"))
    global word_counts

    try:
        text = BeautifulSoup(content, "html.parser").get_text().lower()
        words = re.findall(r'\w+', text)
        # filtered_words = [word for word in words if word not in stop_words]
        word_counts.update(words)
    except (UnicodeDecodeError, AttributeError) as e:
        print(f"Skipping URL due to decoding error: {url}")
            
def update_subdomain_counts(url, domain="ics.uci.edu"):
    global subdomain_counts

    parsed = urlparse(url)
    if domain in parsed.netloc:
        subdomain = parsed.netloc
        subdomain_counts[subdomain] += 1

        

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
    links = []
    if resp.status == 200:
        try:
            content = BeautifulSoup(resp.raw_response.content)
            update_unique_pages(url)
            update_longest_page(url, content)
            update_most_common_words(url, content)
            update_subdomain_counts(url)
            links = [link.get('href') for link in content.find_all('a') if link.get('href') is not None and is_valid(link.get('href'))]
        except Exception as e:
            print (f"An exception found: {e}")
    return links

def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
        allowed_domains = ["ics.uci.edu", "cs.uci.edu", "informatics.uci.edu", "stat.uci.edu", "today.uci.edudepartment/information_computer_sciences/"]
        if not any(domain in parsed.netloc for domain in allowed_domains):
            return False

        check_date = is_recent(url)
        if check_date == False:
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

def is_recent(url):
    pattern = r"(\d{4})[-/](\d{2})[-/](\d{2})"
    match = re.search(pattern, url)

    if match:
        year, month, day = map(int, match.groups())
        event_date = datetime(year, month, day)
        today = datetime.today()
            
        # stop exploring upcoming events that happens two weeks later
        if (event_date - today).days > 7:
            return False

        # stop exploring events passed more than two weeks
        if (today - event_date).days > 14:
            return False