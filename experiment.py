from macros import *
import numpy as np
import random
import grid_agent as ga
from world import world
from visualize import visualize

class experiment:
    def __init__(self, world_dim, nagents, agent_xy):
        self.world = world(world_dim[1], world_dim[0])
        self.vis = visualize(self.world)
        self.list_agents = []
        for index in range(nagents):
            self.list_agents.append(self.world.new_agent(agent_xy[index][1], agent_xy[index][0]))
        self.init_vis()

    def init_vis(self):
        self.vis.draw_world()
        self.vis.draw_agents()
        self.vis.canvas.pack()
        self.vis.canvas.update()

    def run_random(self, ts, T):
        nsteps = int(T/ts)
        for step in range(nsteps):
            random.shuffle(self.list_agents)
            for agent in self.list_agents:
                agent.move(random.choice(agent.move_actions))
                agent.observe_quadrant(random.choice(agent.obs_actions))
                agent.broadcast_msg(random.choice(agent.comm_actions))
                self.vis.canvas.update()
                self.vis.canvas.after(int(ts * 200))
            print '\n'
            for agent in self.list_agents:
                print agent
            print '\n\n'
        self.vis.canvas.after(int(ts * 1000))

if __name__ == "__main__":
    my_exp = experiment( (10,10), 7, ((3,2),(1,6),(7,8),(2,6),(0,9),(5,6),(4,7)) )
    my_exp.run_random(0.5, 3)
    # my_exp = experiment( (5,5), 6, ((3,2),(1,2),(2,4),(0,4),(3,0),(4,4)) )
    # my_exp.run_random(0.5, 3)
