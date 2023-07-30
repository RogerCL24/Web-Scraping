from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from time import sleep

def get_soup(url):  # web page content 
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches',['enable-logging'])
    service = Service('driver/chromedriver')
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    sleep(3)
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

def init():
    name = input("Write the product name to search: ").replace(" ", "+")
    amazon_result_url = f'https://www.amazon.es/s?k={name}&__mk_es_ES=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=N76EZZXYML22&sprefix={name}%2Caps%2C107&ref=nb_sb_noss_1'
    ebay_result_url = f'https://www.ebay.es/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw={name}&_sacat=0&LH_TitleDesc=0&_odkw=c922&_osacat=0'
    amazon_soup = get_soup(amazon_result_url)
    ebay_soup = get_soup(ebay_result_url)
    get_amazon_object(amazon_soup)
    print('\n')
    get_ebay_object(ebay_soup)




if __name__ == "__main__":
    init()