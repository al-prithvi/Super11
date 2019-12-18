import cvxpy as cp
import numpy as np
import pandas as pd
from Generate_Ordered_Cost_Utility_List import getCostAndUtilityList
from Get_Playing_22_List import getPlayerList
from Get_Player_Stats import getCompleteStats


np.random.seed(100)
total_cost = 100
max_batsmen = 5
min_batsmen = 3
max_bowlers = 5
min_bowlers = 3
max_allrounders = 3
min_allrounders = 1
max_wk = 1


def computeSum(l):
  sum = 0
  for index in range(0, len(l)):
      sum = sum + l[index]
  return sum

def getTeam(match_id, team_1, team_2, type):
  points_df = pd.read_csv("CSVs/match_" + match_id +"_stats.csv")
  player_list, wicketkeeper_1, wicketkeeper_2 = getPlayerList(match_id, team_1, team_2)
  player_df = getCompleteStats(wicketkeeper_1, wicketkeeper_2)
  sortedPlayerList, playerUtilityList, playerCostList, pointsList, num_batsmen, num_bowlers, num_allrounders = getCostAndUtilityList(player_df, points_df, player_list)
  batsmen_constraint = np.append(np.ones(num_batsmen), np.zeros(22-num_batsmen))
  bowlers_constraint = np.append(np.zeros(num_batsmen), np.ones(num_bowlers))
  bowlers_constraint = np.append(bowlers_constraint, np.zeros(22-(len(bowlers_constraint))))
  allrounders_constraint = np.append(np.zeros(num_batsmen + num_bowlers), np.ones(num_allrounders))
  allrounders_constraint = np.append(allrounders_constraint, np.zeros(22-(len(allrounders_constraint))))
  wk_constraint = np.append(np.zeros(20), np.ones(2))
  total_players_constraint = np.ones(22)
  # The variable we are solving for
  selection = cp.Variable(len(playerUtilityList),boolean=True)
  # Constraints
  constraints = [playerCostList * selection <= total_cost , 
                total_players_constraint * selection == 11, 
                batsmen_constraint * selection <=5,
                batsmen_constraint * selection >=3,
                bowlers_constraint * selection <=5,
                bowlers_constraint * selection >=3,
                allrounders_constraint * selection <=3,
                allrounders_constraint * selection >=1,
                wk_constraint * selection == 1
                ]
  if(type == "P"):
    total_utility = playerUtilityList * selection
  else:
    total_utility = pointsList * selection
  optimal_team = cp.Problem(cp.Maximize(total_utility), constraints)
  optimal_team.solve(solver=cp.GLPK_MI)
  total_points = 0
  if type == "P":
  	total_points = computeSum(pointsList*selection.value)
  else:
  	total_points = computeSum(pointsList*selection.value)*0.9
  #print("Utility My Team " + str(computeSum(playerUtilityList*selection.value)))
  #print("Points My Team " + str(computeSum(pointsList*selection.value)))
  return selection, sortedPlayerList, pointsList, total_points