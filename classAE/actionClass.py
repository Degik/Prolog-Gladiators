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
            "eat": 29,
            "pick": 49,
            "wield": 78,
            "attack": 4,
        }
        
    def setAgentPosition(self, x:int, y:int): # Set agent postion
        self.kb.retractall(f"position(agent,_,_,_)") # Remove
        self.kb.assertz(f"position(agent,_,{x},{y})") # Add
    
    def setEnemyPosition(self, x:int, y:int, type:str = "orc"): # Set enemy postion and type
        self.kb.retractall(f"position(enemy,_,_,_)") # Remove
        self.kb.assertz(f"position(enemy,{type},{x},{y})") # Add

    def setHp(self, hp:int = 100): # Set hp
        self.kb.retractall(f"health(_)") # Remove
        self.kb.assertz(f"health({hp})") # Add
    
    def setWeapon(self, type:str = "_"):
        self.kb.retractall(f"wields_weapong(agent, _)") # Remove
        self.kb.assertz(f"wields_weapong(agent, {type})") # Add
    
    def setHasObject(self, type:str = "_", name:str = "_"):
        self.kb.retractall(f"has(agent, _, _)") # Remove
        self.kb.retractall(f"has(agent, {type}, {name})") # Add
    
    def setSteppingOn(self):
        self.kb.retractall(f"stepping_on(agent, ObjClass, _)") # Remove
        self.kb.assertz(f"stepping_on(agent, ObjClass, _)") # Add
    
    def setUnsafePosition(self):
        self.kb.retractall(f"unsafe_position(_,_)") # Remove
        self.kb.assertz(f"unsafe_position(_,_)") # Add
        
    def queryAction(self):
        result = list(self.kb.query("action(Action)"))
        return result
        
    def performAction(self, actions:list):
        if not isinstance(actions, list):
            raise ValueError("Actions must be a list of dictionaries")
        return self.actionIdMap[actions[0]["Action"]]

    def initActionStatus(self, game_map):
        # :- dynamic position/4.
        # :- dynamic wields_weapon/2.
        # :- dynamic health/1.
        # :- dynamic has/3.
        # :- dynamic stepping_on/3.
        # :- dynamic unsafe_position/2.
        player = utils.get_player_location(game_map)
        self.setAgentPosition(player[0], player[1]) #Update player pos
        self.setWeapon()
        self.setHp()
        self.setHasObject()
        self.setSteppingOn()
        self.setUnsafePosition()



    def startSearchWeapon(self, env, game, game_map:np.ndarray, displayBool:bool = True):
        player = utils.get_player_location(game_map)
        weapon = utils.get_target_location(game_map, ")")
        path = algo.a_star(game_map, player, weapon[1], utils.manhattan_distance)
        actions_move = utils.actions_from_path(player, path[1:])
        if displayBool:
            image = plt.imshow(game[25:350, 475:825])
        for move in actions_move:
            state,_,_,_ = env.step(move)
            player = utils.get_player_location(game_map) #Take new player pos
            self.setAgentPosition(player[0], player[1])#Update player pos
            ## Print display
            if displayBool:
                display.display(plt.gcf())
                display.clear_output(wait=True)
                image.set_data(state["pixel"][25:350, 475:825])
                time.sleep(0.2)
            ###
        #env.step("5") # pick_up action
        queryResult = self.queryAction()
        if queryResult:
            action = self.performAction(queryResult)
            print(f"Next action: {action}")
            state,_,_,_ = env.step(action)
            ## Print display
            if displayBool:
                display.display(plt.gcf())
                display.clear_output(wait=True)
                image.set_data(state["pixel"][25:350, 475:825])
            ###
            self.setWeapon("tsurugi")
        else:
            print("There isn't any action to do!")
    
    def startSearchObjects(self, env, game, game_map:np.ndarray, objectsList:list, displayBool:bool = True):
        objectFound = {name: [] for name in objectsList.keys()}
        for name, symbol in objectsList.items():
            positions = utils.get_objects_location(game_map, symbol)
            if positions:
                for pos in zip(positions[0], positions[1]):
                    objectFound[name].append(pos)
        player = utils.get_player_location(game_map)
        print(objectFound)
        for objectType, objectPositions in objectFound.items():
            for objectPos in objectPositions:
                path = algo.a_star(game_map, player, objectPos, utils.manhattan_distance)
                actions_move = utils.actions_from_path(player, path[1:])
                if displayBool:
                    image = plt.imshow(game[25:350, 475:825])
                for move in actions_move:
                    state,_,_,_ = env.step(move)
                    player = utils.get_player_location(game_map) # Take new player pos
                    self.setAgentPosition(player[0], player[1]) # Update player pos
                    ## Print display
                    if displayBool:
                        display.display(plt.gcf())
                        display.clear_output(wait=True)
                        image.set_data(state["pixel"][25:350, 475:825])
                        time.sleep(0.2)
                    ###
                #env.step("5") # pick_up action
                queryResult = self.queryAction()
                if queryResult:
                    action = self.performAction(queryResult)
                    print(f"Next action: {action}")
                    state,_,_,_ = env.step(action)
                    ## Print display
                    if displayBool:
                        display.display(plt.gcf())
                        display.clear_output(wait=True)
                        image.set_data(state["pixel"][25:350, 475:825])
                    ###
                    if objectType == "apple":
                        self.setHasObject("commestible", objectType)
                    else:
                        self.setHasObject()
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