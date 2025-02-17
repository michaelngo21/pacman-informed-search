# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    # priority queue as minheap for cost + heuristic
    min_heap = util.PriorityQueue() 

    start_state = problem.getStartState() # note: state is simply an (x, y) tuple

    # declare costs and parents maps
    costs = dict()
    costs[start_state] = 0
    parents = dict() # dictionary that maps child_state to (parent_state, direction_from_parent_to_child)
    parents[start_state] = None, None

    # declare closed set (set of nodes for which we've found an optimal path to)
    closed = set()

    # append start state (with cost) to minheap
    h = heuristic(start_state, problem)   # note: heuristic returns a numeric value
    min_heap.push(problem.getStartState(), 0+h) 

    while not min_heap.isEmpty():
        curr_state = min_heap.pop()
        # print("curr that was popped from min_heap:", curr_state)
        curr_g = costs[curr_state]
        closed.add(curr_state)
        if problem.isGoalState(curr_state): # an optimal path to goal state has been confirmed 
            # return path ...
            # print("FOUND GOAL STATE!")
            actions = backtrack(parents, curr_state)
            return actions
        # expand curr by iterating through its successors
        for child_state, child_direction, child_cost in problem.getSuccessors(curr_state):
            print("child from problem.getSuccessors:", child_state)
            if child_state in closed:
                continue

            child_g = curr_g + 1
            should_update_instead_of_push = False
            if costs.get(child_state) != None:
                if child_g >= costs[child_state]:
                    continue
                else: 
                    should_update_instead_of_push = True

            costs[child_state] = child_g
            parents[child_state] = (curr_state, child_direction)

            # calculate heuristic for this current path to s
            child_h = heuristic(child_state, problem)
            
            if should_update_instead_of_push:
                min_heap.update(child_state, child_g + h)
                # print("updating child_state:", child_state, "with cost:", child_g + child_h)
            else:
                min_heap.push(child_state, child_g + child_h)
                # print("pushing child_state:", child_state, "with cost:", child_g + child_h)

            # question: is this okay for determining cost of move from parent to successor?
            
def backtrack(parents, goal_state): # note: parents is a dictionary that maps child_state to (parent_state, direction_from_parent_to_child)
    actions = []
    
    parent, direction_to_child = parents[goal_state]
    while parent != None:
        actions.append(direction_to_child)
        parent, direction_to_child = parents[parent]
    actions.reverse()
    return actions

# Abbreviations
astar = aStarSearch
