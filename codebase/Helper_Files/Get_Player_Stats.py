import numpy as np
import pandas as pd

def isNaN(num):
    return num != num

def getPoints(min_score, max_score, num_of_bins, reward_per_interval, base_score, player_score):
  interval_size = (max_score - min_score)/num_of_bins
  if player_score < min_score:
    return base_score
  return (base_score + ((player_score - min_score)/interval_size)*reward_per_interval)

def getCompleteStats(wicketkeeper_1, wicketkeeper_2):
  #Add New Columns
  player_df = pd.read_csv('CSVs/player_stats.csv')
  player_df['avg_score_utility'] = np.zeros(player_df.shape[0])
  player_df['strike_rate_utility'] = np.zeros(player_df.shape[0])
  player_df['sixes_utility'] = np.zeros(player_df.shape[0])
  player_df['fours_utility'] = np.zeros(player_df.shape[0])
  player_df['wickets_utility'] = np.zeros(player_df.shape[0])
  player_df['total_wickets_utility'] = np.zeros(player_df.shape[0])
  player_df['economy_utility'] = np.zeros(player_df.shape[0])
  player_df['batting_utility'] = np.zeros(player_df.shape[0])
  player_df['bowler_utility'] = np.zeros(player_df.shape[0])
  player_df['player_type'] = "Bowler"

  #Compute Utilities for each player
  for index in range(0, player_df.shape[0]):
    #Batting Utilities
    player_df.iloc[index, player_df.columns.get_loc('avg_score_utility')] = getPoints(10, 42, 6, 2, 1, player_df.iloc[index]['Average Score'])
    player_df.iloc[index, player_df.columns.get_loc('strike_rate_utility')] = getPoints(100, 170, 7, 0.5, 1, player_df.iloc[index]['Strike Rate'])
    player_df.iloc[index, player_df.columns.get_loc('sixes_utility')] = getPoints(1, 6, 5, 0.5, 0, player_df.iloc[index]['Average Six'])
    player_df.iloc[index, player_df.columns.get_loc('fours_utility')] = getPoints(1, 16, 5, 1, 0, player_df.iloc[index]['Average Four'])

    #Bowling Utilities
    player_df.iloc[index, player_df.columns.get_loc('wickets_utility')] = getPoints(0, 3, 6, 0.5, 0, player_df.iloc[index]['Wicket Average'])
    player_df.iloc[index, player_df.columns.get_loc('total_wickets_utility')] = getPoints(0, 155,3, 1, 0, player_df.iloc[index]['Wicket'])
    if(player_df.iloc[index]['Economy Rate'])>0:
      player_df.iloc[index, player_df.columns.get_loc('economy_utility')] = getPoints(-23, -3, 6, 0.7, 0, player_df.iloc[index]['Economy Rate']*-1)
    else:
      player_df.iloc[index, player_df.columns.get_loc('economy_utility')] = 0
    
    #Full Batting Utilities
    player_df.iloc[index, player_df.columns.get_loc('batting_utility')] = player_df.iloc[index]['avg_score_utility'] + player_df.iloc[index]['strike_rate_utility'] + player_df.iloc[index]['sixes_utility'] + player_df.iloc[index]['fours_utility']
    #Full Bowling Utilities
    player_df.iloc[index, player_df.columns.get_loc('bowler_utility')] = 1.5*(player_df.iloc[index]['wickets_utility'] + player_df.iloc[index]['economy_utility'] + player_df.iloc[index]['total_wickets_utility']) 
    
    if(player_df.iloc[index]['Bowler Match Count']<=20):
      player_df.iloc[index, player_df.columns.get_loc('bowler_utility')] = player_df.iloc[index, player_df.columns.get_loc('bowler_utility')] - 1
    
    if(player_df.iloc[index]['Player'] == wicketkeeper_1 or player_df.iloc[index]['Player'] == wicketkeeper_2):
      player_df.iloc[index, player_df.columns.get_loc('player_type')] = "WicketKeeper"
    elif(player_df.iloc[index]['batting_utility']>=6 and player_df.iloc[index]['bowler_utility']>=6):
      player_df.iloc[index, player_df.columns.get_loc('player_type')] = "AllRounder"
    elif(player_df.iloc[index]['batting_utility']>=7):
      player_df.iloc[index, player_df.columns.get_loc('player_type')] = "Batsman"
    elif(player_df.iloc[index]['bowler_utility']>=7):
      player_df.iloc[index, player_df.columns.get_loc('player_type')] = "Bowler"
    elif(player_df.iloc[index]['bowler_utility'] > player_df.iloc[index]['batting_utility']):
      player_df.iloc[index, player_df.columns.get_loc('player_type')] = "Bowler"
    else:
      player_df.iloc[index, player_df.columns.get_loc('player_type')] = "Batsman"

  for index in range(0, player_df.shape[0]):
    if isNaN(player_df.iloc[index]['batting_utility']):
      player_df.iloc[index, player_df.columns.get_loc('batting_utility')]  = 2.0
  return player_df

