'''
Import player stats and save to a sqlite database
'''

# Import scraping modules
from urllib.request import urlopen
from bs4 import BeautifulSoup

# Import data manipulation modules
import pandas as pd
import sqlite3

def create_database():
    # create a new database and open a connection to it
    db_conn = sqlite3.connect('test_database') 

    # create a database cursor in order to execute SQL statements and fetch results from SQL queries
    c = db_conn.cursor()

    # Example create table in database
    # data type is optional
    # cur.execute("CREATE TABLE movie(title, year, score)")

    c.execute('''
        CREATE TABLE IF NOT EXISTS stat_cat({})
        '''.format(stat_categories))

    c.execute('''
            CREATE TABLE IF NOT EXISTS products
            ([product_id] INTEGER PRIMARY KEY, [product_name] TEXT)
            ''')
            
    c.execute('''
            CREATE TABLE IF NOT EXISTS prices
            ([product_id] INTEGER PRIMARY KEY, [price] INTEGER)
            ''')
                        
    db_conn.commit()

    a = db_conn.execute('SELECT * FROM stat_cat')

    names = [description[0] for description in a.description]
    print(names)

    return db_conn




a = create_database()