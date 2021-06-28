
import copy

from domain.Individual import *
import numpy as np


class Population():
    def __init__(self, populationSize=0, individualSize=0):
        self.__populationSize = populationSize
        self.__population = [Individual(individualSize) for _ in range(populationSize)]

    def evaluate(self, map, drone):
        # evaluates the population
        for x in self.__population:
            x.fitness(map, drone)

    def selection(self, k=0):
        # perform a selection of k individuals from the population
        # and returns that selection
        selected = []
        individuals_copy = copy.deepcopy(self.__population)
        individuals_copy.sort(key = lambda x : x.get_fitness(), reverse = True)
        for i in range(0, k):
            selected.append(individuals_copy[i])
        return selected


    def add_individual(self, individual: Individual, map, drone):
        individual.fitness(map, drone)
        self.__population.append(individual)

    def get_first_path(self, map, drone):
        individual_copy = copy.deepcopy(self.__population)
        individual_copy.sort(key = lambda x : x.get_fitness(), reverse = True)
        # print(individual_copy[0].compute_path(map, drone))
        return individual_copy[0].compute_path(map, drone)

    def compute_average_and_deviation(self, map, drone):
        fitness = []
        for x in self.__population:
            x.fitness(map, drone)
            fitness.append(x.get_fitness())
        return [np.average(fitness), np.std(fitness)]

    @property
    def population(self):
        return self.__population

    @population.setter
    def population(self, other):
        self.__population = other

    def __getitem__(self, item):
        return self.__population[item]

    def __setitem__(self, key, value):
        self.__population[key] = value

    def __len__(self):
        return len(self.__population)