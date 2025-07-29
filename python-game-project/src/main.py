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

def can_move(new_rect, obstacles, screen_width, screen_height):
    # Check screen boundaries
    if not (0 <= new_rect.left and new_rect.right <= screen_width and 0 <= new_rect.top and new_rect.bottom <= screen_height):
        return False
    # Check collision with obstacles
    for rect in obstacles:
        if new_rect.colliderect(rect):
            return False
    return True

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle key presses
    keys = pygame.key.get_pressed()
    obstacles = game_map.get_obstacle_rects()
    move_x, move_y = 0, 0
    if keys[pygame.K_UP]:
        tim.change_image("assets/Up.png")
        move_y = -10
       
    if keys[pygame.K_DOWN]:
        tim.change_image("assets/Down.png")
        move_y = 10
  
    if keys[pygame.K_LEFT]:
        tim.toggle_image("assets/Left1.png", "assets/Left2.png")  # Alternate between Right1 and Right2
        move_x = -10

    if keys[pygame.K_RIGHT]:
        tim.toggle_image("assets/Right1.png", "assets/Right2.png")  # Alternate between Right1 and Right2
        move_x = 10
      
    # Only move if no collision
    if move_x != 0 or move_y != 0:
        new_rect = tim.get_rect().move(move_x, move_y)
        if can_move(new_rect, obstacles, SCREEN_WIDTH, SCREEN_HEIGHT):
            tim.move(move_x, move_y)
        time.sleep(0.1)

    # Draw everything
    screen.fill((0, 0, 0))  # Clear the screen with black
    game_map.draw(screen)
    tim.draw(screen)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()