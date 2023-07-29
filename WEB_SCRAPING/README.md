# Web scraping

## Setup
In order to use the Mysql DB we install [`XAMPP`](https://www.apachefriends.org/es/index.html) to use an Apache server to host it, this way we handle the DB with ``phpmyadmin`` in the localhost.

We will be using de virtual environment from python in vscode
- First we open the console and type:
```
python3 -m venv virtual_env_name
```
> -m: used to indicate the use of a library
- Then, to activate it:
```
source virtual_env_name/bin/activate
```
The libraries we need to install are `Selenium` to automate processes, `BeautifulSoup` to scrap the information from the web pages and a ``mysql-python-connector``, so:
```
pip install selenium
pip install bs4
pip install mysql-connector-python
```
