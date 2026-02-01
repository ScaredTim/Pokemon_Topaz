import pygame
import json
import os
import math
with open(os.path.join(os.path.dirname(__file__), "dialogue.json"), "r") as f:
    dialogue_data = json.load(f)

class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.color = (144, 238, 144)  # Light Green background for the map
         # Load and scale the flower image once
        flower_img = pygame.image.load("./assets/flower.png")
        self.flower_img = pygame.transform.scale(flower_img, (40, 40))
        self.house_rects = []
        self.tree_rects = []
        self.door_rects = [
            pygame.Rect(120 + 200 // 2 - 40 // 2, 100 + 160 - 70, 40, 70),  # Door for house 1
            pygame.Rect(500 + 200 // 2 - 40 // 2, 100 + 160 - 70, 40, 70),  # Door for house 2
        ]
        self.transition_rect = pygame.Rect(width // 2 - 30, 0, 60, 60)  # Middle top

    def draw_tree(self, screen, x, y, trunk_width=30, trunk_height=90, leaves_radius=40):
        dark_green = (0, 100, 0)
        trunk_color = (101, 67, 33)
        # Draw trunk
        pygame.draw.rect(screen, trunk_color, (x, y, trunk_width, trunk_height))
        # Draw leaves (circle centered above the trunk)
        pygame.draw.circle(screen, dark_green, (x + trunk_width // 2, y), leaves_radius)
        self.tree_rects.append(pygame.Rect(x, y-leaves_radius/2-10, trunk_width, trunk_height+30))
        

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
        
        # self.house_rects.append(pygame.Rect(x+20, y, width-40, height))
        # --- House collision rects, leaving a gap for the door ---
        left_rect = pygame.Rect(x+20, y-20, width//2 - door_width//2 - 40, height)
        right_rect = pygame.Rect(x + width//2 + door_width//2+20, y-20, width//2 - door_width//2 - 40, height)
        self.house_rects.append(left_rect)
        self.house_rects.append(right_rect)

    def draw_flower(self, screen, x, y):
        # Draw the flower image at (x, y)
        screen.blit(self.flower_img, (x, y))

    def get_obstacle_rects(self):
        return self.house_rects + self.tree_rects

    def draw(self, screen, camera_x=0, camera_y=0):
        # # Fill the screen with the map color
        # screen.fill(self.color)
        screen_surface = pygame.Surface((self.width, self.height))
        screen_surface.fill(self.color)

        self.house_rects = []

        # Draw houses using draw_house
        self.draw_house(screen_surface, 120, 100)
        self.draw_house(screen_surface, 500, 100)

      # Draw big trees on the edges using draw_tree
      #Left trees
        self.draw_tree(screen_surface, 30, 64)
        self.draw_tree(screen_surface, 30, 200)
        self.draw_tree(screen_surface, 30, 336)
        self.draw_tree(screen_surface, 30, 472)
        #Right trees
        self.draw_tree(screen_surface, 740, 64)
        self.draw_tree(screen_surface, 740, 200)
        self.draw_tree(screen_surface, 740, 336)
        self.draw_tree(screen_surface, 740, 472)
        #Bottom trees
        self.draw_tree(screen_surface, 120, 502)
        self.draw_tree(screen_surface, 210, 502)
        self.draw_tree(screen_surface, 300, 502)
        self.draw_tree(screen_surface, 390, 502)
        self.draw_tree(screen_surface, 480, 502)
        self.draw_tree(screen_surface, 570, 502)
        self.draw_tree(screen_surface, 660, 502)

        # Draw some flowers
        self.draw_flower(screen_surface, 200, 300)
        self.draw_flower(screen_surface, 400, 200)
        self.draw_flower(screen_surface, 600, 350)

        # Draw the transition space (for visual reference)
        pygame.draw.rect(screen_surface, (255, 0, 225), self.transition_rect)

        # Draw boundaries for all obstacles (for debugging)
        #SHOW HITBOXES
        for rect in self.get_obstacle_rects():
            pygame.draw.rect(screen_surface, (255, 0, 0), rect, 2)  # Red outline, thickness 2
        for door_rect in self.door_rects:
            pygame.draw.rect(screen_surface, (0, 0, 255), door_rect, 3)
        # Blit the visible area to the screen
        screen.blit(screen_surface, (-camera_x, -camera_y))

    def handle_doors(self, tim, current_map, in_house, current_house, in_house_map, in_house_map2, screen_width):
        # Only check doors if not in a house
        if not in_house and current_map == self:
            # Left house door
            if tim.get_rect().colliderect(self.door_rects[0]):
                current_map = in_house_map
                in_house = True
                current_house = 1
                tim.x = screen_width // 2 - tim.width // 2
                tim.y = 300
            # Right house door
            elif tim.get_rect().colliderect(self.door_rects[1]):
                current_map = in_house_map2
                in_house = True
                current_house = 2
                tim.x = screen_width // 2 - tim.width // 2
                tim.y = 300
        else:
            # Leaving left house
            if current_house == 1 and tim.get_rect().colliderect(in_house_map.door_rect):
                current_map = self
                in_house = False
                current_house = None
                tim.x = 120 + 200 // 2 - tim.width // 2
                tim.y = 100 + 160
            # Leaving right house
            elif current_house == 2 and tim.get_rect().colliderect(in_house_map2.door_rect):
                current_map = self
                in_house = False
                current_house = None
                tim.x = 500 + 200 // 2 - tim.width // 2
                tim.y = 100 + 160

        return current_map, in_house, current_house
class InHouseMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.color = (245, 222, 179)  # Light brown for in-house
        
        self.text_scroll_index = 0
        self.text_scroll_speed = 2  # Higher is faster
        self.text_scroll_timer = 0
        self.text_box_lines = []      # List of lines for the current dialogue
        self.text_box_page = 0        # Current page index
        self.lines_per_page = 3       # Number of lines per page (adjust for your box size)
        self.ignore_space_for_scroll = False
        # Load and scale furniture images
        self.table_img = pygame.transform.scale(
            pygame.image.load("./assets/Table_w_book.png"), (140, 140)
        )
        self.chair_img = pygame.transform.scale(
            pygame.image.load("./assets/Chair.png"), (60, 60)
        )
        self.cooking_img = pygame.transform.scale(
            pygame.image.load("./assets/Cooking_equipment.png"), (330, 150)
        )
        self.stairs_img = pygame.transform.scale(
            pygame.image.load("./assets/Stairs going up.png"), (150, 150)
        )

        # # Load and scale mom NPC image
        # self.mom_img = pygame.transform.scale(
        #     pygame.image.load("./assets/Momsprites/Momright.png"), (180, 120)
        # )

        # Load and scale mom NPC images
        self.momright_img = pygame.transform.scale(
            pygame.image.load("./assets/Momsprites/Momright.png"), (180, 120)
        )
        self.momfacing_img = pygame.transform.scale(
            pygame.image.load("./assets/Momsprites/Momfacing.png"), (180, 120)
        )
        self.mom_img = self.momright_img  # Default

        # Define the return door (e.g., at the bottom center)
        self.door_rect = pygame.Rect(width // 2 - 30, height - 80, 60, 60)
        # # Define furniture collision rects (positions must match blit positions and sizes)
        self.furniture_rects = [
            pygame.Rect(20, 20, 330, 150),  # Cooking equipment
            pygame.Rect(self.width//2 - 180, self.height//2 - 30, 140, 140),  # Table
            pygame.Rect(self.width//2 - 250, self.height//2 + 40, 60, 60),    # Chair
            pygame.Rect(self.width - 200, 10, 150, 150),
            pygame.Rect(self.width//2 - 235, self.height//2 + 0, 55, 120) #mom hitbox
            
        ]
        self.ignore_space_for_scroll = False
        # Mom's position (on top of the chair)
        self.mom_x = self.width//2 - 290
        self.mom_y = self.height//2 + 0
        self.mom_rect = pygame.Rect(self.width//2 - 235, self.height//2 + 0, 50, 125)

        # Text box state
        self.show_text_box = False
        self.text_box_text = "Hello! This is a placeholder text."

    def update_mom_image(self, character_rect):
        # Change mom image based on collision with character
        if self.mom_rect.colliderect(character_rect):
            self.mom_img = self.momfacing_img
        else:
            self.mom_img = self.momright_img

    def get_dialogue(self, npc, state="default"):
        return dialogue_data.get(npc, {}).get(state, ["..."])
    def toggle_text_box(self):
        self.show_text_box = not self.show_text_box
        if self.show_text_box:
            self.text_scroll_index = 0
            self.text_scroll_timer = 0
    def update_text_scroll(self, space_pressed=False):
        if not self.show_text_box or not self.text_box_lines:
            return

        start = self.text_box_page * self.lines_per_page
        end = start + self.lines_per_page
        current_lines = self.text_box_lines[start:end]
        full_text = "\n".join(current_lines)

        # Scroll automatically
        if self.text_scroll_index < len(full_text):
            self.text_scroll_timer += 1
            if self.text_scroll_timer >= self.text_scroll_speed:
                self.text_scroll_index += 1
                self.text_scroll_timer = 0

        # Handle space pressed
        if space_pressed:
            # Ignore the space used to open the textbox
            if self.ignore_space_for_scroll:
                self.ignore_space_for_scroll = False
                return

            if self.text_scroll_index < len(full_text):
                # Finish scrolling instantly
                self.text_scroll_index = len(full_text)
            else:
                # Move to next page or close
                total_pages = (len(self.text_box_lines) - 1) // self.lines_per_page + 1
                if self.text_box_page < total_pages - 1:
                    self.text_box_page += 1
                    self.text_scroll_index = 0
                    self.text_scroll_timer = 0
                else:
                    self.show_text_box = False  # close textbox




    def get_obstacle_rects(self):
        # Return furniture and door as obstacles
        return self.furniture_rects
    def set_text_box_text(self, text, font, box_width):
        words = text.split(' ')
        lines = []
        current_line = ""
        for word in words:
            test_line = current_line + (" " if current_line else "") + word
            if font.size(test_line)[0] <= box_width - 32:  # 32px padding
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
        self.text_box_lines = lines
        self.text_box_page = 0
        self.text_scroll_index = 0
        self.text_scroll_timer = 0
    def draw(self, screen, camera_x=0, camera_y=0):
        # # Fill background
        # screen.fill(self.color)
        screen_surface = pygame.Surface((self.width, self.height))
        screen_surface.fill(self.color)
        
        # Draw furniture
        screen_surface.blit(self.table_img, (self.width//2 - 180, self.height//2 - 30))
        screen_surface.blit(self.chair_img, (self.width//2 - 250, self.height//2 + 40))
        screen_surface.blit(self.cooking_img, (20, 20))
        screen_surface.blit(self.stairs_img, (self.width - 200, 10))
        
        # Draw Mom
        screen_surface.blit(self.mom_img, (self.mom_x, self.mom_y))

        # Draw door
        pygame.draw.rect(screen_surface, (139, 69, 19), self.door_rect)  # Brown filled door
        pygame.draw.rect(screen_surface, (255, 255, 255), self.door_rect, 2)  # White outline
        knob_x = self.door_rect.right - 15
        knob_y = self.door_rect.centery
        pygame.draw.circle(screen_surface, (218, 165, 32), (knob_x, knob_y), 5)
        screen.blit(screen_surface, (-camera_x, -camera_y))
    def draw_textbox(self, screen, camera_x=0, camera_y=0):
        screen_surface = pygame.Surface((self.width, self.height),pygame.SRCALPHA)
        if self.show_text_box and self.text_box_lines:
            box_height = self.lines_per_page * 28 + 20
            box_rect = pygame.Rect(20, self.height - box_height - 20, 360, box_height)
            pygame.draw.rect(screen_surface, (0, 0, 0, 220), box_rect)
            pygame.draw.rect(screen_surface, (255, 255, 255), box_rect, 2)
            start = self.text_box_page * self.lines_per_page
            end = start + self.lines_per_page
            current_lines = self.text_box_lines[start:end]
            full_text = "\n".join(current_lines)
            visible_text = full_text[:self.text_scroll_index]
            lines_to_draw = visible_text.split("\n")
            font = pygame.font.SysFont(None, 28)
            for i, line in enumerate(lines_to_draw):
                text_surf = font.render(line, True, (255, 255, 255))
                screen_surface.blit(text_surf, (box_rect.x + 10, box_rect.y + 10 + i*28))
        # print("draw_textbox called")
        # print("Drawing textbox:", self.show_text_box, self.text_box_lines)
        screen.blit(screen_surface, (-camera_x, -camera_y))

    def handle_mom_interaction(self, tim, space_pressed, font, box_width, mom_dialogue_index):
        # Only interact if Tim is touching mom and space is pressed and textbox is not open
        if self.mom_rect.colliderect(tim.get_rect()):
            mom_dialogue = self.get_dialogue("mom", "default")
            selected_line = mom_dialogue[mom_dialogue_index]
            self.set_text_box_text(selected_line, font, box_width)
            self.show_text_box = True
            self.ignore_space_for_scroll = True
            self.text_scroll_index = 0
            self.text_scroll_timer = 0
            mom_dialogue_index = (mom_dialogue_index + 1) % len(mom_dialogue)
        # print("handle_mom_interaction called")
        # print("Trying to interact with mom:", self.mom_rect.colliderect(tim.get_rect()), space_pressed, not self.show_text_box)
        return mom_dialogue_index
    
class Route1_1Map:
    def __init__(self, width, height):
        self.width = int(width * 2.5)
        self.height = int(height * 3)
        self.color = (139, 196, 74)
        self.transition_rect = pygame.Rect(self.width // 2 - 30, self.height - 60, 60, 60)
        grass_img = pygame.image.load("./assets/grasstile.png")
        self.grass_tile = pygame.transform.scale(grass_img, (48, 48))
        self.circle_cx = self.width // 2
        self.circle_cy = self.height - 300
        self.circle_radius = 240
        self.spawn_x = self.circle_cx
        self.spawn_y = self.circle_cy + self.circle_radius - 80
        self.obstacle_rects = []

    def draw(self, screen, camera_x=0, camera_y=0):
        surface = pygame.Surface((self.width, self.height))
        surface.fill(self.color)
        tile_w, tile_h = self.grass_tile.get_size()
        for x in range(0, int(self.width), tile_w):
            for y in range(0, int(self.height), tile_h):
                surface.blit(self.grass_tile, (x, y))
        
        self.obstacle_rects = []  # Reset each frame
# ...existing code...

        ledge_left_img = pygame.image.load("./assets/ledgeleft.png")
        ledge_img = pygame.image.load("./assets/ledge.png")
        ledge_right_img = pygame.image.load("./assets/ledgeright.png")
        ledge_height = 40
        ledge_width = 100
        ledge_left_img = pygame.transform.scale(ledge_left_img, (ledge_width, ledge_height))
        ledge_img = pygame.transform.scale(ledge_img, (ledge_width, ledge_height))
        ledge_right_img = pygame.transform.scale(ledge_right_img, (ledge_width, ledge_height))

        # Main ledge
        ledge_y = self.circle_cy - 1250
        ledge_x_start = self.circle_cx - 750
        ledge_x_end = self.circle_cx - 650 + 76
        num_middle = (ledge_x_end - ledge_x_start) // ledge_width - 1
        surface.blit(ledge_left_img, (ledge_x_start, ledge_y))
        for i in range(num_middle):
            surface.blit(ledge_img, (ledge_x_start + ledge_width * (i + 1), ledge_y))
        surface.blit(ledge_right_img, (ledge_x_start + ledge_width * (num_middle + 1), ledge_y))

        # Ledge 1 (moved down and left)
        ledge_y1 = self.circle_cy - 1050 + 40
        ledge_x_start1 = self.circle_cx - 290 - 40
        ledge_x_end1 = self.circle_cx - 190 + 76 - 40
        num_middle1 = (ledge_x_end1 - ledge_x_start1) // ledge_width - 1
        surface.blit(ledge_left_img, (ledge_x_start1, ledge_y1))
        for i in range(num_middle1):
            surface.blit(ledge_img, (ledge_x_start1 + ledge_width * (i + 1), ledge_y1))
        surface.blit(ledge_right_img, (ledge_x_start1 + ledge_width * (num_middle1 + 1), ledge_y1))

        # Ledge 2 (moved down and left)
        ledge_y2 = self.circle_cy - 850 + 40
        ledge_x_start2 = self.circle_cx - 750 - 40
        ledge_x_end2 = self.circle_cx - 650 + 76 - 40
        num_middle2 = (ledge_x_end2 - ledge_x_start2) // ledge_width - 1
        surface.blit(ledge_left_img, (ledge_x_start2, ledge_y2))
        for i in range(num_middle2):
            surface.blit(ledge_img, (ledge_x_start2 + ledge_width * (i + 1), ledge_y2))
        surface.blit(ledge_right_img, (ledge_x_start2 + ledge_width * (num_middle2 + 1), ledge_y2))

        # Store all ledge rects for special logic
        self.ledge_rects = [
            pygame.Rect(ledge_x_start, ledge_y, ledge_x_end - ledge_x_start, ledge_height),
            pygame.Rect(ledge_x_start1, ledge_y1, ledge_x_end1 - ledge_x_start1, ledge_height),
            pygame.Rect(ledge_x_start2, ledge_y2, ledge_x_end2 - ledge_x_start2, ledge_height),
        ]

        # Optionally, draw the hitboxes for debugging
        for ledge_rect in self.ledge_rects:
            pygame.draw.rect(surface, (0, 255, 0), ledge_rect, 2)
        # Entrance at bottom center
        pygame.draw.rect(surface, (255, 255, 0), self.transition_rect)

        # Draw spawn circle of trees and bushes
        num_points = 14
        bush_indices = [0, 13]
        bottom_index = num_points // 2
        for i in range(num_points):
            if i == bottom_index:
                continue
            angle = 2 * math.pi * i / num_points - math.pi / 2
            cx = self.circle_cx
            cy = self.circle_cy
            r = self.circle_radius
            if i in bush_indices:
                bush_x = int(cx + r * math.cos(angle)) - 20
                bush_y = int(cy + r * math.sin(angle)) - 30
                pygame.draw.ellipse(surface, (34, 139, 34), (bush_x, bush_y, 32, 48))
                self.obstacle_rects.append(pygame.Rect(bush_x, bush_y, 32, 48))
            else:
                tree_x = int(cx + r * math.cos(angle)) - 35
                tree_y = int(cy + r * math.sin(angle)) - 60
                self.draw_medium_tree(surface, tree_x, tree_y)
                collider_x = tree_x + 32 - 38
                collider_y = tree_y + 60 - 38
                collider_w = 38 * 2
                collider_h = 38 + 44
                self.obstacle_rects.append(pygame.Rect(collider_x, collider_y, collider_w, collider_h))
        custom_tree_positions = [
            # Example positions (replace/add as needed)
            (self.circle_cx - 250, self.circle_cy - 350),
            (self.circle_cx - 350, self.circle_cy - 350),
            (self.circle_cx - 450, self.circle_cy - 350),
            (self.circle_cx - 550, self.circle_cy - 350),
            (self.circle_cx + 50, self.circle_cy - 400),
            (self.circle_cx + 150, self.circle_cy - 400),
            (self.circle_cx + 250, self.circle_cy - 400),
            (self.circle_cx + 350, self.circle_cy - 400),
            (self.circle_cx + 50, self.circle_cy - 700),
            (self.circle_cx + 150, self.circle_cy - 700),
            (self.circle_cx + 250, self.circle_cy - 700),
            (self.circle_cx + 350, self.circle_cy - 700),
            (self.circle_cx - 250, self.circle_cy - 650),
            (self.circle_cx - 350, self.circle_cy - 650),
            (self.circle_cx - 450, self.circle_cy - 650),
            (self.circle_cx - 550, self.circle_cy - 650),
            (self.circle_cx - 550, self.circle_cy - 850),
            (self.circle_cx - 450, self.circle_cy - 850),
            (self.circle_cx - 350, self.circle_cy - 850),
            (self.circle_cx - 250, self.circle_cy - 850),
            (self.circle_cx - 150, self.circle_cy - 850),
            (self.circle_cx - 50, self.circle_cy - 850),
            (self.circle_cx + 50, self.circle_cy - 800),
            (self.circle_cx - 650, self.circle_cy - 650),
            (self.circle_cx - 750, self.circle_cy - 650),
            (self.circle_cx - 850, self.circle_cy - 650),
            (self.circle_cx - 950, self.circle_cy - 650),
            (self.circle_cx - 990, self.circle_cy - 750),
            (self.circle_cx - 990, self.circle_cy - 850),
            (self.circle_cx - 990, self.circle_cy - 950),
            (self.circle_cx - 990, self.circle_cy - 1050),
            (self.circle_cx - 890, self.circle_cy - 1050),
            (self.circle_cx - 790, self.circle_cy - 1050),
            (self.circle_cx - 690, self.circle_cy - 1050),
            (self.circle_cx - 590, self.circle_cy - 1050),
            (self.circle_cx - 490, self.circle_cy - 1050),
            (self.circle_cx - 390, self.circle_cy - 1050),
            (self.circle_cx + 50, self.circle_cy - 1000),
            (self.circle_cx + 50, self.circle_cy - 900),
            (self.circle_cx + 50, self.circle_cy - 1100),
            (self.circle_cx + 50, self.circle_cy - 1200),
            (self.circle_cx + 50, self.circle_cy - 1300),
            (self.circle_cx - 50, self.circle_cy - 1300),
            (self.circle_cx - 150, self.circle_cy - 1300),
            (self.circle_cx - 250, self.circle_cy - 1300),
            (self.circle_cx - 350, self.circle_cy - 1300),
            (self.circle_cx - 450, self.circle_cy - 1300),
            (self.circle_cx - 550, self.circle_cy - 1300),
            (self.circle_cx - 990, self.circle_cy - 1250),
            (self.circle_cx - 990, self.circle_cy - 1150),
            (self.circle_cx - 990, self.circle_cy - 1350),
            (self.circle_cx - 990, self.circle_cy - 1450),
            (self.circle_cx - 890, self.circle_cy - 1520),
            (self.circle_cx - 790, self.circle_cy - 1520),
            (self.circle_cx - 690, self.circle_cy - 1520),
            (self.circle_cx - 590, self.circle_cy - 1520),
            (self.circle_cx - 490, self.circle_cy - 1520),
            (self.circle_cx - 190, self.circle_cy - 1420),
            (self.circle_cx - 190, self.circle_cy - 1520),
        ]

        # Draw all custom trees
        for tx, ty in custom_tree_positions:
            self.draw_medium_tree(surface, tx, ty)
            # Collider covers leaves and trunk
            collider_x = tx + 32 - 38  # left edge of leaves
            collider_y = ty + 60 - 38  # top edge of leaves
            collider_w = 38 * 2        # diameter of leaves
            collider_h = 38 + 44       # leaves radius + trunk height
            self.obstacle_rects.append(pygame.Rect(collider_x, collider_y, collider_w, collider_h))
            
        # Draw boundaries for all obstacles (for debugging)
        #SHOW HITBOXES
        for rect in self.get_obstacle_rects():
            pygame.draw.rect(surface, (255, 0, 0), rect, 2)  # Red outline, thickness 2
            screen.blit(surface, (-camera_x, -camera_y))

    def draw_medium_tree(self, surface, x, y):
        trunk_color = (101, 67, 33)
        leaves_color = (34, 139, 34)
        pygame.draw.rect(surface, trunk_color, (x + 22, y + 60, 20, 44))
        pygame.draw.circle(surface, leaves_color, (x + 32, y + 60), 38)

    def get_obstacle_rects(self):
        return self.obstacle_rects