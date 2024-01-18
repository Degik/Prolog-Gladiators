import gym
import random
from minihack import LevelGenerator

#Possible object inside the envirnoment
##MONSTERS LIST
objectsList = {
    "apple": "%",
    "gold piece": "$"
}

##MONSTERS LIST
monstersList = {
    "giant ant": "a",
    "goblin": "o",
    "scorpion": "s",
    "red dragon": "D"
}
# CLASS FOR ENVIRONMENT MANAGEMENT
class EnvMng:
    def __init__(self, width:int = 20, height:int = 20):
        self.level_generated = LevelGenerator(w = width, h=height)
        
    def addWeapon(self, weapon:str="tsurugi"):
        self.level_generated.add_object(name=weapon, symbol=")")
        #self.level_generated.add_object(')', (7, 7))  # Aggiungi un'arma
        #self.level_generated.add_object('*', (9, 9))  # Aggiungi un oggetto
        
    def addObject(self, symbol:str, object:str = "apple"):
        self.level_generated.add_object(object, symbol)
    
    def addMonster(self, symbol:str, monster:str = "goblin"):
        self.level_generated.add_monster(monster, symbol=symbol)
        
    def generateMonsters(self, seed=None, num_monsters=None):
        # Seed for generated random int
        random.seed(seed)
        # Number of monsters
        if num_monsters is None:
            num_monsters = random.randint(1, 5)
        # Use the list for random choise
        monster_names = list(self.monstersList.keys())
        for i in range(num_monsters):
            monster, symbol = random.choice(monster_names)
            print(f"[Adding monster {i+1} Name:{monster}, Symbol:{symbol}]")
            self.addMonster(symbol, monster)
    
    def generateObjects(self, seed=None, num_objects=None):
        random.seed(seed)
        if num_objects is None:
            num_objects = random.randint(1,3)
        objects_names = list(self.objectsList.keys())
        for i in range(num_objects):
            objectName, symbol = random.choice(objects_names)
            print(f"[Adding object {i+1} Name:{objectName}, Symbol:{symbol}]")
            self.addObject(symbol, objectName)
    
            
    # Create game with env
    # desFile can be used for load custom env
    # return: env, state game_map, game
    def createGame(self, desFile = None):
        if desFile is None:
            desFile = self.level_generated.get_des()
        self.env = gym.make("MiniHack-Skill-Custom-v0", observation_keys = ("chars", "pixel_crop", "pixel"), des_file=desFile)
        self.state = self.env.reset()
        self.game_map = self.state["chars"]
        self.game = self.state["pixel"]
        return self.env, self.state, self.game_map, self.game
    
    # Render environment
    def printEnv(self):
        self.env.render()