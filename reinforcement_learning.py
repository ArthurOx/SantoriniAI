# from learning_agent import ReinforcementAgent
from agent import Agent
import random, util, math, mdp, time
import numpy as np
from board import *
from player import Player
import environment
import heuristics
from learning_agent import ReinforcementAgent

FIRST_PLAYER = 1
SECOND_PLAYER = 2
BOARD_SIZE = 5

SETUP = 0
MOVE = 1
BUILD = 2


class QLearningAgent(ReinforcementAgent):
    def __init__(self, epsilon=0.05, gamma=0.8, alpha=0.2, numTraining=0):
        super().__init__()
        # self.player = player
        self.epsilon = epsilon
        self.gamma = gamma
        self.alpha = alpha
        self.numTraining = numTraining
        self.index = 0
        ReinforcementAgent.__init__(self)
        self.QValue_player_1 = util.Counter()
        self.QValue_player_2 = util.Counter()

    def getQValue(self, state, action, player):
        if player == FIRST_PLAYER:
            if (state, action) in self.QValue_player_1:
                return self.QValue_player_1[(state, action)]
        elif player == SECOND_PLAYER:
            if (state, action) in self.QValue_player_2:
                return self.QValue_player_2[(state, action)]
        return 0.0

    def setQValue(self, state, action, value, player):
        if player == FIRST_PLAYER:
            self.QValue_player_1[(state, action)] = value
        else:
            self.QValue_player_2[(state, action)] = value

    def getValue(self, state, player):
        if not self.getLegalActions(state, player):
            return 0.0
        max_value = -np.inf
        for action in self.getLegalActions(state, player):
            value = self.getQValue(state, action, player)
            if value > max_value:
                max_value = value
        return max_value

    def getPolicy(self, state, player):
        # returns the best action
        if not self.getLegalActions(state, player):
            return 0.0
        max_value = -np.inf
        max_action = None
        for action in self.getLegalActions(state, player):
            value = self.getQValue(state, action, player)
            if value > max_value:
                max_value = value
                max_action = action
            elif value == max_value:
                max_action = random.choice([max_action, action])
        return max_action

    def get_action(self, state, player):
        legalActions = self.getLegalActions(state, player)
        action = None
        if legalActions:
            if util.flipCoin(self.epsilon):
                # probability epsilon, take action
                action = random.choice(legalActions)
            else:
                # probability 1-epsilon, take best policy action
                action = self.getPolicy(state, player)
        return action

    def update(self, state, action, nextState, reward, player):
        if player == FIRST_PLAYER:
            self.QValue_player_1[(state, action)] += self.alpha * (
                        reward + self.discount * self.getValue(nextState, player) - self.getQValue(state, action,
                                                                                                   player))
        else:
            self.QValue_player_2[(state, action)] += self.alpha * (
                        reward + self.discount * self.getValue(nextState, player) - self.getQValue(state, action,
                                                                                                   player))

    def __str__(self):
        return "Q Learning Agent"


class SantoriniEnvironment(environment.Environment):  # todo 怎么运行
    def __init__(self, evaluation_function):
        # super().__init__(evaluation_function)
        self.evaluation_function = evaluation_function
        self.state = None
        self.player = None
        self.enemy = None

    def getCurrentState(self):
        return self.state

    def getPossibleActions(self, state):
        return Board.get_legal_moves(state, self.player)

    #原来的逻辑： 定义next state和reward=None，找到原来的坐标，根据每个不同的动作更新next state，
    #然后算出reward，并且更新state

    #网上逻辑： do move，定义reward，检查有没有结束
    #while圈检查玩家是不是2

    def doAction(self, action):
        reward, next_state = -np.inf, None
        successors = Board.get_legal_moves(self.state, self.player)
        for succ in successors:
            score = self.evaluation_function(succ, self.player, self.enemy)
            if score > reward:
                reward = score
                next_state = succ
        self.state = next_state
        return next_state, reward

    def reset(self):
        """
         Resets the Environment to the initial state
        """
        Board.clear(self.state)

