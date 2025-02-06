from urllib.parse import urlparse, urlunparse
from bs4 import BeautifulSoup
from collections import Counter,defaultdict
import re
from nltk.corpus import stopwords
import nltk



#Question 1
def get_unique_pages(urls):
    unique_pages = set()
    for url in urls:
        parsed = urlparse(url)
        cleaned_url = urlunparse((parsed.scheme, parsed.netloc, parsed.path, '', '', ''))
        unique_pages.add(cleaned_url)
    return len(unique_pages),unique_pages

#Question 2
def get_longest_page(url_content_map):
    longest_page = None
    max_word_count = 0
    
    for url, content in url_content_map.items():
        words=[]
        try:
            soup = BeautifulSoup(content, "html.parser")
            words.extend(re.findall(r'\w+', soup.get_text()))
            word_count = len(words)

            if word_count > max_word_count:
                longest_page = url
                max_word_count = word_count
        except (UnicodeDecodeError, AttributeError) as e:
            print(f"Skipping URL due to decoding error: {url}")
            continue

    return longest_page, max_word_count

#Question3
stop_words = set(stopwords.words("english"))
def get_most_common_words(url_content_map, top_n=50):
    word_counter = Counter()

    for url,content in url_content_map.items():
        try:
            text = BeautifulSoup(content, "html.parser").get_text().lower()
            words = re.findall(r'\w+', text)
            filtered_words = [word for word in words if word not in stop_words]
            word_counter.update(filtered_words)
        except (UnicodeDecodeError, AttributeError) as e:
            print(f"Skipping URL due to decoding error: {url}")
            continue


    return word_counter.most_common(top_n)

#Question4
def get_subdomain_counts(urls, domain="ics.uci.edu"):
    subdomain_counts = defaultdict(int)

    for url in urls:
        parsed = urlparse(url)
        if domain in parsed.netloc:
            subdomain = parsed.netloc
            subdomain_counts[subdomain] += 1

    return len(subdomain_counts),sorted(subdomain_counts.items())

if __name__ == "__main__":
    urls = [
        "http://www.ics.uci.edu#aaa",
        "http://www.ics.uci.edu#bbb",
        "http://www.ics.uci.edu/path"
    ]
    number,unique_pages = get_unique_pages(urls)
    print(f"Number of unique pages: {number}")
