import numpy as np
import world

class grid_agent:
    def __init__(self, world_obj, pos_row, pos_col):
        self.world = world_obj
        self.pos_row = pos_row
        self.col_row = pos_col
        world_obj.new_agent(self)

    def move_agent(move_cmd):
        # 0 - wait, 1 - up, 2 - down
        # 3 - left, 4 - right
        world_rows, world_cols = self.world.get_size()
        if(move_cmd == 1):
            move_vec = (1, 0)
        elif(move_cmd == 2):
            move_vec = (-1, 0)
        elif(move_cmd == 3):
            move_vec = (0, -1)
        elif(move_cmd == 4):
            move_vec = (0, 1)
        else:
            move_vec = (0, 0)

        self.pos_row = (self.pos_row + move_row_dp) % world_rows
        self.pos_col = (self.pos_col + move_col_dp) % world_cols
