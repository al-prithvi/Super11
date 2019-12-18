import json

list_of_players = []
with open('12_teams.json') as json_file:
    data = json.load(json_file)
    cnt = 0
    for p in data:
    	#print("Match :", data[p])
    	cnt += 1
    	for i in data[p]:
    		#print((set(data[p][i])), "players")
    		#print(i)
    		list_of_players.extend(data[p][i])

'''
print(len(list_of_players))
print()
print(len(set(list_of_players)) )
'''
#print(len(list_of_players))
print()
print(len(set(list_of_players)) )
print()
print((set(list_of_players)) )

for i in (set(list_of_players)):
	print(i, " : 140000000")