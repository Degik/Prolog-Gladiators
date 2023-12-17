import gym
import numpy as np
import minihack
import matplotlib.pyplot as plt
import IPython.display as display
# Costruisco l'ambienete con il comando make e lo ritorno nella variabile env
env = gym.make("MiniHack-ExploreMaze-Hard-Mapped-v0", observation_keys=("chars", "pixel"))
# Prendo lo stato mediante reset nella variabile state
state = env.reset()
# Disegno l'ambiente
env.render()
# Plot entro le coordinate (x,y)
plt.imshow(state["pixel"][25:300, :400])
#
game_map = state['chars']
game = state['pixel']
# Prendo le coordinate di partenza e il target
startPoint = get_player_location(game_map)
print(startPoint)
targetPoint = get_target_location(game_map) # Il target dev'essere visibile altrimenti ritorna errore
print(targetPoint)
