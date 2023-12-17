import gym
import nle
import utils.utils as utils
import minihack
import class.envClass as envClass
import class.actionClass as actionClass
import numpy as np
import utils.algorithms as algo
import matplotlib.pyplot as plt
import IPython.display as display

#Load Knowledgebase
agentAction = actionClass.AgentAction()

#Generate level
level = envClass.EnvMng()
level.addMonster()
level.addObject()
level.addWeapon()
level.createGame()
level.printEnv()

