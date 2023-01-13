import pandas as pd
# Data visualization
import seaborn as sns
import matplotlib.pyplot as plt

from save_player_stats import *


def main():
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
    passing = scrape_stats(2022, 'passing')
    rush_rec = pd.merge(rushing, receiving, on=['Player','Tm', 'Age', 'Pos', 'G', 'GS', 'Fmb'], suffixes=["_rush","_rec"], how="outer")

    rush_rec['FantasyPoints'] = (
        rush_rec['Yds_rush']*scoring_weights['rushing_yds'] +
        rush_rec['TD_rush']*scoring_weights['rushing_td'] +
        rush_rec['Yds_rec']*scoring_weights['receiving_yds'] +
        rush_rec['TD_rec']*scoring_weights['receiving_td'] +
        rush_rec['Rec']*scoring_weights['receptions'] + 
        rush_rec['Fmb']*scoring_weights['FL']
    )
    rush_rec['PPG'] = rush_rec['FantasyPoints']/rush_rec['G']
    rush_rec['PPG_Rank'] = rush_rec.groupby('Pos')['PPG'].rank(ascending=False)

    te = rush_rec.loc[rush_rec['Pos']=='TE']
    rb = rush_rec.loc[rush_rec['Pos']=='RB']
    wr = rush_rec.loc[rush_rec['Pos']=='WR']

    print(wr.sort_values(by="PPG_Rank", ascending=True).head())

    sns.lineplot(
        data = rush_rec,
        x = "PPG_Rank",
        y = "PPG",
        hue='Pos'
    )

    #plt.show()

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

if __name__ == '__main__':
    main()