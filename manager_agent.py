import math
from environment import env, Environment


class ManagerAgent:

    def __init__(self, aid):
        self.aid = aid

    '''
    Break the environment level in micro levels for each agent
    Each micro level will contain 1 agent, 1 object and 1 goal position
    '''

    def create_micro_envs(self, level, goal_positions):
        print("initial level")
        env.print_level(level)
        # extract agents positions, objects positions and goal positions from level
        agents_positions = []
        objects_positions = []
        for i in range(len(level)):
            for j in range(len(level[i])):
                if level[i][j] == '@':
                    agents_positions.append((i, j))
                elif level[i][j] == '$':
                    objects_positions.append((i, j))

        print("micro levels:")
        # create micro level for each agent
        micro_levels = []
        for agent in agents_positions:
            # get nearest object
            nearest_object = self.get_nearest(agent, objects_positions)
            objects_positions.remove(nearest_object)
            # get nearest goal
            nearest_goal = self.get_nearest(nearest_object, goal_positions)
            goal_positions.remove(nearest_goal)
            # create level with agent, nearest object, nearest goal
            micro_level = self.create_level(level, agent, nearest_object)
            micro_goal = self.create_goal(level, nearest_goal)
            micro_level_str = self.serialize(micro_level)
            micro_goal_str = self.serialize(micro_goal)
            micro_env = MicroEnv(micro_level_str, micro_goal_str, agent[1], agent[0])
            micro_levels.append(micro_env)

        return micro_levels

    def get_nearest(self, current_position, items):
        if len(items) == 0:
            return None
        min_distance = self.distance(current_position, items[0])
        point = items[0]
        for item in items:
            dist = self.distance(current_position, item)
            if dist < min_distance:
                min_distance = dist
                point = item

        return point

    def distance(self, a, b):
        dx = abs(a[0] - b[0])
        dy = abs(a[1] - b[1])
        return math.sqrt(dx * dx + dy * dy)

    def create_level(self, level, agent_pos, object_pos):
        new_level = []
        for i in range(len(level)):
            row = []
            for j in range(len(level[i])):
                if level[i][j] == '#':
                    row.append('#')
                elif agent_pos == (i, j):
                    row.append('@')
                elif object_pos == (i, j):
                    row.append('$')
                else:
                    row.append(' ')
            new_level.append(row)
        return new_level

    def create_goal(self, level, goal_pos):
        new_goal = []
        for i in range(len(level)):
            row = []
            for j in range(len(level[i])):
                if goal_pos == (i, j):
                    row.append('.')
                else:
                    row.append(' ')
            new_goal.append(row)
        return new_goal

    def print_level(self, level):
        for i in range(len(level)):
            for j in range(len(level[i])):
                print(level[i][j], end='')
            print()

    def serialize(self, obj):
        str = ""
        for i in range(len(obj)):
            str += "\n"
            for j in range(len(obj[i])):
                str += obj[i][j]
        str += "\n"
        return str


class MicroEnv:

    def __init__(self, level, goals, x, y):
        self.env = Environment(level, goals)
        self.agent_x = x
        self.agent_y = y
