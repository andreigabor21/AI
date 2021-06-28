from constants import *
from ant import Path, Ant
from map import *


class Controller:
    def __init__(self, screen, map=Map()):
        self.sensors_visibility = {}
        self.ant_count = 20
        self.map = map
        self.compute_sensors()
        self.g = numpy.full((map.n, map.m), numpy.inf)
        self.f = numpy.full((map.n, map.m), numpy.inf)
        self.screen = screen
        self.minimum_distance_between_sensors = {}
        self.pheromone_level_between_sensors = {}


    def compute_minimum_distance_between_sensors(self):
        #determinam distanta minima dintre fiecare pereche de senzori (pasul 2)
        sensors = self.map.sensors
        for i in range(len(sensors)-1):
            for j in range(i + 1, len(sensors)): #calculam distanta dintre cei doi cu A*
                path = Path(self.searchAStar(self.map, sensors[i][0], sensors[i][1], sensors[j][0], sensors[j][1], self.screen))
                self.minimum_distance_between_sensors[(sensors[i], sensors[j])] = path
                self.pheromone_level_between_sensors[(sensors[i], sensors[j])] = 0
        return self.minimum_distance_between_sensors

    def run(self, rho=0.1, iterations=400):
        #pentru iteratii
        self.compute_minimum_distance_between_sensors()
        best_ant = -1
        paths = self.minimum_distance_between_sensors
        for k in range(iterations):
            minim = numpy.inf
            for _ in range(self.ant_count):
                ant_path, energy_left = self.compute_one_ant()
                if k == iterations - 1:
                    res = []
                    for i in range(len(ant_path)-1):
                        key = (ant_path[i], ant_path[i+1])
                        if key not in paths:
                            key = (ant_path[i+1], ant_path[i])
                            res.extend(paths[key].path[::-1])
                        else:
                            res.extend(paths[key].path)
                    # length = self.seen_by_sensors(ant_path, energy_left)
                    length = len(res)
                    if minim > length:
                        minim = length
                        best_one = res
                        best_ant = (ant_path, energy_left)
            for key in self.pheromone_level_between_sensors:
                #scadem nivelul de feromoni cu rho dupa fiecare tura de furnici (se evapora)
                self.pheromone_level_between_sensors[key] *= rho
        self.seen_by_sensors(best_ant[0], best_ant[1])
        return best_one

    def compute_sensors(self):
        ''' pasul 1
            Verificam la toti senzorii cat vad pentru o anumita energie intre 0 si 5
        '''
        sensors = self.map.sensors
        visibility = {} #mapare dintre un senzor cu lista cu cat vede per energie

        for sensor in sensors:
            seen = [0, 0, 0, 0, 0] #prima pozitie este by default cu 0 pentru ca nu poate vedea cu 0 energie
            x = sensor[0]
            y = sensor[1]
            for d in directions:
                for i in range(1, 6):
                    new_x = x + d[0] * i
                    new_y = y + d[1] * i
                    if 0 <= new_x < self.map.n and 0 <= new_y < self.map.m and self.map.surface[new_x][new_y] == 0:
                        seen[i-1] += 1
                    else:
                        break
            visibility[sensor] = seen
        self.sensors_visibility = visibility
        #return visibility

    def best_node(self, nodes):
        queue = list(nodes.keys())
        best_index = 0
        for i in range(len(queue)):
            if nodes[queue[i]] < nodes[queue[best_index]]:
                best_index = i
        result = queue[best_index]
        return result

    def h(self, x, y, finalX, finalY):
        return abs(finalX - x) + abs(finalY - y)

    def searchAStar(self,mapM, initialX, initialY, finalX, finalY, screen):
        #functie pentru calculat distanta dintre 2 sezori

        current_node = (initialX, initialY)
        open_nodes = {(initialX, initialY): 0}
        visited = []
        parents = {}

        while len(open_nodes) > 0:
            current_node = self.best_node(open_nodes)
            del open_nodes[current_node]
            visited.append(current_node)
            if current_node[0] == finalX and current_node[1] == finalY:
                return self.path(parents, (initialX, initialY), current_node)

            for d in directions:
                x = current_node[0] + d[0]
                y = current_node[1] + d[1]
                if (x, y) not in visited:
                    if 0 <= x < mapM.n and 0 <= y < mapM.m:
                        if mapM.surface[x][y] == 0 or mapM.surface[x][y] == 2:
                            if self.g[current_node[0]][current_node[1]] + 1 < self.g[x][y] or (x, y) not in open_nodes:
                                self.f[x][y] = self.g[current_node[0]][current_node[1]] + 1 + self.h(x, y, finalX, finalX)
                                parents[(x, y)] = current_node
                                if (x, y) not in open_nodes:
                                    open_nodes[(x, y)] = self.f[x][y]
        return []

    def path(self, parents, start_node, final_node):
        #auxiliara pentru A*
        current_node = parents[final_node]
        path = [final_node]
        while current_node != start_node:
            path.append(current_node)
            current_node = parents[current_node]
        path.append(start_node)
        path.reverse()
        return path

    def compute_one_ant(self):
        #iteratie pentru o furnica
        first_sensor = random.choice(self.map.sensors)
        ant = Ant(first_sensor)
        sensors_order = [first_sensor]
        for _ in range(len(self.map.sensors) - 1):
            new_sensor = ant.shortest_part_ACO(self.map, self.minimum_distance_between_sensors, self.pheromone_level_between_sensors, self.sensors_visibility)
            if new_sensor != "No more sensors":
                sensors_order.append(new_sensor)

        return sensors_order, ant.energy

    def seen_by_sensors(self, sensors_order, energy_left):
        # pasul 4 - scadem energia pentru senzor
        count = 0
        left_to_each_sensor = [0 for _ in range(len(sensors_order))]
        while energy_left:
            sensor = -1
            maximum_visibility_for_one_sensor = 0
            for i in range(len(sensors_order)):
                if left_to_each_sensor[i] < 4:
                    seen_count = self.sensors_visibility[sensors_order[i]][left_to_each_sensor[i]]
                    # print(seen_count)
                    if seen_count > maximum_visibility_for_one_sensor:
                        maximum_visibility_for_one_sensor = seen_count
                        sensor = i
            if sensor == -1:
                break
            left_to_each_sensor[sensor] += 1
            count += maximum_visibility_for_one_sensor
            energy_left -= 1

        seen_squares = set()
        for sensor in sensors_order:
            for d in directions:
                for e in range(1, left_to_each_sensor[sensors_order.index(sensor)] + 1):
                    x = sensor[0] + d[0] * e
                    y = sensor[1] + d[1] * e
                    if 0 <= x < self.map.n and 0 <= y < self.map.m and self.map.surface[x][y] == 0:
                        seen_squares.add((x, y))
                        self.map.surface[x][y] = 3
                    else:
                        break

        #print("Seen:", len(seen_squares))
        print("Sensor order:", sensors_order)
        #print("Left to sensors:", left_to_each_sensor)

        return count, sensors_order, left_to_each_sensor
