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
        return successorGameState.getScore()

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
        def minValue(gameState, depth, agentCounter):
            minimum = ["", float("inf")]
            
            #pos_actions is a list of legal actions for the agent agentCounter in the state gameState
            pos_actions = gameState.getLegalActions(agentCounter)
            
            if not pos_actions:
                return self.evaluationFunction(gameState)
            
            for action in pos_actions:
                #returns the gameState curr_state after the agent agentCounter takes an action 
                curr_state = gameState.generateSuccessor(agentCounter, action)
                
                #returns the value for the next agent, due to the action
                current = minOrMax(curr_state, depth, agentCounter + 1)
                
                #gets the value of the next agent
                if type(current) is not list:
                    newValue = current
                else:
                    newValue = current[1]

                if newValue < minimum[1]:
                    minimum = [action, newValue]
            return minimum

        def maxValue(gameState, depth, agentCounter):
            maximum = ["", -float("inf")]
            #pos_actions is a list of legal actions for the agent agentCounter in the state gameState
            pos_actions = gameState.getLegalActions(agentCounter)

            if not pos_actions:
                return self.evaluationFunction(gameState)

            for action in pos_actions:
                #returns the gameState curr_state after the agent agentCounter takes an action 
                curr_State = gameState.generateSuccessor(agentCounter, action)
                
                #returns the value for the next agent, due to the action
                current = minOrMax(curr_State, depth, agentCounter + 1)
                
                #gets the value of the next agent
                if type(current) is not list:
                    newValue = current
                else:
                    newValue = current[1]
                if newValue > maximum[1]:
                    maximum = [action, newValue]
            return maximum

        def minOrMax(gameState, depth, agentCounter):
            #if agentCounter is bigger than the number of agents in the current gameState,
            #increase the depth with one(adds one agent) and start on agentCounter 0 (pacman)
            if agentCounter >= gameState.getNumAgents():
                depth += 1
                agentCounter = 0

            if (depth == self.depth or gameState.isWin() or gameState.isLose()):
                return self.evaluationFunction(gameState)
            #if one has reached the final layer in the action tree or the game is won/lost
            #-> evaluate
            
            elif (agentCounter == 0):
                return maxValue(gameState, depth, agentCounter)
            else:
                return minValue(gameState, depth, agentCounter)

        actionsList = minOrMax(gameState, 0, 0)
        return actionsList[0]

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        #a and b are the alpha-beta pruning variables
        #a- the value of the best choice we have found so far at the choice point along the path for max
        #b - the value of the best choice we have found so far at the choice point along the path for min
        def minValue(gameState, depth, agentCounter,a,b):
            minimum = ["", float("inf")]
            
            #pos_actions is a list of legal actions for the agent agentCounter in the state gameState
            pos_actions = gameState.getLegalActions(agentCounter)
            
            if not pos_actions:
                return self.evaluationFunction(gameState)
            
            for action in pos_actions:
                #returns the gameState curr_state after the agent agentCounter takes an action 
                curr_state = gameState.generateSuccessor(agentCounter, action)
                
                #returns the value for the next agent, due to the action
                current = minOrMax(curr_state, depth, agentCounter + 1,a,b)
                
                #gets the value of the next agent
                if type(current) is not list:
                    newValue = current
                else:
                    newValue = current[1]

                if newValue < minimum[1]:
                    minimum = [action, newValue]
                    
                if newValue < a: 
                    return [action, newValue]
                #updates the b-value
                b = min(b,newValue)
            return minimum

        def maxValue(gameState, depth, agentCounter, a, b):
            maximum = ["", -float("inf")]
            #pos_actions is a list of legal actions for the agent agentCounter in the state gameState
            pos_actions = gameState.getLegalActions(agentCounter)

            if not pos_actions:
                return self.evaluationFunction(gameState)

            for action in pos_actions:
                #returns the gameState curr_state after the agent agentCounter takes an action 
                curr_State = gameState.generateSuccessor(agentCounter, action)
                
                #returns the value for the next agent, due to the action
                current = minOrMax(curr_State, depth, agentCounter + 1,a,b)
                
                #gets the value of the next agent
                if type(current) is not list:
                    newValue = current
                else:
                    newValue = current[1]
                    
                if newValue > maximum[1]:
                    maximum = [action, newValue]
                if newValue > b:
                    return [action, newValue]
                #updates the a-value
                a = max(a,newValue)
            return maximum

        def minOrMax(gameState, depth, agentCounter, a, b):
            #if agentCounter is bigger than the number of agents in the current gameState,
            #increase the depth with one(adds one agent) and start on agentCounter 0 (pacman)
            if agentCounter >= gameState.getNumAgents():
                depth += 1
                agentCounter = 0

            if (depth == self.depth or gameState.isWin() or gameState.isLose()):
                return self.evaluationFunction(gameState)
            #if one has reached the final layer in the action tree or the game is won/lost
            #-> evaluate
            
            elif (agentCounter == 0):
                return maxValue(gameState, depth, agentCounter,a,b)
            else:
                return minValue(gameState, depth, agentCounter,a,b)

        actionsList = minOrMax(gameState, 0, 0,-float("inf"),float("inf"))
        return actionsList[0]

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

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

