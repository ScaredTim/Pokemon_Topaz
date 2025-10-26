import pygame
import json
import os
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

    def draw(self, screen):
        # Fill the screen with the map color
        screen.fill(self.color)

        self.house_rects = []

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

        # Draw boundaries for all obstacles (for debugging)
        # for rect in self.get_obstacle_rects():
        #     pygame.draw.rect(screen, (255, 0, 0), rect, 2)  # Red outline, thickness 2

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
        # Define furniture collision rects (positions must match blit positions and sizes)
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
    def draw(self, screen):
        # Fill background
        screen.fill(self.color)

        # Draw furniture
        screen.blit(self.table_img, (self.width//2 - 180, self.height//2 - 30))
        screen.blit(self.chair_img, (self.width//2 - 250, self.height//2 + 40))
        screen.blit(self.cooking_img, (20, 20))
        screen.blit(self.stairs_img, (self.width - 200, 10))

        # Draw Mom
        screen.blit(self.mom_img, (self.mom_x, self.mom_y))

        # Draw door (optional visual)
        pygame.draw.rect(screen, (100, 100, 100), self.door_rect, 2)

    def draw_textbox(self, screen):
        if self.show_text_box and self.text_box_lines:
            box_height = self.lines_per_page * 28 + 20
            box_rect = pygame.Rect(20, self.height - box_height - 20, 360, box_height)
            pygame.draw.rect(screen, (0, 0, 0), box_rect)
            pygame.draw.rect(screen, (255, 255, 255), box_rect, 2)
            start = self.text_box_page * self.lines_per_page
            end = start + self.lines_per_page
            current_lines = self.text_box_lines[start:end]
            full_text = "\n".join(current_lines)
            visible_text = full_text[:self.text_scroll_index]
            lines_to_draw = visible_text.split("\n")
            font = pygame.font.SysFont(None, 28)
            for i, line in enumerate(lines_to_draw):
                text_surf = font.render(line, True, (255, 255, 255))
                screen.blit(text_surf, (box_rect.x + 10, box_rect.y + 10 + i*28))