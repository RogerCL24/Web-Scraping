# Web scraping

## Setup
1. In order to use the Mysql DB we install [`XAMPP`](https://www.apachefriends.org/es/index.html) to use an Apache server to host it, this way we handle the DB with ``phpmyadmin`` in the localhost.
- To run the control panel we move to the directory the ``.run`` is downloaded it, <sub>by default `/opt/lampp`</sub> and we execute it:
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
- 1. URL of the results: The one is in the search bar when you are looking for many products with a similar name
- 2. HTML product element:
 ![1](https://github.com/RogerCL24/Web-Scraping/assets/90930371/9be528f9-3500-48d4-acc6-2470aa9968f6)
 
- 3. HTML name element:
 ![2](https://github.com/RogerCL24/Web-Scraping/assets/90930371/ab2bc512-556d-4529-97bc-1636a835910a)
   
- 4. HTML price element:
 ![3](https://github.com/RogerCL24/Web-Scraping/assets/90930371/ae46b69d-8b52-4aa3-8514-1ff216de5dcd)

- 5. HTML URL element:
![4](https://github.com/RogerCL24/Web-Scraping/assets/90930371/3eda05f2-50d2-4a5c-b67a-8bacbdef1ab3)

All the relevant information <sub> the html elements </sub> is marked with **Red** squares and you can find all the elements already written in [info.txt](info.txt)

