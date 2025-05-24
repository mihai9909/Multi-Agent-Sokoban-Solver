import environment
from agent import Agent
from manager_agent import ManagerAgent

main_env = environment.env
manager_agent = ManagerAgent(0)
micro_envs = manager_agent.create_micro_envs(main_env.level, main_env.goal_positions_list)

aid = 1
for micro_env in micro_envs:
    agent = Agent(micro_env.agent_x, micro_env.agent_y, aid, micro_env.env)
    print("Agent: ", aid)
    aid += 1
    agent.act()