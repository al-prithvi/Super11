# COMPUTE THE AGGREGATE STATS OF ALL PLAYERS

"""
Original file is located at
    https://colab.research.google.com/drive/13NaazmBT67gbSFE9JCkfNfCVaXa1QCKX

"""
# Importing the libraries
import pandas as pd

pd.set_option('max_rows', 200)
pd.set_option('max_columns', 100)

match_deliveries = pd.read_csv('../data/deliveries.csv')
matches = pd.read_csv('../data/matches.csv')
city = matches.groupby([matches.city, matches.venue]).venue.count().sort_values(ascending=False)

matches.city.fillna('unknown', inplace=True)
matches.winner.fillna('draw', inplace=True)
matches.player_of_match.fillna('draw', inplace=True)

# Batsman Statistics
batsman_strike_rate = match_deliveries.groupby(['batsman']).agg({'ball': 'count', 'batsman_runs': 'mean'}).sort_values(
    by='batsman_runs', ascending=False)
batsman_strike_rate.rename(columns={'batsman_runs': 'strike rate'}, inplace=True)
batsman_runs_per_match = match_deliveries.groupby(['batsman', 'match_id']).agg({'batsman_runs': 'sum'})
batsman_total_runs = batsman_runs_per_match.groupby(['batsman']).agg({'sum', 'mean', 'count'})
batsman_total_runs.rename(columns={'sum': 'batsman run', 'count': 'match count', 'mean': 'average score'}, inplace=True)
batsman_total_runs.columns = batsman_total_runs.columns.droplevel()
batsman_sixes = match_deliveries[['batsman', 'batsman_runs']][match_deliveries.batsman_runs == 6].groupby(
    ['batsman']).agg({'batsman_runs': 'count'})
batsman_four = match_deliveries[['batsman', 'batsman_runs']][match_deliveries.batsman_runs == 4].groupby(
    ['batsman']).agg({'batsman_runs': 'count'})

batsman_stats = pd.merge(
    pd.merge(pd.merge(batsman_strike_rate, batsman_total_runs, left_index=True, right_index=True, how='outer'),
             batsman_sixes, left_index=True, right_index=True, how='outer'), batsman_four, left_index=True,
    right_index=True, how='outer')
batsman_stats.rename(columns={'ball': 'Ball', 'strike rate': 'Strike Rate', 'batsman run': 'Batsman Run',
                              'match count': 'Batsman Match Count', 'average score': 'Average Score',
                              'batsman_runs_x': 'Six', 'batsman_runs_y': 'Four'}, inplace=True)
batsman_stats['Strike Rate'] = batsman_stats['Strike Rate'] * 100
batsman_stats.sort_values(by='Batsman Run', ascending=False)

# Dismissed Players
batsman_dismissed = match_deliveries.groupby("player_dismissed").agg({'ball': 'count'})
batsman_stats = pd.merge(batsman_stats, batsman_dismissed, left_index=True, right_index=True, how='outer')
batsman_stats.rename(columns={'ball': 'Out'}, inplace=True)

# Calculating 1s, 2s, 3s, 5s
batsman_ones = match_deliveries[['batsman', 'batsman_runs']][match_deliveries.batsman_runs == 1].groupby(
    ['batsman']).agg({'batsman_runs': 'count'})
batsman_twos = match_deliveries[['batsman', 'batsman_runs']][match_deliveries.batsman_runs == 2].groupby(
    ['batsman']).agg({'batsman_runs': 'count'})
batsman_threes = match_deliveries[['batsman', 'batsman_runs']][match_deliveries.batsman_runs == 3].groupby(
    ['batsman']).agg({'batsman_runs': 'count'})
batsman_fives = match_deliveries[['batsman', 'batsman_runs']][match_deliveries.batsman_runs == 5].groupby(
    ['batsman']).agg({'batsman_runs': 'count'})

batsman_stats = pd.merge(batsman_stats, batsman_ones, left_index=True, right_index=True, how='outer')
batsman_stats.rename(columns={'batsman_runs': 'One'}, inplace=True)

batsman_stats = pd.merge(batsman_stats, batsman_twos, left_index=True, right_index=True, how='outer')
batsman_stats.rename(columns={'batsman_runs': 'Two'}, inplace=True)

batsman_stats = pd.merge(batsman_stats, batsman_threes, left_index=True, right_index=True, how='outer')
batsman_stats.rename(columns={'batsman_runs': 'Three'}, inplace=True)

batsman_stats = pd.merge(batsman_stats, batsman_fives, left_index=True, right_index=True, how='outer')
batsman_stats.rename(columns={'batsman_runs': 'Five'}, inplace=True)

