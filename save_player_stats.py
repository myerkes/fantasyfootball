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
BASE_URL = 'https://www.pro-football-reference.com/years/{0}/{1}.htm'
#STAT_COL = ['passing', 'rushing', 'receiving', 'kicking']
STAT_COL = ['passing', 'rushing', 'receiving']

def create_database(db_name = "test_db", table_name="",columns=[]):
    # create a new database and open a connection to it
    db_conn = sqlite3.connect(db_name) 

    # create a database cursor in order to execute SQL statements and fetch results from SQL queries
    c = db_conn.cursor()

    # Example create table in database
    # data type is optional
    # cur.execute("CREATE TABLE movie(title, year, score)")

    sql_str = 'CREATE TABLE IF NOT EXISTS {0}({1})'.format(table_name, columns)

    c.execute('''CREATE TABLE IF NOT EXISTS {0}({1})'''.format(table_name, columns))
                        
    db_conn.commit()

    return db_conn

def upload_data(db_name: str, tbl_name: str, df: pd.DataFrame()):
    # connect to a test DB with one three-column table titled "Demo"
    cnx = sqlite3.connect(db_name)

    df.to_sql(name=tbl_name, con=cnx, if_exists="append")

    return True

def scrape_stats(years=[2022], category=""):

    # Create table using first year
    # Open URL and pass to BeautifulSoup
    url = BASE_URL.format(years[0], category)
    html = urlopen(url)

    stats_page = BeautifulSoup(html, features="html.parser")

    # Collect table headers
    # receiving and kicking have extra table header row
    if category == 'passing' or category == 'receiving':
        column_headers = stats_page.findAll('tr')[0]
    else:
        column_headers = stats_page.findAll('tr')[1]

    column_headers = [i.getText() for i in column_headers.findAll('th')]
    column_headers.append('Year')

    for y, year in enumerate(years):
        # Open URL and pass to BeautifulSoup
        url = BASE_URL.format(year, category)
        html = urlopen(url)

        stats_page = BeautifulSoup(html, features="html.parser")

        # receiving and kicking have extra table header row
        if category == 'passing' or category == 'receiving':
            # Collect table rows
            rows = stats_page.findAll('tr')[1:]
        else:
            # Collect table rows
            rows = stats_page.findAll('tr')[2:]

        # Get stats from each row
        stats = []
        for i in range(len(rows)):
            new_stat = [col.getText() for col in rows[i].findAll('td')]
            new_stat.append(year)
            stats.append(new_stat)
            
        if y == 0:
            # Create DataFrame from our scraped data and remove rank column
            data = pd.DataFrame(stats, columns=column_headers[1:])
        else:
            # Append to dataframe
            # TODO - swap to concat instead of append which is depreciated
            temp = pd.DataFrame(stats, columns=column_headers[1:])
            data = pd.concat([data, temp], ignore_index=True)

    # remove duplicate column name
    if category == "passing":
        # Rename sack yards column to `Yds_Sack`
        new_columns = data.columns.values
        # TODO - replace hard coded value with lookup to position of Yds_Sack column
        new_columns[-7] = 'Yds_Sack'
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

        
    return num_data

def main():
    rushing = scrape_stats([2022], 'rushing')

    db_conn = create_database("db1", "rushing_receiving_stats", rushing.columns.to_list())

    upload_data("db2", "rushing_receiving_stats", rushing)

    test = pd.read_sql("SELECT * FROM rushing_receiving_stats WHERE Pos='TE'", db_conn)

    print(test.head())

        

if __name__ == '__main__':
    main()
