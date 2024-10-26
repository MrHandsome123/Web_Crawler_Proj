import os
import re
from urllib.parse import urlparse

def store_url_content(resp):
    print("in store url_contetn AOIHODAFOIAFO")
    url = resp.raw_response.url
    content = resp.raw_response.content

    folder_path = get_domain_path(url)
    os.makedirs(folder_path, exist_ok=True)

    # Avoid special characters like '&', '/', '?' in urls that mean smt different in file paths
    url_hash = hashlib.md5(url.encode()).hexdigest()
    zip_filename = os.path.join(folder_path, f"{url_hash}.zip")

    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.writestr(f"{url_hash}", content)

    return []

def get_domain_path(url):
    parsed_url = urlparse(url)
    host = parsed_url.hostname

    # Split hostname into parts
    host_parts = host.split('.')

    # End in uci.edu
    if len(parts) >= 2 and parts[-2] == 'uci' and parts[-1] == '.edu':
        base_domain = '.'.join(parts[-2:])
        subdomain = '/'.join(parts[:-2]) if len(parts) > 2 else 'www'
    else:
        base_domain = '.'.join(parts[-2:])
        subdomain = '/'.join(parts[:-2]) if len(parts) > 2 else 'www'

    folder_path = os.path.join(base_domain, subdomain)
    return folder_path

def compress(resp):
    url = resp.raw_response.url
    content = resp.raw_response.content
    return 
