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
