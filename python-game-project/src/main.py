#IMPORTANT!!! REMEMBER TO CHANGE THE MOVEMENT SPEED BACK TO 10 WHEN YOU FINISH TESTING --- IGNORE ---
import pygame
import json
from map import GameMap, InHouseMap, Route1_1Map
from character import Character
from menu import Menu, BagMenu
from battle import Battle, Player, Enemy
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
current_music=None
# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pokemon Topaz")

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Load the map and character
game_map = GameMap(SCREEN_WIDTH, SCREEN_HEIGHT)
in_house_map = InHouseMap(SCREEN_WIDTH, SCREEN_HEIGHT)
in_house_map2 = InHouseMap(SCREEN_WIDTH, SCREEN_HEIGHT)
route1_1_map = Route1_1Map(SCREEN_WIDTH, SCREEN_HEIGHT)

current_map = game_map
in_house = False
current_house = None

tim = Character("assets/Down.png", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, width=80, height=100)
def play_music(music_path):
    global current_music
    if current_music != music_path:
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play(-1)
        current_music = music_path
def can_move(new_rect, obstacles, screen_width, screen_height):
    # Check screen boundaries
    if not (0 <= new_rect.left and new_rect.right <= screen_width and 0 <= new_rect.top and new_rect.bottom <= screen_height):
        return False
    # Check collision with obstacles
    for rect in obstacles:
        if new_rect.colliderect(rect):
            return False
    return True

def get_camera_pos(character, map_obj):
    # Center camera on character
    cam_x = character.x + character.width // 2 - SCREEN_WIDTH // 2
    cam_y = character.y + character.height // 2 - SCREEN_HEIGHT // 2
    # Clamp camera to map bounds
    cam_x = max(0, min(cam_x, map_obj.width - SCREEN_WIDTH))
    cam_y = max(0, min(cam_y, map_obj.height - SCREEN_HEIGHT))
    return cam_x, cam_y

def draw_boundaries(screen, character, offset=(0, 0)):
    # Draw the character's boundary as a blue rectangle
    rect = character.get_rect()
    rect = rect.move(offset)
    pygame.draw.rect(screen, (0, 0, 255), rect, 2)

def save_game(character, current_map, in_house, current_house, player):
    save_data = {
        "x": character.x,
        "y": character.y,
        "in_house": in_house,
        "current_house": current_house,
        "current_map": "in_house" if in_house else "game_map"
    }
    with open("./data/map/player_location.json", "w") as f:
        json.dump(save_data, f)
    # Save player info
    player_data = {
        "name": player.name,
        "level": player.level,
        "exp": player.exp,
        "exp_max": player.exp_max,
        "hp": player.hp,
        "hp_max": player.hp_max,
        "attack": player.attack,
        "defense": player.defense,
        "moves": player.moves,
        "move_info": player.move_info
    }
    with open("./data/battle/player_data.json", "w") as f:
        json.dump(player_data, f, indent=2)
    print("Game saved!")

def load_game(character):
    try:
        with open("./data/map/player_location.json", "r") as f:
            save_data = json.load(f)
        character.x = save_data["x"]
        character.y = save_data["y"]
        in_house = save_data.get("in_house", False)
        current_house = save_data.get("current_house", None)
        if save_data.get("current_map") == "in_house":
            current_map = in_house_map if current_house == 1 else in_house_map2
        else:
            current_map = game_map
        print("Game loaded!")
        return current_map, in_house, current_house
    except Exception as e:
        print("Failed to load game:", e)
        return None, None, None
    
menu = Menu(SCREEN_WIDTH, SCREEN_HEIGHT)
bag_menu = BagMenu(SCREEN_WIDTH, SCREEN_HEIGHT)

# Load player and enemy info from JSON
with open("data/battle/player_data.json") as f:
    player_data = json.load(f)
with open("data/battle/enemy_data.json") as f:
    enemy_data = json.load(f)

