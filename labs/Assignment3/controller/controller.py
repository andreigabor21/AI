import time
from random import randint, seed

import pygame

from repository.repository import Repository
from domain.Population import *


class Controller():
    def __init__(self, repository: Repository):
        self.__repository = repository
        self.__population_size = 50
        self.__individual_size = 10
        self.__crossover_probability = 0.4
        self.__mutation_probability = 0.1
        self.__number_of_iterations = 100
        self.__number_of_seeds = 10
        self.__statistics = []
        self.__iteration_count = 1

    def set_drone_position(self, x, y):
        self.__repository.set_drone_position(x, y)

    def set_individual_size(self, new_size):
        self.__individual_size = new_size

    def set_iterations(self, new_iterations):
        self.__number_of_iterations = new_iterations

    def set_population_size(self, new_size):
        self.__population_size = new_size

    def set_mutation_prob(self, new_prob):
        self.__mutation_probability = new_prob

    def set_seeds(self, new_seeds):
        self.__number_of_seeds = new_seeds

    def set_crossover_prob(self, new_prob):
        self.__crossover_probability = new_prob

    def set_args(self, args):
        self.__repository.createPopulation(args)

    def iteration(self, args = 0):
        # args - list of parameters needed to run one iteration
        # a iteration:
        # selection of the parrents
        # create offsprings by crossover of the parents
        # apply some mutations

        # print("Iteration: ", self.__iteration_count)
        self.__iteration_count += 1

        population = self.__repository.current_population()
        self.__repository.evaluate_population(population)
        select = population.selection(self.__population_size - 2)
        parents = select[:len(select) // 2]
        pairs = len(parents) // 2
        used_pairs = []
        for i in range(pairs):
            first = parents[randint(0, len(parents) - 1)]
            second = parents[randint(0, len(parents) - 1)]
            if [first, second] not in used_pairs:
                used_pairs.append([first, second])
                first_crossed, second_crossed = first.crossover(second, self.__crossover_probability)
                first.mutate(self.__mutation_probability)
                second_crossed.mutate(self.__mutation_probability)
                self.__repository.add_individual(population, first_crossed)
                self.__repository.add_individual(population, second_crossed)
        population.population = select

    def run(self, args = 0):
        # args - list of parameters needed in order to run the algorithm

        # until stop condition
        #    perform an iteration
        #    save the information need it for the satistics

        # return the results and the info for statistics
        f = []
        stats = []
        for i in range(0, self.__number_of_iterations):
            self.iteration()
            stats.append(self.__repository.average_and_deviation())
        # print(stats)
        for elem in stats:
            f.append(elem[0])
        self.__statistics.append([np.average(f), np.std(f)])


    def solver(self, args = 0):
        # args - list of parameters needed in order to run the solver

        # create the population,
        # run the algorithm
        # return the results and the statistics
        start_time = time.time()
        for i in range(self.__number_of_seeds):
            seed(30 - i)
            population = self.__repository.createPopulation([self.__population_size, self.__individual_size])
            self.__repository.add_population(population)
            self.run()
            # print(self.__statistics[i])
        end_time = time.time()
        print(f"{end_time - start_time} seconds")
        return self.__repository.get_first_path(), self.__statistics

    
    def map_with_drone(self, mapImage):
        drona = pygame.image.load("drona.png")
        # mapImage.blit(drona, (0, 0))
        mapImage.blit(drona, (0, 0))
        return mapImage


    def print_for_test(self):
        print(self.__population_size, self.__individual_size, self.__crossover_probability,
              self.__mutation_probability, self.__number_of_iterations, self.__number_of_seeds)


       