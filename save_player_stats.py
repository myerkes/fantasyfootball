'''
Import player stats and save to a sqlite database
'''

# Import scraping modules
from urllib.request import urlopen
from bs4 import BeautifulSoup

# Import data manipulation modules
import pandas as pd
import sqlite3

# URL of page
BASE_URL = 'https://www.pro-football-reference.com/years/2022/{0}.htm'
#STAT_COL = ['passing', 'rushing', 'receiving', 'kicking']
STAT_COL = ['passing', 'rushing', 'receiving']

def create_database(table_name="",columns=[]):
    # create a new database and open a connection to it
    db_conn = sqlite3.connect('test_database3') 

    # create a database cursor in order to execute SQL statements and fetch results from SQL queries
    c = db_conn.cursor()

    # Example create table in database
    # data type is optional
    # cur.execute("CREATE TABLE movie(title, year, score)")

    c.execute('''
        CREATE TABLE IF NOT EXISTS {}({})
        '''.format(table_name, columns))
                        
    db_conn.commit()

    a = db_conn.execute('SELECT * FROM {}'.format(table_name))

    names = [description[0] for description in a.description]
    print(names)

    return db_conn

def scrape_stats(url=""):

    # Open URL and pass to BeautifulSoup
    html = urlopen(url)

    stats_page = BeautifulSoup(html, features="html.parser")

    # Collect table headers
    # receiving and kicking have extra table header row
    if stat_category == 'passing' or stat_category == 'receiving':
        column_headers = stats_page.findAll('tr')[0]
        # Collect table rows
        rows = stats_page.findAll('tr')[1:]
    else:
        column_headers = stats_page.findAll('tr')[1]
        # Collect table rows
        rows = stats_page.findAll('tr')[2:]

    column_headers = [i.getText() for i in column_headers.findAll('th')]

    # Get stats from each row
    stats = []
    for i in range(len(rows)):
        stats.append([col.getText() for col in rows[i].findAll('td')])
        
    # Create DataFrame from our scraped data and remove rank column
    data = pd.DataFrame(stats, columns=column_headers[1:])

    if stat_category == "passing":
        # Rename sack yards column to `Yds_Sack`
        new_columns = data.columns.values
        new_columns[-6] = 'Yds_Sack'
        data.columns = new_columns

    # Remove ornamental characters for achievements
    col_with_dec = ['Player', 'Ctch%']
    for col in col_with_dec:
        if col in data.columns:
            data[col] = data[col].str.replace('*', '', regex=False)
            data[col] = data[col].str.replace('+', '', regex=False)
            data[col] = data[col].str.replace('%', '', regex=False)

    # Convert data to numerical values
    numeric_col = data.columns.to_list()
    for col in ['Player', 'Tm', 'Pos', 'QBrec']:
        if col in numeric_col:
            numeric_col.remove(col)

    num_data = data
    num_data[numeric_col] = num_data[numeric_col].apply(pd.to_numeric)
    print(num_data.head())

    return ""


for stat_category in STAT_COL:

    a = scrape_stats(BASE_URL.format(stat_category))
    '''
    html = urlopen(BASE_URL.format(stat_category))
    

    stats_page = BeautifulSoup(html, features="html.parser")

    # Collect table headers
    # receiving and kicking have extra table header row
    if stat_category == 'passing' or stat_category == 'receiving':
        column_headers = stats_page.findAll('tr')[0]
        # Collect table rows
        rows = stats_page.findAll('tr')[1:]
    else:
        column_headers = stats_page.findAll('tr')[1]
        # Collect table rows
        rows = stats_page.findAll('tr')[2:]

    column_headers = [i.getText() for i in column_headers.findAll('th')]

    con = create_database(stat_category, column_headers)

    # Get stats from each row
    stats = []
    for i in range(len(rows)):
        stats.append([col.getText() for col in rows[i].findAll('td')])
        
    # Create DataFrame from our scraped data
    data = pd.DataFrame(stats, columns=column_headers[1:])

    print(data.head())

    '''



        
    '''

    # Collect table rows
    rows = stats_page.findAll('tr')[1:]
    # Get stats from each row
    stats = []
    for i in range(len(rows)):
        stats.append([col.getText() for col in rows[i].findAll('td')])

    # Create DataFrame from our scraped data
    data = pd.DataFrame(stats, columns=column_headers[1:])
    '''
