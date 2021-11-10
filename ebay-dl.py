import argparse
import requests
from bs4 import BeautifulSoup
import json
import csv
import sys


def parse_itemssold(text):
    '''
    Takes as input a string and returns the number of items sold, as specified in the string.

    >>> parse_itemssold('72 sold')
    72
    >>> parse_itemssold('14 watchers')
    0
    >>> parse_itemssold('Almost gone')
    0
    '''
    numbers = ''
    for char in text:
        if char in '1234567890':
            numbers += char
    if 'sold' in text:
        return int(numbers)
    else:
        return 0
    

def parse_price(text):
    '''
    Takes as input a string and returns the price, as specified in the string.

    >>> parse_price('$54.99 to $79.99')
    5499
    >>> parse_price('$17.99')
    1799
    >>> parse_price('$5.95')
    595
    >>> parse_price('Free shipping')
    0
    >>> parse_price('+$5.00 shipping')
    500
    >>> parse_price('+$15.80 shipping')
    1580
    
    '''
    numbers = ''
    if text.find('$')==-1:
        return 0
    if text.find("to")!=-1:
        text = text[:text.find("to")]
    for char in text:
        if char in '1234567890':
            numbers += char
    if 'Free' in text:
        return 0
    else:
        return int(numbers)

#this if statement means only run the code below when the python file is run "normally"
if __name__ == '__main__':

#get command line arguments

    parser = argparse.ArgumentParser(description='Download information from ebay and convert to JSON.')
    parser.add_argument('search_term')
    parser.add_argument('--num_pages', default=10)
    parser.add_argument('--csv', action='store_true')
    args = parser.parse_args()
    print('args.search_term=', args.search_term)
    print('args.csv=', args.csv)
    print('args.num_pages=', args.num_pages)

    items = []

    for page_number in range(1,int(args.num_pages)+1):

    #build the url
        url = 'https://www.ebay.com/sch/i.html?_from=R40&_nkw=' 
        url += args.search_term 
        url += '&_sacat=0&LH_TitleDesc=0&_pgn='
        url += str(page_number)
        url += 'rt=nc'
        print('url=', url)

    #download the url
        r = requests.get(url)
        status = r.status_code
        print('status=', status)

        html = r.text
        print('html=', html[:50])

    #process the html
        soup = BeautifulSoup(html, 'html.parser')

# loop over the items in the page
        tags_items = soup.select('.s-item')
        for tag_item in tags_items:
    
        #extract the name
            name = None
            tags_name = tag_item.select('.s-item__title')
            for tag in tags_name:
                name = tag.text
        
        #extract the free returns
            freereturns = False
            tags_freereturns = soup.select('.s-item__free-returns')
            for tag in tags_freereturns:
                freereturns = True

        #extract items sold
            items_sold = None
            tags_itemssold = tag_item.select('.s-item__hotness')
            for tag in tags_itemssold:
                items_sold = parse_itemssold(tag.text)

        #extract status
            status = None
            tags_status = tag_item.select('.SECONDARY_INFO')
            for tag in tags_status:
                status = tag.text

        #extract price
            price = None
            tags_price = tag_item.select('.s-item__price')
            for tag in tags_price:
                price = tag.text

        #extract shipping
            shipping = None
            tags_shipping = tag_item.select('.s-item__shipping')
            for tag in tags_shipping:
                shipping = parse_price(tag.text)
    
            item = {
                'name' : name,
                'free_returns' : freereturns,
                'items_sold' : items_sold,
                'status' : status,
                'price' : price,
                'shipping' : shipping
            }
            items.append(item)
        items = items[1:]


        print('len(tags_items)=', len(tags_items))
        print('len(items)=', len(items))



    #for item in items:
    #   print('item=', item)

        if args.csv == True:
            filename = args.search_term+'.csv'
        with open(filename, 'w') as f:
            columnnames = ["name", "freereturns", "itemssold", "status", "price", "shipping"]
            writer = csv.DictWriter(f, fieldnames=columnnames)
            writer.writeheader()
            for data in items:
                writer.writerow(data)
    else:
        filename = args.search_term+'.json'
        with open(filename, 'w', encoding='UTF-8') as f:
            f.write(json.dumps(items))

