import os
import re
from urllib.parse import urlparse
import hashlib
import zipfile
import base64

def store_url_content(resp):
    url = resp.raw_response.url
    content = resp.raw_response.content

    folder_path = get_domain_path(url)
    os.makedirs(folder_path, exist_ok=True)

    # Avoid special characters like '&', '/', '?' in urls that mean smt different in file paths
    url_encoded = base64.urlsafe_b64encode(url.encode()).decode()
    zip_filename = os.path.join(folder_path, f"{url_encoded}.zip")

    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.writestr(f"{url_encoded}.txt", content.decode('utf-8', errors='ignore'))

    return []

def get_domain_path(url):
    parsed_url = urlparse(url)
    host = parsed_url.hostname

    # Split hostname into parts
    host_parts = host.split('.')

    # Check if the domain ends in uci.edu
    if len(host_parts) >= 2 and host_parts[-2] == 'uci' and host_parts[-1] == 'edu':
        base_domain = '.'.join(host_parts[-2:])  # "uci.edu"
        
        # Join parts before the base domain as subdomain, but exclude "www"
        if len(host_parts) > 2:
            subdomain_parts = host_parts[:-2]
            if subdomain_parts[0] == "www":
                subdomain_parts = subdomain_parts[1:]  # Remove "www"
            subdomain = '/'.join(subdomain_parts)
        else:
            subdomain = 'www'
    else:
        # Handle other domains
        base_domain = '.'.join(host_parts[-2:])
        subdomain_parts = host_parts[:-2]
        if subdomain_parts and subdomain_parts[0] == "www":
            subdomain_parts = subdomain_parts[1:]  # Remove "www"
        subdomain = '/'.join(subdomain_parts) if subdomain_parts else 'www'

    folder_path = os.path.join(base_domain, subdomain)
    return folder_path

def compress(resp):
    url = resp.raw_response.url
    content = resp.raw_response.content
    return 
