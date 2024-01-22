import time
import numpy as np
import utils.utils as utils
import utils.algorithms as algo
import matplotlib.pyplot as plt

from pyswip import Prolog
import IPython.display as display

class AgentAction:
    def __init__(self):
        self.kb = Prolog()
        self.kb.consult('kb/kb.pl')

        self.actionIdMap = {
            "move_north": 0,
            "move_est": 1,
            "move_south": 2,
            "move_ovest": 3,
            "attack": 4,
            "pick_up": 5,
            "drop": 6,
            "use": 7,
            "talk_to": 8,
            "open": 9,
            "close": 10,
            "unlock": 11,
            "lock": 12,
            "read": 13,
            "write": 14,
            "enter": 15,
            "exit": 16,
            "wait": 17,
            "say": 18,
            "think": 19,
            "pray": 20,
            "cast": 21,
            "learn": 22,
            "practice": 23,
            "rest": 24,
            "heal": 25,
            "identify": 26,
            "equip": 27,
            "unequip": 28,
            "drop_all": 29,
            "save": 30,
            "quit": 31,
        }
        
    def setAgentPosition(self, x:int, y:int): # Set agent postion
        self.kb.retractall(f"position(agent,_,{x},{y})")
    
    def setAgentPosition(self, type:str, x:int, y:int): # Set enemy postion and type
        self.kb.retractall(f"position(enemy,{type},{x},{y})")

    def setHp(self, hp:int): # Set hp
        self.kb.retractall(f"health({hp})")
    
    def setWeapon(self, type:str):
        self.kb.retractall(f"wields_weapong(agent, {type})")
        
    def queryAction(self):
        return list(self.kb.query("action(Action)"))
        
    def performAction(self, actions:list):
        if not isinstance(actions, list):
            raise ValueError("Actions must be a list of dictionaries")
        return self.actionIdMap[actions[0]["Action"]]

    def startSearchWeapon(self, env, game, game_map:np.ndarray, displayBool:bool = True):
        print(f"GAME MAP: {game_map}")
        print(f"ENV: {env}")
        player = utils.get_player_location(game_map)
        weapon = utils.get_target_location(game_map, ")")
        path = algo.a_star(game_map, player, weapon[1], utils.manhattan_distance)
        actions_move = utils.actions_from_path(player, path[1:])
        if displayBool:
            image = plt.imshow(game[25:350, 475:825])
        for move in actions_move:
            state,_,_,_ = env.step(move)
            ## Print display
            if displayBool:
                display.display(plt.gcf())
                display.clear_output(wait=True)
                image.set_data(state["pixel"][25:350, 475:825])
            ###
            player = utils.get_player_location(game_map) #Take new player pos
            #actionMap.setAgentPosition(player[0], player[1])#Update player pos
            time.sleep(0.5)
        #env.step("5") # pick_up action
        queryResult = self.queryAction()
        if queryResult:
            action = self.performAction(queryResult)
            print(f"Next action: {action}")
            pickObject = env.step(action)
            ## Print display
            if displayBool:
                display.display(plt.gcf())
                display.clear_output(wait=True)
                image.set_data(state["pixel"][25:350, 475:825])
            ###
            print(pickObject)
            self.setWeapon("tsurugi")
        else:
            print("There isn't any action to do!")
    

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