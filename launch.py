from configparser import ConfigParser
from argparse import ArgumentParser

from numpy import sort

from utils.server_registration import get_cache_server
from utils.config import Config
from crawler import Crawler
# from analysis import get_longest_page,get_unique_pages,get_subdomain_counts,get_most_common_words
from scraper import unique_pages, longest_page, longest_page_number, word_counts, subdomain_counts


def main(config_file, restart):
    cparser = ConfigParser()
    cparser.read(config_file)
    config = Config(cparser)
    config.cache_server = get_cache_server(config, restart)
    crawler = Crawler(config, restart)
    crawler.start()
    print("Starting analysis...")
    # num_unique_pages, unique_pages = get_unique_pages(crawler.url_content_map.keys())
    print(f"Number of unique pages: {len(unique_pages)}")

    # longest_page, max_words = get_longest_page(crawler.url_content_map)
    # print(f"Longest page: {longest_page} with {max_words} words")
    print(f"Longest page: {longest_page} with {longest_page_number} words")

    # ensure_stopwords()
    # most_common_words = get_most_common_words(crawler.url_content_map)
    print("Most common words:")
    # for word, count in most_common_words:
    for word, count in word_counts:
        print(f"{word}: {count}")

    # number_sub,subdomain_counts = get_subdomain_counts(crawler.url_content_map.keys())
    # print(f"Subdomain counts: {number_sub}")
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
