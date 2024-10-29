import re
from urllib.parse import urlparse, urljoin, urldefrag
from bs4 import BeautifulSoup


# Define a maximum file size threshold in bytes (e.g., 1MB for our purposes)
MAX_FILE_SIZE = 1 * 1024 * 1024  # 1 MB

def scraper(url, resp):
    # Check if the response has a 'Content-Length' header
    content_length = int(resp.raw_response.headers.get('Content-Length', 0))
    if content_length > MAX_FILE_SIZE:
        print(f"Skipping large file: {url} ({content_length} bytes)")
        return []
    
    # Check the content type to avoid crawling non-HTML content
    content_type = resp.raw_response.headers.get('Content-Type', '').lower()
    if not content_type.startswith("text/html"):
        print(f"Skipping non-HTML content: {url} ({content_type})")
        return []

    # If the file is within acceptable limits and HTML, proceed
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

    # Ensure the response is successful
    if resp.status != 200 or not resp.raw_response:
        return links  # Return empty list if response is not OK

    # Parse HTML content with BeautifulSoup
    soup = BeautifulSoup(resp.raw_response.content, 'lxml')
    
    # Extract all 'a' tags with href attributes
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        # Convert relative URLs to absolute and defragment them
        absolute_url = urljoin(url, href)
        defragmented_url, _ = urldefrag(absolute_url)
        links.append(defragmented_url)
    
    # Remove duplicates
    return list(set(links))
    
    return links

def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        parsed = urlparse(url)

        # Only allow HTTP/HTTPS schemes
        if parsed.scheme not in {"http", "https"}:
            return False
        
        # Ensure URL is within a specific domain (e.g., 'ics.uci.edu')
        if not re.match(r".*\.ics\.uci\.edu$", parsed.netloc):
            return False

        # Filter out URLs with unwanted file extensions
        if re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower()):
            return False

        # Check for trap patterns (e.g., session IDs, infinite scroll, etc.)
        trap_patterns = [
            r"(\?|&)sessionid=",
            r"(\?|&)sid=",
            r"(\?|&)page=\d+",       # Pagination
            r"/calendar/",           # Calendar URLs may loop
            r"/events/",             # Event pages can also be repetitive
            r"(\?|&)sort=",          # Sorting traps
            r"/search"               # Avoid search result pages if possible
        ]
        if any(re.search(pattern, parsed.query) for pattern in trap_patterns):
            return False

        return True
    except TypeError:
        print("TypeError for ", url)
        raise
