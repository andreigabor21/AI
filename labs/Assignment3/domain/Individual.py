from random import random, randint

from domain.utils import *


class Individual:
    def __init__(self, size = 0):
        self.__size = size
        self.__representation = [randint(1,4) for _ in range(self.__size)]
        self.__fitness = None

    def fitness(self, current_map, drone):
        # compute the fitness for the individual
        # and save it in self.__f
        self.__fitness = 0
        path = self.compute_path(current_map, drone)
        visited = []
        for i in range(len(path)):
            x = path[i][0]
            y = path[i][1]
            if [x, y] not in visited:
                visited.append([x, y])
                if 0 > x or 0 > y or x >= current_map.n or y >= current_map.m:
                    i -= 1
                    self.__fitness -= 1
                    continue
                if current_map.surface[x][y] == WALL:
                    i -= 1
                    self.__fitness -= 2
                    continue
                self.__fitness += 1
                for var in index_variation:
                    while ((0 <= x + var[0] < current_map.n and
                            0 <= y + var[1] < current_map.m) and
                           current_map.surface[x + var[0]][y + var[1]] != WALL):
                        if [x + var[0], y + var[1]] not in visited:
                            visited.append([x + var[0], y + var[1]])
                            self.__fitness += 1
                        x = x + var[0]
                        y = y + var[1]

    def get_fitness(self):
        return self.__fitness

    def compute_path(self, current_map, drone):
        path = [[drone[0], drone[1]]]
        for i in self.__representation:
            next_pos = path[-1]
            next_x = next_pos[0]
            next_y = next_pos[1]
            if i == 1:
                path.append([next_x - 1, next_y])
            elif i == 2:
                path.append([next_x, next_y + 1])
            elif i == 3:
                path.append([next_x + 1, next_y])
            elif i == 4:
                path.append([next_x, next_y - 1])
        return path

    def mutate(self, mutateProbability = 0.04):
        # perform a mutation with respect to the representation
        if random() < mutateProbability:
            self.__representation[randint(0, self.__size - 1)] = randint(1, 4)


    def crossover(self, otherParent, crossoverProbability = 0.8):
        offspring1, offspring2 = Individual(self.__size), Individual(self.__size)
        if random() < crossoverProbability:
            position = randint(0, self.__size - 1)
            offspring1.__representation = otherParent.__representation[:position] + self.__representation[position:]
            offspring2.__representation = self.__representation[:position] + otherParent.__representation[position:]

        return offspring1, offspring2
