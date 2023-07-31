from connection import *

class Products:
    def __init__(self, name, amazon_url, ebay_url, amazon_price, ebay_price):
        self.name = name
        self.amazon_url = amazon_url
        self.ebay_url = ebay_url
        self.amazon_price = amazon_price
        self.ebay_price = ebay_price

    def save_products(self):
        try:
            conn = connect()
            cursor = conn.cursor()
            sql = 'INSERT INTO products (name, amazon_url, ebay_url, amazon_price, ebay_price) VALUES (%s, %s, %s, %s, %s)'
            data = (self.name, self.amazon_url, self.ebay_url, self.amazon_price, self.ebay_price)
            cursor.execute(sql, data)
            conn.commit()
            conn.close()
            return "Products stored"
        except mysql.Error as err:
            return "An error has occurred"    

    def get_products(self):
        try:
            conn = connect()
            cursor = conn.cursor()
            sql = 'SELECT * FROM products'
            cursor.execute(sql)
            products = cursor.fetchall()
            conn.close()
            return products
        except mysql.Error as err:
            return "An error has ocurred"