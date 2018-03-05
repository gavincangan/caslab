#!/usr/bin/env python
import macros
import numpy as np
from collections import deque
import world

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

class distrib_agent:
    actions = (WAIT, UP, DOWN, LEFT, RIGHT)
    agent_count = 0
    def __init__(self, world_obj, y, x):
        self.world_act = world_obj
        self.obs_map = np.ones_like(world_obj.occ_map)
        self.y = INVALID
        self.x = INVALID
        self.aindex = distrib_agent.agent_count
        self.states = (self.x, self.y, self.obs_map)
        self.msg_buf = deque([],MSG_BUFFER_SIZE)
        self.msg_rcvd = False
        self.__fill_buffer_w_zeros__()
        self.vis_obj = 0
        self.world_act.add_agent(self, y, x)
        distrib_agent.agent_count +=1

    @staticmethod
    def __move_cmd_to_vector__(move_cmd):
        dy = 0
        dx = 0
        if(move_cmd == UP):
            dy = -MOVE_SPEED
        elif(move_cmd == DOWN):
            dy = MOVE_SPEED
        elif(move_cmd == LEFT):
            dx = -MOVE_SPEED
        elif(move_cmd == RIGHT):
            dx = MOVE_SPEED
        else:
            pass
        return (dy, dx)

    # Represent the view of the agewnt in matrix indices
    # => Q1 has a negative dy, for example
    @staticmethod
    def __quadrant_to_dxdy__(quadrant):
        if(quadrant == 1):
            dx = SENSE_RANGE
            dy = -SENSE_RANGE
        elif(quadrant == 2):
            dx = -SENSE_RANGE
            dy = -SENSE_RANGE
        elif(quadrant == 3):
            dx = -SENSE_RANGE
            dy = SENSE_RANGE
        else: #(quadrant == 4)
            dx = SENSE_RANGE
            dy = SENSE_RANGE
        return (dy, dx)

    def __fill_buffer_w_zeros__(self):
        for index in range(MSG_BUFFER_SIZE):
            self.msg_buf.append(0x00)

    def move(self, move_cmd):
        # 0 - wait, 1 - up, 2 - down
        # 3 - left, 4 - right
        wnrows, wncols = self.world_act.get_size()
        (dy, dx) = self.__move_cmd_to_vector__(move_cmd)
        # print 'dy:', dy, ' dx:', dx
        new_y = (self.y + dy) % wnrows
        new_x = (self.x + dx) % wncols
        # print 'New position: ', new_y, new_x
        self.update_position(new_y, new_x)

    def __str__(self):
        return('Agent #' + str(self.aindex) + ' @ ' + str(self.y) + ', ' + str(self.x) + ' :: ' + str(self.msg_buf[0]) + ', ' + str(self.msg_buf[1]) + ', ' + str(self.msg_buf[2]))

    def update_position(self, pos_y, pos_x):
        old_x = self.x
        old_y = self.y
        self.x = pos_x
        self.y = pos_y
        if not(old_x == self.x and old_y == self.y):
            if (old_x > 0 and old_x < self.world_act.ncols and old_y > 0 and old_y < self.world_act.nrows):
                self.world_act.occ_map[old_y][old_x] -= 1
                self.world_act.ptr_map[old_y][old_x].remove(self)
            self.world_act.occ_map[self.y][self.x] += 1
            self.world_act.ptr_map[self.y][self.x].append(self)
            if(self.vis_obj):
                self.world_act.visualize.move_agent_vis(self, self.vis_obj, old_y, old_x, pos_y, pos_x)

    def observe_quadrant(self, quadrant):
        (dy, dx) = __quadrant_to_dxdy__(quadrant)
        sensor_map = self.world_act.map_view(self.y, self.x, dy, dx)

    def broadcast_msg(self, message):
        # wnrows, wncols = self.world_act.get_size()
        x1 = (self.x - COMM_RANGE)
        y1 = (self.y - COMM_RANGE)
        x1, y1 = self.world_act.xy_saturate(x1,y1)
        x2 = (self.x + COMM_RANGE)
        y2 = (self.y + COMM_RANGE)
        x2, y2 = self.world_act.xy_saturate(x2,y2)
        # print(y1, x1, y2, x2, self.y, self.x)
        agents_in_range = self.world_act.agents_in_range(y1, x1, y2, x2)
        # agents_in_range.remove(self)
        for agent in agents_in_range:
            if(message < MSG_LIMITLOWER):
                message = MSG_LIMITLOWER
            elif(message > MSG_LIMITUPPER):
                message = MSG_LIMITUPPER
            agent.msg_buf.append(message)
            agent.msg_rcvd = True
        print 'Agent #', self.aindex, ' broadcasts : ', message

    def print_msgs(self):
        if(self.msg_rcvd):
            for index in range(MSG_BUFFER_SIZE):
                if(self.msg_buf[index] != 0x0):
                    print self.msg_buf[index],
