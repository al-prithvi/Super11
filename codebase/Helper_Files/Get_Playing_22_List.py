import json
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt

def getPlayerList(match_id, team_1, team_2):
  with open('CSVs/12_teams.json') as json_file:
    data = json.load(json_file)
  player_list = data[match_id][team_1] + data[match_id][team_2]
  wicketkeeper_1 = data[match_id]["WicketKeeper"][0]
  wicketkeeper_2 = data[match_id]["WicketKeeper"][1]
  return player_list, wicketkeeper_1, wicketkeeper_2

def printPlaying11(match_id, team_1, team_2):
    with open('CSVs/12_teams.json') as json_file:
        data = json.load(json_file)

    fmt = '{:<8}{:<20}{}'

    print("Playing 11 for :")
    print(fmt.format('', team_1, team_2))
    i = 1
    for i, (t1, t2) in enumerate(zip(data[match_id][team_1], data[match_id][team_2])):
        print(fmt.format(i, t1, t2))
    print()
    print()

def getTeams(s_1, team, points, s_2):
    super_11 = []
    dream_11 = []
    points_1 = []
    points_2 = []
    for i in range(0, 22):
        if s_1.value[i]==1:
            super_11.append(team[i])
            points_1.append(points[i])
        if s_2.value[i]==1:
            dream_11.append(team[i])
            points_2.append(points[i])
    return super_11, dream_11, points_1, points_2

def printSelectedTeams(s_1 ,team, points, s_2):
    fmt = '{:<8}{:<20}{}'
    print(fmt.format('', 'Predicted Team', 'Most Optimal Team'))
    super_11, dream_11, points_1, points_2 = getTeams(s_1, team, points, s_2)
    
    i = 1
    for i, (t1, t2) in enumerate(zip(super_11, dream_11)):
        print(fmt.format(i, t1, t2))
    print()
    print()

def generateGraph(s_1, team, points, s_2, p_1, p_2):
    super_11, dream_11, points_1, points_2 = getTeams(s_1, team, points, s_2)
    plt.rcdefaults()
    fig, axis = plt.subplots()

    y_pos = np.arange(len(super_11))
    performance = 3 + 10 * np.random.rand(len(super_11))
    error = np.random.rand(len(super_11))

    axis.barh(y_pos, points_1, align='center', color="green")
    axis.set_yticks(y_pos)
    axis.set_yticklabels(super_11)
    axis.invert_yaxis()  # labels read top-to-bottom
    axis.set_xlabel('Player Points')
    axis.set_title('Prediced 11')

    plt.show()
    plt.clf()

    bar_width = [0.3, 0.3]
    y_pos = [2,2.5]

    barlist=plt.bar(y_pos, [p_1, p_2], width = bar_width)
    plt.xticks(y_pos, ['Predicted Team', 'Optimal Team'])
    barlist[0].set_color('g')
    barlist[1].set_color('r')
    plt.title("Total Team Points (Predicted vs Optimal)")
    plt.xlabel("Team")
    plt.ylabel("Total Points")
    plt.legend()
    plt.show()
    plt.clf()