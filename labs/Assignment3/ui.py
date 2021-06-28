# -*- coding: utf-8 -*-


from repository.repository import Repository
from gui import *
import matplotlib
import matplotlib.pyplot as pl

# create a menu
#   1. map options:
#         a. create random map
#         b. load a map
#         c. save a map
#         d visualise map
#   2. EA options:
#         a. parameters setup
#         b. run the solver
#         c. visualise the statistics
#         d. view the drone moving on a path
#              function gui.movingDrone(currentMap, path, speed, markseen)
#              ATENTION! the function doesn't check if the path passes trough walls


class UI:
    def __init__(self, controller: Controller, repository: Repository):
        self._controller = controller
        self._repository = repository
        self._path = []
        self._stats = []
        self._iterations = []

    def _print_map_options(self):
        print("0. Exit")
        print("1. Create random map")
        print("2. Load a map")
        print("3. Save a map")
        print("4. Visualize map")
        print("5. Move to next menu")

    def _print_second_menu(self):
        print("0. Exit")
        print("1. Parameters setup")
        print("2. Run the solver")
        print("3. Visualise the statistics")
        print("4. View the drone moving on a path")


    def menu(self):
        while True:
            self._print_map_options()
            option = int(input("Read>>"))
            if option == 0:
                break
            if option == 1:
                self._random_map()
            elif option == 2:
                self._load_map()
            elif option == 3:
                self._save_map()
            elif option == 4:
                self._visualize_map()
            elif option == 5:
                self._second_menu()
            else:
                print("Invalid option")



    def _second_menu(self):
        while True:
            self._print_second_menu()
            option = int(input("Read>>"))
            if option == 0:
                break
            if option == 1:
                self._parameter_setup()
            elif option == 2:
                self._run_solver()
            elif option == 3:
                self._view_statistics()
            elif option == 4:
                self._view_drone_moving()
            else:
                print("Invalid option")


    def _random_map(self):
        self._repository.map.randomMap()
        self._repository.random_drone()
        print(self._repository.drone)

    def _load_map(self):
        file_name = input("Map file>>")
        if file_name == "":
            self._repository.map.loadMap("test1.map")
        else:
            self._repository.map.loadMap(file_name)

    def _save_map(self):
        file_name = input("Map file>>")
        self._repository.map.saveMap(file_name)


    def _visualize_map(self):
        visualize_map(self._controller, self._repository)

    def _parameter_setup(self):
        file_name = input("Read file>>")
        if file_name == "":
            file_name = "parameters.txt"
        f = open(file_name, "r")
        i = 0
        for line in f:
            if i == 0:
                pass
                l = line.split(",")
                self._controller.set_drone_position(int(l[0]), int(l[1]))
            elif i == 1:
                self._controller.set_individual_size(int(line))
            elif i == 2:
                self._controller.set_iterations(int(line))
            elif i == 3:
                self._controller.set_population_size(int(line))
            elif i == 4:
                self._controller.set_mutation_prob(float(line))
            elif i == 5:
                self._controller.set_crossover_prob(float(line))
            elif i == 6:
                self._controller.set_seeds(int(line))
            else:
                break
            i += 1
        self._controller.print_for_test()
        f.close()


    def _run_solver(self):
        self._path, self._stats = self._controller.solver()
        # print(self._stats)
        self._view_drone_moving()


    def _view_statistics(self):
        x = []
        average = []
        deviations = []
        for i in range(len(self._stats)):
            x.append(i)
            average.append(self._stats[i][0])
            deviations.append(self._stats[i][1])
        pl.plot(x, average)
        pl.plot(x, deviations)
        pl.show()


    def _view_drone_moving(self):
        print("PATH: ", self._path)
        movingDrone(self._repository.map, self._path, 0.4)





        