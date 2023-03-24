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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        #change chosenIndex? 


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
        #print(successorGameState)
        #print(newPos) - returns x and y coordinates of pacman in form (a,b)
        #print (newFood.asList()) -returns list of x and y coordinates of food pellets remaining in form [(a,b), (c,d), ...]

        score = successorGameState.getScore() / 10 

       #manhattan distance between pacman agent and the nearest food (the closer, the better it is)
      
        listOfFoods = newFood.asList()
        #successor pacman distance to foods
        distanceToFoods = []
        for foodPos in listOfFoods:
            distanceToFoods.append(manhattanDistance(newPos, foodPos)) #find min in list and compare to smallest one fro
        
        #current pacman distance to foods
        currFoodDists = [] 
        for foodPos in listOfFoods:
            currFoodDists.append(manhattanDistance(currentGameState.getPacmanPosition(), foodPos))


        if len(distanceToFoods) > 0 and len(currFoodDists) > 0:
            if min(distanceToFoods) < min(currFoodDists): #if closer to food, then its good
             score += 1

       
       #calculate distance between pacman agent and the ghost (the further, the better it is)

        succ_ghost_distances = []
        curr_ghost_distances = []


        for ghost in successorGameState.getGhostPositions():
            succ_ghost_distances.append(manhattanDistance(ghost,newPos))

        for ghost in currentGameState.getGhostPositions(): 
             curr_ghost_distances.append(manhattanDistance(ghost, currentGameState.getPacmanPosition()))
        

        if len(succ_ghost_distances) > 0 and len(curr_ghost_distances) > 0:
            #if ghosts are scared lesser distance to ghosts is better
            if(sum(newScaredTimes) > 0): 
                 if min(succ_ghost_distances) < min(curr_ghost_distances): #if closer to ghost then its good
                  score += 1

            #if ghosts are not scared then greater distance to ghosts is better 
            else: 
                if min(succ_ghost_distances) < min(curr_ghost_distances): #if closer to ghost then its bad
                  score -= 1
             
        #if pacman in same position as ghost, set it to negative infinity 
        for ghost in newGhostStates:
            if ghost.getPosition() == newPos: 
                score = float('-inf')

        return score

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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
       # util.raiseNotDefined()

        numGhosts = gameState.getNumAgents() -1

        #for GHOSTS (agentIndex >= 1)
        def minState(gameState, depth, agentIndex): #dont have to keep track of depth
            #check all of the ghost indexes

            minVal = 9999
            if gameState.isWin() or gameState.isLose(): 
                return self.evaluationFunction(gameState)
            for action in gameState.getLegalActions(agentIndex):  #legal actions for pacman
                successorGameState = gameState.generateSuccessor(agentIndex, action) 
                if agentIndex == numGhosts: #agentindex is the last one 
                    minVal = min(minVal, maxState(successorGameState, depth))
                else:
                    minVal = min(minVal, minState(successorGameState, depth, agentIndex+ 1))

            return minVal


        #for PACMAN (agentIndex = 0)
        def maxState(gameState, depth): #agentindex will always be zero so no need for agentindex
            #check depth 
             currDepth = depth + 1
             #base case
             if gameState.isWin() or gameState.isLose() or currDepth==self.depth: 
                return self.evaluationFunction(gameState)
             maxVal = -99999
             for action in gameState.getLegalActions(0):  #legal actions for pacman
                successorGameState = gameState.generateSuccessor(0, action)
                maxVal = max(maxVal, minState(successorGameState, currDepth, 1))
             return maxVal

       #getAction code 
        legalActions = gameState.getLegalActions(0) 
        bestScore = -9999
        bestAction = ''
        for action in legalActions:
            #find the next state
            nextGameState = gameState.generateSuccessor(0, action)
            currScore = minState(nextGameState, 0, 1) 
            if currScore > bestScore:
                bestScore = currScore
                bestAction = action
        return bestAction


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()
        numGhosts = gameState.getNumAgents() -1
        #for GHOSTS (agentIndex >= 1) 
        # 
        # --TO DO: UPDATE WITH ALPHA BETA STUFF 

        def minState(gameState, depth, agentIndex, alpha, beta): #dont have to keep track of depth
            #check all of the ghost indexes

            minVal = 9999
            if gameState.isWin() or gameState.isLose(): 
                return self.evaluationFunction(gameState)
            for action in gameState.getLegalActions(agentIndex):  #legal actions for pacman
                successorGameState = gameState.generateSuccessor(agentIndex, action) 
                if agentIndex == numGhosts: #agentindex is the last one 
                    minVal = min(minVal, maxState(successorGameState, depth))
                else:
                    minVal = min(minVal, minState(successorGameState, depth, agentIndex+ 1))

            return minVal


        #for PACMAN (agentIndex = 0) 

        # ---TO DO: UPDATE WITH ALPHA BETA STUFF 


        def maxState(gameState, depth, alpha, beta): #agentindex will always be zero so no need for agentindex
            #check depth 
             currDepth = depth + 1
             #base case
             if gameState.isWin() or gameState.isLose() or currDepth==self.depth: 
                return self.evaluationFunction(gameState)
             maxVal = -99999
             for action in gameState.getLegalActions(0):  #legal actions for pacman
                successorGameState = gameState.generateSuccessor(0, action)
                maxVal = max(maxVal, minState(successorGameState, currDepth, 1))
             return maxVal

       #getAction code (root) -- DONE
        alphaVal = -9999
        betaVal = 9999

        legalActions = gameState.getLegalActions(0) 
        bestScore = -9999
        bestAction = ''
        
        for action in legalActions:
            #find the next state
            nextGameState = gameState.generateSuccessor(0, action)
            currScore = minState(nextGameState, 0, 1, alphaVal, betaVal) 
            if currScore > bestScore:
                bestScore = currScore
                bestAction = action

            if currScore > betaVal: 
                return bestAction
                
        alphaVal = max(alphaVal, currScore)
        return bestAction



class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        numGhosts = gameState.getNumAgents() -1

        #for GHOSTS (agentIndex >= 1)
        def expectiMax(gameState, depth, agentIndex): #dont have to keep track of depth
            #check all of the ghost indexes
            curVal = 0
            exVal = 0
            if gameState.isWin() or gameState.isLose(): 
                return self.evaluationFunction(gameState)
            
            numberofactions = 0
            for action in gameState.getLegalActions(agentIndex):  #legal actions for pacman
                numberofactions = numberofactions+1
                successorGameState = gameState.generateSuccessor(agentIndex, action) 
                if agentIndex == numGhosts: #agentindex is the last one 
                    curVal = maxState(successorGameState, depth)
                else:
                    curVal = expectiMax(successorGameState, depth, agentIndex + 1)
                exVal += curVal
            
            return exVal/numberofactions


        def maxState(gameState, depth): #agentindex will always be zero so no need for agentindex
             currDepth = depth + 1
             #base case
             if gameState.isWin() or gameState.isLose() or currDepth==self.depth: 
                return self.evaluationFunction(gameState)
             maxVal = -99999
             for action in gameState.getLegalActions(0):  #legal actions for pacman
                successorGameState = gameState.generateSuccessor(0, action)
                maxVal = max(maxVal, expectiMax(successorGameState, currDepth, 1))
             return maxVal

       #getAction code 
        legalActions = gameState.getLegalActions(0) 
        bestScore = -9999
        bestAction = ''
        for action in legalActions:
            #find the next state
            nextGameState = gameState.generateSuccessor(0, action)
            currScore = expectiMax(nextGameState, 0, 1) 
            if currScore > bestScore:
                bestScore = currScore
                bestAction = action
        return bestAction

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
