# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
	"""
	  A reflex agent chooses an action at each choice point by examining
	  its alternatives via a state evaluation function.

	  The code below is provided as a guide.  You are welcome to change
	  it in any way you see fit, so long as you don't touch our method
	  headers.
	"""


	def getAction(self, gameState):
		"""
		You do not need to change this method, but you're welcome to.

		getAction chooses among the best options according to the evaluation function.

		Just like in the previous project, getAction takes a GameState and returns
		some Directions.X for some X in the set {North, South, West, East, Stop}
		"""
		# Collect legal moves and successor states
		legalMoves = gameState.getLegalActions()

		# Choose one of the best actions
		scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
		bestScore = max(scores)
		bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
		chosenIndex = random.choice(bestIndices) # Pick randomly among the best

		"Add more of your code here if you want to"

		return legalMoves[chosenIndex]

	def evaluationFunction(self, currentGameState, action):
		"""
		Design a better evaluation function here.

		The evaluation function takes in the current and proposed successor
		GameStates (pacman.py) and returns a number, where higher numbers are better.

		The code below extracts some useful information from the state, like the
		remaining food (newFood) and Pacman position after moving (newPos).
		newScaredTimes holds the number of moves that each ghost will remain
		scared because of Pacman having eaten a power pellet.

		Print out these variables to see what you're getting, then combine them
		to create a masterful evaluation function.
		"""
		# Useful information you can extract from a GameState (pacman.py)
		successorGameState = currentGameState.generatePacmanSuccessor(action)
		newPos = successorGameState.getPacmanPosition()
		newFood = successorGameState.getFood()
		newGhostStates = successorGameState.getGhostStates()
		newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

		"*** YOUR CODE HERE ***"
		measure = 999999

		numFood = successorGameState.getNumFood()
		newCapsules = successorGameState.getCapsules()
		numCapsules = len(newCapsules)

		if numFood > 0:
			nearestFood_dist = newFood.width+newFood.height
			for x in range(newFood.width):
				for y in range(newFood.height):
					if newFood[x][y]:
						nearestFood_dist = min(manhattanDistance(newPos,(x,y)),nearestFood_dist)
			measure -= nearestFood_dist

		measure -= numCapsules*100
		measure -= numFood*10
		measure += successorGameState.getScore()

		for ghostState in newGhostStates:
			ghostpos = ghostState.configuration.getPosition()
			if ghostState.scaredTimer < 1:
				ghostdist = manhattanDistance(newPos,ghostpos)
				if ghostdist < 3:
					return ghostdist

		return measure

def scoreEvaluationFunction(currentGameState):
	"""
	  This default evaluation function just returns the score of the state.
	  The score is the same one displayed in the Pacman GUI.

	  This evaluation function is meant for use with adversarial search agents
	  (not reflex agents).
	"""
	return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
	"""
	  This class provides some common elements to all of your
	  multi-agent searchers.  Any methods defined here will be available
	  to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

	  You *do not* need to make any changes here, but you can if you want to
	  add functionality to all your adversarial search agents.  Please do not
	  remove anything, however.

	  Note: this is an abstract class: one that should not be instantiated.  It's
	  only partially specified, and designed to be extended.  Agent (game.py)
	  is another abstract class.
	"""

	def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
		self.index = 0 # Pacman is always agent index 0
		self.evaluationFunction = util.lookup(evalFn, globals())
		self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
	"""
	  Your minimax agent (question 2)
	"""

	def getAction(self, gameState):
		"""
		  Returns the minimax action from the current gameState using self.depth
		  and self.evaluationFunction.

		  Here are some method calls that might be useful when implementing minimax.

		  gameState.getLegalActions(agentIndex):
			Returns a list of legal actions for an agent
			agentIndex=0 means Pacman, ghosts are >= 1

		  gameState.generateSuccessor(agentIndex, action):
			Returns the successor game state after an agent takes an action

		  gameState.getNumAgents():
			Returns the total number of agents in the game
		"""
		"*** YOUR CODE HERE ***"
		self.num_agents = gameState.getNumAgents()
		all_actions_root = gameState.getLegalActions(0)
		utility_score = -float("inf")
		opt_action = 0
		for action in all_actions_root:
			if action != Directions.STOP:
				next_state_root = gameState.generateSuccessor(0,action)
				curr_score_root = self.min_value(next_state_root,1,0)
				if curr_score_root > utility_score:
					utility_score = curr_score_root
					opt_action = action

		return opt_action

	def max_value(self, state, player, curr_depth):
		if state.isWin() or state.isLose() or curr_depth == self.depth:
			return self.evaluationFunction(state)
		else:
			curr_utility = -float("inf")
			all_actions = state.getLegalActions(player)
			for action in all_actions:
				if action != Directions.STOP:
					next_state = state.generateSuccessor(player, action)
					curr_score = self.min_value(next_state,player+1,curr_depth)
					curr_utility = max(curr_score,curr_utility)

			return curr_utility


	def min_value(self, state, player, curr_depth):
		curr_utility = float("inf")
		if state.isWin() or state.isLose() or curr_depth == self.depth:
			return self.evaluationFunction(state)
		if (player+1)%self.num_agents == 0:
			all_actions = state.getLegalActions(player)
			for action in all_actions:
				if action != Directions.STOP:
					next_state = state.generateSuccessor(player, action)
					curr_score = self.max_value(next_state,0,curr_depth+1)
					curr_utility = min(curr_score,curr_utility)
			return curr_utility
		else:
			all_actions = state.getLegalActions(player)
			for action in all_actions:
				if action != Directions.STOP:
					next_state = state.generateSuccessor(player, action)
					curr_score = self.min_value(next_state,player+1,curr_depth)
					curr_utility = min(curr_score,curr_utility)
			return curr_utility

