# Check if url has repeated segments or is too long
def infinite_trap(resp):
    return len(resp.raw_response.url) > 200 or len(resp.raw_response.url.split('/')) > 10

def is_large_file(resp):
    max_size = 1024*1024 # 1 MB max size

    # Check if headers exist in raw_response
    if hasattr(resp.raw_response, 'headers'):
        content_length = resp.raw_response.headers.get('Content-Length')
        
        # If Content-Length is available, compare it directly
        if content_length and int(content_length) > max_size:
            print(f"Skipping large file: {resp.raw_response.url}")
            return True
    
    if len(resp.raw_response.content) > max_size:
        return True
    return False

# Check low info when processing file
def is_low_info(resp):
    content = resp.raw_response.content
    words = content.split()

    # Less than 100 words
    if len(words) < 100:
        return True
    
    unique = set(words)

    # Checking for repeated vocab
    if (unique / len(words)) < 0.3:
        return True

    # Check simHash
    return False
