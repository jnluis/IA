# Diogo Falcão, Nmec: 108712
# João Luís, Nmec:
# José Gameiro, Nmec: 108840

from complementary_functions import *


import heapq


def heuristic(initial, goal):
    diffX = abs(initial[0] - goal[0])
    diffY = abs(initial[1] - goal[1])
    return diffX + diffY + max(diffX, diffY)

def get_neighbors(state):
    x, y = state
    neighbors = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
    return [(neighbor, action) for neighbor, action in zip(neighbors, ["d", "a", "s", "w"])]

def is_below_OR_IN_rock(state, rocks):
    x, y = state
    for rock_x, rock_y in rocks:
        if x == rock_x and y == rock_y - 1: # se estiver por baixo da pedra
            return 50
        if x == rock_x and y == rock_y: # se estiver na pedra
            return 1000
    return 1

def a_star_search(initial_state, goal_state, rocks):
    initial_state = tuple(initial_state)
    goal_state = tuple(goal_state)
    open_set = [(0, initial_state, [])]
    closed_set = set()

    while open_set:
        current_cost, current_state, current_path = heapq.heappop(open_set)

        if current_state == goal_state:
            return current_path

        if current_state in closed_set:
            continue

        closed_set.add(current_state)
        neighbors = get_neighbors(current_state)

        for neighbor, action in neighbors:
            if neighbor not in closed_set:
                add_cost = is_below_OR_IN_rock(neighbor, rocks)
                neighbor_cost = current_cost + add_cost  # Assuming uniform cost
                total_cost = neighbor_cost + heuristic(neighbor, goal_state)
                heapq.heappush(open_set, (total_cost, neighbor, current_path + [action]))
    return None  # No path found



        


    


            


            




