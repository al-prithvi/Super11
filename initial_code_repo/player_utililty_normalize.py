
import pandas as pd
data = pd.read_csv("all_stats.csv")#("utility_stats.csv") 


'''
file = open("all_player_cost.txt", "r")


low = 1000000
high = 145000000
ran = 11 - 7

for line in file:
	st = line.split(':')
	ex = float(st[1].strip())
	norm = ex / (high - low)

	print(st[0], " : ", norm*ran+7)

'''
low = 0    #1000000
high = 15   #.  145000000
ran = 11 - 7

def norm(val):
	rang = high - low
	a = (val - low) / rang;
	range2 = ran
	a = (a * range2) + 7;
	if (a>11):
		print("wtf", val)
	#print(a)
	return a
	#norm = val/(high-low)
	#return norm*ran+7

#print(data)
op_df = []
for index, row in data.iterrows():
	utility = None
	if (row['player_type'] == 'Batsman'):
		utility = row['batting_utility']
	elif (row['player_type'] == 'Bowler'):
		utility = row['bowler_utility']
	else:
		utility = 1.3 * (row['bowler_utility'] + row['batting_utility'])
		#print (row['Player'])
		if (row['Player'] == 'Anand Rajan'):
			pass
			#print(row)
			#print("ok")
	if (row['player_type']=='AllRounder'):
		pass #print(row['Player'], " : ", norm(utility), row['player_type'] )
	l = [row['Player'], norm(utility), row['player_type']]
	op_df.append(l)

df = pd.DataFrame(op_df)

df.to_csv("utility_cost.csv")