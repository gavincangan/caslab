import numpy as np
import grid_agent as ga
from world import world
from visualize import visualize

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

if __name__ == "__main__":
    not_my_home = world(5,6)
    not_my_home.new_agent(3,4)
    my_agent = not_my_home.new_agent(4,2)
    not_my_home.new_agent(2,1)
    not_my_home.new_agent(3,2)
    all_agents = not_my_home.list_all_agents()
    agents_in_range = not_my_home.agents_in_range(0, 3, 3, 0)
    for agent in agents_in_range:
        print agent
    my_agent.broadcast_msg(0x7)

    for agent in all_agents:
        print str(agent)

    # root = Tk()
    # canvas = Canvas(root, width=400, height=400)
    # canvas.grid()
    # root.mainloop()

    vis = visualize(not_my_home)
    vis.draw_world()
    vis.draw_agents()
    # vis.do_loop()
    vis.canvas.pack()
    vis.canvas.update()
    vis.canvas.after(2000)

    print '\n\n'
    for agent in all_agents:
        print str(agent)

    my_agent.move(UP)
    vis.canvas.update()

    print '\n\n'
    for agent in all_agents:
        print str(agent)

    vis.canvas.after(2000)
    my_agent.move(UP)
    vis.canvas.update()
    vis.canvas.after(2000)

    my_agent.move(LEFT)
    vis.canvas.update()
    vis.canvas.after(2000)

    my_agent.move(DOWN)
    vis.canvas.update()
    vis.canvas.after(2000)

    my_agent.move(RIGHT)
    vis.canvas.update()
    vis.canvas.after(2000)

    my_agent.move(RIGHT)
    vis.canvas.update()
    vis.canvas.after(2000)

    my_agent.move(RIGHT)
    vis.canvas.update()
    vis.canvas.after(2000)

    for agent in all_agents:
        print str(agent)
    print("Hello")
