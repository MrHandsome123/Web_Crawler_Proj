from configparser import ConfigParser
from argparse import ArgumentParser

from numpy import sort

from utils.server_registration import get_cache_server
from utils.config import Config
from crawler import Crawler
# from analysis import get_longest_page,get_unique_pages,get_subdomain_counts,get_most_common_words
# from scraper import unique_pages, longest_page, longest_page_number, word_counts, subdomain_counts
from scraper import get_unique_pages, get_longest_page, get_word_counts, get_subdomain_counts


def main(config_file, restart):
    cparser = ConfigParser()
    cparser.read(config_file)
    config = Config(cparser)
    config.cache_server = get_cache_server(config, restart)
    crawler = Crawler(config, restart)
    crawler.start()
    print("Starting analysis...")
    
    unique_pages = get_unique_pages()
    print(f"Number of unique pages: {len(unique_pages)}")

    longest_page, longest_page_number = get_longest_page()
    print(f"Longest page: {longest_page[0]} with {longest_page_number} words")
    
    word_counts = get_word_counts()
    print("Most common words:")
    top_50_words = word_counts.most_common(50)
    for word, count in top_50_words:
        print(f"{word}: {count}")

    subdomain_counts = get_subdomain_counts()
    print(f"Subdomain counts: {len(subdomain_counts)}")
    sorted_subdomain_counts=sorted(subdomain_counts.items())
    for subdomain, count in sorted_subdomain_counts:
        print(f"{subdomain}: {count}")
    


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--restart", action="store_true", default=False)
    parser.add_argument("--config_file", type=str, default="config.ini")
    args = parser.parse_args()
    main(args.config_file, args.restart)
