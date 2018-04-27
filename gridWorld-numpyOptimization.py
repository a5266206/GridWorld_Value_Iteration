import numpy

def printInput(numRows,numColumns,numWalls,wallList,numTerminals,terminalList,pWalk,pRun,rWalk,rRun, f):
	print "Row:",numRows," Column:",numColumns
	print "num Wall",numWalls
	print "Wall position:",wallList
	print "num Terminal",numTerminals
	print "Terminal position/rewards:",terminalList
	print "P walk:",pWalk," P run:",pRun
	print "R walk:",rWalk," R run:",rRun
	print "discount factor:",f
	print "====================================================================================================================="

def read_file():
	global gamma
	global numRows
	global numColumns
	global wallList
	global pWalk
	global pRun
	global rWalk
	global rRun
	global terminalStates
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
	printInput(numRows,numColumns,numWalls,wallList,numTerminals,terminalList,pWalk,pRun,rWalk,rRun,gamma)
	# build terminal state
	terminalStates = {}
	for i in terminalList:
		a,b,c = i.split(",")
		terminalStates[a+","+b] = float(c)

read_file()

def value_iteration():
	# returns the best policy for states after convergence
	BP = numpy.zeros((numRows, numColumns), dtype=int)
	for state in terminalStates:
		r,c = state.split(",")
		BP[numRows-int(r)][int(c)-1] = 8
	for state in wallList:
		r,c = state.split(",")
		BP[numRows-int(r)][int(c)-1] = -1
	#initialize value of all the states
	V = numpy.zeros((numRows, numColumns), dtype=float)
	for state in terminalStates:
		r,c = state.split(",")
		V[numRows-int(r)][int(c)-1] = terminalStates[state]
	while True:
		delta = 0
		V0 = V.copy()
		Vwu = V.copy()
		Vwd = V.copy()
		Vwl = V.copy()
		Vwr = V.copy()
		Vru = V.copy()
		Vrd = V.copy()
		Vrl = V.copy()
		Vrr = V.copy()
		#Bellman update, update the utility values
		# Update 8 action boards
		# Walk Up
		Vwu = numpy.roll(Vwu, 1, axis=0)
		Vwu[0] = V0[0]
		# Walk Down
		Vwd = numpy.roll(Vwd, -1, axis=0)
		Vwd[numRows-1] = V0[numRows-1]
		# Walk Left
		Vwl = numpy.roll(Vwl, 1, axis=1)
		Vwl[:,0] = V0[:,0]
		# Walk Right
		Vwr = numpy.roll(Vwr, -1, axis=1)
		Vwr[:,numColumns-1] = V0[:,numColumns-1]
		# Run Up
		Vru = numpy.roll(Vru, 2, axis=0)			
		Vru[0] = V0[0]
		Vru[1] = V0[1]
		# Run Down
		Vrd = numpy.roll(Vrd, -2, axis=0)
		Vrd[numRows-1] = V0[numRows-1]
		Vrd[numRows-2] = V0[numRows-2]
		# Run Left
		Vrl = numpy.roll(Vrl, 2, axis=1)
		Vrl[:,0] = V0[:,0]
		Vrl[:,1] = V0[:,1]
		# Run Right
		Vrr = numpy.roll(Vrr, -2, axis=1)
		Vrr[:,numColumns-1] = V0[:,numColumns-1]
		Vrr[:,numColumns-2] = V0[:,numColumns-2]
		for s in wallList:
			r,c = s.split(",")
			r = int(r)
			c = int(c)
			# WU
			Vwu[numRows-r][c-1] = 0.0
			if numRows-r < numRows-1:
				Vwu[numRows-r+1][c-1] = V0[numRows-r+1][c-1]
			# WD
			Vwd[numRows-r][c-1] = 0.0
			if numRows-r > 0:
				Vwd[numRows-r-1][c-1] = V0[numRows-r-1][c-1]
			# WL
			Vwl[numRows-r][c-1] = 0.0
			if c-1 < numColumns-1:
				Vwl[numRows-r][c] = V0[numRows-r][c]
			# WR
			Vwr[numRows-r][c-1] = 0.0
			if c-1 > 0:
				Vwr[numRows-r][c-2] = V0[numRows-r][c-2]
			# RU
			Vru[numRows-r][c-1] = 0.0
			if numRows-r < numRows-1:
				Vru[numRows-r+1][c-1] = V0[numRows-r+1][c-1]
				if numRows-r < numRows-2:
					Vru[numRows-r+2][c-1] = V0[numRows-r+2][c-1]
			# RD
			Vrd[numRows-r][c-1] = 0.0
			if numRows-r > 0:
				Vrd[numRows-r-1][c-1] = V0[numRows-r-1][c-1]
				if r > 1:
					Vrd[numRows-r-2][c-1] = V0[numRows-r-2][c-1]
			# RL
			Vrl[numRows-r][c-1] = 0.0
			if c-1 < numColumns-1:
				Vrl[numRows-r][c] = V0[numRows-r][c]
				if c-1 < numColumns-2:
					Vrl[numRows-r][c+1] = V0[numRows-r][c+1]
			# RR
			Vrr[numRows-r][c-1] = 0.0
			if c-1 > 0:
				Vrr[numRows-r][c-2] = V0[numRows-r][c-2]
				if c-1 > 1:
					Vrr[numRows-r][c-3] = V0[numRows-r][c-3]
		# Update V board
		Uwu = rWalk + gamma*(pWalk*Vwu + (1-pWalk)/2*Vwl + (1-pWalk)/2*Vwr)
		Uwd = rWalk + gamma*(pWalk*Vwd + (1-pWalk)/2*Vwl + (1-pWalk)/2*Vwr)
		Uwl = rWalk + gamma*(pWalk*Vwl + (1-pWalk)/2*Vwu + (1-pWalk)/2*Vwd)
		Uwr = rWalk + gamma*(pWalk*Vwr + (1-pWalk)/2*Vwu + (1-pWalk)/2*Vwd)
		Uru = rRun + gamma*(pRun*Vru + (1-pRun)/2*Vrl + (1-pRun)/2*Vrr)
		Urd = rRun + gamma*(pRun*Vrd + (1-pRun)/2*Vrl + (1-pRun)/2*Vrr)
		Url = rRun + gamma*(pRun*Vrl + (1-pRun)/2*Vru + (1-pRun)/2*Vrd)
		Urr = rRun + gamma*(pRun*Vrr + (1-pRun)/2*Vru + (1-pRun)/2*Vrd)
		for s in terminalStates:
			r,c = s.split(",")
			Uwu[numRows-int(r)][int(c)-1] = terminalStates[s]
			Uwd[numRows-int(r)][int(c)-1] = terminalStates[s]
			Uwl[numRows-int(r)][int(c)-1] = terminalStates[s]
			Uwr[numRows-int(r)][int(c)-1] = terminalStates[s]
			Uru[numRows-int(r)][int(c)-1] = terminalStates[s]
			Urd[numRows-int(r)][int(c)-1] = terminalStates[s]
			Url[numRows-int(r)][int(c)-1] = terminalStates[s]
			Urr[numRows-int(r)][int(c)-1] = terminalStates[s]
		for s in wallList:
			r,c = s.split(",")
			Uwu[numRows-int(r)][int(c)-1] = 0.0
			Uwd[numRows-int(r)][int(c)-1] = 0.0
			Uwl[numRows-int(r)][int(c)-1] = 0.0
			Uwr[numRows-int(r)][int(c)-1] = 0.0
			Uru[numRows-int(r)][int(c)-1] = 0.0
			Urd[numRows-int(r)][int(c)-1] = 0.0
			Url[numRows-int(r)][int(c)-1] = 0.0
			Urr[numRows-int(r)][int(c)-1] = 0.0
		V = numpy.maximum.reduce([Uwu,Uwd,Uwl,Uwr,Uru,Urd,Url,Urr])
		#calculate maximum difference
		Vdiff = abs(V-V0)
		delta = numpy.amax(Vdiff)
		#convergence check
		if delta == 0:
			# -1: None, 0:Walk Up, 1:Walk Down, 2:Walk Left, 3:Walk Right, 
			# 4:Run Up, 5:Run Down, 6:Run Left, 7:Run Right, 8:Exit
			for s in numpy.argwhere((V==Urr) == True):
				state = str(numRows-s[0])+","+str(s[1]+1)
				if state not in terminalStates and state not in wallList:
					BP[s[0]][s[1]] = 7
			for s in numpy.argwhere((V==Url) == True):
				state = str(numRows-s[0])+","+str(s[1]+1)
				if state not in terminalStates and state not in wallList:
					BP[s[0]][s[1]] = 6
			for s in numpy.argwhere((V==Urd) == True):
				state = str(numRows-s[0])+","+str(s[1]+1)
				if state not in terminalStates and state not in wallList:
					BP[s[0]][s[1]] = 5
			for s in numpy.argwhere((V==Uru) == True):
				state = str(numRows-s[0])+","+str(s[1]+1)
				if state not in terminalStates and state not in wallList:
					BP[s[0]][s[1]] = 4
			for s in numpy.argwhere((V==Uwr) == True):
				state = str(numRows-s[0])+","+str(s[1]+1)
				if state not in terminalStates and state not in wallList:
					BP[s[0]][s[1]] = 3
			for s in numpy.argwhere((V==Uwl) == True):
				state = str(numRows-s[0])+","+str(s[1]+1)
				if state not in terminalStates and state not in wallList:
					BP[s[0]][s[1]] = 2
			for s in numpy.argwhere((V==Uwd) == True):
				state = str(numRows-s[0])+","+str(s[1]+1)
				if state not in terminalStates and state not in wallList:
					BP[s[0]][s[1]] = 1
			for s in numpy.argwhere((V==Uwu) == True):
				state = str(numRows-s[0])+","+str(s[1]+1)
				if state not in terminalStates and state not in wallList:
					BP[s[0]][s[1]] = 0
			return BP

