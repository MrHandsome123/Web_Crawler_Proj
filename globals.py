from collections import defaultdict, deque
from operator import __eq__
import random
from typing import Any, Callable  # , TypeAlias
from DomainTrie import DomainTrie
from threading import Lock
from test_suite import test_function
import save_data

GLOBAL_PRINTS_ACTIVE: bool = False
allowed_domains = [
    "ics.uci.edu",
    "cs.uci.edu",
    "informatics.uci.edu",
    "stat.uci.edu",
    "today.uci.edu"
]


unique_urls_trie: DomainTrie = DomainTrie()
unique_urls_trie_lock: Lock = Lock()
unique_urls = set()
unique_urls_lock = Lock()
longest_page = {
    'url': '',
    'word_count': 0
}
longest_page_lock = Lock()
word_frequencies = defaultdict(int)
word_frequencies_lock: Lock = Lock()
subdomains = defaultdict(int)
subdomains_lock: Lock = Lock()
MAX_TOKEN_LENGTH = 10000  # Set a reasonable maximum length

today_uci_edu_path = "/department/information_computer_sciences"
# add type alias letter
Token = str
HASH = int
Token_Tuple = tuple[Token, Token, Token]
url_string = str

lock_to_global_dict: dict[Lock, Any] = dict()
currently_looking_at_set: set[url_string] = set()
currently_looking_at_set_lock: Lock = Lock()
generic_global_var: list = list()
generic_global_var_lock = Lock()


def currently_looking_at_url(url: url_string) -> bool:
    return url in currently_looking_at_set


def currently_looking_at_url_atomic(url: url_string) -> bool:
    with currently_looking_at_set_lock:
        return currently_looking_at_url(url)


def add_url_to_looking_at_set(url: url_string):
    with currently_looking_at_set_lock:
        global currently_looking_at_set
        currently_looking_at_set.add(url)


def remove_url_from_currently_looking_at_set(url: url_string):
    with currently_looking_at_set_lock:
        global currently_looking_at_set
        currently_looking_at_set.remove(url)
# lock_to_global_dict[generic_global_var_lock] = generic_global_var


def url_already_in_unique_urls(url: url_string) -> bool:
    with unique_urls_lock:
        if GLOBAL_PRINTS_ACTIVE:
            print(f'Is {url} already in unique_urls: {url in unique_urls}')
        return url in unique_urls


def add_url_to_unique_urls(url: url_string) -> None:
    with unique_urls_lock:
        global unique_urls
        unique_urls.add(url)

    if GLOBAL_PRINTS_ACTIVE:
        print(f'Added {url} to unique_urls')


def read_global_variable(global_to_read: Any, global_variable_lock: Lock, action_to_take: Callable[..., Any] = None, *args) -> Any:
    with global_variable_lock:
        if GLOBAL_PRINTS_ACTIVE:
            print(f"\n\tAcessing global variable {global_to_read}")
            print(f"\tRunning operation {action_to_take.__name__}", end=', ')
            print(f"({global_to_read, args})")
        if action_to_take == None:
            result = global_to_read
        elif len(args) == 0:
            result = action_to_take(global_to_read)
        else:
            result = action_to_take(global_to_read, *args)

    return result


def read_global_variable_action_does_not_pass_global(global_to_read: Any, global_variable_lock: Lock, action_to_take: Callable[..., Any] = None, *args) -> Any:
    with global_variable_lock:
        # note that this print could be out of date if the global variable is passed by value and not by reference
        if GLOBAL_PRINTS_ACTIVE:
            print(f"\n\tAcessing global variable {global_to_read}")
            print(f"\tRunning operation {action_to_take.__name__}", end=', ')
            print(f"({global_to_read, args})")
        if action_to_take == None:
            result = global_to_read
        elif len(args) == 0:
            result = action_to_take()
        else:
            result = action_to_take(*args)

    return result


def write_global_variable(global_to_read: Any, global_variable_lock: Lock, action_to_take: Callable[..., Any], *args) -> Any:
    with global_variable_lock:
        # note that this print could be out of date if the global variable is passed by value and not by reference
        if GLOBAL_PRINTS_ACTIVE:
            print(f"\n\tAcessing global variable {global_to_read}")
            print(f"\tRunning operation {action_to_take.__name__}", end=', ')
            print(f"({global_to_read, args})")
        if len(args) == 0:
            result = action_to_take(global_to_read)
        else:
            result = action_to_take(global_to_read, *args)

        print(f'Successfully altered global variable')

    return result


