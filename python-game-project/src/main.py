import pygame
from map import GameMap, InHouseMap
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
in_house_map = InHouseMap(SCREEN_WIDTH, SCREEN_HEIGHT)
current_map = game_map
in_house = False
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

def draw_boundaries(screen, character):
    # Draw the character's boundary as a blue rectangle
    pygame.draw.rect(screen, (0, 0, 255), character.get_rect(), 2)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle key presses
    keys = pygame.key.get_pressed()
    obstacles = current_map.get_obstacle_rects()
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

    # Check for door entry if on outdoor map
    if not in_house:
        for door_rect in game_map.door_rects:
            if tim.get_rect().colliderect(door_rect):
                current_map = in_house_map
                in_house = True
                # Optionally, reposition Tim inside the house
                tim.x, tim.y = SCREEN_WIDTH // 2, SCREEN_HEIGHT - 120

    # Draw everything
    screen.fill((0, 0, 0))  # Clear the screen with black
    current_map.draw(screen)
    tim.draw(screen)
    draw_boundaries(screen, tim)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()