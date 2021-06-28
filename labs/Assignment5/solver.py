# -*- coding: utf-8 -*-
"""
In this file your task is to write the solver function!

"""
from random import randint
from utils import *
from fuzzy import *


def functions(ranges: dict) -> dict:
    # associates a fuzzy function to a given range (fuzzy_set -> interval)
    # return a map: fuzzy_set -> fuzzyfier
    return {fuzzy_set: Fuzzyfier(*interval) for (fuzzy_set, interval) in ranges.items()}

def caculate_fuzzy_value(value: int, functions: dict) -> dict:
    # calculates for each fuzzy set, it's values in (0, 1)
    return {fuzzy_set: function.compute_fuzzy_triangle(value) for (fuzzy_set, function) in functions.items()}

thetaFunctions = functions(thetaRanges)
omegaFunctions = functions(omegaRanges)

def solver(t, w):
    """
       Parameters
       ----------
       t : TYPE: float
           DESCRIPTION: the angle theta
       w : TYPE: float
           DESCRIPTION: the angular speed omega
       Returns
       -------
       F : TYPE: float
           DESCRIPTION: the force that must be applied to the cart
       or
       None :if we have a division by zero
       """

    # compute the membership degrees for θ and ω to each set using the data from diagrams
    thetaValues = caculate_fuzzy_value(t, thetaFunctions)
    omegaValues = caculate_fuzzy_value(w, omegaFunctions)

    degree_F = {}

    for thetaSet in fuzzyTable:
        for omegaSet, fSet in fuzzyTable[thetaSet].items(): # omegaSet = key, fSet = values
            # we take the minimum of the membership values of the index set
            value = min(thetaValues[thetaSet], omegaValues[omegaSet])
            if fSet not in degree_F:
                degree_F[fSet] = value
            else:
                # The membership degree of F to each class will be the maximum value for that class taken from the rules’ table
                degree_F[fSet] = max(value, degree_F[fSet])

    s = sum(degree_F.values())
    if s == 0:
        return

    # defuzzify the results for F using a weighted average of the membership degrees
    # and the b values of the sets
    defuzzy = 0
    for fSet in degree_F.keys():
        defuzzy += degree_F[fSet] * vectors[fSet]
    defuzzy /= s

    return defuzzy