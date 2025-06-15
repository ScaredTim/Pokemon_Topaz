import pygame
from map import GameMap
from character import Character
import time
# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tim's Adventure")

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Load the map and character
game_map = GameMap(SCREEN_WIDTH, SCREEN_HEIGHT)
# tim = Character("assets/timothy.png", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
tim = Character("assets/Down.png", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, width=100, height=100)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle key presses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        tim.change_image("assets/Up.png")
        tim.move(0, -7)
        time.sleep(0.1)  # Optional: Add a small delay for smoother movement
    if keys[pygame.K_DOWN]:
        tim.change_image("assets/Down.png")
        tim.move(0, 7)
        time.sleep(0.1)  # Optional: Add a small delay for smoother movement
    if keys[pygame.K_LEFT]:
        tim.toggle_image("assets/Left1.png", "assets/Left2.png")  # Alternate between Right1 and Right2
        tim.move(-7, 0)
        time.sleep(0.1)  # Optional: Add a small delay for smoother movement
    if keys[pygame.K_RIGHT]:
        tim.toggle_image("assets/Right1.png", "assets/Right2.png")  # Alternate between Right1 and Right2
        tim.move(7, 0)
        time.sleep(0.1)  # Optional: Add a small delay for smoother movement

    # Draw everything
    screen.fill((0, 0, 0))  # Clear the screen with black
    game_map.draw(screen)
    tim.draw(screen)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()