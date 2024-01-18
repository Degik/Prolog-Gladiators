import gym
import nle
import utils.utils as utils
import minihack
import numpy as np
import utils.algorithms as algo
import matplotlib.pyplot as plt
import IPython.display as display

from classAE import envClass
from classAE import actionClass

#Load Knowledgebase
agentAction = actionClass.AgentAction()

#Generate level
level = envClass.EnvMng()
#level.addMonster()
#level.addObject()
#level.addWeapon()
level.createGame()
level.printEnv()

#We can start the agent inside the level generated