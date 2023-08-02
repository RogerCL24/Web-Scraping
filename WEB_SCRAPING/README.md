# Web scraping

> All the pyhton code you see here is in [main.py](main.py), if it's not said the opposite

## Setup
1. In order to use the Mysql DB we install [`XAMPP`](https://www.apachefriends.org/es/index.html) to use an Apache server to host it, this way we handle the DB with ``phpmyadmin`` in the localhost.
- To run the control panel we have to move to the directory where the ``.run`` is downloaded it, <sub>by default `/opt/lampp`</sub> and we execute it:
```bash
cd /opt/lampp
sudo ./manager-linux-x64.run
```

2. We will be using de virtual environment from python in vscode
- First we open the console and type:
```bash
python3 -m venv virtual_env_name
```
> -m is used to indicate the use of a library
- Then, to activate it:
```bash
source virtual_env_name/bin/activate
```
- The libraries we need to install are `Selenium` to automate processes, `BeautifulSoup` to scrap the information from the web pages and a ``mysql-python-connector``, so:
```shell
pip install selenium
pip install bs4
pip install mysql-connector-python
```
3. Finally we need the google chrome driver so as to connect our pyhton program to the google browse, to get the driver we only need to access [here](https://sites.google.com/chromium.org/driver/downloads) and select the google chrome version we have, download the zip, unzip it and that's it.

## Reading the HTML code
We will need 5 features from both pages, Amazon and eBay. <sub> The sample photos are from Amazon, you only have to do the same at eBay's web page </sub>
- 1. URL of the results: The one is in the search bar when you are looking for many products with the similar name
- 2. HTML product element:
 ![1](https://github.com/RogerCL24/Web-Scraping/assets/90930371/9be528f9-3500-48d4-acc6-2470aa9968f6)
 
- 3. HTML name element:
 ![2](https://github.com/RogerCL24/Web-Scraping/assets/90930371/ab2bc512-556d-4529-97bc-1636a835910a)
   
- 4. HTML price element:
 ![3](https://github.com/RogerCL24/Web-Scraping/assets/90930371/ae46b69d-8b52-4aa3-8514-1ff216de5dcd)

- 5. HTML URL element:
![4](https://github.com/RogerCL24/Web-Scraping/assets/90930371/3eda05f2-50d2-4a5c-b67a-8bacbdef1ab3)

All the relevant information <sub> the html elements </sub> is marked with **Red** squares and you can find all the elements already written in [info.txt](info.txt)

## Products content
1. First we need the url where the web page with all the products we are searching for are listed, namely, the url from [info.txt](info.txt) <sub> URL of the results </sub>
```python
def init():
    name = input("Write the product name to search: ").replace(" ", "+")
    amazon_result_url = f'https://www.amazon.es/s?k={name}&__mk_es_ES=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=N76EZZXYML22&sprefix={name}%2Caps%2C107&ref=nb_sb_noss_1'
    ebay_result_url = f'https://www.ebay.es/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw={name}&_sacat=0&LH_TitleDesc=0&_odkw=c922&_osacat=0'
    amazon_soup = get_soup(amazon_result_url)
    ebay_soup = get_soup(ebay_result_url)
```
- We replace the example name for the name of the product we are searching, then with that url we pass it as a parameter to another function

2. This function reads all the html code using the ``selenium`` library and the driver formerly downloaded
```python
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
```

3. Finally the function that will select the features we really need from all the html code <sub> the `soup` parameter </sub>, with the library ``BeautifulSoup`` we can obtain the exact elements from the html web page and then print it to the console.

```python
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
```

## Connecting to the DB

1. The table where we are going to store all the data will be this one:
```SQL
CREATE TABLE products (
 id INTEGER PRIMARY KEY AUTO_INCREMENT,
 name TEXT NOT NULL,
 amazon_url TEXT NOT NULL,
 ebay_url TEXT NOT NULL,
 amazon_price VARCHAR(50) NOT NULL,
 ebay_price VARCHAR(50) NOT NULL
);
```
> amazon_price & ebay price fields are VARCHAR() instead of DECIMAL(10,2) because the price format from Amazon and eBay are quite difficult to deal with if we want to cast them to DECIMAL data types, this will be changed in the future for obvious reasons (to operate), by the moment we only want to show them

2. We will a need an isolated module with the connection functionality, [connection.py](connection.py), with only 1 function:
```python
def connect():
    try:
        connection = mysql.connect(
            host = 'localhost',
            user = 'root',
            password = '',
            database = 'web_scraping',
            port = '3306'
        )
        print("Connection to the database settled")
        return connection
    except mysql.Error as err:
        print("An error has ocurred: "+err)
```
- Using the mysql connector library formerly downloaded to our virtual environment, `host` , `user` and `password` are by default, `port` is not necessary if you have the 5432 active for the DB connection but if are using another one indicate it.

3. Finally this connection module is going to be used by the `Products` class at [products.py](products.py)
- The attributes of the class (the elements that will be stored at the table) will be:
```python
   def __init__(self, name, amazon_url, ebay_url, amazon_price, ebay_price):
        self.name = name
        self.amazon_url = amazon_url
        self.ebay_url = ebay_url
        self.amazon_price = amazon_price
        self.ebay_price = ebay_price
  ```
- And the method which is going to insert the elements in the table:
```python
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
```
## Storing the data into the DB
1. We are already showing what products are but now we add a select funciton, we add this code to the `get_amazon_object()` function:
```python
 selected = int(input("Select a product from the Amazon's store: "))
    amazon_url = products[selected - 1].find('a',{'class':'a-link-normal s-no-outline'}).attrs['href']
    amazon_price = products[selected - 1].find('span',{'class':'a-price'}).text
    return amazon_url, amazon_price
```
<sub> The same for the eBay's prodcuts </sub>

2. In the former function we return 2 vars, the url and the price, so we only need to receive that vars in the main functions, `init`, and use the Products class previously implemented:
```python
    amazon_url, amazon_price = get_amazon_object(amazon_soup)
    print('\n')
    ebay_url, ebay_price = get_ebay_object(ebay_soup)
    name.replace('+', ' ')
    products = Products(name, amazon_url, ebay_url, amazon_price, ebay_price)
    print(products.save_products())
```
3. An example
- We select the Amazon's product
![1](https://github.com/RogerCL24/Web-Scraping/assets/90930371/1536f222-bf8d-4331-b437-987ed08f25ad)

- Now the eBay's product
![2](https://github.com/RogerCL24/Web-Scraping/assets/90930371/71e2d8af-43ac-47a8-b0e3-fbd7cfc2a780)

- Finally it's stored automatically
![3](https://github.com/RogerCL24/Web-Scraping/assets/90930371/aa49b263-9de7-4211-8974-1ba3ccf7b9ca)

## Comparison old vs new prices
The idea is the following one, every time we execute the program a comparison functionality between the old products (the ones that are in the DB) and the new products (the same product in the DB) to check any price update of the same product is triggered, namely, since the moment their price was consulted (when it was stored in the DB) and now (when we execute the program), if there is any change we pop up a notification.

- We add a new method to the ``Products`` class in order to select all the products in the `web_scraping` table:
```python
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
```
> This method returns a list (products)

- Now in ``main.py`` we implement a new function which it will get the old prices <sub> `products` var is a list because calls .get_products()</sub> and the new ones <sub> ``new_amazon/ebay_price`` vars:
  ```python
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
        print(f'Product {product[1].replace("+"," ")}:')
        print(f'Amazon: Former price: {str(product[4])} // New price: {new_amazon_price}') 
        print(f'eBay: Former price: {str(product[5])} // New price: {new_ebay_price}')
  ```
- To send a notification we use the ``notifypy`` library and we code a new function to create the notify messages <sub> In main.py </sub>:
```python
def send_alert(message):
    notification = Notify()
    notification.title = "Product price change"
    notification.message = message
    notification.send()
```
- After that we create the notify event triggers in `check_price()` function:
```python
 if float(new_amazon_price) < float(product[4]):
  send_alert(f'The product {product[1].replace("+"," ")} price has dropped on Amazon')
 if float(new_amazon_price) > float(product[4]):
  send_alert(f'The product {product[1].replace("+"," ")} price has risen on Amazon')
 if float(new_ebay_price) < float(product[5]):
  send_alert(f'The product {product[1].replace("+"," ")} price has dropped on eBay')
 if float(new_ebay_price) > float(product[5]):
  send_alert(f'The product {product[1].replace("+"," ")} price has risen on eBay')
 if  float(new_amazon_price) > float(new_ebay_price):
  send_alert(f'The product {product[1].replace("+"," ")} price on eBay is lower')
 if float(new_amazon_price) < float(new_ebay_price):
  send_alert(f'The product {product[1].replace("+"," ")} price on Amazon is lower')
```
- For instance
![notify](https://github.com/RogerCL24/Web-Scraping/assets/90930371/5810be57-6b72-46cb-9b3c-a431ff10e9a8)


## Executing ``check_price()`` on background
To execute a function in background we use the `threading` library.
- In order to select whether we want to register a new product in the DB and compare prices or only compare prices <sub> executing the comparison function on background </sub>, the new init() funciton would be:
``` python
def init():
    response = input("You want a new product to be registered? y/n: ")
    if response == "y":
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

    thread = Thread(target=check_price) # execute on background
    thread.start()
```
And finally to execute the checking of the prices periodically we encapsulate the `check_price()` code in a infinit loop and to execute it every amount of time we add sleep() from `time` library:

```python
def check_price():
    while True:
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
            if float(new_amazon_price) < float(product[4]):
                send_alert(f'The product {product[1].replace("+"," ")} price has dropped on Amazon')
            if float(new_amazon_price) > float(product[4]):
                send_alert(f'The product {product[1].replace("+"," ")} price has risen on Amazon')
            if float(new_ebay_price) < float(product[5]):
                send_alert(f'The product {product[1].replace("+"," ")} price has dropped on eBay')
            if float(new_ebay_price) > float(product[5]):
                send_alert(f'The product {product[1].replace("+"," ")} price has risen on eBay')
            if  float(new_amazon_price) > float(new_ebay_price):
                send_alert(f'The product {product[1].replace("+"," ")} price on eBay is lower')
            if float(new_amazon_price) < float(new_ebay_price):
                send_alert(f'The product {product[1].replace("+"," ")} price on Amazon is lower')
        response = input("You want to keep executing? y/n: ")
        if response == "y":
            sleep(60)
        else:
            break
```
> OBSERVATION: In this code `check_price()` is executed every minute (60 seconds), to execute it every day, for example, would be `sleep(86400)`

## Drawbacks
### HTML code
In `get_amazon_object()` we are depending on the html code from the Amazon web page, in case they change the code (instead of a span they use a div or a li for example) our code will not work, therefore before use the program we have to check our html code at [info.txt](info.txt) match with their html code.

<sub> The same for `get_ebay_object()` </sub>
### Google driver
At ``get_soup()`` function the driver we are using to connect our program to the google browse has a determinated version which has to match with the real version of google chrome browse we have (or atleast the one we are going to use), to avoid problems check the version of your google chrome browse to download the proper driver.
### URL
Same thing as the html code and the driver, URL encoding can change.+

