import pandas as pd
# Data visualization
import seaborn as sns
import matplotlib.pyplot as plt


df = pd.read_csv('https://raw.githubusercontent.com/fantasydatapros/LearnPythonWithFantasyFootball/master/2022/06-Data%20Munging/01-Fantasy%20Pros%20Projections%20-%20(2022.08.25).csv')


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

df['FantasyPoints'] = (
    df['Receptions']*scoring_weights['receptions'] + df['ReceivingYds']*scoring_weights['receiving_yds'] + \
    df['ReceivingTD']*scoring_weights['receiving_td'] + df['FL']*scoring_weights['FL'] + \
    df['RushingYds']*scoring_weights['rushing_yds'] + df['RushingTD']*scoring_weights['rushing_td'] + \
    df['PassingYds']*scoring_weights['passing_yds'] + df['PassingTD']*scoring_weights['passing_td'] + \
    df['Int']*scoring_weights['int'] 
)

base_columns = ['Player', 'Team', 'Pos']
rushing_columns = ['FantasyPoints', 'Receptions', 'ReceivingYds', 'ReceivingTD', 'RushingAtt', 'RushingYds', 'RushingTD', 'FL']

receiving_columns = ['FantasyPoints', 'Receptions', 'ReceivingYds', 'ReceivingTD', 'FL']

# Mask and filter in one step
rb_df = df.loc[(df['Pos'] == 'RB', base_columns + rushing_columns)]
wr_df = df.loc[(df['Pos'] == 'WR', base_columns + receiving_columns)]

"""
The rank method can be used to rank players based on a given column.
Set ascending = False to rank the column in descending order.
We will be using this rank players on value over replacement and also on ADP.
Ties are split and rank is shared (such ad 5.5 for 5th place tie)
"""
# add columns with name and function
rb_df['PPG'] = rb_df['FantasyPoints']/17
rb_df['FantasyPointsRank'] = rb_df['FantasyPoints'].rank(ascending=False)
wr_df['PPG'] = wr_df['FantasyPoints']/17
wr_df['FantasyPointsRank'] = wr_df['FantasyPoints'].rank(ascending=False)

# sort RBs by RushingYds in descending order and get us back the top 15 rows.
print(rb_df.sort_values(by='FantasyPoints', ascending=False).head())
print(wr_df.sort_values(by='FantasyPoints', ascending=False).head())

sns.lineplot(
    data = rb_df,
    x = "FantasyPointsRank",
    y = "PPG",
    hue='Pos'
)

sns.lineplot(
    data = wr_df,
    x = "FantasyPointsRank",
    y = "PPG"
)
plt.show()