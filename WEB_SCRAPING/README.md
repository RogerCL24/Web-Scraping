# Web scraping

## Setup
1. In order to use the Mysql DB we install [`XAMPP`](https://www.apachefriends.org/es/index.html) to use an Apache server to host it, this way we handle the DB with ``phpmyadmin`` in the localhost.
- To run the control panel we move to the directory it's downloaded, by default `/opt/lampp` and we execute it:
```shell
cd /opt/lampp
sudo ./manager-linux-x64.run
```

2. We will be using de virtual environment from python in vscode
- First we open the console and type:
```
python3 -m venv virtual_env_name
```
> -m used to indicate the use of a library
- Then, to activate it:
```console
source virtual_env_name/bin/activate
```
- The libraries we need to install are `Selenium` to automate processes, `BeautifulSoup` to scrap the information from the web pages and a ``mysql-python-connector``, so:
```console
pip install selenium
pip install bs4
pip install mysql-connector-python
```
3. Finally we need the google chrome driver so as to connect our pyhton program to the google browse, to get the driver we only need to access [here](https://sites.google.com/chromium.org/driver/downloads) and select the google chrome version we have, download the zip, unzip it and that's it.

## Reading the HTML code

