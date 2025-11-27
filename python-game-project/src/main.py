import pygame
import json
from map import GameMap, InHouseMap
from character import Character
from menu import Menu, BagMenu
from battle import Battle, Battler
import time
import random
import os
os.chdir(os.path.dirname(__file__))
# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
mom_dialogue_index = 0
# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tim's Adventure")

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Load the map and character
game_map = GameMap(SCREEN_WIDTH, SCREEN_HEIGHT)
in_house_map = InHouseMap(SCREEN_WIDTH, SCREEN_HEIGHT)
in_house_map2 = InHouseMap(SCREEN_WIDTH, SCREEN_HEIGHT)

current_map = game_map
in_house = False
# tim = Character("assets/timothy.png", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
tim = Character("assets/Down.png", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, width=80, height=100)

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

menu = Menu(SCREEN_WIDTH, SCREEN_HEIGHT)
bag_menu = BagMenu(SCREEN_WIDTH, SCREEN_HEIGHT)

# Load player and enemy info from JSON
with open("data/battle/player_data.json") as f:
    player_data = json.load(f)
with open("data/battle/enemy_data.json") as f:
    enemy_data = json.load(f)

current_enemy_key = random.choice(list(enemy_data.keys()))
enemy_info = enemy_data[current_enemy_key]

player = Battler(
    name=player_data["name"],
    level=player_data["level"],
    hp=player_data["hp"],
    hp_max=player_data["hp_max"],
    attack=player_data["attack"],
    defense=player_data["defense"],
    moves=player_data["moves"],
    move_info=player_data["move_info"]
)

enemy = Battler(
    name=enemy_info["name"],
    level=enemy_info["level"],
    hp=enemy_info["hp"],
    hp_max=enemy_info["hp_max"],
    attack=enemy_info["attack"],
    defense=enemy_info["defense"],
    moves=enemy_info["moves"],
    move_info=enemy_info["move_info"]
)

battle = Battle(SCREEN_WIDTH, SCREEN_HEIGHT, player, enemy)