current_enemy_key = random.choice(list(enemy_data.keys()))
enemy_info = enemy_data[current_enemy_key]
player = Player(player_data)
enemy = Enemy(enemy_info)
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
        
        if menu.open and menu.options[menu.selected] == "Save":
            if getattr(menu, "enter_pressed", False):
                save_game(tim, current_map, in_house, current_house, player)
                menu.enter_pressed = False  # Reset the flag

        if menu.open and menu.options[menu.selected] == "Load":
            if getattr(menu, "enter_pressed", False):
                loaded_map, loaded_in_house, loaded_current_house = load_game(tim)
                if loaded_map is not None:
                    current_map = loaded_map
                    in_house = loaded_in_house
                    current_house = loaded_current_house
                menu.enter_pressed = False  # Reset the flag        

        if menu.open and menu.options[menu.selected] == "Test Battle":
        # If Enter was pressed, open the bag menu
        # You need a way to detect that Enter was pressed this frame
        # For example, set a flag in Menu.handle_event when Enter is pressed:
            if getattr(menu, "enter_pressed", False):
                battle.open = True
                battle.just_opened = True 
                menu.enter_pressed = False  # Reset the flag
                battle.player_dead = False           # <-- Reset dead flag
                battle.death_message_start = None    # <-- Reset timer
                menu.open = False           # Close main menu when bag opens
        # If in battle mode, only handle battle events
        if battle.open:
            if battle.just_opened:
                battle.just_opened = False  # Skip input for this frame
            else:
                battle.handle_event(event)
            
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_c) or battle.enemy.hp <= 0:
                if battle.enemy.hp <= 0:
                    player.exp += battle.enemy.expyield
                # Level up as many times as needed
                while player.exp >= player.exp_max:
                    player.level += 1
                    hp_increase = random.randint(2, 4)
                    atk_increase = random.randint(1, 3)
                    def_increase = random.randint(1, 3)
                    player.hp_max += hp_increase
                    player.attack += atk_increase
                    player.defense += def_increase
                    player.hp += hp_increase
                    player.exp_max = int(0.8 * (player.level ** 3))
                    player.exp -= player.exp_max
                # Pick a random different enemy
                enemy_keys = list(enemy_data.keys())
                enemy_keys.remove(current_enemy_key)
                if enemy_keys:
                    new_enemy_key = random.choice(enemy_keys)
                    current_enemy_key = new_enemy_key
                    enemy_info = enemy_data[current_enemy_key]
                    enemy = Enemy(enemy_info)
                    battle.set_enemy(enemy)
                    battle.enemy = enemy
                else:
                    # If no other enemies, just reset current enemy
                    battle.enemy.hp = battle.enemy.hp_max    
            if not battle.open or player.hp <= 0:
                if player.hp <= 0 and not battle.player_dead:
                    battle.show_death_message()
                    battle.showing_message = True
                # Wait for death message to finish
                if battle.player_dead and time.time() - battle.death_message_start < battle.death_message_duration:
                    # Don't exit to menu yet, just show message
                    continue
                # After message duration, exit to menu and reset battle
                battle.open = False
                menu.open = True  # Return to menu when battle closes
                enemy.hp = enemy.hp_max  # Reset enemy HP for next battle
                player.hp = player.hp_max  # Reset player HP for next battle
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
        if not (in_house and in_house_map.show_text_box):
            move_x, move_y = 0, 0
            if keys[pygame.K_UP]:
                tim.change_image("assets/Up.png")
                move_y = -30
            if keys[pygame.K_DOWN]:
                tim.change_image("assets/Down.png")
                move_y = 30
            if keys[pygame.K_LEFT]:
                tim.toggle_image("assets/Left1.png", "assets/Left2.png")
                move_x = -30
            if keys[pygame.K_RIGHT]:
                tim.toggle_image("assets/Right1.png", "assets/Right2.png")
                move_x = 30

            if move_x != 0 or move_y != 0:
                new_rect = tim.get_rect().move(move_x, move_y)
                obstacles = current_map.get_obstacle_rects()
                map_w = current_map.width
                map_h = current_map.height

                # Ledge logic (unchanged)
                if isinstance(current_map, Route1_1Map):
                    crossed_ledge = False
                    for ledge in current_map.ledge_rects:
                        if move_y > 0 and tim.get_rect().bottom <= ledge.top and new_rect.colliderect(ledge):
                            tim.y = ledge.bottom
                            crossed_ledge = True
                            break
                        elif new_rect.colliderect(ledge):
                            obstacles = obstacles + [ledge]
                    if crossed_ledge:
                        continue

                if can_move(new_rect, obstacles, map_w, map_h):
                    tim.x += move_x
                    tim.y += move_y              
                time.sleep(0.1)    
                    # # Special ledge logic
                # if isinstance(current_map, Route1_1Map):
                #     ledge = current_map.ledge_rect
                #     if move_y > 0:  # Moving down
                #         # If character is above the ledge and would collide after moving
                #         if tim.get_rect().bottom <= ledge.top and new_rect.colliderect(ledge):
                #             # Teleport character to just below the ledge
                #             tim.y = ledge.bottom + tim.height
                #             # Optionally, you can skip normal movement for this frame
                #             continue
                #         elif new_rect.colliderect(ledge):
                #             obstacles = obstacles + [ledge]  # block as normal
                #     elif new_rect.colliderect(ledge):
                #         obstacles = obstacles + [ledge]

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
        if not in_house and current_map == game_map:
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
        # Transition from game_map to route1_1
        if current_map == game_map and tim.get_rect().colliderect(game_map.transition_rect):
            current_map = route1_1_map
            tim.x = int(route1_1_map.spawn_x - tim.width // 2)
            tim.y = int(route1_1_map.spawn_y - tim.height // 2)  # Place at bottom of route1_1

        # Transition from route1_1 to game_map
        if current_map == route1_1_map and tim.get_rect().colliderect(route1_1_map.transition_rect):
            current_map = game_map
            tim.x = SCREEN_WIDTH // 2 - tim.width // 2
            tim.y = 60  # Place at top of game_map        

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
    if battle.open:
        play_music("./assets/music/DecisiveEncounter.mp3")
    else:
                #HEY FUTURE TIMOTHY. YOU NEED TO CHANGE THIS WHEN YOU GET OUT OF LITTLEROOT TOWN. - 2025 Timothy
        play_music("./assets/music/APlaceCalledHome.mp3")
    # Draw everything
    screen.fill((0, 0, 0))  # Clear the screen with black
    if battle.open:
        battle.update_blink()
        battle.draw(screen)
        if battle.turn == "enemy" and not battle.action_text_showing():
            battle.update()
    else:
        camera_x, camera_y = get_camera_pos(tim, current_map)
        current_map.draw(screen, camera_x, camera_y)
        tim.draw(screen, offset=(-camera_x, -camera_y))
        draw_boundaries(screen, tim, offset=(-camera_x, -camera_y))  # <-- SHOW HITBOXES for character
        if in_house:
            current_map.draw_textbox(screen, camera_x, camera_y)
        menu.draw(screen)  # <-- draw menu on top
        if bag_menu.open:
            bag_menu.draw(screen)
    
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)
    # print("Text box lines:", in_house_map.text_box_lines)
    
pygame.quit()