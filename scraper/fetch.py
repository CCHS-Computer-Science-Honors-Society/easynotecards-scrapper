
import requests

def fetch_page(url, headers=None):
    """
    Fetches the content of the given URL.

    :param url: The URL to fetch.
    :param headers: Optional headers to include in the request.
    :return: The HTML content of the page.
    :raises: requests.exceptions.RequestException if the request fails.
    """
    if headers is None:
        headers = {
            "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                           "AppleWebKit/537.36 (KHTML, like Gecko) "
                           "Chrome/90.0.4430.93 Safari/537.36")
        }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text
