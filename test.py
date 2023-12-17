import gym
import minihack
import numpy as np
import matplotlib.pyplot as plt
import IPython.display as display


env = gym.make("MiniHack-ExploreMaze-Easy-Mapped-v0", observation_keys=("chars", "pixel"))
state = env.reset()
env.render()