class AlphaBetaAgent(MultiAgentSearchAgent):
	"""
	  Your minimax agent with alpha-beta pruning (question 3)
	"""

	def getAction(self, gameState):
		"""
		  Returns the minimax action using self.depth and self.evaluationFunction
		"""
		"*** YOUR CODE HERE ***"
		self.num_agents = gameState.getNumAgents()
		all_actions_root = gameState.getLegalActions(0)
		utility_score = -float("inf")
		opt_action = 0
		alpha = -float("inf")
		beta = float("inf")
		for action in all_actions_root:
			if action != Directions.STOP:
				next_state_root = gameState.generateSuccessor(0,action)
				curr_score_root = self.min_value(next_state_root,1,0, alpha, beta)
				if curr_score_root > utility_score:
					utility_score = curr_score_root
					opt_action = action
				if utility_score > beta:
						return action
				alpha = max(alpha,utility_score)

		return opt_action

	def max_value(self, state, player, curr_depth, alpha, beta):
		if state.isWin() or state.isLose() or curr_depth == self.depth:
			return self.evaluationFunction(state)
		else:
			curr_utility = -float("inf")
			all_actions = state.getLegalActions(player)
			for action in all_actions:
				if action != Directions.STOP:
					next_state = state.generateSuccessor(player, action)
					curr_score = self.min_value(next_state,player+1,curr_depth, alpha, beta)
					curr_utility = max(curr_score,curr_utility)
					if curr_utility > beta:
						return curr_utility
					alpha = max(alpha,curr_utility)
			return curr_utility


	def min_value(self, state, player, curr_depth, alpha, beta):
		curr_utility = float("inf")
		if state.isWin() or state.isLose() or curr_depth == self.depth:
			return self.evaluationFunction(state)
		if (player+1)%self.num_agents == 0:
			all_actions = state.getLegalActions(player)
			for action in all_actions:
				if action != Directions.STOP:
					next_state = state.generateSuccessor(player, action)
					curr_score = self.max_value(next_state,0,curr_depth+1, alpha, beta)
					curr_utility = min(curr_score,curr_utility)
					if curr_utility < alpha:
						return curr_utility
					beta = min(beta,curr_utility)
			return curr_utility
		else:
			all_actions = state.getLegalActions(player)
			for action in all_actions:
				if action != Directions.STOP:
					next_state = state.generateSuccessor(player, action)
					curr_score = self.min_value(next_state,player+1,curr_depth, alpha, beta)
					curr_utility = min(curr_score,curr_utility)
					if curr_utility < alpha:
						return curr_utility
					beta = min(beta,curr_utility)
			return curr_utility


def betterEvaluationFunction(currentGameState):
	"""
	  Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
	  evaluation function (question 5).

	  DESCRIPTION: 
	  So, the measure I used takes into account the following things:
	  1. Number of food particles left on the map
	  2. Number of capsules left on the map
	  3. Distance of the nearest food particle. Note that this is taken into 
	  	 account only if there is atleast one food particle on the map
	  4. The game score
	  5. Checking if any ghost is dangerously close enough
	  6. The distances of the ghosts from pacman
	  So , if a ghost is at the same state as pacman(which means pacman will die), then the measure returned 
	  is very low, infact, it is zero. This ensures that such a state is avoided at all costs as then it is the worst state
	  Then all I did was put in weights for each of the factors mentioned above 
	  and kept adjusting the weights till I got the best result according to my constraints
	"""
	"*** YOUR CODE HERE ***"
	newPos = currentGameState.getPacmanPosition()
	newFood = currentGameState.getFood()
	newGhostStates = currentGameState.getGhostStates()
	newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

	measure = 99999

	numFood = currentGameState.getNumFood()
	newCapsules = currentGameState.getCapsules()
	numCapsules = len(newCapsules)

	if numFood > 0:
		nearestFood_dist = newFood.width+newFood.height
		for x in range(newFood.width):
			for y in range(newFood.height):
				if newFood[x][y]:
					nearestFood_dist = min(manhattanDistance(newPos,(x,y)),nearestFood_dist)
		measure -= nearestFood_dist

	measure -= numCapsules*100
	measure -= numFood*10
	measure += currentGameState.getScore()

	for ghostState in newGhostStates:
		ghostpos = ghostState.configuration.getPosition()
		if ghostState.scaredTimer < 1:
			ghostdist = manhattanDistance(newPos,ghostpos)
			if ghostdist < 1:
				return ghostdist
			else:
				measure += ghostdist

	return measure

# Abbreviation
better = betterEvaluationFunction

