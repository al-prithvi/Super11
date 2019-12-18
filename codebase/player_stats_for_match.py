# -*- coding: utf-8 -*-
"""match1_2017.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1OnQ6PECgJ7I1oqjBHwHSlsU8m1sx5MxR

#**Basic Setup**
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
pd.set_option('max_rows',200)
pd.set_option('max_columns',100)
import numpy as np
import matplotlib.pyplot as plt
import sys, argparse
import json
# %matplotlib inline


def run_for_match(matchid):

  deliveries = pd.read_csv('../data/deliveries.csv')
  matches = pd.read_csv('../data/matches.csv')
  city = matches.groupby([matches.city,matches.venue]).venue.count().sort_values(ascending=False)
  city_df = pd.DataFrame(city)
  city_df.columns = ['count']

  matches.city.fillna('unknown',inplace=True)
  matches.winner.fillna('draw',inplace=True)
  matches.player_of_match.fillna('draw',inplace=True)

  """# **SET MATCH ID HERE => CRITICAL**

  Only match_ids **1 to 59** inclusive a valid for the **2017** season that is being used for prediction
  """

  match_id = matchid

  #'''
  # testing
  with open('CSVs/12_teams.json') as f:
    data = json.load(f)

  key = str(match_id)
  all_players = []
  match = (data[key])
  for k in match:
    all_players.append(match[k])
  #'''
  #print(all_players)
  #sys.exit()


  #Filter out the deliveries for the particular match
  deliveries = deliveries[deliveries["match_id"] == match_id]
  match = matches[matches["id"] == match_id]

  """# **Match Details**"""

  team1  = match["team1"].values[0]
  team2  = match["team2"].values[0]
  date  = match["date"].values[0]
  venue  = match["venue"].values[0]
  city  = match["city"].values[0]
  print("Match {} : {} vs {} on {} \n\t\t @ {}, {}"
  .format(match_id, team1, team2, date, venue, city))

  """# **Batsman Statistics**"""

  df_strike_rate = deliveries.groupby(['batsman']).agg({'ball':'count','batsman_runs':'mean'}).sort_values(by='batsman_runs',ascending=False)
  df_strike_rate.rename(columns ={'batsman_runs' : 'strike rate'}, inplace=True)
  df_runs_per_match = deliveries.groupby(['batsman','match_id']).agg({'batsman_runs':'sum'})
  df_total_runs = df_runs_per_match.groupby(['batsman']).agg({'sum' ,'mean','count'})
  df_total_runs.rename(columns ={'sum' : 'batsman run','count' : 'match count','mean' :'average score'}, inplace=True)
  df_total_runs.columns = df_total_runs.columns.droplevel()
  df_sixes = deliveries[['batsman','batsman_runs']][deliveries.batsman_runs==6].groupby(['batsman']).agg({'batsman_runs':'count'})
  df_four = deliveries[['batsman','batsman_runs']][deliveries.batsman_runs==4].groupby(['batsman']).agg({'batsman_runs':'count'})

  df_batsman_stat = pd.merge(pd.merge(pd.merge(df_strike_rate,df_total_runs, left_index=True, right_index=True, how='outer'),df_sixes, left_index=True, right_index=True, how='outer'),df_four, left_index=True, right_index=True, how='outer')
  df_batsman_stat.rename(columns = {'ball' : 'Ball', 'strike rate':'Strike Rate','batsman run' : 'Batsman Run','match count' : 'Match Count','average score' : 'Average score' ,'batsman_runs_x' :'Six','batsman_runs_y':'Four'},inplace=True)
  df_batsman_stat['Strike Rate'] = df_batsman_stat['Strike Rate']*100
  df_batsman_stat.sort_values(by='Batsman Run',ascending=False)

  #Dismissed Players
  df_batsman_dismissed = deliveries.groupby("player_dismissed").agg({'ball':'count'})
  df_batsman_stat = pd.merge(df_batsman_stat, df_batsman_dismissed, left_index=True, right_index=True, how='outer')
  df_batsman_stat.rename(columns={'ball' : 'Out'}, inplace=True)

  df_ones = deliveries[['batsman','batsman_runs']][deliveries.batsman_runs==1].groupby(['batsman']).agg({'batsman_runs':'count'})
  df_twos = deliveries[['batsman','batsman_runs']][deliveries.batsman_runs==2].groupby(['batsman']).agg({'batsman_runs':'count'})
  df_threes = deliveries[['batsman','batsman_runs']][deliveries.batsman_runs==3].groupby(['batsman']).agg({'batsman_runs':'count'})
  df_fives = deliveries[['batsman','batsman_runs']][deliveries.batsman_runs==5].groupby(['batsman']).agg({'batsman_runs':'count'})

  df_batsman_stat = pd.merge(df_batsman_stat, df_ones, left_index=True, right_index=True, how='outer')
  df_batsman_stat.rename(columns={'batsman_runs' : 'One'}, inplace=True)

  df_batsman_stat = pd.merge(df_batsman_stat, df_twos, left_index=True, right_index=True, how='outer')
  df_batsman_stat.rename(columns={'batsman_runs' : 'Two'}, inplace=True)

  df_batsman_stat = pd.merge(df_batsman_stat, df_threes, left_index=True, right_index=True, how='outer')
  df_batsman_stat.rename(columns={'batsman_runs' : 'Three'}, inplace=True)

  df_batsman_stat = pd.merge(df_batsman_stat, df_fives, left_index=True, right_index=True, how='outer')
  df_batsman_stat.rename(columns={'batsman_runs' : 'Five'}, inplace=True)

  df_batsman_stat.sort_values(by='Batsman Run',ascending=False)

  # Calculating 50s
  temp50 = df_runs_per_match[df_runs_per_match["batsman_runs"] >= 50]
  temp50 = temp50[temp50["batsman_runs"] < 100]
  temp50 = temp50.groupby(['batsman']).agg({'count'})

  temp50.columns = temp50.columns.droplevel()
  temp50.rename(columns={'count': "Fifty"}, inplace=True)

  # Calculating 100s
  temp100 = df_runs_per_match[df_runs_per_match["batsman_runs"] >= 100]
  temp100 = temp100.groupby(['batsman']).agg({'count'})

  temp100.columns = temp100.columns.droplevel()
  temp100.rename(columns={'count': "Hundred"}, inplace=True)

  # Merge 50s and 100s
  df_batsman_stat = pd.merge(df_batsman_stat, temp50, left_index=True, right_index=True, how='outer')
  df_batsman_stat = pd.merge(df_batsman_stat, temp100, left_index=True, right_index=True, how='outer')

  df_batsman_stat = df_batsman_stat.fillna(0)

  # Points for Each Batsman Action
  every_run = 0.5
  duck = -2
  each_four = 0.5
  each_six = 1
  each_fifty = 4
  each_hundred = 8

  # Computing Batsman Points
  df_batsman_stat["Batsman Points"] =  every_run * df_batsman_stat["Batsman Run"] + each_four * df_batsman_stat["Four"] + each_six * df_batsman_stat["Six"] + each_fifty * df_batsman_stat["Fifty"] + each_hundred * df_batsman_stat["Hundred"]

  batsman_updated_points = []

  for index, row in df_batsman_stat.iterrows():
    points = row["Batsman Points"]
    if row["Out"] == 1.0:
      print("Dismissed : " + index)
      if row["Batsman Run"] == 0.0:
        print("Old Points" + str(points))
        points += duck
        print("Updated Points because of Duck" + str(points))
    batsman_updated_points.append(points)

  df_batsman_stat["Batsman Points"] = batsman_updated_points

  df_batsman_stat

  """# **Bowler Statistics**"""

  condition = (deliveries.dismissal_kind.notnull()) &(deliveries.dismissal_kind != 'run out')&(deliveries.dismissal_kind != 'retired hurt')
  condition_fielding = (deliveries.dismissal_kind == 'caught') | (deliveries.dismissal_kind == 'run out')
  df_bowlers = deliveries.loc[condition,:].groupby(deliveries.bowler).dismissal_kind.count().sort_values(ascending=False)
  df_runs_match = deliveries.groupby(['bowler']).agg({'total_runs':'sum','ball':'count'})
  df_total_runs = df_runs_match.groupby(['bowler']).agg({'count'})
  df_runs_match.total_runs = df_runs_match.total_runs
  df_runs_match['run_rate'] = df_runs_match.total_runs/df_runs_match.ball*6
  df_bowlers = pd.merge(df_bowlers,df_runs_match, how='outer', left_index=True, right_index=True)

  # Computing Maiden Overs
  df_per_over = deliveries.groupby(['bowler', 'over']).agg({'total_runs':'sum'})
  df_per_over = df_per_over[df_per_over["total_runs"] == 0]
  df_per_over = df_per_over.groupby(['bowler']).agg({'total_runs':'count'})

  df_bowlers = pd.merge(df_bowlers,df_per_over, how='outer', left_index=True, right_index=True)
  df_bowlers = df_bowlers.fillna(0)
  df_bowlers.columns = ["Wicket", "Bowler Run", "Ball", "Economy Rate", "Maiden"]

  # Points for Each Bowler Action
  wicket = 10
  maiden_over = 2
  four_wicket_haul = 4
  five_wicket_haul = 6

  def points_for_economy_rate(df) :
    points = []
    for row in df.iteritems():
      #print(row)
      if row[1] < 4:
        points.append(8)
      elif row[1] < 5:
        points.append(6)
      elif row[1] < 6:
        points.append(4)
      elif row[1] < 7:
        points.append(0)
      elif row[1] < 8:
        points.append(-1)
      elif row[1] < 9:
        points.append(-2)
      elif row[1] < 10:
        points.append(-4)
      else:
        points.append(-6)
    return points

  # Computing Bowler Points
  df_bowlers['Bowler Economy Points'] = points_for_economy_rate(df_bowlers['Economy Rate'])
  df_bowlers["Bowler Points"] = wicket * df_bowlers["Wicket"] + maiden_over * df_bowlers["Maiden"] + df_bowlers['Bowler Economy Points']

  updated_points = []

  for index, row in df_bowlers.iterrows():
    points = row["Bowler Points"]
    if row["Wicket"] >= 5:
      points += five_wicket_haul
    elif row["Wicket"] == 4:
      points += four_wicket_haul
    updated_points.append(points)  
   
  df_bowlers["Bowler Points"] = updated_points
  df_bowlers

  """# **Fielding Stats**"""

  # Points for Each Fielding Action
  caught_or_runout = 4

  df_fielding_stats = deliveries.groupby(['fielder']).agg({'dismissal_kind':'count'})
  df_fielding_stats.columns = ["Dismissal Count"]

  df_fielding_stats["Fielding Points"] = df_fielding_stats["Dismissal Count"] * caught_or_runout

  df_fielding_stats

  """# **Join Stats**"""

  # Points for Making the playing 11
  playing_11 = 2

  df_combined = pd.merge(df_batsman_stat, df_bowlers, how="outer", left_index=True, right_index=True)
  df_combined = df_combined.fillna(0)
  df_combined["Total Points"] = df_combined["Batsman Points"] + df_combined["Bowler Points"] + playing_11

  # adding the fielding stats
  df_combined = pd.merge(df_combined, df_fielding_stats, how="outer", left_index=True, right_index=True)
  df_combined = df_combined.fillna(0)
  df_combined["Total Points"] = df_combined["Total Points"] + df_combined["Fielding Points"]


  # Basic Stats of Match
  team1  = match["team1"].values[0]
  team2  = match["team2"].values[0]
  date  = match["date"].values[0]
  venue  = match["venue"].values[0]
  city  = match["city"].values[0]
  print("Match {} : {} vs {} on {} \n\t\t @ {}, {}"
  .format(match_id, team1, team2, date, venue, city))

  # Dropping Unnessary Columns
  df_combined = df_combined.drop(['Ball_x', 'Ball_y'], axis=1)
  df_combined.sort_values(by='Total Points',ascending=False)

  df_combined.index.name = "Name"


  # --------
  # add player who's not in the list (set all to NaN)
  for ls in all_players:
    for player in ls:
      if (player in df_combined.index):
        pass#print("all good")
      else:
        print("not there ", player)
        #df2 = pd.DataFrame()
        s = pd.Series()#df2.xs()
        s.name = player
        df_combined = df_combined.append(s)
  df_combined = df_combined.fillna(0)
  # --------

  # Export to CSV
  filename = "CSVs/match_" + str(match_id) + "_stats.csv"
  df_combined.to_csv(filename)

if __name__ == '__main__':
  '''
    #usage: test.py -i <inputfile>
  if len(sys.argv) == 0:
    print("usage <scriptname> <match-id>")
    sys.exit()
  match_id = int(sys.argv[1])
  run_for_match(match_id)
  '''
  with open('12_teams.json') as f:
    data = json.load(f)

  all_match_id = [k for k in data]
  
  for i in all_match_id:
    run_for_match(int(i))



