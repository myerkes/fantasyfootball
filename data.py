'''
https://towardsdatascience.com/scraping-nfl-stats-to-compare-quarterback-efficiencies-4989642e02fe
'''
# Import scraping modules
from urllib.request import urlopen
from bs4 import BeautifulSoup

# Import data manipulation modules
import pandas as pd
import numpy as np
# Import data visualization modules
import matplotlib as mpl
import matplotlib.pyplot as plt

# URL of page
url = 'https://www.pro-football-reference.com/years/2022/passing.htm'
# Open URL and pass to BeautifulSoup
html = urlopen(url)

stats_page = BeautifulSoup(html, features="html.parser")

# Collect table headers
column_headers = stats_page.findAll('tr')[0]
column_headers = [i.getText() for i in column_headers.findAll('th')]

#print(column_headers)
# Collect table rows
rows = stats_page.findAll('tr')[1:]
# Get stats from each row
qb_stats = []
for i in range(len(rows)):
  qb_stats.append([col.getText() for col in rows[i].findAll('td')])

# Create DataFrame from our scraped data
data = pd.DataFrame(qb_stats, columns=column_headers[1:])

# Rename sack yards column to `Yds_Sack`
new_columns = data.columns.values
new_columns[-6] = 'Yds_Sack'
data.columns = new_columns