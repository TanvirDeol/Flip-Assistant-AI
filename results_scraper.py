import requests
from bs4 import BeautifulSoup
import pandas as pd
import listing_scraper

searchterm = 'iphone+8'

def get_data(searchterm):
    url = "https://www.ebay.ca/sch/i.html?_nkw="+searchterm
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def parse(soup):
    productslist = []
    results = soup.find_all('div', {'class': 's-item__info clearfix'})
    for item in results:
        productslist.append(item.find('a', {'class': 's-item__link'})['href'])
    return productslist

def output(productslist, searchterm):
    productsdf =  pd.DataFrame(productslist)
    productsdf.to_csv(searchterm + 'output.csv', index=False)
    print('Saved to CSV')
    return

soup = get_data(searchterm)
productslist = parse(soup)
cnt=0
for prod in productslist:
    listing_scraper.add_data(prod)
listing_scraper.save_data()