#call value iteration
pi = value_iteration()
print "best policy:\n",pi

def output_file():
	f = open("output.txt", "w")
	for i in range(numRows):
		for j in range(numColumns):
			if j == 0:	
				if pi[i][j] == -1:
					f.write("None")
				elif pi[i][j] == 0:
					f.write("Walk Up")
				elif pi[i][j] == 1:
					f.write("Walk Down")
				elif pi[i][j] == 2:
					f.write("Walk Left")
				elif pi[i][j] == 3:
					f.write("Walk Right")
				elif pi[i][j] == 4:
					f.write("Run Up")
				elif pi[i][j] == 5:
					f.write("Run Down")
				elif pi[i][j] == 6:
					f.write("Run Left")
				elif pi[i][j] == 7:
					f.write("Run Right")
				elif pi[i][j] == 8:
					f.write("Exit")									
			else:
				if pi[i][j] == -1:
					f.write(",None")
				elif pi[i][j] == 0:
					f.write(",Walk Up")
				elif pi[i][j] == 1:
					f.write(",Walk Down")
				elif pi[i][j] == 2:
					f.write(",Walk Left")
				elif pi[i][j] == 3:
					f.write(",Walk Right")
				elif pi[i][j] == 4:
					f.write(",Run Up")
				elif pi[i][j] == 5:
					f.write(",Run Down")
				elif pi[i][j] == 6:
					f.write(",Run Left")
				elif pi[i][j] == 7:
					f.write(",Run Right")
				elif pi[i][j] == 8:
					f.write(",Exit")
		f.write("\n")
	f.close()

output_file()
