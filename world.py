import numpy as np
import grid_agent as ga

class world:
    def __init__(self, num_rows, num_cols):
        self.map = np.zeros(num_rows, num_cols)
        self.agents = []

    def add_agent(self, agent_obj, pos_row, pos_col):
        agent_obj.update_position(self, pos_row, pos_col)
        self.agents.append(agent_obj)

    def add_agent(self, agent_obj):
        self.agents.append(agent_obj)

    def new_agent(self, agent_obj, pos_row, pos_col):
        self.agents.append(agent_obj)

    def move_agent(self, agent_obj, move_cmd):
        # 0 - wait, 1 - up, 2 - down
        # 3 - left, 4 - right
        agent_obj.move_agent(move_cmd)

    def rm_agent(self, agent_obj):
        self.agents.remove(agent_obj)

    def get_size(self):
        return (self.num_rows, self.num_cols)
