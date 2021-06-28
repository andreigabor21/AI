from math import sqrt
from queue import PriorityQueue

# define indexes variations
v = [[-1, 0], [1, 0], [0, 1], [0, -1]]
count = 0

def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def euclidean_distance(a, b):
    return sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

def chebyshev_distance(a, b):
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))


def is_inside(next, mapM):
    return next[0] >= 0 and next[0] < mapM.n and next[1] >= 0 and next[1] < mapM.m

def is_not_wall(position, mapM):
    return mapM.surface[position[0]][position[1]] != 1

def get_path(current: tuple, start: tuple, came_from: dict):
    global count
    path = []
    while current != start:
        path.append([current[0], current[1]])
        current = came_from[current]
        count += 1
    path.append([current[0], current[1]])
    count += 1
    print("Number of steps: ", count)
    return path[::-1]


def searchGreedy(mapM, initialX, initialY, finalX, finalY):
    found = False
    start = (initialX, initialY)
    goal = (finalX, finalY)
    visited = []
    to_visit = []
    came_from = {} #parent dictionary

    to_visit.append(start)
    came_from[start] = None

    while len(to_visit) != 0 and not found:
        if not to_visit:
            return False

        current = to_visit[-1]
        visited.append(current)
        x, y = current
        del to_visit[-1]

        if current == goal:
            found = True
        else:
            aux = []
            neighbors = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
            for next in neighbors:
                if next not in visited and is_inside(next, mapM) and is_not_wall(next, mapM):
                    aux.append(next)
                    came_from[next] = (x, y)
            to_visit += aux
            to_visit.sort(key = lambda point: manhattan_distance(point, goal), reverse=True)

    if found:
        return get_path(goal, start, came_from)
    else:
        return None

def hill_climbing(mapM, initialX, initialY, finalX, finalY):
    # TO DO
    # implement the search function and put it in controller
    # returns a list of moves as a list of pairs [x,y]
    found = False
    start = (initialX, initialY)
    goal = (finalX, finalY)
    visited = []
    to_visit = [] #fifo sorted list
    came_from = {} #parent dictionary

    to_visit.append(start)
    came_from[start] = None

    while len(to_visit) != 0 and not found:
        if not to_visit:
            return False

        current = to_visit[-1]
        visited.append(current)
        x, y = current
        del to_visit[-1]

        if current == goal:
            found = True
        else:
            aux = []
            neighbors = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
            for next in neighbors:
                if next not in visited and is_inside(next, mapM) and is_not_wall(next, mapM):
                    aux.append(next)
                    came_from[next] = (x, y)
            aux.sort(key = lambda point: manhattan_distance(point, goal), reverse=True)
            to_visit += aux

    if found:
        return get_path(goal, start, came_from)
    else:
        return None


def searchGreedyPQ(mapM, initialX, initialY, finalX, finalY):
    found = False
    start = (initialX, initialY)
    goal = (finalX, finalY)
    visited = []
    to_visit = PriorityQueue() # FIFO sorted list
    came_from = {} # parent dictionary

    to_visit.put((0, start))
    came_from[start] = None
    while not to_visit.empty() and not found:
        current = to_visit.get()[1]
        visited.append(current)
        x, y = current

        if current == goal:
            found = True
        else:
            neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
            for next in neighbors:
                if next not in visited and is_inside(next, mapM) and is_not_wall(next, mapM):
                    priority = manhattan_distance(next, goal)
                    to_visit.put((priority, next))
                    came_from[next] = (x, y)
    if found:
        return get_path(goal, start, came_from)
    else:
        return None


def searchAStar(mapM, initialX, initialY, finalX, finalY):
    # TO DO
    # implement the search function and put it in controller
    # returns a list of moves as a list of pairs [x,y]
    found = False
    start = (initialX, initialY)
    goal = (finalX, finalY)
    visited = []
    cost_so_far = {}
    to_visit = PriorityQueue()  # fifo sorted list
    came_from = {}  # parent dictionary

    to_visit.put((0, start))
    came_from[start] = None
    cost_so_far[start] = 0
    while not to_visit.empty() and not found:
        current = to_visit.get()[1]
        visited.append(current)
        x, y = current

        if current == goal:
            found = True
        else:
            neighbors = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
            for next in neighbors:
                if next not in visited and is_inside(next, mapM) and is_not_wall(next, mapM):
                    new_cost = cost_so_far[current] + 1
                    if next not in cost_so_far or new_cost < cost_so_far[next]:
                        cost_so_far[next] = new_cost
                        priority = new_cost + manhattan_distance(next, goal)
                        to_visit.put((priority, next))
                        came_from[next] = (x, y)
    if found:
        return get_path(goal, start, came_from)
    else:
        return None

def dfs(mapM, initialX, initialY, finalX, finalY):
    found = False
    start = (initialX, initialY)
    goal = (finalX, finalY)
    visited = []
    to_visit = []
    came_from = {} #parent dictionary

    to_visit.append(start)
    came_from[start] = None

    while len(to_visit) != 0 and not found:
        if not to_visit:
            return False

        current = to_visit[-1]
        visited.append(current)
        x, y = current
        del to_visit[-1]

        if current == goal:
            found = True
        else:
            neighbors = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
            for next in neighbors:
                if next not in visited and is_inside(next, mapM) and is_not_wall(next, mapM):
                    to_visit.append(next)
                    came_from[next] = (x, y)
    if found:
        return get_path(goal, start, came_from)
    else:
        return None


def dummysearch():
    # example of some path in test1.map from [5,7] to [7,11]
    return [[5, 7], [5, 8], [5, 9], [5, 10], [5, 11], [6, 11], [7, 11]]