def write_global_variable_action_does_not_pass_global(global_to_read: Any, global_variable_lock: Lock, action_to_take: Callable[..., Any], *args) -> Any:
    with global_variable_lock:
        if GLOBAL_PRINTS_ACTIVE:
            print(f"\n\tAcessing global variable {global_to_read}")
            print(f"\tRunning operation {action_to_take.__name__}", end=', ')
            print(f"({global_to_read, args})")
        if len(args) == 0:
            result = action_to_take()
        else:
            result = action_to_take(*args)

        print(f'Successfully altered global variable')

    return result


def unique_urls_trie_insert_thread_safe(domain_to_insert: url_string) -> bool:
    with unique_urls_trie_lock:
        global unique_urls_trie
        unique_urls_trie.insert(domain_to_insert)
    return True


def unique_urls_get_num_unique_trie_read_thread_safe() -> tuple[int, int]:
    with unique_urls_trie_lock:
        total_num_unique_domains = unique_urls_trie.get_num_unique_domains()
        if GLOBAL_PRINTS_ACTIVE:
            print(f'num unique domains total = {total_num_unique_domains}')
        for domain in allowed_domains:
            curr_node = unique_urls_trie.search(domain)
            num_unique_subdomains: int = unique_urls_trie.get_num_unique_subdomains_for_domain(
                curr_node)
            if GLOBAL_PRINTS_ACTIVE:
                print(f'unique subdomains for {domain}', end='')
                print(f' = {num_unique_subdomains}')

        return (total_num_unique_domains, num_unique_subdomains)


def pollute_generic_global_var_with_test_data(num_generic_test_data: int = 100, max_range: int = 100):
    for i in range(num_generic_test_data):
        generic_global_var.append(random.randint(0, max_range))


def get_generic_data_sum() -> int:
    return sum(generic_global_var)


def test_generic_data_sum() -> int:
    test_function(get_generic_data_sum(), __eq__, read_global_variable_action_does_not_pass_global,
                  generic_global_var, generic_global_var_lock, get_generic_data_sum)

    test_function(None, __eq__, write_global_variable_action_does_not_pass_global,
                  generic_global_var, generic_global_var_lock, pollute_generic_global_var_with_test_data)

    test_function(get_generic_data_sum(), __eq__, read_global_variable_action_does_not_pass_global,
                  generic_global_var, generic_global_var_lock, get_generic_data_sum)


def change_longest_page_subroutine(new_url: url_string, new_word_count: int):
    global longest_page
    longest_page["url"] = new_url
    longest_page["word_count"] = new_word_count


def change_longest_page_threadsafe(new_url: url_string, new_word_count: int):
    write_global_variable_action_does_not_pass_global(
        longest_page, longest_page_lock, change_longest_page_subroutine, new_url, new_word_count)


def update_word_frequencies(tokens: list[Token]):

    global word_frequencies

    for token in tokens:
        word_frequencies[token] += 1
        save_data.update_word_frequencies(token)


def update_word_frequencies_thread_safe(tokens: list[Token]):
    with word_frequencies_lock:
        update_word_frequencies(tokens)


# def read_word_frequences_thread_safe()

def get_top_50_words() -> dict[str, int]:
    # this function is already thread_safe
    sorted_words = sorted(word_frequencies.items(),
                          key=lambda item: item[1], reverse=True)
    top_50_words = sorted_words[:50]
    if GLOBAL_PRINTS_ACTIVE:
        print("Top 50 words:")
        for word, freq in top_50_words:
            print(f"{word}: {freq}")

    return top_50_words


def get_top_50_words_atomic_access() -> dict[str, int]:
    # this function is already thread_safe
    with word_frequencies_lock:
        result = get_top_50_words()

    return result


if __name__ == "__main__":
    print(f'Running {__file__.split("/")[-1]}')
    test_generic_data_sum()

    print(f'\n\n\n\nglobals = {globals()}')
