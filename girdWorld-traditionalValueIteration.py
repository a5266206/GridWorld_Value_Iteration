Transitions = {}
Reward = {}
terminalStates = {}
epsilon = 0.00000000000000000000000000000000000000000000000000000000000000000000001

def failMovement(state,wallList):
	if state in wallList:
		return True
	x,y = state.split(",")
	y = int(y)
	x = int(x)
	if y > numColumns or y < 1:
		return True
	if x > numRows or x < 1:
		return True
	return False

def read_file():
	global gamma
	global numRows
	global numColumns
	global wallList
	f = open("input.txt", "r")
	content = f.read().splitlines()
	f.close()
	numRows,numColumns = content[0].split(",")
	numRows = int(numRows)
	numColumns = int(numColumns)
	numWalls = int(content[1])
	wallList = []
	if numWalls > 0:
		for i in range(2,2+numWalls):
			wallList.append(content[i])
	numTerminals = int(content[2+numWalls])
	terminalList = []
	if numTerminals > 0:
		for i in range(3+numWalls,3+numWalls+numTerminals):
			terminalList.append(content[i])
	pWalk,pRun = content[3+numWalls+numTerminals].split(",")
	pWalk = float(pWalk)
	pRun = float(pRun)
	rWalk,rRun = content[4+numWalls+numTerminals].split(",")
	rWalk = float(rWalk)
	rRun = float(rRun)
	gamma = float(content[5+numWalls+numTerminals])
	# build states list
	states = []
	for i in range(1,numRows+1):
		for j in range(1,numColumns+1):
			states.append(str(i)+","+str(j))
	for s in wallList:
		states.remove(s)

	for i in range(1,numRows+1):
		for j in range(1,numColumns+1):
			Reward[str(i)+","+str(j)] = [rWalk, rRun]
	for i in terminalList:
		a,b,c = i.split(",")
		terminalStates[a+","+b] = float(c)
	# build transitions dictionary
	for i in states:
		if i in terminalStates:
			Transitions[i] = {"Exit": [(0.0, i)]}
			Reward[i] = terminalStates[i]
		else:
			Transitions[i] = {"Wr":[],"Wl":[],"Wu":[],"Wd":[],"Rr":[],"Rl":[],"Ru":[],"Rd":[]}
			# Walk right
			x,y = i.split(",")
			y1 = int(y)+1
			s1wr = x+","+str(y1)
			if failMovement(s1wr,wallList):
				Transitions[i]["Wr"].append((pWalk, i))
			else:
				Transitions[i]["Wr"].append((pWalk, s1wr))
			x1 = int(x)+1
			s2wr = str(x1)+","+y
			if failMovement(s2wr,wallList):
				Transitions[i]["Wr"].append(((1-pWalk)/2, i))
			else:
				Transitions[i]["Wr"].append(((1-pWalk)/2, s2wr))
			x2 = int(x)-1
			s3wr = str(x2)+","+y
			if failMovement(s3wr,wallList):
				Transitions[i]["Wr"].append(((1-pWalk)/2, i))
			else:
				Transitions[i]["Wr"].append(((1-pWalk)/2, s3wr))
			# Walk left
			y1 = int(y)-1
			s1wl = x+","+str(y1)
			if failMovement(s1wl,wallList):
				Transitions[i]["Wl"].append((pWalk, i))
			else:
				Transitions[i]["Wl"].append((pWalk, s1wl))
			x1 = int(x)+1
			s2wl = str(x1)+","+y
			if failMovement(s2wl,wallList):
				Transitions[i]["Wl"].append(((1-pWalk)/2, i))
			else:
				Transitions[i]["Wl"].append(((1-pWalk)/2, s2wl))
			x2 = int(x)-1
			s3wl = str(x2)+","+y
			if failMovement(s3wl,wallList):
				Transitions[i]["Wl"].append(((1-pWalk)/2, i))
			else:
				Transitions[i]["Wl"].append(((1-pWalk)/2, s3wl))
			# Walk up
			x1 = int(x)+1
			s1wu = str(x1)+","+y
			if failMovement(s1wu,wallList):
				Transitions[i]["Wu"].append((pWalk, i))
			else:
				Transitions[i]["Wu"].append((pWalk, s1wu))
			y1 = int(y)+1
			s2wu = x+","+str(y1)
			if failMovement(s2wu,wallList):
				Transitions[i]["Wu"].append(((1-pWalk)/2, i))
			else:
				Transitions[i]["Wu"].append(((1-pWalk)/2, s2wu))
			y2 = int(y)-1
			s3wu = x+","+str(y2)
			if failMovement(s3wu,wallList):
				Transitions[i]["Wu"].append(((1-pWalk)/2, i))
			else:
				Transitions[i]["Wu"].append(((1-pWalk)/2, s3wu))
			# Walk down
			x1 = int(x)-1
			s1wd = str(x1)+","+y
			if failMovement(s1wd,wallList):
				Transitions[i]["Wd"].append((pWalk, i))
			else:
				Transitions[i]["Wd"].append((pWalk, s1wd))
			y1 = int(y)+1
			s2wd = x+","+str(y1)
			if failMovement(s2wd,wallList):
				Transitions[i]["Wd"].append(((1-pWalk)/2, i))
			else:
				Transitions[i]["Wd"].append(((1-pWalk)/2, s2wd))
			y2 = int(y)-1
			s3wd = x+","+str(y2)
			if failMovement(s3wd,wallList):
				Transitions[i]["Wd"].append(((1-pWalk)/2, i))
			else:
				Transitions[i]["Wd"].append(((1-pWalk)/2, s3wd))
			# Run right
			y1 = int(y)+2
			s1rr = x+","+str(y1)
			if failMovement(s1wr,wallList) or failMovement(s1rr,wallList):
				Transitions[i]["Rr"].append((pRun, i))
			else:
				Transitions[i]["Rr"].append((pRun, s1rr))
			x1 = int(x)+2
			s2rr = str(x1)+","+y
			if failMovement(s2wr,wallList) or failMovement(s2rr,wallList):
				Transitions[i]["Rr"].append(((1-pRun)/2, i))
			else:
				Transitions[i]["Rr"].append(((1-pRun)/2, s2rr))
			x2 = int(x)-2
			s3rr = str(x2)+','+y
			if failMovement(s3wr,wallList) or failMovement(s3rr,wallList):
				Transitions[i]["Rr"].append(((1-pRun)/2, i))
			else:
				Transitions[i]["Rr"].append(((1-pRun)/2, s3rr))
			# Run left
			y1 = int(y)-2
			s1rl = x+","+str(y1)
			if failMovement(s1wl,wallList) or failMovement(s1rl,wallList):
				Transitions[i]["Rl"].append((pRun, i))
			else:
				Transitions[i]["Rl"].append((pRun, s1rl))
			x1 = int(x)+2
			s2rl = str(x1)+","+y
			if failMovement(s2wl,wallList) or failMovement(s2rl,wallList):
				Transitions[i]["Rl"].append(((1-pRun)/2, i))
			else:
				Transitions[i]["Rl"].append(((1-pRun)/2, s2rl))
			x2 = int(x)-2
			s3rl = str(x2)+','+y
			if failMovement(s3wl,wallList) or failMovement(s3rl,wallList):
				Transitions[i]["Rl"].append(((1-pRun)/2, i))
			else:
				Transitions[i]["Rl"].append(((1-pRun)/2, s3rl))
			# Run up
			x1 = int(x)+2
			s1ru = str(x1)+","+y
			if failMovement(s1wu,wallList) or failMovement(s1ru,wallList):
				Transitions[i]["Ru"].append((pRun, i))
			else:
				Transitions[i]["Ru"].append((pRun, s1ru))
			y1 = int(y)+2
			s2ru = x+","+str(y1)
			if failMovement(s2wu,wallList) or failMovement(s2ru,wallList):
				Transitions[i]["Ru"].append(((1-pRun)/2, i))
			else:
				Transitions[i]["Ru"].append(((1-pRun)/2, s2ru))
			y2 = int(y)-2
			s3ru = x+","+str(y2)
			if failMovement(s3wu,wallList) or failMovement(s3ru,wallList):
				Transitions[i]["Ru"].append(((1-pRun)/2, i))
			else:
				Transitions[i]["Ru"].append(((1-pRun)/2, s3ru))
			# Run down
			x1 = int(x)-2
			s1rd = str(x1)+","+y
			if failMovement(s1wd,wallList) or failMovement(s1rd,wallList):
				Transitions[i]["Rd"].append((pRun, i))
			else:
				Transitions[i]["Rd"].append((pRun, s1rd))
			y1 = int(y)+2
			s2rd = x+","+str(y1)
			if failMovement(s2wd,wallList) or failMovement(s2rd,wallList):
				Transitions[i]["Rd"].append(((1-pRun)/2, i))
			else:
				Transitions[i]["Rd"].append(((1-pRun)/2, s2rd))
			y2 = int(y)-2
			s3rd = x+","+str(y2)
			if failMovement(s3wd,wallList) or failMovement(s3rd,wallList):
				Transitions[i]["Rd"].append(((1-pRun)/2, i))
			else:
				Transitions[i]["Rd"].append(((1-pRun)/2, s3rd))

