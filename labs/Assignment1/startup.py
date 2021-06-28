from controller import *
from ui import *


# define a main function
def main_dfs():
    # we create the environment
    e = Environment()
    e.loadEnvironment("test2.map")
    # print(str(e))

    # we create the map
    m = DMap()

    # initialize the pygame module
    pygame.init()
    # load and set the logo
    logo = pygame.image.load("logo32x32.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("drone exploration")

    # we position the drone somewhere in the area
    x = randint(0, 19)
    y = randint(0, 19)

    # cream drona
    d = Drone(x, y)

    # create a surface on screen that has the size of 800 x 480
    screen = pygame.display.set_mode((800, 400))
    screen.fill(WHITE)
    screen.blit(e.image(), (0, 0))

    # define a variable to control the main loop
    running = True
    d.setupVisited()
    stack.append((x, y))

    while running:
        m.markDetectedWalls(e, d.x, d.y)
        d.moveDFS(m)
        screen.blit(m.image(d.x, d.y), (400, 0))
        pygame.display.flip()
        time.sleep(0.05)
        if not len(stack):
            running = False

    x, y = None, None
    pygame.quit()


def main_play():
    # we create the environment
    e = Environment()
    e.loadEnvironment("test2.map")
    # print(str(e))

    # we create the map
    m = DMap()

    # initialize the pygame module
    pygame.init()
    # load and set the logo
    logo = pygame.image.load("logo32x32.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("drone exploration")

    # we position the drone somewhere in the area
    x = randint(0, 19)
    y = randint(0, 19)

    # cream drona
    d = Drone(x, y)

    # create a surface on screen that has the size of 800 x 480
    screen = pygame.display.set_mode((800, 400))
    screen.fill(WHITE)
    screen.blit(e.image(), (0, 0))

    # define a variable to control the main loop
    running = True

    # main loop
    while running:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
            if event.type == KEYDOWN:
                # use this function instead of move
                # d.moveDSF(m)
                d.move(m)
        m.markDetectedWalls(e, d.x, d.y)
        screen.blit(m.image(d.x, d.y), (400, 0))
        pygame.display.flip()

    pygame.quit()


def main_bfs():
    # we create the environment
    e = Environment()
    e.loadEnvironment("test2.map")
    # print(str(e))

    # we create the map
    m = DMap()

    # initialize the pygame module
    pygame.init()
    # load and set the logo
    logo = pygame.image.load("logo32x32.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("drone exploration")

    # we position the drone somewhere in the area
    x = randint(0, 19)
    y = randint(0, 19)

    # cream drona
    d = Drone(x, y)

    # create a surface on screen that has the size of 800 x 480
    screen = pygame.display.set_mode((800, 400))
    screen.fill(WHITE)
    screen.blit(e.image(), (0, 0))

    # define a variable to control the main loop
    running = True
    d.setupVisited()
    stack.append((x, y))

    while running:
        m.markDetectedWalls(e, d.x, d.y)
        d.moveBFS(m)
        screen.blit(m.image(d.x, d.y), (400, 0))
        pygame.display.flip()
        time.sleep(0.3)
        if not len(stack):
            running = False

    x, y = None, None
    pygame.quit()
