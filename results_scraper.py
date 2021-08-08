import requests
from bs4 import BeautifulSoup
import pandas as pd
import listing_scraper

searchterm = ''

def get_data(searchterm):
    url = 'https://www.ebay.ca/sch/i.html?_from=R40&_trksid=p2380057.m570.l1313&_nkw='+searchterm+'&_sacat=0'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return [soup,url]

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

#makes query to eBay and saves all results in csv
def start(query):
    searchterm = query
    soup,url = get_data(searchterm)
    productslist = parse(soup)
    cnt=0
    for prod in productslist:
        #cnt+=1
        listing_scraper.add_data(prod)
        #if cnt>20: break
    listing_scraper.save_data()
    return url