from urllib.parse import urlsplit, urlunsplit, quote

def iri2uri(iri):
    """
    Convert an IRI to a URI

    Function arguments :
    - iri : iri to convert
    
    Returns :
    - uri : the converted IRI
    """
    uri = ''
    if isinstance(iri, str):
        (scheme, netloc, path, query, fragment) = urlsplit(iri)
        scheme = quote(scheme)
        netloc = netloc.encode('idna').decode('utf-8')
        path = quote(path)
        query = quote(query)
        fragment = quote(fragment)
        uri = urlunsplit((scheme, netloc, path, query, fragment))

    return uri