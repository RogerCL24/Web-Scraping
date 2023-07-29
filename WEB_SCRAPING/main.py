from selenium import webdriver
from bs4 import BeautifulSoup

def init():
    name = input("Write the product name to search").replace(" ", "+")
    amazon_result_url = f'https://www.amazon.es/s?k={name}&__mk_es_ES=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=N76EZZXYML22&sprefix={name}%2Caps%2C107&ref=nb_sb_noss_1'
    ebay_result_url = f'https://www.ebay.es/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw={name}&_sacat=0&LH_TitleDesc=0&_odkw=c922&_osacat=0'
    
if __name__ == "__main__":
    init()