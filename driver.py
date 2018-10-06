"""
Driver.py -- a driver program for the 8-puzzle solving code
A. Thall
CSC 345 F18

Project 1:  This implements a multi-method solver for an 8-puzzle as discussed
in the EdX CSMM.101x course F18 on A.I.

The code is based on a code-skeleton provided for the course.

From the course webpage:

$ python driver.py <method> <board>

The method argument will be one of the following. You need to implement all three of them:

bfs (Breadth-First Search)
dfs (Depth-First Search)
ast (A-Star Search)

The board argument will be a comma-separated list of integers containing no spaces.
For example, to use the breadth-first search strategy to solve the input board given
by the starting configuration {0,8,7,6,5,4,3,2,1}, the program will be executed like
so (with no spaces between commas):

$ python driver.py bfs 0,8,7,6,5,4,3,2,1
"""


import Queue as Q
import time
import resource
import sys
import math
from collections import deque
from UPQueue import UPQueue

# xxAT: my imports
from datetime import datetime

#### SKELETON CODE ####

# xxAT: Global variables for output
path_to_goal = deque()
cost_of_path = 0
nodes_expanded = 0
search_depth = 0
max_search_depth = 0
running_time = 0.0
max_ram_usage = 0.0

## The Class that Represents the Puzzle
class PuzzleState(object):
    """docstring for PuzzleState"""

    def __init__(self, config, n, parent=None, action="Initial", cost=0):

        if n*n != len(config) or n < 2:
            raise Exception("the length of config is not correct!")

        self.n = n
        self.cost = cost
        self.parent = parent
        self.action = action
        self.dimension = n
        self.config = config
        self.children = []

        for i, item in enumerate(self.config):
            if item == 0:
                self.blank_row = i / self.n
                self.blank_col = i % self.n
                break

    def __str__(self):
        """xxAT: I added a toString() method"""
        return str(self.__dict__)

    def display(self):

        for i in range(self.n):
            line = []
            offset = i * self.n
            for j in range(self.n):
                line.append(self.config[offset + j])
            print line

    def move_left(self):

        if self.blank_col == 0:
            return None
        else:
            blank_index = self.blank_row * self.n + self.blank_col
            target = blank_index - 1
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, parent=self, action="Left", cost=self.cost + 1)

    def move_right(self):

        if self.blank_col == self.n - 1:
            return None
        else:
            blank_index = self.blank_row * self.n + self.blank_col
            target = blank_index + 1
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, parent=self, action="Right", cost=self.cost + 1)

    def move_up(self):

        if self.blank_row == 0:
            return None
        else:
            blank_index = self.blank_row * self.n + self.blank_col
            target = blank_index - self.n
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, parent=self, action="Up", cost=self.cost + 1)

    def move_down(self):

        if self.blank_row == self.n - 1:
            return None
        else:
            blank_index = self.blank_row * self.n + self.blank_col
            target = blank_index + self.n
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, parent=self, action="Down", cost=self.cost + 1)

    def expand(self):
        """expand the node"""

        # add child nodes in order of UDLR
        if len(self.children) == 0:
            up_child = self.move_up()
            if up_child is not None:
                self.children.append(up_child)

            down_child = self.move_down()
            if down_child is not None:
                self.children.append(down_child)

            left_child = self.move_left()
            if left_child is not None:
                self.children.append(left_child)

            right_child = self.move_right()
            if right_child is not None:
                self.children.append(right_child)

        return self.children

# Function that Writes to output.txt

### Students need to change the method to have the corresponding parameters

def writeOutput():
    with open("output.txt", "w") as f:
        f.write("%s\n" % str(datetime.now()))
        f.write("path_to_goal:  %s\n" % str(path_to_goal))
        f.write("cost_of_path:  %d\n" % cost_of_path)
        f.write("nodes_expanded:  %d\n" % nodes_expanded)
        f.write("search_depth:  %d\n" % search_depth)
        f.write("max_search_depth:  %d\n" % max_search_depth)
        f.write("running_time:  %f\n" % running_time)
        f.write("max_ram_usage:  %f\n" % max_ram_usage)

        ### Student Code Goes here

# xxAT: goal_test uses goal value
goal = tuple()
def goal_test(state):
    return state.config == goal

# xxAT: simple loops over states from achieved goal back along parent path
# assembles solution actions, etc., and prints out in reverse order.
# NOTE:  DO NOT call this for DFS!  without removing the print statements
# You could modify this to create the list of actions for the solution path
def set_solution_stats(final_state):
    traveler = final_state
    while traveler != None:
        if traveler.action != "Initial":
            path_to_goal.appendleft(traveler.action)
        #traveler.display()
        #print
        traveler = traveler.parent

def bfs_search(initial_state):
    """BFS search"""
    print "calling bfs on", initial_state
    ### STUDENT CODE GOES HERE ###
    global goal, path_to_goal, cost_of_path, nodes_expanded, search_depth
    global max_search_depth, running_time, max_ram_usage

    goal = tuple([i for i in range(initial_state.n**2)])

    if goal_test(initial_state):
        writeOutput()
        return True

    frontier = deque([initial_state])
    frontier_set = set()
    frontier_set.add(initial_state.config)
    explored = {}

    while len(frontier) > 0:
        # pop the next node and remove it from the frontier_set as well
        node = frontier.popleft()
        frontier_set.remove(node.config)

        explored[node.config] = node
        node.expand()
        nodes_expanded += 1
        for child_node in node.children:
            if not child_node.config in explored and not child_node.config in frontier_set:
                if goal_test(child_node):
                    cost_of_path = child_node.cost
                    # xxAT: fill in rest of this stuff, figure out parent chain
                    #   depth and actions from parent-chain lookup

                    # print-solution here is optional -- DONT use in DFS!!
                    set_solution_stats(child_node)
                    writeOutput()
                    return True
                else:
                    # add to frontier, so you can return nodes in FIFO order in O(1)
                    frontier.append(child_node)
                    #add to frontier_set, so you can get an O(1) test for presence
                    frontier_set.add(child_node.config)
    return False

