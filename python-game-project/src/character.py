import pygame

class Character:
    def __init__(self, image_path, x, y, width=50, height=50):
        # Load and scale the image
        original_image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(original_image, (width, height))
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.toggle_state = False  # To track the toggle state for alternating images

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def change_image(self, image_path):
        # Change the character's image and scale it
        self.image = pygame.transform.scale(pygame.image.load(image_path), (self.width, self.height))

    def toggle_image(self, image_path1, image_path2):
        # Alternate between two images
        if self.toggle_state:
            self.change_image(image_path1)
        else:
            self.change_image(image_path2)
        self.toggle_state = not self.toggle_state

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)    

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    