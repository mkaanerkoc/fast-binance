from itertools import islice

def chunked_iterable(iterable, chunk_size):
    """
    slices the given iterable into chunks with chunk_size size.
    
    """
    it = iter(iterable)
    while True:
        chunk = list(islice(it, chunk_size))
        if not chunk:
            break
        yield chunk
