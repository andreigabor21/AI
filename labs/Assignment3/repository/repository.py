# -*- coding: utf-8 -*-

import pickle
from random import randint

from domain.Map import Map
from domain.Population import Population


class Repository():

    def __init__(self):
        self.__populations = []
        self.__map = Map()
        self.__drone = [0, 0]
        
    def set_drone_position(self, x, y):
        self.__drone = [x, y]

    def add_individual(self, population, individual):
        population.add_individual(individual, self.__map, self.__drone)

    def evaluate_population(self, population):
        population.evaluate(self.__map, self.__drone)

    def current_population(self) -> Population:
        return self.__populations[-1]

    def createPopulation(self, args):
        # args = [populationSize, individualSize] -- you can add more args    
        return Population(args[0], args[1])

    def add_population(self, population):
        self.__populations.append(population)
        
    def random_drone(self):
        x = randint(0, self.__map.n - 1)
        y = randint(0, self.__map.m - 1)
        while self.__map.surface[x][y] != 0:
            x = randint(0, self.__map.n - 1)
            y = randint(0, self.__map.m - 1)
        self.__drone = [x, y]

    def get_first_path(self):
        return self.__populations[-1].get_first_path(self.__map, self.__drone)

    @property
    def populations(self):
        return self.__populations

    @property
    def map(self):
        return self.__map

    def average_and_deviation(self):
        return self.__populations[-1].compute_average_and_deviation(self.__map, self.__drone)

    @property
    def drone(self):
        return self.__drone