read_file()

class MarkovDecisionProcess:

	def __init__(self, transition={}, reward={}):
		self.states = transition.keys()
		self.transition = transition
		self.reward = reward

	def R(self, state, action):
		# return reward of the state
		tmp = self.reward[state]
		if action[0] == 'W':
			return tmp[0]
		elif action[0] == 'R':
			return tmp[1]
		else:
			return tmp

	def actions(self, state):
		# return set of actions that can be performed in this state
		if len(self.transition[state].keys())>1:
			return ['Wu','Wd','Wl',"Wr",'Ru','Rd','Rl','Rr']
		else:
			return ['Exit']

	def T(self, state, action):
		# return a list of probability and result-state pairs.
		return self.transition[state][action]

#Initialize the MarkovDecisionProcess object
mdp = MarkovDecisionProcess(transition=Transitions, reward=Reward)

def value_iteration():
	# solve the MDP by value iteration
	# returns utility values
	states = mdp.states
	actions = mdp.actions
	T = mdp.T
	R = mdp.R
	# initialize value of all the states
	V1 = {s: 0.0 for s in states}
	for t in terminalStates:
		V1[t] = terminalStates[t]
	while True:
		U = V1.copy()
		delta = 0
		for s in states:
			#Bellman update
			policy = []
			for a in actions(s):
				Psum = 0.0
				for p,s1 in T(s,a):
					Psum = Psum + p*U[s1]
				policy.append(R(s,a)+gamma*Psum)
			V1[s] = max(policy)
			#calculate maximum difference in value
			delta = max(delta, abs(V1[s] - U[s]))
		#convergence check
		if delta < epsilon * (1 - gamma) / gamma:
			return U

