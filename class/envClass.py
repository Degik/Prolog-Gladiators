import gym
from minihack import LevelGenerator

# CLASS FOR ENVIRONMENT MANAGEMENT
class EnvMng:
    def __init__(self, width:int = 20, height:int = 20):
        self.level_generated = LevelGenerator(w = width, h=height)
        
    def addWeapon(self, weapon:str="tsurugi"):
        self.level_generated.add_object(name=weapon, symbol=")")
        #self.level_generated.add_object(')', (7, 7))  # Aggiungi un'arma
        #self.level_generated.add_object('*', (9, 9))  # Aggiungi un oggetto
        
    def addObject(self, object:str = "apple", symbol:str = "%"):
        self.level_generated.add_object(object, symbol)
    
    def addMonster(self, monster:str = "goblin"):
        self.level_generated.add_monster(monster)
    
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