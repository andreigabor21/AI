from domain import *
from service import *
import time

# def displayWithPath(image, path):
#     mark = pygame.Surface((20, 20))
#     mark.fill(GREEN)
#     for move in path:
#         image.blit(mark, (move[1] * 20, move[0] * 20))
#
#     return image
def displayWithPath(image, path):
    mark = pygame.Surface((40, 40))
    mark.fill(GREEN)
    for move in path:
        image.blit(mark, (move[1] * 40, move[0] * 40))
    drona = pygame.image.load("rsz_drone.jpg").convert()
    move = path[0]
    image.blit(drona, (move[1] * 40, move[0] * 40))
    end = pygame.image.load("flag.png").convert()
    move = path[-1]
    image.blit(end, (move[1] * 40, move[0] * 40))
    return image

# define a main function
def main():
    # we create the map
    m = Map()
    # m.randomMap()
    # m.saveMap("test2.map")
    m.loadMap("test1.map")

    # initialize the pygame module
    pygame.init()
    # load and set the logo
    logo = pygame.image.load("logo32x32.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("Path in simple environment")

    # we position the drone somewhere in the area
    # x = randint(0, 19)
    # y = randint(0, 19)
    x = 0
    y = 3
    # create drone
    d = Drone(x, y)

    # create a surface on screen that has the size of 400 x 480
    screen = pygame.display.set_mode((800, 800))
    screen.fill(WHITE)

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

            # if event.type == KEYDOWN:
            #     d.move(m)  # this call will be erased

        screen.blit(d.mapWithDrone(m.image()), (0, 0))
        pygame.display.flip()

    begin_time = time.time()
    path = searchAStar(m, x, y, 19, 19)
    end_time = time.time()
    if path is not None:
        screen.blit(displayWithPath(m.image(), path), (0, 0))
    else:
        print("Unreachable point")
    print("Time: ", end_time - begin_time)
    pygame.display.flip()
    time.sleep(100)
    pygame.quit()


# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    # call the main function
    main()