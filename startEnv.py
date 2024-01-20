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

def startSearchWeapong(env, game_map, actionMap:actionClass.AgentAction):
    player = utils.get_player_location(game_map)
    weapon = utils.get_target_location(game_map, ")")
    path = algo.a_star(game_map, player, weapon)
    actions_move = utils.actions_from_path(player, path[1:])
    for move in actions_move():
        env.step(move)
        player = utils.get_player_location(game_map) #Take new player pos
        actionMap.setAgentPosition(player[0], player[1])#Update player pos
    #env.step("5") # pick_up action
    queryResult = list(prolog.query("action(Action)"))
    if queryResult:
        action = queryResult[0]["Action"]
        
        
    prolog.retractall("wields_weapon(agent, tsurugi)")
    

#Prima di cercare un nemico bisogna verificare che sia disponibile un'arma
def startSearchMonsters(env, game_map, prolog):
    # Dare la lista dei simboli presenti in gioco, se un simbolo non è presente, si passa al successivo
    # Lista simboli
    #Monsters
    MonstersSymbolList = ["a", "o", "s", "D"]
    #Objects
    ObjectSymbolList = ["%", "$"]
    #Move to enemy
    #Cycle every monster symbol
    for monsterSymbol in MonstersSymbolList:
        #Take new player position
        player = utils.get_player_location(game_map)
        #Take target position
        target = utils.get_target_location(game_map, monsterSymbol)
        print("Monster found!")
        #Search path with A*
        path = algo.a_star(game_map, player, target)
        #Convert the path in action for move
        actions_move = utils.actions_from_path(player, path[1:])
        #Move to the monster
        for move in actions_move:
            env.step(move)
            prolog.assertz(f"agent({player[0]},{player[1]})")
            prolog.assertz(f"apple({target[0]},{target[1]})")
        #Try to attack the enemy
        
        
    
    #prolog.assertz(f"agent({player[0]},{player[1]})")
    #prolog.assertz(f"apple({target[0]},{target[1]})")
    print(f"agent({player[0]},{player[1]})")
    print(f"apple({target[0]},{target[1]})")

    queryResult = list(prolog.query("action(Action)"))
    if queryResult:
        nextMove = queryResult[0]["Action"]
        #stepAction = performAction(nextMove)
        return env.step(stepAction)
    else:
        print("Nessuna azione trovata")
        return None