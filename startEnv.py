import gym
import nle
import utils.utils as utils
import minihack
import numpy as np
import utils.algorithms as algo
import matplotlib.pyplot as plt
import IPython.display as display

from pyswip import Prolog
from class.envClass import createLevel
    
def loadLogic():
    prolog = Prolog()
    try:
        prolog.consult('actionLogic.pl')  # No need to use join, just pass the file name directly
    except Exception as e:
        print(f"Error: {e}")
    return prolog

def createGame():
    desFile = createLevel()
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
    
def performAction(nextMove):
    #
    if nextMove == "move_north":
        return 0
    elif nextMove == "move_est":
        return 1
    elif nextMove == "move_south":
        return 2
    elif nextMove == "move_ovest":
        return 3
    
    
def startSearch(env, game_map, prolog):
    prolog.retractall("agent(_,_)")
    prolog.retractall("apple(_,_)")
    player = utils.get_player_location(game_map)
    try:
        target = utils.get_target_location(game_map)
    except Exception as e:
        print("Simbolo @ mancante")
        return None
    
    prolog.assertz(f"agent({player[0]},{player[1]})")
    prolog.assertz(f"apple({target[0]},{target[1]})")
    print(f"agent({player[0]},{player[1]})")
    print(f"apple({target[0]},{target[1]})")

    queryResult = list(prolog.query("action(Action)"))
    if queryResult:
        nextMove = queryResult[0]["Action"]
        stepAction = performAction(nextMove)
        return env.step(stepAction)
    else:
        print("Nessuna azione trovata")
        return None