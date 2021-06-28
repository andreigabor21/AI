'''
min functiei f(x) = x_1^2 + ... + x_n^2
'''
from random import random, randint


def individual(length, vmin, vmax):
    '''
    Create a member of the population - an individual
    :param length: number of genes
    :param vmin: min possible value
    :param vmax: max possible value
    '''
    return [ (random() * (vmax - vmin) + vmin) for _ in range(length) ]

def population(count, length, vmin, vmax):
    '''
    Create a number of individuals (population)
    :param count: number of individuals in the population
    :param length: number of values per individual
    :param vmin: min possible value
    :param vmax: max possible value
    :return:
    '''
    return [ individual(length, vmin, vmax) for _ in range(count) ]

def fitness(individual):
    '''
    Determine the fitness of an individual. Lower is better (min problem)
    For this problem we have the Rastrigin function
    :param individual:
    :return:
    '''
    sum = 0
    for number in individual:
        sum += number ** 2
    return sum

def mutate(individual, pM, vmin, vmax):
    '''
    Performs a mutation on an individual with the probability pM.
    If the event will take place, at a random position a new value will be
    generated in the interval [vmin, vmax]
    :param individual: the individual to be mutated
    :param pM: the probability of the mutation to occure
    :param vmin: min possible value
    :param vmax: max possible value
    :return:
    '''
    if random() < pM:
        p = randint(0, len(individual) - 1)
        individual[p] = random() * (vmax - vmin) + vmin
    return individual

def crossover(parent1, parent2):
    '''
    crossover between 2 parents
    '''
    child = []
    alpha = random()
    for i in range(len(parent1)):
        child.append(alpha * (parent1[i] - parent2[i]) + parent2[i])
    return child

def iteration(pop, pM, vmin, vmax):
    '''
    an iteration
    :param pop: the current population
    :param pM: the prob of the mutation to occure
    :param vmin: min possible value
    :param vmax: max possible value
    :return:
    '''
    ind1 = randint(0, len(pop) - 1)
    ind2 = randint(0, len(pop) - 1)
    if ind1 != ind2:
        c = crossover(pop[ind1], pop[ind2])
        c = mutate(c, pM, vmin, vmax)
        f1 = fitness(pop[ind1])
        f2 = fitness(pop[ind2])
        '''
        The repeated evaluation of the parents can be avoided if 
        next to the values stored in the individuals we keep also their fitnesses
        '''
        fc = fitness(c)
        if f1 > f2 and f1 > fc:
            pop[ind1] = c
        if f1 < f2 and f2 > fc:
            pop[ind2] = c
    return pop

def main(noIteratii = 200):
    #PARAMETERS:

    #population size
    dimPopulation = 100
    #individual size
    dimIndividual = 2
    #the boundaries of the search interval
    vmin = -5.12
    vmax = 5.12
    #the mutation probability
    pM = 0.01

    p = population(dimPopulation, dimIndividual, vmin, vmax)
    for i in range(noIteratii):
        p = iteration(p, pM, vmin, vmax)

    #print the best individual
    graded = [ (fitness(x), x) for x in p ]
    graded = sorted(graded)
    result = graded[0]
    fitnessOptim = result[0]
    individualOptim = result[1]
    print('Result: The detected minimum point after %d iterations is f(%3.2f %3.2f) = %3.2f' % \
          (noIteratii, individualOptim[0], individualOptim[1], fitnessOptim))
    print(individualOptim)
main()


# indiv1 = individual(4, 2, 6)
# indiv2 = individual(4, 2, 6)
# print("Indiv1: ", indiv1)
# print("Indiv2: ",indiv2)
# print(crossover(indiv1, indiv2))
#
# # print("After mutation: ", mutate(indiv, 0.5, 2, 6))
# # print(fitness(indiv))
# print(population(3, 2, 2, 4))