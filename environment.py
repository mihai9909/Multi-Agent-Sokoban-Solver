from threading import Thread, Lock

class Environment():
    def __init__(self):
        self.global_lock = Lock()
        self.level = """
#########
#    #  #
#   $#  #
# @     #
# # $   #
# #     #
#########
"""
        self.goal_positions = """
#########
#       #
#   .   #
#   .   #
#       #
#       #
#########
"""
        self.level = [list(row) for row in self.level.split('\n') if row]
        self.goal_positions = [list(row) for row in self.goal_positions.split('\n') if row]
        self.goal_positions_list = []
        for i in range(len(self.goal_positions)):
            for j in range(len(self.goal_positions[i])):
                if self.goal_positions[i][j] == '.':
                    self.goal_positions_list.append((i, j))

        print("Goal positions:", self.goal_positions_list)

    # Moves the agent in the environment
    def move(self, agent, direction):
        x, y = agent.position
        dx, dy = direction
        nx, ny = x + dx, y + dy
        nnx, nny = x + 2*dx, y + 2*dy
        with self.global_lock:
            current = self.level[y][x]
            next_cell = self.level[ny][nx]
            after_next = self.level[nny][nnx] if self.within_bounds(nnx, nny) else None

            if next_cell in ' ':
                # Just move player
                self.level[y][x] = ' '
                self.level[ny][nx] = '@'
                return (nx, ny)
            elif next_cell in '$' and after_next != None:
                if after_next == ' ':
                    self.level[nny][nnx] = '$'
                    self.level[ny][nx] = '@'
                    self.level[y][x] = ' '
                    return (nx, ny)
                else:
                    return (x, y)

            return (x, y)

    # Returns the next state of the environment
    # based on the current state and the action taken
    # by the agent
    def get_next_state(self, position, level, direction):
        x, y = position
        dx, dy = direction
        nx, ny = x + dx, y + dy
        nnx, nny = x + 2*dx, y + 2*dy

        with self.global_lock:
            new_level = [level[i][:] for i in range(len(level))]  # Deep copy of the level
            current = new_level[y][x]
            next_cell = new_level[ny][nx]
            after_next = new_level[nny][nnx] if self.within_bounds(nnx, nny) else None

            if next_cell in ' ':
                # Just move player
                new_level[y][x] = ' '
                new_level[ny][nx] = '@'
                return ((nx, ny), new_level)
            elif next_cell in '$' and after_next != None:
                if after_next == ' ':
                    new_level[nny][nnx] = '$'
                    new_level[ny][nx] = '@'
                    new_level[y][x] = ' '
                    return ((nx, ny), new_level)
                else:
                    return ((x, y), new_level)

            return ((x, y), new_level)

    def is_goal_state(self, level):
        for pos in self.goal_positions_list:
            x, y = pos
            if level[x][y] != '$':
                return False
        return True

    def clamp(self, x, y):
        if x < 0 or y < 0 or x >= len(self.level[0]) or y >= len(self.level):
            return (min(max(x, 0), len(self.level[0]) - 1), min(max(y, 0), len(self.level) - 1))
        return (x, y)

    def within_bounds(self, x, y):
        return 0 <= x < len(self.level[0]) and 0 <= y < len(self.level)

    def to_string(self):
        with self.global_lock:
            return '\n'.join([''.join(row) for row in self.level])

    def print_level(self, new_level):
        for i in range(len(new_level)):
            for j in range(len(new_level[i])):
                if new_level[i][j] == '$' and self.goal_positions[i][j] == '.':
                    print('*', end='')
                elif new_level[i][j] == '@':
                    print('@', end='')
                elif self.goal_positions[i][j] == '.':
                    print('.', end='')
                else:
                    print(new_level[i][j], end='')
            print()

    def write_to_file(self, new_level):
        with open('level.txt', 'a') as f:
            for i in range(len(new_level)):
                for j in range(len(new_level[i])):
                    if new_level[i][j] == '$' and self.goal_positions[i][j] == '.':
                        f.write('*')
                    elif new_level[i][j] == '@':
                        f.write('@')
                    elif self.goal_positions[i][j] == '.':
                        f.write('.')
                    else:
                        f.write(new_level[i][j])
                f.write('\n')

    def print(self):
        with self.global_lock:
            for i in range(len(self.level)):
                for j in range(len(self.level[i])):
                    if self.level[i][j] == '$' and self.goal_positions[i][j] == '.':
                        print('*', end='')
                    elif self.level[i][j] == '@':
                        print('@', end='')
                    elif self.goal_positions[i][j] == '.':
                        print('.', end='')
                    else:
                        print(self.level[i][j], end='')
                print()

env = Environment()