def best_policy(V):
	states = mdp.states
	actions = mdp.actions
	T = mdp.T
	R = mdp.R
	pi = {}
	for s in states:
		policy = [None] * 8
		for a in actions(s):
			Psum = 0.0
			for p,s1 in T(s,a):
				Psum = Psum + p * V[s1]
			if a == "Wu" or a == "Exit":
				if a == "Wu":
					policy[0] = R(s,"Wu") + gamma * Psum
				else:
					policy[0] = R(s,"Exit") + gamma * Psum					
			elif a == "Wd":
				policy[1] = R(s,"Wd") + gamma * Psum
			elif a == "Wl":
				policy[2] = R(s,"Wl") + gamma * Psum
			elif a == "Wr":
				policy[3] = R(s,"Wr") + gamma * Psum
			elif a == "Ru":
				policy[4] = R(s,"Ru") + gamma * Psum
			elif a == "Rd":
				policy[5] = R(s,"Rd") + gamma * Psum
			elif a == "Rl":
				policy[6] = R(s,"Rl") + gamma * Psum
			elif a == "Rr":
				policy[7] = R(s,"Rr") + gamma * Psum
		maxVal = policy[0]
		maxAct = 0
		if policy[1] != None:
			for i in range(1,8):
				if policy[i] > maxVal:
					maxVal = policy[i]
					maxAct = i
			if maxAct == 0:
				pi[s] = "Wu"
			elif maxAct == 1:
				pi[s] = "Wd"
			elif maxAct == 2:
				pi[s] = "Wl"
			elif maxAct == 3:
				pi[s] = "Wr"
			elif maxAct == 4:
				pi[s] = "Ru"
			elif maxAct == 5:
				pi[s] = "Rd"
			elif maxAct == 6:
				pi[s] = "Rl"	
			elif maxAct == 7:
				pi[s] = "Rr"
		else:
			pi[s] = "Exit"
	return pi

#call value iteration
V = value_iteration()
pi = best_policy(V)

def output_file():
	f = open("output.txt", "w")
	for i in range(1,numRows+1):
		for j in range(1,numColumns+1):
			tmp = str(numRows+1-i)+","+str(j)
			if j == 1:
				if tmp in wallList:
					f.write("None")
				else:
					if pi[tmp] == "Wu":
						f.write("Walk Up")
					elif pi[tmp] == "Wd":
						f.write("Walk Down")
					elif pi[tmp] == "Wl":
						f.write("Walk Left")
					elif pi[tmp] == "Wr":
						f.write("Walk Right")
					elif pi[tmp] == "Ru":
						f.write("Run Up")
					elif pi[tmp] == "Rd":
						f.write("Run Down")
					elif pi[tmp] == "Rl":
						f.write("Run Left")
					elif pi[tmp] == "Rr":
						f.write("Run Right")
					elif pi[tmp] == "Exit":
						f.write("Exit")
			else:
				if tmp in wallList:
					f.write(",None")
				else:
					if pi[tmp] == "Wu":
						f.write(",Walk Up")
					elif pi[tmp] == "Wd":
						f.write(",Walk Down")
					elif pi[tmp] == "Wl":
						f.write(",Walk Left")
					elif pi[tmp] == "Wr":
						f.write(",Walk Right")
					elif pi[tmp] == "Ru":
						f.write(",Run Up")
					elif pi[tmp] == "Rd":
						f.write(",Run Down")
					elif pi[tmp] == "Rl":
						f.write(",Run Left")
					elif pi[tmp] == "Rr":
						f.write(",Run Right")
					elif pi[tmp] == "Exit":
						f.write(",Exit")
		f.write("\n")
	f.close()

output_file()
