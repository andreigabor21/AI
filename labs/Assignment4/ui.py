from controller import *
import pygame
import time

n = 20
m = 20
map = Map(n, m)
pygame.init()
screen = pygame.display.set_mode((20 * n, 20 * m))
screen.fill(WHITE)
# screen.blit(map.image(), (0, 0))
pygame.display.flip()
map.randomMap()
# map.loadMap("test.map")
# sensors = [(1, 2), (15, 4), (5, 15), (10, 10), (19, 18)]
sensors = []
for i in range(5):
    x = random.randint(0, n-1)
    y = random.randint(0, m-1)
    sensors.append((x, y))
map.Sensors = sensors


if __name__ == '__main__':
    controller = Controller(screen, map)
    #res = controller.searchAStar(map, 1, 2, 15, 4, screen)

    best = controller.run()
    screen.blit(map.image_path([]), (0, 0))
    pygame.display.flip()
    time.sleep(3)
    for i in range(len(best)):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        pygame.time.delay(15)
        sal = best[:i]
        screen.blit(map.image_path(sal), (0, 0))
        pygame.display.flip()
        pygame.display.update()
    time.sleep(10)

# print(res)

# print(map.surface)


