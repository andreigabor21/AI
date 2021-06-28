import random


class Ant:
    def __init__(self, starting_sensor, energy=70):
        self.path = []
        self.energy_given = [] # energie pt fiecare senzor
        self.visited_sensors = [starting_sensor] #lista cu senzorii vizitati
        self.energy = energy #nivelul de energie

    def shortest_part_ACO(self, map, distances_between_sensors, pheromone_level, sensors_visibility, alpha=0.8, beta=1.5):
        '''
        Determinam folosind ACO drumul de lungime minima dintre sezori (pasul 3)
        '''
        last_sensor = self.visited_sensors[-1]
        possible_sensors = [] #lista de senzori care se pot vizita ulterior
        for sensor_tuple in distances_between_sensors: #(senzor0, senzor1) -> Path
            if sensor_tuple[0] == last_sensor and sensor_tuple[1] not in self.visited_sensors: #unul dintre ei sa fie ultimul vizitat si urmatorul sa fie nevizitat
                possible_sensors.append([sensor_tuple[1], distances_between_sensors[sensor_tuple]])
            if sensor_tuple[1] == last_sensor and sensor_tuple[0] not in self.visited_sensors:
                possible_sensors.append([sensor_tuple[0], distances_between_sensors[sensor_tuple]])

        #print(possible_sensors)
        probabilities = []
        for s in possible_sensors:
            key = (s[0], last_sensor)
            if key not in pheromone_level.keys():
                key = (last_sensor, s[0])
            distance = s[1].Length
            if distance <= self.energy:
                if pheromone_level[key] != 0: #daca au fost pusi feromoni
                    probabilities.append((1 / distance ** beta) * (pheromone_level[key] ** alpha))
                else: #daca este la prima tura si nu sunt feromoni
                    probabilities.append((1 / distance ** beta))

        # cream lista cu probabilitati
        s = sum(probabilities)
        if s == 0:
            return "No more sensors"
        p = [probabilities[i]/s for i in range(len(probabilities))]
        p = [sum(p[0:i+1]) for i in range(len(p))]
        r = random.random()
        i = 0
        while r > p[i]:
            i = i+1 #alegem cel cu probabilitatea buna din ruleta
        chosen = possible_sensors[i][0]

        self.visited_sensors.append(chosen)
        key = (chosen, last_sensor)
        if key not in pheromone_level:
            key = (last_sensor, chosen)
        pheromone_level[key] += 1 #updatam nevelul de feromoni
        self.energy -= distances_between_sensors[key].Length #scadem energie egala cu lungimea drumului
        return chosen


class Path: #clasa pentru retinerea unui drum si a nivelului de feromoni
    def __init__(self, path):
        self.path = path
        self.length = len(path)
        self.pheromone_level = []

    @property
    def Length(self):
        return self.length
