import pygame
from ui import *
from startup import *

window = pygame.display.set_mode((1280, 720))
window.fill((255, 255, 255))
image = pygame.image.load('Game-of-Drones.jpg')


class Button:
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, window, outline=None):  # draw button on screen
        if outline:
            pygame.draw.rect(window, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            pygame.font.init()
            font = pygame.font.Font('got_font.ttf', 27)
            text = font.render(self.text, 1, (0, 0, 0))
            window.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True
        return False


def redrawWindow():
    window.fill((255, 255, 255))
    window.blit(image, (0, 0))
    greenButton.draw(window, (0, 0, 0))
    yellowButton.draw(window, (0, 0, 0))
    blueButton.draw(window, (0, 0, 0))


run = True
greenButton = Button(OLD_GOLD, 30, 520, 340, 100, 'DFS  Exploration')
yellowButton = Button(OLD_GOLD, 450, 520, 340, 100, 'BFS  Teleportation')
blueButton = Button(OLD_GOLD, 870, 520, 340, 100, 'Play')

if __name__ == '__main__':
    while run:
        redrawWindow()
        pygame.display.update()
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if greenButton.isOver(pos):
                    main_dfs()
                elif yellowButton.isOver(pos):
                    main_bfs()
                elif blueButton.isOver(pos):
                    main_play()
                run = False
            if event.type == pygame.MOUSEMOTION:
                if greenButton.isOver(pos):
                    greenButton.color = METALLIC_GOLD
                elif blueButton.isOver(pos):
                    blueButton.color = METALLIC_GOLD
                elif yellowButton.isOver(pos):
                    yellowButton.color = METALLIC_GOLD
                else:
                    greenButton.color = OLD_GOLD
                    blueButton.color = OLD_GOLD
                    yellowButton.color = OLD_GOLD
