import macros
import numpy as np
import grid_agent as ga

WAIT = 0
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

INVALID = -999
MSG_LIMITLOWER = 0x0
MSG_LIMITUPPER = 0xF

SENSE_RANGE = 2
COMM_RANGE = 2
MOVE_SPEED = 1
MSG_BUFFER_SIZE = 3

FRAME_HEIGHT = 480
FRAME_WIDTH = 600

FRAME_MARGIN = 10
CELL_MARGIN = 5

MAX_AGENTS_IN_CELL = 4

COLORS = ['red', 'green', 'blue', 'black', 'white', 'magenta', 'cyan', 'yellow']

class world:
    def __init__(self, nrows, ncols):
        self.nrows = nrows
        self.ncols = ncols
        self.occ_map = np.zeros((nrows, ncols)) #occupancy map
        self.ptr_map = [[[] for row in range(ncols)] for row in range(nrows)]
        self.agents = []
        self.visualize = None

    def add_agent(self, agent_obj, pos_y, pos_x):
        pos_x, pos_y = self.xy_saturate(pos_x, pos_y)
        agent_obj.update_position(pos_y, pos_x)
        print 'Adding: ', str(agent_obj)
        self.agents.append(agent_obj)

    def new_agent(self, pos_row, pos_col):
        agent_obj = ga.distrib_agent(self, pos_row, pos_col)
        #agent_obj.update_position(self, pos_row, pos_col)
        return agent_obj

    def move_agent(self, agent_obj, move_cmd):
        agent_obj.move(move_cmd)
        raise NotImplementedError

    def rm_agent(self, agent_obj):
        self.agents.remove(agent_obj)

    def get_size(self):
        return (self.nrows, self.ncols)

    def xy_saturate(self, x,y):
        if(x<0): x=0
        if(x>self.ncols): x=self.ncols
        if(y<0): y=0
        if(y>self.nrows): y=self.nrows
        return(x, y)

    def occ_map_view(self, y, x, dy, dx):
        x1 = (x + dx)
        y1 = (y + dy)
        x,y = self.xy_saturate(x, y)
        x1,y1 = self.xy_saturate(x1, y1)
        return (self.map[y: y1, x: x1])

    def agents_in_range(self, y1, x1, y2, x2):
        # print(y1, x1, y2, x2)
        x1,y1 = self.xy_saturate(x1, y1)
        x2,y2 = self.xy_saturate(x2, y2)
        if(x2 > x1):
            sx = x1
            bx = x2
        else:
            sx = x2
            bx = x1
        if(y2 > y1):
            sy = y1
            by = y2
        else:
            sy = y2
            by = y1
        # print(sy, sx, by, bx)
        # print(sy, sx, by-sy+1, bx-sx+1)
        ptr_map_range = self.ptr_map[sy: by-sy+1]
        ptr_map_range = [ cells_row[sx:bx-sx+1] for cells_row in ptr_map_range ]
        list_agents = []
        for row in ptr_map_range:
            for cell in row:
                if cell: #is not empty
                    for agent in cell:
                        list_agents.append(agent)
        return list_agents

    def list_all_agents(self):
        return self.agents

    def print_all_agents(self):
        for agent in self.agents:
            print(str(agent))
