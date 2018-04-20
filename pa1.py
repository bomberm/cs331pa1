#! /usr/bin/env python2

from sys import argv

nodesExpanded = 0 
maxDepth = 400 #up here so easy to update

class ShoreState:
		"""
		ShoreState keeps track of the conditions of a single side of the river, namely, number of chickens, number of wolves and boat state.
		"""

		def __init__(self, chickens, wolves, boat):
				self.chx = chickens
				self.wolf = wolves
				self.boat = boat

		def __eq__(self, other):
				return self.chx == other.chx and self.wolf == other.wolf and self.boat == other.boat

		def __str__(self):
				return str(self.chx)+","+str(self.wolf)+","+str(int(self.boat))

		def __hash__(self):
				return hash((self.chx, self.wolf, self.boat))

class RiverState:
		"""
		RiverState extends ShoreState to track both sides of the river.
		"""
		def __init__(self, leftBank, rightBank):
				self.leftBank = leftBank
				self.rightBank = rightBank

		def __eq__(self, other):
				return self.leftBank == other.leftBank and self.rightBank == other.rightBank

		def __str__(self):
				return str(self.leftBank)+"\n"+str(self.rightBank)

		def __hash__(self):
				return hash((self.leftBank, self.rightBank))

		def current(self):
				return([self.leftBank, self.rightBank])
		
		def chickens(self):
				return([self.leftBank.chx, self.rightBank.chx])
		
		def wolves(self):
				return([self.leftBank.wolf, self.rightBank.wolf])

		def boatLocation(self): 
				return self.leftBank.boat

		def toString():
				left = ' ',join(leftBank.chix, leftBank.wolf, int(leftBank.boat))
				right = ' ',join(rightBank.chix, rightBank.wolf, int(rightBank.boat))
				return [left, right]

		def ride(self, move): 
				if self.boatLocation(): #true is left--> right, otherwise right--> left
						left = ShoreState(self.leftBank.chx-move['chx'], self.leftBank.wolf-move['wolf'],False)
						right = ShoreState(self.rightBank.chx+move['chx'], self.rightBank.wolf+move['wolf'],True)

				else:
						left = ShoreState(self.leftBank.chx+move['chx'], self.leftBank.wolf+move['wolf'],True)
						right = ShoreState(self.rightBank.chx-move['chx'], self.rightBank.wolf-move['wolf'],False)

				return(RiverState(left, right))

		def validMove(self, action):
				result = self.ride(action)

				if result.leftBank.chx < 0 or result.leftBank.wolf < 0:
						return False
				
				if result.rightBank.chx < 0 or result.rightBank.wolf < 0:
						return False

				if result.leftBank.chx < result.leftBank.wolf and result.leftBank.chx != 0:
						return False

				if result.rightBank.chx < result.rightBank.wolf and result.rightBank.chx != 0:
						return False

				return True

class Problem:
		def __init__(self, initialRiver, riverGoal, mode):
				self.initial = Node(initialRiver, None, 0)
				self.goal = riverGoal
				self.mode = mode
				
		def expand(self, node):
				testActions = []
				successors = []
				testActions.append({'chx':1, 'wolf':0})
				testActions.append({'chx':2, 'wolf':0})
				testActions.append({'chx':0, 'wolf':1})
				testActions.append({'chx':1, 'wolf':1})
				testActions.append({'chx':0, 'wolf':2})
				for action in testActions:
						if node.state.validMove(action):
								s = Node(node.setState(action), node, node.depth+1) #as each step cost is one, pathCost = depth
								node.children.append(s)
								successors.append(s)
				return successors
						
		def checkGoal(self, node):
				if self.goal == node.state:
						return True
				return False


def astar(frontier):
		lowest = 100000 #for these test cases, effectively infinity
		
		for i in range(0, len(frontier)):
				if frontier[i].fVal < lowest:
						lowest = frontier[i].fVal
						loc = i
		return loc
				
def heuristic(node):
		"""
		The river heuristic is half the state of the right bank + depth. No matter what the input is, the goal is to have the right bank completely empty and sans a boat. This number is halved so it can represent the minimum number of moves required to reach the goal state from the current state. This also is identical to representing (goal - left bank)/2, which was the first planned heuristic. Depth is added to count for g(n)..
		"""
		chx = node.state.chickens()
		wlvs = node.state.wolves()

		right = chx[1]+wlvs[1]
		
		return (right/2)+node.depth

def choose(mode, frontier, depth):
		if mode == "bfs":
				return 0
		if mode == "dfs":
				return (-1)
		if mode == "iddfs":
				for i in range(0, len(frontier)):
						if frontier[i].depth == depth:
								return i
				return None
		
def graphSearch(problem):
		frontier = [problem.initial]
		explored = set()
		depth=0
		global maxDepth

		while True:
				if not frontier:
						return False
				if problem.mode == "astar":
						leafIndex = astar(frontier)
				else:
						leafIndex = choose(problem.mode, frontier, depth)
				while leafIndex == None: #increasing depth
						depth += 1
						if depth == maxDepth:
								return False 
						leafIndex = choose(problem.mode, frontier, depth)
				leaf = frontier.pop(leafIndex)
				if problem.checkGoal(leaf):
						return leaf
				explored.add(leaf)
				for result in problem.expand(leaf):
						global nodesExpanded
						nodesExpanded += 1
						if result not in frontier and result not in explored:
								frontier.append(result)	

class Node:
		def __init__(self, river, parent, depth):
				self.state = river
				self.parent = parent
				self.children = []
				self.depth = depth
				self.fVal = heuristic(self)

		def __eq__(self, other):
				if type(other) != type(self):
						return False
				return self.state == other.state

		def __hash__(self):
				return hash(self.state)

		def addPath(self, river):
				self.children += river

		def removePath(self, location):
				return self.children.pop(location)

		def chickens():
				return self.state.chickens()

		def wolves():
				return self.state.wolves()

		def setState(self, action):
				return (self.state.ride(action))

def setBank(inputFile):
				state = inputFile.readline()
				state = state.split(',')
				return ShoreState(int(state[0]), int(state[1]), True if state[2].strip() == '1' else False)

def main():
		usage = """pa1.py < initial state file > < goal state file > < mode > < output file >"""			
		if len(argv) < 4:
				print usage
				exit(-1)
		
		mode = argv[3]
		with open(argv[1], 'r') as state:
				leftBank = setBank(state)
				rightBank = setBank(state)

		river = RiverState(leftBank, rightBank)

		with open(argv[2], 'r') as goal:
				leftBank = setBank(goal)
				rightBank = setBank(goal)

		rivergoal = RiverState(leftBank, rightBank)

		problem = Problem(river, rivergoal, mode)
		solution = graphSearch(problem)

		with open(argv[4], 'w+') as f:
				f.write("nodes expanded: "+str(nodesExpanded)+'\n')
				if solution == False:
						f.write("no solution found\n")

				else:
						f.write("nodes in solution: "+str(solution.depth)+"\n")
						solPath = []

						while not solution == None:
								solPath.insert(0, solution.state)
								solution = solution.parent
		
						for state in solPath:
								f.write(str(state)+"\n\n")
		
if __name__ == "__main__":
		main()		
