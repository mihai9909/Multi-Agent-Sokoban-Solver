from agent import UP, DOWN, LEFT, RIGHT, STAY, agent
from environment import env

solution = agent.bfs(env.level, agent.position)

print("Solution found: ", solution)