batsman_stats.sort_values(by='Batsman Run', ascending=False)

# Calculating Batsman 50s
batsman_50 = batsman_runs_per_match[batsman_runs_per_match["batsman_runs"] >= 50]
batsman_50 = batsman_50[batsman_50["batsman_runs"] < 100]
batsman_50 = batsman_50.groupby(['batsman']).agg({'count'})
batsman_50.columns = batsman_50.columns.droplevel()
batsman_50.rename(columns={'count': "Fifty"}, inplace=True)

# Calculating 100s
batsman_100 = batsman_runs_per_match[batsman_runs_per_match["batsman_runs"] >= 100]
batsman_100 = batsman_100.groupby(['batsman']).agg({'count'})
batsman_100.columns = batsman_100.columns.droplevel()
batsman_100.rename(columns={'count': "Hundred"}, inplace=True)

# Merge 50s and 100s
batsman_stats = pd.merge(batsman_stats, batsman_50, left_index=True, right_index=True, how='outer')
batsman_stats = pd.merge(batsman_stats, batsman_100, left_index=True, right_index=True, how='outer')

batsman_stats = batsman_stats.fillna(0)

# Bowler Stats

bowling_condition = (match_deliveries.dismissal_kind.notnull()) & (match_deliveries.dismissal_kind != 'run out') & (
        match_deliveries.dismissal_kind != 'retired hurt')
bowling_condition_for_fielding = (match_deliveries.dismissal_kind == 'caught') | (
        match_deliveries.dismissal_kind == 'run out')
bowler_stats = match_deliveries.loc[bowling_condition, :].groupby(
    match_deliveries.bowler).dismissal_kind.count().sort_values(
    ascending=False)
bowler_runs_match = match_deliveries.groupby(['bowler']).agg({'total_runs': 'sum', 'ball': 'count'})
batsman_total_runs = bowler_runs_match.groupby(['bowler']).agg({'count'})

bowler_runs_match.total_runs = bowler_runs_match.total_runs
bowler_runs_match['run_rate'] = bowler_runs_match.total_runs / bowler_runs_match.ball * 6
bowler_stats = pd.merge(bowler_stats, bowler_runs_match, how='outer', left_index=True, right_index=True)

# Computing Maiden Overs
bowler_runs_per_over = match_deliveries.groupby(['bowler', 'over']).agg({'total_runs': 'sum'})
bowler_runs_per_over = bowler_runs_per_over[bowler_runs_per_over["total_runs"] == 0]
bowler_runs_per_over = bowler_runs_per_over.groupby(['bowler']).agg({'total_runs': 'count'})

bowler_stats = pd.merge(bowler_stats, bowler_runs_per_over, how='outer', left_index=True, right_index=True)
bowler_stats = bowler_stats.fillna(0)
bowler_stats.columns = ["Wicket", "Bowler Run", "Ball", "Economy Rate", "Maiden"]

# Computing Bowler Match Count
bowler_match_count = match_deliveries.groupby(['bowler', 'match_id']).agg({'match_id': 'count'})
bowler_match_count.rename(columns={'match_id': 'bowler_count'}, inplace=True)
bowler_match_count = bowler_match_count.groupby(['bowler']).agg({'count'})
bowler_match_count.columns = ["Bowler Match Count"]

# Merge df_bowler_match_count with df_bowlers
bowler_stats = pd.merge(bowler_stats, bowler_match_count, how='outer', left_index=True, right_index=True)

# Combine Stats

agg_stats = pd.merge(batsman_stats, bowler_stats, how="outer", left_index=True, right_index=True)
agg_stats = agg_stats.fillna(0)

# Dropping Unnecessary Columns
agg_stats = agg_stats.drop(['Ball_x', 'Ball_y'], axis=1)
agg_stats = agg_stats.sort_values(by='Batsman Run', ascending=False)

agg_stats['Average Four'] = agg_stats['Four'] / agg_stats['Batsman Match Count']
agg_stats['Average Six'] = agg_stats['Six'] / agg_stats['Batsman Match Count']
agg_stats.head(2)

# Export to Excel

# taking approximation for total matches (might contain overlap)
agg_stats['Total Matches'] = agg_stats[['Batsman Match Count', 'Bowler Match Count']].max(axis=1)
# max(df_combined['Batsman Match Count'],df_combined['Bowler Match Count'])
agg_stats['Wicket Average'] = agg_stats['Wicket'] / agg_stats['Total Matches']

agg_stats.index.name = "Name"

# Export to CSV
filename = "./CSVs/player_stats.csv" # changed code  from agg_stats
agg_stats.to_csv(filename)
