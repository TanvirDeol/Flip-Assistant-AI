from numpy import exp
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

prodlist = []

def price_to_float(price):
    if price is None or len(price)==0: return 0.0
    p =0
    if price.find("US")>=0:
        p = float(price[4:].replace(',',''))
        p*=1.26
    elif price.find("C")>=0:
        p = float(price[3:].replace(',',''))
    else:
        return -1.00
    return p

def conv_condition(cond):
    #order: for parts, used, seller refurbished, open box, new
    if cond.find("For parts or not working")>=0: return 0
    elif cond.find("Used")>=0: return 1
    elif cond.find("Seller refurbished")>=0: return 2
    elif cond.find("Open box")>=0: return 3
    elif cond.find("New")>=0: return 3
    else: return -1

def conv_shipping(ship):
    if ship.find("FREE")>=0: return 0.0
    return price_to_float(ship)

def conv_import(imp):
    if imp is None or len(imp)==0: return 0.0
    return price_to_float(imp)

def conv_views(views):
    if views is None or len(views)==0: return -1
    s = views.split()
    return int(s[0])

def conv_sale_type(sale_type):
    if sale_type.find("Price:")>=0: 
        return 1
    else:
        return 0

def conv_capacity(capacity):
    if capacity is None or len(capacity)==0: return 0
    sz =0
    try :
        sz = int(capacity[:2])
    except:
        return 0
    return sz

def conv_model(model):
    model = model.lower()
    #order: 3G,3GS,4,4S,5C,5,5S,6,SE 1st Gen,6 Plus,
    # 6S Plus,7,7 Plus,8,SE 2nd Gen,8 Plus,X,XR,XS,
    # XS Max,11, 11 Pro, 11 Pro Max,12,12 Pro,12 Pro Max
    if model.find("iphone se")>=0:
        if model.find('1st')>=0: return 9
        elif model.find('2nd')>=0: return 15
    iphones = ['3g','3gs','4','4s','5c','5','5s','6','6 plus','6s plus',
    '7','7 plus','8','8 plus','xr','x','xs','xs max','11','11 pro','11 pro max'
    '12','12 pro','12 pro max']
    idx = [1,2,3,4,5,6,7,8,10,11,12,13,14,16,17,18,19,20,21,22,23,24,25,26]
    i = 22
    while i>=0:
        if model.find(iphones[i])>=0: return idx[i]
        i-=1
    return -1

def get_data(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def parse(soup,url):
    desc = ''
    try: desc = soup.find('div',{'class':'itemAttr'}).find_all('td',{'class':'attrLabels'})
    except: return
    for i in range(len(desc)):
        desc[i] = str(desc[i].string.replace('\t','').replace('\n',''))
    vals = soup.find('div',{'class':'itemAttr'}).find_all('td',{'width':'50.0%'})
    specs = {}
    model =''
    capacity = ''
    color = ''

    for i in range(len(desc)):
        specs[desc[i]]=vals[i].span.string
        if desc[i].find("Model:")>=0:
            model = specs[desc[i]]
        elif desc[i].find("Capacity")>=0:
            capacity = specs[desc[i]]
        elif desc[i].find("Color")>=0:
            color = specs[desc[i]]
    #print(specs)
    
    title = ''
    try: title = soup.find('h1', {'class': 'it-ttl'}).string
    except: title = ''
    price = ''
    try: price = soup.find(id= 'prcIsum').string 
    except: 
        try: price = soup.find(id= 'prcIsum_bidPrice').string
        except: price = '-1'
    condition = ''
    try: condition = soup.find('div', {'class': 'u-flL condText'}).string
    except: condition = ''
    shipping = ''
    try: shipping = soup.find('div', {'id': 'shSummary'}).find('span',{'id':'fshippingCost'}).span.string
    except: shipping = ''
    import_charges = ''
    try: import_charges = soup.find('span', {'id': 'impchCost'}).string
    except: import_charges= ''
    views = ''
    try: views = soup.find('div', {'class': 'vi-notify-new-bg-dBtm'}).span.string
    except: views = ''
    buy_now = ''
    try: buy_now = soup.find('div', {'class': 'lbl-value-set'}).find('div',{'class':'lbl'}).string.replace(' ','').replace('\n','')
    except: buy_now =''

    product = {
        'price': price_to_float(price),
        'views per hour': conv_views(views),
        'link': url,
        'condition': conv_condition(condition),
        'shipping': conv_shipping(shipping),
        'import charges': conv_import(import_charges),
        'sale type': conv_sale_type(buy_now),
        'model': conv_model(model),
        'capacity' : conv_capacity(capacity),
        'color': color,
    }
    prodlist.append(product)
    return

def output(productslist):
    if os.path.exists("output.csv"):
        os.remove("output.csv")
    productsdf =  pd.DataFrame(productslist)
    productsdf.to_csv('output.csv', index=False)
    print('Saved to CSV')
    return

def add_data(url):
    soup = get_data(url)
    parse(soup,url)

def save_data():
    print(prodlist)
    output(prodlist)


