import pygame

class Character:
    # def __init__(self, image_path, x, y):
    #     self.image = pygame.image.load(image_path)
    #     self.x = x
    #     self.y = y

    def __init__(self, image_path, x, y, width=50, height=50):
        # Load and scale the image
        original_image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(original_image, (width, height))
        self.x = x
        self.y = y

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))