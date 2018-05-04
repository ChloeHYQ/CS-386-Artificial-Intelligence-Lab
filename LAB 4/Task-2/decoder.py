import sys

file_name = sys.argv[1]
policy_file_name = sys.argv[2]
grid_file = open(file_name,'r')

grid = []
rows = 0
cols = 0
numStates = 0
start_state = 0
end_state = 0
map_pos = {}
map_rev = {}
for line in grid_file:
	temp = line.split()
	
	if cols == 0:
		cols = len(temp)

	for i in range(cols):
		if temp[i] == '0':
			map_pos[(rows,i)] = numStates
			map_rev[numStates] = (rows,i)
			numStates += 1

		elif temp[i] == '2':
			map_pos[(rows,i)] = numStates
			map_rev[numStates] = (rows,i) 
			start_state = numStates
			numStates += 1

		elif temp[i] == '3':
			map_pos[(rows,i)] = numStates
			map_rev[numStates] = (rows,i) 
			end_state = numStates
			numStates += 1

	grid.append(temp)
	rows += 1

grid_file.close()

policy_file = open(policy_file_name,'r')

map_dir = {	'0':'N',
		    '1':'E',
			'2':'W',
			'3':'S'}

policy = {}

state = 0
for line in policy_file:
	temp = line.split()
	if temp[0] == "iterations":
		break
	if temp[1] == '-1':
		policy[state] = "end"
	else:
		policy[state] = map_dir[temp[1]]
	state+=1

curr_state = start_state
while(1):
	if policy[curr_state] != "end":
		print(policy[curr_state],end=' ')
		r = map_rev[curr_state][0]
		c = map_rev[curr_state][1]
		if policy[curr_state] == 'N':
			curr_state = map_pos[(r-1,c)]
		elif policy[curr_state] == 'E':
			curr_state = map_pos[(r,c+1)]
		elif policy[curr_state] == 'W':
			curr_state = map_pos[(r,c-1)]
		elif policy[curr_state] == 'S':
			curr_state = map_pos[(r+1,c)]
	else:
		 break
print()