def dfs_search(initial_state):
    """DFS search"""
    print "calling dfs on", initial_state
    ### STUDENT CODE GOES HERE ###
    global goal, path_to_goal, cost_of_path, nodes_expanded, search_depth
    global max_search_depth, running_time, max_ram_usage

    goal = tuple([i for i in range(initial_state.n ** 2)])

    if goal_test(initial_state):
        writeOutput()
        return True

    frontier = deque([initial_state])
    frontier_set = set()
    frontier_set.add(initial_state.config)
    explored = {}

    while len(frontier) > 0:
        # pop the next node and remove it from the frontier_set as well
        node = frontier.pop()
        frontier_set.remove(node.config)

        explored[node.config] = node
        node.expand()
        nodes_expanded += 1
        for child_node in node.children:
            if not child_node.config in explored and not child_node.config in frontier_set:
                if goal_test(child_node):
                    cost_of_path = child_node.cost
                    # xxAT: fill in rest of this stuff, figure out parent chain
                    #   depth and actions from parent-chain lookup

                    # print-solution here is optional -- DONT use in DFS!!
                    set_solution_stats(child_node)
                    writeOutput()
                    return True
                else:
                    # add to frontier, so you can return nodes in FIFO order in O(1)
                    frontier.append(child_node)
                    # add to frontier_set, so you can get an O(1) test for presence
                    frontier_set.add(child_node.config)
    return False

def A_star_search(initial_state):
    """A* search"""
    print "calling ast on", initial_state
    print "with initial total cost", calculate_total_cost(initial_state)
    ### STUDENT CODE GOES HERE ###
    global goal, path_to_goal, cost_of_path, nodes_expanded, search_depth
    global max_search_depth, running_time, max_ram_usage

    goal = tuple([i for i in range(initial_state.n ** 2)])

    if goal_test(initial_state):
        writeOutput()
        return True

    # don't need frontier_set, since can just check for key in UPQueue with in
    frontier = UPQueue()
    # xxAT:  hack for now, using cost increasing by 1 each time, get FIFO queue
    #  behavior from the priority queue.  Next do a Best First Heuristic on
    #  a Manhattan metric, then the full A*.

    frontier.insert(initial_state.config, initial_state,
                    calculate_total_cost(initial_state))
    explored = {}

    while len(frontier) > 0:
        # pop the next node and remove it from the frontier_set as well
        node, useless = frontier.remove_min()

        if goal_test(node):
            cost_of_path = node.cost
            # xxAT: fill in rest of this stuff, figure out parent chain
            #   depth and actions from parent-chain lookup

            # print-solution here is optional -- DONT use in DFS!!
            set_solution_stats(node)
            writeOutput()
            return True

        explored[node.config] = node
        node.expand()
        nodes_expanded += 1
        for child_node in node.children:
            if not child_node.config in explored and not child_node.config in frontier:

                frontier.insert(child_node.config, child_node,
                                calculate_total_cost(child_node))
            elif child_node.config in frontier:
                old_cost = frontier.get_priority(child_node.config)
                new_cost = calculate_total_cost(child_node)
                if new_cost < old_cost:
                    frontier.replace(child_node.config, child_node, new_cost)
    return False

def calculate_total_cost(state):
    """
    calculate the total estimated cost of a state
    This uses the sum of Manhattan distances as the heuristic
    """
    ### STUDENT CODE GOES HERE ###
    config = state.config
    n = state.dimension
    total_cost = state.cost
    for pos, val in enumerate(config):
        if val != 0:
            total_cost += calculate_manhattan_dist(pos, val, n)

    return total_cost

def calculate_manhattan_dist(idx, value, n):
    """calculatet the manhattan distance of a tile"""
    ### STUDENT CODE GOES HERE ###
    tile_row = idx//n
    tile_col = idx % n
    dest_row = value//n
    dest_col = value % n
    dx = math.fabs(tile_row - dest_row)
    dy = math.fabs(tile_col - dest_col)
    return int(dx + dy)

def test_goal(puzzle_state):
    """test the state is the goal state or not"""
    pass
    ### STUDENT CODE GOES HERE ###

# Main Function that reads in Input and Runs corresponding Algorithm

def main():
    sm = sys.argv[1].lower()

    begin_state = sys.argv[2].split(",")
    begin_state = tuple(map(int, begin_state))

    size = int(math.sqrt(len(begin_state)))

    hard_state = PuzzleState(begin_state, size)
    if sm == "bfs":
        if bfs_search(hard_state):
            print "BFS solution found"
        else:
            print "no BFS solution found"
    elif sm == "dfs":
        if dfs_search(hard_state):
            print "DFS solution found"
        else:
            print "no DFS solution found"
    elif sm == "ast":
        if A_star_search(hard_state):
            print "A* solution found"
        else:
            print "no A* solution found"
    else:
        print("Enter valid command arguments !")


if __name__ == '__main__':

    main()
