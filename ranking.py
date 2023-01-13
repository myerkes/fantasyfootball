import pandas as pd
# Data visualization
import seaborn as sns
import matplotlib.pyplot as plt

from save_player_stats import *

sns.set_style('whitegrid')

'''
sns.displot(df['RushingTD'])
plt.show()
'''

# fantasy scoring weights dictionary
scoring_weights = {
    'receptions': 0.5,
    'receiving_yds': 0.1,
    'receiving_td': 6,
    'FL': -2,
    'rushing_yds': 0.1,
    'rushing_td': 6,
    'passing_yds': 0.04,
    'passing_td': 4,
    'int': -2
}

rushing = scrape_stats(2022, 'rushing')
receiving = scrape_stats(2022, 'receiving')
rush_rec = pd.merge(rushing, receiving, on=['Player','Tm', 'Age', 'Pos', 'G', 'GS', 'Fmb'], suffixes=["_rush","_rec"])
print(rush_rec.columns)

quit()

stats_db = create_database("rush_rec_stats")

base_columns = ['Player', 'Team', 'Pos']
rushing_columns = ['FantasyPoints', 'Receptions', 'ReceivingYds', 'ReceivingTD', 'RushingAtt', 'RushingYds', 'RushingTD', 'FL']
receiving_columns = ['FantasyPoints', 'Receptions', 'ReceivingYds', 'ReceivingTD', 'FL']

# Mask and filter in one step
#rb_df = df.loc[(df['Pos'] == 'RB', base_columns + rushing_columns)]
#wr_df = df.loc[(df['Pos'] == 'WR', base_columns + receiving_columns)]

df['PPG'] = df['FantasyPoints']/17

df['PPG_Rank'] = df.groupby('Pos')['PPG'].rank(ascending=False)
df.sort_values(by="PPG_Rank", ascending=False)

sns.lineplot(
    data = df,
    x = "PPG_Rank",
    y = "PPG",
    hue='Pos'
)

plt.show()
