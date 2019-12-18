import numpy as np
import pandas as pd
import math


def getCostAndUtilityList(player_df, points_df, player_list):
  sortedPlayerList = []
  playerUtilityList = []
  playerCostList = []
  pointsList = []
  num_batsmen = 0
  num_bowlers = 0
  num_allrounders = 0
  cost_df = pd.read_csv('CSVs/player_costs.csv')

  for i in range(0, len(player_list)):
    for j in range(0, player_df.shape[0]):
      if player_df.iloc[j]['Player'] == player_list[i]:
        if(player_df.iloc[j]['player_type'] == "Batsman"):
          #print(player_df.iloc[j]['Player'])
          sortedPlayerList.append(player_list[i])
          playerUtilityList.append(player_df.iloc[j]['batting_utility'])
          for k in range(0, cost_df.shape[0]):
            if cost_df.iloc[k]['Name'] == player_list[i]:
              playerCostList.append(cost_df.iloc[k]['Cost'])
          for k in range(0, points_df.shape[0]):
            if points_df.iloc[k]['Name'] == player_list[i]:
              pointsList.append(points_df.iloc[k]['Total Points'])
          num_batsmen = num_batsmen + 1

  for i in range(0, len(player_list)):
    for j in range(0, player_df.shape[0]):
      if str(player_df.iloc[j]['Player']) == str(player_list[i]):
        if(player_df.iloc[j]['player_type'] == "Bowler"):
          #print(player_df.iloc[j]['Player'])
          sortedPlayerList.append(player_list[i])
          playerUtilityList.append(player_df.iloc[j]['bowler_utility'])
          for k in range(0, cost_df.shape[0]):
            if cost_df.iloc[k]['Name'] == player_list[i]:
              playerCostList.append(cost_df.iloc[k]['Cost'])
          for k in range(0, points_df.shape[0]):
            if points_df.iloc[k]['Name'] == player_list[i]:
              pointsList.append(points_df.iloc[k]['Total Points'])
          num_bowlers = num_bowlers + 1

  for i in range(0, len(player_list)):
    for j in range(0, player_df.shape[0]):
      if str(player_df.iloc[j]['Player']) == str(player_list[i]):
        if(player_df.iloc[j]['player_type'] == "AllRounder"):
          #print(player_df.iloc[j]['Player'])
          sortedPlayerList.append(player_list[i])
          playerUtilityList.append(1.3*(player_df.iloc[j]['batting_utility']+player_df.iloc[j]['bowler_utility'])/2)
          for k in range(0, cost_df.shape[0]):
            if cost_df.iloc[k]['Name'] == player_list[i]:
              playerCostList.append(cost_df.iloc[k]['Cost'])
          for k in range(0, points_df.shape[0]):
            if points_df.iloc[k]['Name'] == player_list[i]:
              pointsList.append(points_df.iloc[k]['Total Points'])
          num_allrounders = num_allrounders + 1
  
  for i in range(0, len(player_list)):
    for j in range(0, player_df.shape[0]):
      if player_df.iloc[j]['Player'] == player_list[i]:
        if(player_df.iloc[j]['player_type'] == "WicketKeeper"):
          #print(player_df.iloc[j]['Player'])
          sortedPlayerList.append(player_list[i])
          playerUtilityList.append(player_df.iloc[j]['batting_utility'])
          for k in range(0, cost_df.shape[0]):
            if cost_df.iloc[k]['Name'] == player_list[i]:
              playerCostList.append(cost_df.iloc[k]['Cost'])
          for k in range(0, points_df.shape[0]):
            if points_df.iloc[k]['Name'] == player_list[i]:
              pointsList.append(points_df.iloc[k]['Total Points'])
          num_batsmen = num_batsmen + 1
  return sortedPlayerList, playerUtilityList, playerCostList, pointsList, num_batsmen, num_bowlers, num_allrounders