from pyswip import Prolog

actionIdMap = {
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

class AgentAction:
    def __init__(self):
        self.kb = Prolog()
        self.kb.consult('kb.pl')
        
    def performAction(self, actions:list):
        if not isinstance(actions, list):
            raise ValueError("Actions must be a list of dictionaries")
        return actionIdMap[actions[0]["Action"]]