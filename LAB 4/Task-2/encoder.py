import sys

file_name = sys.argv[1]
f = open(file_name,'r')

grid = []
rows = 0
cols = 0
numStates = 0
start_state = 0
end_state = 0
map_pos = {}
for line in f:
	temp = line.split()
	
	if cols == 0:
		cols = len(temp)

	for i in range(cols):
		if temp[i] == '0':
			map_pos[(rows,i)] = numStates 
			numStates += 1

		elif temp[i] == '2':
			map_pos[(rows,i)] = numStates 
			start_state = numStates
			numStates += 1

		elif temp[i] == '3':
			map_pos[(rows,i)] = numStates 
			end_state = numStates
			numStates += 1

	grid.append(temp)
	rows += 1

discount = 1
# print(map_pos)
# numStates 2
# numActions 2
# start 1
# end -1
# transitions 0 0 0 1 1
# transitions 0 1 1 2 1
# transitions 1 0 1 2 1
# transitions 1 1 0 1 1
# discount  0.9
# Mapping : 0,1,2,3 = N,E,W,S

print("numStates", numStates)
print("numActions 4")
print("start",start_state)
print("end", end_state)
for i in range(1,rows-1):
	for j in range(1,cols-1):
		if grid[i][j] == '0' or grid[i][j] == '2':
			if grid[i-1][j] == '0' or grid[i-1][j] == '2':
				print("transitions",map_pos[(i,j)],0,map_pos[(i-1,j)],-1,1)
			if grid[i-1][j] == '3':
				print("transitions",map_pos[(i,j)],0,map_pos[(i-1,j)],-1,1)

			if grid[i+1][j] == '0' or grid[i+1][j] == '2':
				print("transitions",map_pos[(i,j)],3,map_pos[(i+1,j)],-1,1)
			if grid[i+1][j] == '3':
				print("transitions",map_pos[(i,j)],3,map_pos[(i+1,j)],-1,1)

			if grid[i][j+1] == '0' or grid[i][j+1] == '2':
				print("transitions",map_pos[(i,j)],1,map_pos[(i,j+1)],-1,1)
			if grid[i][j+1] == '3':
				print("transitions",map_pos[(i,j)],1,map_pos[(i,j+1)],-1,1)

			if grid[i][j-1] == '0' or grid[i][j-1] == '2':
				print("transitions",map_pos[(i,j)],2,map_pos[(i,j-1)],-1,1)
			if grid[i][j-1] == '3':
				print("transitions",map_pos[(i,j)],2,map_pos[(i,j-1)],-1,1)

print("discount",discount)