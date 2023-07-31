from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from time import sleep
from notifypy import Notify
from connection import *
from products import Products

def get_soup(url):  # web page content 
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches',['enable-logging'])
    service = Service('driver/chromedriver')
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    sleep(1)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    driver.close()
    return soup

def get_amazon_object(soup):
    products = soup.find_all('div', {'class': 'sg-col-4-of-24 sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col s-widget-spacing-small sg-col-4-of-20'})
    print('Amazon products\n')
    for i, product in enumerate(products):
        try:
            name = product.find('span', {'class':'a-size-base-plus a-color-base a-text-normal'}).text
            price = product.find('span',{'class':'a-price'}).text
            print(f'{i+1}. {name}. Price: {price}')
        except:
            pass
    selected = int(input("Select a product from the Amazon's store: "))
    amazon_url = products[selected - 1].find('a',{'class':'a-link-normal s-no-outline'}).attrs['href']
    amazon_price = products[selected - 1].find('span',{'class':'a-price'}).text
    # 699,00 €699,00€
    return amazon_url, amazon_price.split('€')[1].replace('.','').replace(',','.')


def get_ebay_object(soup):
    products = soup.find_all('li', {'class': 's-item s-item__pl-on-bottom'})
    print('eBay products\n')
    for i, product in enumerate(products):
        try:
            name = product.find('div', {'class':'s-item__title'}).text
            price = product.find('span',{'class':'s-item__price'}).text
            print(f'{i+1}. {name}. Price: {price}')
        except:
            pass
    selected = int(input("Select a product from the eBay's store: "))
    ebay_url = products[selected - 1].find('a', {'class':'s-item__link'}).attrs['href']
    ebay_price = products[selected - 1].find('span',{'class':'s-item__price'}).text
    # 1.350,18 EUR
    return ebay_url, ebay_price[0:-4].replace('.','').replace(',','.')

def check_price():
    products = Products(None, None, None, None, None).get_products()
    for product in products:
        amazon_soup = get_soup("https://www.amazon.es"+product[2])
        ebay_soup = get_soup(product[3])
        new_amazon_price = amazon_soup.find('span',{'class':'a-offscreen'}).text
        new_amazon_price = new_amazon_price.split('€')[0].replace('.','').replace(',','.')
        new_ebay_price = ebay_soup.find('div',{'class':'x-price-primary'}).text
        if new_ebay_price[0] == 'U':    # USD format
            new_ebay_price = new_ebay_price[3:].replace('.','').replace(',','.')
        else:                           # EUR format
            new_ebay_price = new_ebay_price[0:-4].replace('.','').replace(',','.')
        print(f'Producto {product[1].replace("+"," ")}:')
        print(f'Amazon: Former price: {str(product[4])} // New price: {new_amazon_price}') 
        print(f'eBay: Former price: {str(product[5])} // New price: {new_ebay_price}')
        if float(new_amazon_price) == float(product[4]):
            send_alert(f'The product {product[1].replace("+"," ")} price dropped on Amazon')

def send_alert(message):
    notification = Notify()
    notification.title = "Product price change"   
    notification.message = message
    notification.send()

def init():
    check_price()
    name = input("Write the product name to search: ").replace(" ", "+")
    amazon_result_url = f'https://www.amazon.es/s?k={name}&__mk_es_ES=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=N76EZZXYML22&sprefix={name}%2Caps%2C107&ref=nb_sb_noss_1'
    ebay_result_url = f'https://www.ebay.es/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw={name}&_sacat=0&LH_TitleDesc=0&_odkw=c922&_osacat=0'
    amazon_soup = get_soup(amazon_result_url)
    ebay_soup = get_soup(ebay_result_url)
    amazon_url, amazon_price = get_amazon_object(amazon_soup)
    print('\n')
    ebay_url, ebay_price = get_ebay_object(ebay_soup)
    products = Products(name, amazon_url, ebay_url, amazon_price, ebay_price)
    print(products.save_products())


if __name__ == "__main__":
    init()