import pygame

class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.color = (144, 238, 144)  # Light Green background for the map
         # Load and scale the flower image once
        flower_img = pygame.image.load("./assets/flower.png")
        self.flower_img = pygame.transform.scale(flower_img, (40, 40))

    def draw_tree(self, screen, x, y, trunk_width=30, trunk_height=90, leaves_radius=40):
        dark_green = (0, 100, 0)
        trunk_color = (101, 67, 33)
        # Draw trunk
        pygame.draw.rect(screen, trunk_color, (x, y, trunk_width, trunk_height))
        # Draw leaves (circle centered above the trunk)
        pygame.draw.circle(screen, dark_green, (x + trunk_width // 2, y), leaves_radius)

    def draw_house(self, screen, x, y, width=200, height=160, door_width=40, door_height=70):
        house_color = (139, 69, 19)
        roof_color = (255, 0, 0)
        door_color = (210, 180, 140)
        # Draw house body
        pygame.draw.rect(screen, house_color, (x, y, width, height))
        # Draw roof (triangle)
        pygame.draw.polygon(
            screen,
            roof_color,
            [
                (x, y),  # left corner
                (x + width // 2, y - height // 2),  # top peak
                (x + width, y)  # right corner
            ]
        )
        # Draw door (centered)
        door_x = x + width // 2 - door_width // 2
        door_y = y + height - door_height
        pygame.draw.rect(screen, door_color, (door_x, door_y, door_width, door_height))
        # Optional: door knob
        pygame.draw.circle(screen, (160, 82, 45), (door_x + door_width - 10, door_y + door_height // 2), 5)

    def draw_flower(self, screen, x, y):
        # Draw the flower image at (x, y)
        screen.blit(self.flower_img, (x, y))

    def draw(self, screen):
        # Fill the screen with the map color
        screen.fill(self.color)

        # Draw houses using draw_house
        self.draw_house(screen, 120, 100)
        self.draw_house(screen, 500, 100)

      # Draw big trees on the edges using draw_tree
      #Left trees
        self.draw_tree(screen, 30, 64)
        self.draw_tree(screen, 30, 200)
        self.draw_tree(screen, 30, 336)
        self.draw_tree(screen, 30, 472)
        #Right trees
        self.draw_tree(screen, 740, 64)
        self.draw_tree(screen, 740, 200)
        self.draw_tree(screen, 740, 336)
        self.draw_tree(screen, 740, 472)
        #Bottom trees
        self.draw_tree(screen, 120, 502)
        self.draw_tree(screen, 210, 502)
        self.draw_tree(screen, 300, 502)
        self.draw_tree(screen, 390, 502)
        self.draw_tree(screen, 480, 502)
        self.draw_tree(screen, 570, 502)
        self.draw_tree(screen, 660, 502)

        # Draw some flowers
        self.draw_flower(screen, 200, 300)
        self.draw_flower(screen, 400, 200)
        self.draw_flower(screen, 600, 350)