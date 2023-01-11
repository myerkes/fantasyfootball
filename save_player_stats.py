'''
Import player stats and save to a sqlite database
'''

# Import scraping modules
from urllib.request import urlopen
from bs4 import BeautifulSoup

# Import data manipulation modules
import pandas as pd

# URL of page
base_url = 'https://www.pro-football-reference.com/years/2022/{0}.htm'

stat_categories = ['passing', 'rushing', 'receiving', 'kicking']

for stat_category in stat_categories:
    print(base_url.format(stat_category))