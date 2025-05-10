import environment
import random
from time import sleep
from threading import Thread
from queue import Queue

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
STAY = (0, 0)

class Agent:
    def __init__(self, x, y, aid):
        self.aid = aid
        self.env = environment.env
        self.position = (x, y)
        self.running = True
    
    # The agent's main loop
    def act(self):
        level = self.env.level
        position = self.position
        while self.running:
            direction = random.choice([UP, DOWN, LEFT, RIGHT, STAY])
            # self.move(direction)
            (position, level) = self.env.get_next_state(position, level, direction)
            sleep(0.5)

    def get_next_state(self, direction, level):
        (pos, level) = self.env.get_next_state(self.position, level, direction)
        if self.aid == 1:
            self.env.print_level(level)

    # Runs the agent in a separate thread
    def run(self):
        print(f"Agent {self.aid} started at position {self.position}")
        Thread(target=self.act).start()

    def serialize_level(self, level):
        return ''.join([''.join(row) for row in level])

    def bfs(self, level, position):
        queue = Queue()
        visited = {}
        parent = {}  # Maps serialized level to (prev_serial, action)

        start_serial = self.serialize_level(level)
        visited[start_serial] = True
        queue.put((position, level))
        parent[start_serial] = (None, None)  # Start has no parent or action

        while not queue.empty():
            current_position, current_level = queue.get()
            current_serial = self.serialize_level(current_level)

            if self.env.is_goal_state(current_level):
                # Reconstruct the sequence of actions
                actions = []
                while parent[current_serial][0] is not None:
                    prev_serial, action = parent[current_serial]
                    actions.append(action)
                    current_serial = prev_serial

                print("Path found:", actions[::-1])
                return actions[::-1]  # Reverse to get path from start to goal

            for direction in [UP, DOWN, LEFT, RIGHT]:
                next_position, next_level = self.env.get_next_state(current_position, current_level, direction)
                next_serial = self.serialize_level(next_level)

                if not visited.get(next_serial):
                    self.env.write_to_file(next_level)
                    visited[next_serial] = True
                    parent[next_serial] = (current_serial, direction)
                    queue.put((next_position, next_level))
        print("No path found")
        return None  # Goal not found



agent = Agent(2, 3, 1)#.run()
# agent2 = Agent(3, 4, 2).run()
