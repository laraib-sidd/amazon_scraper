from selectorlib import Extractor
import requests
from fake_useragent import UserAgent


# Create an Extractor by reading from the YAML file
e = Extractor.from_yaml_file('query_search/selectors.yml')


def scrape(url):
    ua = UserAgent()
    headers = {
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': ua.random,
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.amazon.com/',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

    # Download the page using requests
    print(f"Downloading {url}")
    sess = requests.session()
    r = sess.get(url, headers=headers, timeout=20)
    # Simple check to check if page was blocked (Usually 503)
    if (r.status_code > 500):
        if ("To discuss automated access to Amazon data please contact") in r.text:
            print(
                f"Page {url} was blocked by Amazon. Please try using better proxies\n")
        else:
            print(
                f"Page {url} must have been blocked by Amazon as the status code was {r.status_code}")
        return None
    # Pass the HTML of the page and create
    return e.extract(r.text)
