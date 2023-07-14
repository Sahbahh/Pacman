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

        # Calculate the distance to the closest food
        food_list = successorGameState.getFood().asList()
        min_food_distance = float('inf')
        for food in food_list:
            distance = util.manhattanDistance(newPos, food)
            if distance < min_food_distance:
                min_food_distance = distance

        # Avoid ghosts that are too close
        for ghostState in newGhostStates:
            ghost_pos = ghostState.getPosition()
            ghost_distance = util.manhattanDistance(newPos, ghost_pos)
            if ghost_distance < 2:
                return -float('inf')

        # Calculate the reciprocal of the minimum food distance
        reciprocal_min_food_distance = 1.0 / min_food_distance if min_food_distance > 0 else float('inf')

        # Return the sum of the current score and reciprocal of the minimum food distance
        return successorGameState.getScore() + reciprocal_min_food_distance
    
        #return successorGameState.getScore()

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
        #util.raiseNotDefined()

        def minimax(state,depth,agent):
            # if all agents have been evaluated or max depth is reached, return the evaluation of the state
            if agent == state.getNumAgents():
                if depth == self.depth:
                    return self.evaluationFunction(state)
                else:
                    return minimax(state, depth + 1, 0)
            
            # for Pacman or ghost agents, find the best successor state by recursively calling minimax function
            else:
                if state.getLegalActions(agent):
                    successor = (minimax(state.generateSuccessor(agent, action), depth, agent + 1) for action in state.getLegalActions(agent))
                else:
                    return self.evaluationFunction(state)
            
            # for Pacman agents, return the max value among the successor states
            if agent == 0:
                return max(successor)
            
            # for ghost agents, return the min value among the successor states
            else:
                return min(successor)

        # find the best action for Pacman by calling minimax function for each legal action and selecting the action with max value
        action = max(gameState.getLegalActions(0), key=lambda x: minimax(gameState.generateSuccessor(0, x), 1, 1))
        return action



class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        #util.raiseNotDefined()
        
        # Initialize alpha-beta values and best action
        alpha = float("-inf")
        beta = float("inf")
        best_action = None
        best_score = float("-inf")

        # Loop over legal actions for the pacman agent
        for action in gameState.getLegalActions(0):
            # Generate the successor state for the given action
            successor = gameState.generateSuccessor(0, action)
            # Calculate the score for the successor state
            score = self.min_value(successor, 1, self.depth, alpha, beta)

            # Update best action and score
            if score > best_score:
                best_score = score
                best_action = action

            # Update alpha value
            alpha = max(alpha, best_score)

        # Return the best action
        return best_action

    def max_value(self, gameState, agent_index, depth, alpha, beta):
        # Base cases
        if gameState.isWin() or gameState.isLose() or depth == 0:
            return self.evaluationFunction(gameState)

        # Initialize the value v to negative infinity
        v = float("-inf")

        # Loop over legal actions for the agent
        for action in gameState.getLegalActions(agent_index):
            # Generate the successor state for the given action
            successor = gameState.generateSuccessor(agent_index, action)
            # Calculate the max value for the successor state
            v = max(v, self.min_value(successor, agent_index + 1, depth, alpha, beta))
            # Prune if v is greater than beta
            if v > beta:
                return v
            # Update alpha value
            alpha = max(alpha, v)

        # Return the max value v
        return v

    def min_value(self, gameState, agent_index, depth, alpha, beta):
        # Base cases
        if gameState.isWin() or gameState.isLose() or depth == 0:
            return self.evaluationFunction(gameState)

        # Initialize the value v to positive infinity
        v = float("inf")

        # Loop over legal actions for the agent
        for action in gameState.getLegalActions(agent_index):
            # Generate the successor state for the given action
            successor = gameState.generateSuccessor(agent_index, action)
            # Calculate the min value for the successor state
            if agent_index == gameState.getNumAgents() - 1:
                v = min(v, self.max_value(successor, 0, depth - 1, alpha, beta))
            else:
                v = min(v, self.min_value(successor, agent_index + 1, depth, alpha, beta))
            # Prune if v is less than alpha
            if v < alpha:
                return v
            # Update beta value
            beta = min(beta, v)

        # Return the min value v
        return v

        
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
        #util.raiseNotDefined()
        
        def max_value(gameState, depth):
            # Check if the game state is terminal or the depth is reached.
            if depth == self.depth or gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState), None

            v = float('-inf')  # initialize the value of v to negative infinity
            goAction = None    # initialize the best action to None

            # loop through all possible actions of the Pacman agent and find the maximum value
            for action in gameState.getLegalActions(0):
                successorValue = exp_value(gameState.generateSuccessor(0, action), 1, depth)[0]
                # update v and best action
                if successorValue > v:
                    v, goAction = successorValue, action

            return v, goAction

        "Expectimax value function"
        def exp_value(gameState, agentID, depth):
            # Check if the game state is terminal.
            if gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState), None

            actionList = gameState.getLegalActions(agentID)

            # if the agent is a ghost, calculate expected value based on probability distribution
            if agentID != 0:
                expectedValue = 0
                for action in actionList:
                    if agentID == gameState.getNumAgents() - 1:
                        successorValue = max_value(gameState.generateSuccessor(agentID, action), depth + 1)[0]
                    else:
                        successorValue = exp_value(gameState.generateSuccessor(agentID, action), agentID + 1, depth)[0]
                    expectedValue += successorValue / len(actionList)
                return expectedValue, None

            # if the agent is Pacman, call max_value
            else:
                return max_value(gameState, depth)

        # Call max_value for Pacman agent and return the best action
        return max_value(gameState, 0)[1]
        

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    #util.raiseNotDefined()

    # Get current position of Pacman and all remaining food pellets
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood().asList()

    # Compute minimum distance to remaining food pellets
    minFoodist = float('inf')
    for food in newFood:
        minFoodist = min(minFoodist, manhattanDistance(newPos, food))

    # Compute distance to each ghost, return negative infinity if Pacman is within 2 units of a ghost
    ghostDist = 0
    for ghost in currentGameState.getGhostPositions():
        ghostDist = manhattanDistance(newPos, ghost)
        if (ghostDist < 2):
            return -float('inf')

    # Get number of remaining food pellets and power capsules
    foodLeft = currentGameState.getNumFood()
    capsLeft = len(currentGameState.getCapsules())

    # Set weights for different factors in evaluation function
    foodLeftMultiplier = 90000
    capsLeftMultiplier = 10000
    foodDistMultiplier = 900
    capsuleDistMultiplier = 200

    # Compute additional factors (if game is won or lost)
    additionalFactors = 0
    if currentGameState.isLose():
        additionalFactors -= 10000
    elif currentGameState.isWin():
        additionalFactors += 10000

    # Compute distance to closest power capsule
    capsuleDist = 0
    if capsLeft > 0:
        capsules = currentGameState.getCapsules()
        minCapsDist = float('inf')
        for capsule in capsules:
            dist = manhattanDistance(newPos, capsule)
            if dist < minCapsDist:
                minCapsDist = dist
        capsuleDist = 1.0 / (minCapsDist + 1) * capsuleDistMultiplier

    # Compute overall evaluation function by weighting each factor
    return 1.0 / (foodLeft + 1) * foodLeftMultiplier + ghostDist + \
           1.0 / (minFoodist + 1) * foodDistMultiplier + \
           1.0 / (capsLeft + 1) * capsLeftMultiplier + \
           capsuleDist + additionalFactors

# Abbreviation
better = betterEvaluationFunction
