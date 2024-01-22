import gym
import nle
import utils.utils as utils
import minihack
import numpy as np
import utils.algorithms as algo
import matplotlib.pyplot as plt
import IPython.display as display

from pyswip import Prolog
from classAE import envClass, actionClass
from utils import algorithms as algo

def createGame():
    desFile = envClass.createLevel()
    env = gym.make("MiniHack-Skill-Custom-v0", observation_keys = ("chars", "pixel_crop", "pixel"), des_file=desFile)
    state = env.reset()
    env.render
    game_map = state["chars"]
    game = state["pixel"]
    return env, state, game_map, game

def printMap(env, state):
    env.render()
    plt.figure()
    plt.imshow(state["pixel"][25:350, 475:825])
    plt.figure()
    plt.imshow(state["pixel_crop"])