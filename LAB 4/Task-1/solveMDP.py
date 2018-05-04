import sys

file_name = sys.argv[1]
f = open(file_name,'r')

num_states = int(next(f).split()[1])
num_actions = int(next(f).split()[1])

start_state = int(next(f).split()[1])
end_state = int(next(f).split()[1])

R = [[{} for x in range(num_actions)] for y in range(num_states)] 
T = [[{} for x in range(num_actions)] for y in range(num_states)] 

while(1):
	curr_line = next(f).split()
	if curr_line[0] == "transitions":
		curr_state = int(curr_line[1])
		act = int(curr_line[2])
		next_state = int(curr_line[3])
		rew = float(curr_line[4])
		prob = float(curr_line[5])
		T[curr_state][act][next_state] = prob
		R[curr_state][act][next_state] = rew

	elif curr_line[0] == "discount":
		gamma = float(curr_line[1])
		break

# print(num_states," ",num_actions," ",start_state," ",end_state," ",gamma)
# print(T)
# print(R)		

Val_curr = [0 for i in range(num_states)]
Val_prev = [0 for i in range(num_states)]
Policy = [-1 for i in range(num_states)]

thresh = 1e-16
error = 1
num_iter = 0
while error > thresh:
	for s in range(0, num_states):
		if s == end_state:
			Val_curr[s] = Val_prev[s]
			continue
		max_reward = -float("inf")
		max_action = 0
		for a in range(0, num_actions):
			exp_reward = 0
			if not T[s][a]:
				continue
			for s_prime,prob in T[s][a].items():
				exp_reward += T[s][a][s_prime]*(R[s][a][s_prime] + gamma*Val_prev[s_prime])
			if exp_reward > max_reward:
				max_reward = exp_reward
				max_action = a
		Val_curr[s] = max_reward
		Policy[s] = max_action
	error = abs(max([abs(c-b) for c,b in zip(Val_curr,Val_prev)]))
	Val_prev = Val_curr[:]
	num_iter += 1	

for i in range(len(Val_curr)):
	print(Val_curr[i],"\t",Policy[i])
print("iterations\t",num_iter)