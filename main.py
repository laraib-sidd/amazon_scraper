from product_scraper import scraper
from query_search import query_search
import json
import re
from time import sleep
import pandas as pd

if __name__ == "__main__":
    # Query search
    urls, product_url, names, prices, images, ratings, reviews, asins = (
        [] for i in range(8))
    query = input("What's the keyword you want to search for:")
    url = f'https://www.amazon.com/s?k={query}&ref=nb_sb_noss'
    data = query_search.scrape(url)
    if data:
        for product in data['products'][2:12]:
            product['search_url'] = url
            product['url'] = f'https://www.amazon.com{product["url"]}'
            urls.append(product['url'])
            sleep(5)

    # Product Scraper
    for url in urls:
        url = url.replace('"', '')
        data = scraper.scrape(url)
        if data['name'] is None:
            continue
        if data:
            names.append(data['name'])
            product_url.append(url)
            asins.append(data['asin'])
            if data['price']:
                prices.append(data['price'])
            else:
                prices.append("Not Avaialbe")

            if data['images']:
                images.append(data['images'])
            else:
                images.append("Not Available")

            if data['rating']:
                ratings.append(data['rating'][:3])
            else:
                ratings.append("Not Available")

            if data['reviews']:
                review = data['reviews']
                match = re.split(' ', review)
                reviews.append(match[0])
            else:
                reviews.append("Not Available")

            sleep(5)
    df = pd.DataFrame({"name": names, "product_url": product_url, "price": prices, "images": images,
                      "rating": ratings, "reviews": reviews, "asin": asins})
    df.to_csv('result.csv')
