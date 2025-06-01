import pygame

class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.color = (34, 139, 34)  # Green background for the map

    def draw(self, screen):
        # Fill the screen with the map color
        screen.fill(self.color)