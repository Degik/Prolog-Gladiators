import gym
import nle
import time
import utils.utils as utils
import minihack
import numpy as np
import utils.algorithms as algo
import matplotlib.pyplot as plt

from IPython import display
from classAE import envClass
from classAE import actionClass
##
#SEED
seed = 40

#Load Knowledgebase
agentAction = actionClass.AgentAction()

#Generate level
level = envClass.EnvMng()
#level.addMonster()
#level.addObject()
level.addWeapon()
level.generateObjects(seed)
#level.generateMonsters(seed)
env, state, game_map, game = level.createGame()
level.printEnv()
#
#level.printDisplay()
agentAction.initActionStatus(game_map)
agentAction.startSearchWeapon(env, game, game_map)