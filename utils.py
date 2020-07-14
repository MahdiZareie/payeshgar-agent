from urllib.parse import urlparse


def validate_url(url: str):
    """
    Validate given url, and return True if the url is valid
    :return: True for valid, False for invalid
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