# Game loop
font = pygame.font.SysFont(None, 28)
box_width = 320  # Or whatever width you use for your text box
running = True
while running:
    space_pressed = False
    x_pressed = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
       

        menu.handle_event(event)  # <-- handle menu events here   
        if menu.open and menu.options[menu.selected] == "Bag":
        # If Enter was pressed, open the bag menu
        # You need a way to detect that Enter was pressed this frame
        # For example, set a flag in Menu.handle_event when Enter is pressed:
            if getattr(menu, "enter_pressed", False):
                bag_menu.open = True
                menu.enter_pressed = False  # Reset the flag
                menu.open = False           # Close main menu when bag opens

        # Also, handle events for bag_menu if it's open:
        if bag_menu.open:
            bag_menu.handle_event(event)
            # After menu.handle_event(event)
            if menu.open and getattr(menu, "enter_pressed", False):
                if menu.options[menu.selected] == "Bag":
                    bag_menu.open = True
                    menu.open = False  # Close main menu
                    menu.enter_pressed = False  # Reset flag
        
        if menu.open and menu.options[menu.selected] == "Test Battle":
        # If Enter was pressed, open the bag menu
        # You need a way to detect that Enter was pressed this frame
        # For example, set a flag in Menu.handle_event when Enter is pressed:
            if getattr(menu, "enter_pressed", False):
                battle.open = True
                battle.just_opened = True 
                menu.enter_pressed = False  # Reset the flag
                menu.open = False           # Close main menu when bag opens
                # Play battle music loop
                pygame.mixer.music.load("./assets/music/DecisiveEncounter.mp3")
                pygame.mixer.music.play(-1)  # -1 means loop forever
        # If in battle mode, only handle battle events
        if battle.open:
            if battle.just_opened:
                battle.just_opened = False  # Skip input for this frame
            else:
                battle.handle_event(event)
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                # Pick a random different enemy
                enemy_keys = list(enemy_data.keys())
                enemy_keys.remove(current_enemy_key)
                if enemy_keys:
                    new_enemy_key = random.choice(enemy_keys)
                    current_enemy_key = new_enemy_key
                    enemy_info = enemy_data[current_enemy_key]
                    enemy = Battler(
                        name=enemy_info["name"],
                        level=enemy_info["level"],
                        hp=enemy_info["hp"],
                        hp_max=enemy_info["hp_max"],
                        attack=enemy_info["attack"],
                        defense=enemy_info["defense"],
                        moves=enemy_info["moves"],
                        move_info=enemy_info["move_info"]
                    )
                  
                    battle.enemy = enemy
            if not battle.open:
                menu.open = True  # Return to menu when battle closes
            continue
        # Check for space keydown
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            space_pressed = True    
        if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
            x_pressed = True
   # Block game logic if menu is open
    if not menu.open and not bag_menu.open and not battle.open:
        # Handle key presses
        keys = pygame.key.get_pressed()
        obstacles = current_map.get_obstacle_rects()
        if not (in_house and in_house_map.show_text_box):
            move_x, move_y = 0, 0
            if keys[pygame.K_UP]:
                tim.change_image("assets/Up.png")
                move_y = -10
            if keys[pygame.K_DOWN]:
                tim.change_image("assets/Down.png")
                move_y = 10
            if keys[pygame.K_LEFT]:
                tim.toggle_image("assets/Left1.png", "assets/Left2.png")
                move_x = -10
            if keys[pygame.K_RIGHT]:
                tim.toggle_image("assets/Right1.png", "assets/Right2.png")
                move_x = 10

            # Only move if not blocked by textbox
            if move_x != 0 or move_y != 0:
                new_rect = tim.get_rect().move(move_x, move_y)
                if can_move(new_rect, obstacles, SCREEN_WIDTH, SCREEN_HEIGHT):
                    tim.move(move_x, move_y)
                time.sleep(0.1)

        # Handle mom interaction and paging
            # Handle mom interaction and paging
        # Handle mom interaction and paging
        
        if in_house and current_house == 1:
            if in_house_map.mom_rect.colliderect(tim.get_rect()) and space_pressed and not in_house_map.show_text_box:
                # Start new dialogue
                mom_dialogue = in_house_map.get_dialogue("mom", "default")
                selected_line = mom_dialogue[mom_dialogue_index]
                in_house_map.set_text_box_text(selected_line, font, box_width)
                in_house_map.show_text_box = True  # just turn on the textbox
                in_house_map.ignore_space_for_scroll = True
                in_house_map.text_scroll_index = 0
                in_house_map.text_scroll_timer = 0
                mom_dialogue_index = (mom_dialogue_index + 1) % len(mom_dialogue)



                        

        # Check for door entry if on outdoor map
        if not in_house:
        # Left door
            if tim.get_rect().colliderect(game_map.door_rects[0]):
                current_map = in_house_map
                in_house = True
                current_house = 1
                tim.x = SCREEN_WIDTH // 2 - tim.width // 2
                tim.y = 300
            # Right door
            elif tim.get_rect().colliderect(game_map.door_rects[1]):
                current_map = in_house_map2
                in_house = True
                current_house = 2
                tim.x = SCREEN_WIDTH // 2 - tim.width // 2
                tim.y = 300
        if in_house:
            if current_house == 1 and tim.get_rect().colliderect(in_house_map.door_rect):
                current_map = game_map
                in_house = False
                current_house = None
                # Place Tim just outside the left house door
                tim.x = 120 + 200 // 2 - tim.width // 2
                tim.y = 100 + 160
            elif current_house == 2 and tim.get_rect().colliderect(in_house_map2.door_rect):
                current_map = game_map
                in_house = False
                current_house = None
                # Place Tim just outside the right house door
                tim.x = 500 + 200 // 2 - tim.width // 2
                tim.y = 100 + 160
        # Tim interacts with mom
            in_house_map.update_mom_image(tim.get_rect())
        in_house_map.update_text_scroll(space_pressed)

        
    # Draw everything
    screen.fill((0, 0, 0))  # Clear the screen with black
    if battle.open:
        battle.update_blink()
        battle.draw(screen)
        if battle.turn == "enemy" and not battle.action_text_showing():
            battle.update()
    else:
        current_map.draw(screen)
        tim.draw(screen)
        if in_house:
            current_map.draw_textbox(screen)
  
        menu.draw(screen)  # <-- draw menu on top
        if bag_menu.open:
            bag_menu.draw(screen)
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)
    # print("Text box lines:", in_house_map.text_box_lines)
pygame.quit()