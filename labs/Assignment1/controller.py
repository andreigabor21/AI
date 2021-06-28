import pygame
from ui import *
from constants import *
stack = []
visited = {}


class Drone:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @staticmethod
    def setupVisited():
        for i in range(20):
            for j in range(20):
                visited[i, j] = 0

    def move(self, detectedMap):
        pressed_keys = pygame.key.get_pressed()
        if self.x > 0:
            if pressed_keys[K_UP] and detectedMap.surface[self.x - 1][self.y] == 0:
                self.x = self.x - 1
        if self.x < 19:
            if pressed_keys[K_DOWN] and detectedMap.surface[self.x + 1][self.y] == 0:
                self.x = self.x + 1

        if self.y > 0:
            if pressed_keys[K_LEFT] and detectedMap.surface[self.x][self.y - 1] == 0:
                self.y = self.y - 1
        if self.y < 19:
            if pressed_keys[K_RIGHT] and detectedMap.surface[self.x][self.y + 1] == 0:
                self.y = self.y + 1

    def can_go_LEFT(self, detectedMap):
        return self.y - 1 >= 0 and detectedMap.surface[self.x][self.y - 1] == 0 and visited[self.x, self.y - 1] == 0

    def can_go_RIGHT(self, detectedMap):
        return self.y + 1 < 20 and detectedMap.surface[self.x][self.y + 1] == 0 and visited[self.x, self.y + 1] == 0

    def can_go_UP(self, detectedMap):
        return self.x - 1 >= 0 and detectedMap.surface[self.x - 1][self.y] == 0 and visited[self.x - 1, self.y] == 0

    def can_go_DOWN(self, detectedMap):
        return self.x + 1 < 20 and detectedMap.surface[self.x + 1][self.y] == 0 and visited[self.x + 1, self.y] == 0

    def moveDFS(self, detectedMap):
        append = True
        if self.can_go_UP(detectedMap):
            self.x -= 1
        elif self.can_go_RIGHT(detectedMap):
            self.y += 1
        elif self.can_go_DOWN(detectedMap):
            self.x += 1
        elif self.can_go_LEFT(detectedMap):
            self.y -= 1
        else:
            append = False
            stack.pop()
            if len(stack):
                self.x, self.y = stack[-1]
        if append:
            stack.append((self.x, self.y))
            visited[self.x, self.y] = 1

        # TO DO!
        # rewrite this function in such a way that you perform an automatic
        # mapping with DFS

    def moveBFS(self, detectedMap):
        if self.can_go_UP(detectedMap):
            stack.append((self.x - 1, self.y))
            visited[self.x-1, self.y] = 1
        if self.can_go_RIGHT(detectedMap):
            stack.append((self.x, self.y + 1))
            visited[self.x, self.y+1] = 1
        if self.can_go_DOWN(detectedMap):
            stack.append((self.x + 1, self.y))
            visited[self.x+1, self.y] = 1
        if self.can_go_LEFT(detectedMap):
            stack.append((self.x, self.y - 1))
            visited[self.x, self.y-1] = 1
        self.x, self.y = stack.pop(0)