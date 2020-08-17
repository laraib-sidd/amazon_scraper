from product_scraper import scraper
from query_search import query_search
import json 
from time import sleep

if __name__ == "__main__":
    # Query search
    query = input("What's the keword you want to search for:")
    url = f'https://www.amazon.in/s?k={query}&ref=nb_sb_noss'
    with open('urls.txt', 'w') as outfile:
        data = query_search.scrape(url)
        if data:
            for product in data['products']:
                product['search_url'] = url
                product['url'] = f'https://www.amazon.com{product["url"]}'
                json.dump(product['url'], outfile)
                outfile.write("\n")
                sleep(5)

    # Product Scraper
    with open("urls.txt", 'r') as urllist, open('output.json', 'w') as outfile:
        for url in urllist.readlines():
            url = url.replace('"', '')
            data = scraper.scrape(url)
            if data['name'] is None :
                continue
            if data:
                json.dump(data, outfile)
                outfile.write("\n")
                sleep(5)
