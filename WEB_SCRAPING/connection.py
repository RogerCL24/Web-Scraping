import mysql.connector as mysql

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

