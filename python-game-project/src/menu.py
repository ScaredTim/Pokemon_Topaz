import pygame
import json
import os

class Menu:
    def __init__(self, screen_width, screen_height):
        self.options = ["Bag", "Pokemon", "Map", "Settings", "Save", "Load", "Test Battle", "Exit"]
        self.selected = 0
        self.open = False
        self.screen_width = screen_width
        self.screen_height = screen_height

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.open = not self.open
            elif self.open:
                if event.key == pygame.K_UP:
                    self.selected = (self.selected - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected = (self.selected + 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    self.enter_pressed = True  # <-- set the flag
                    print("Selected:", self.options[self.selected])
    def draw(self, screen):
        if self.open:
            box_width, box_height = 300, 300
            box_x = self.screen_width // 2 - box_width // 2
            box_y = self.screen_height // 2 - box_height // 2
            pygame.draw.rect(screen, (30, 30, 30), (box_x, box_y, box_width, box_height))
            pygame.draw.rect(screen, (255, 255, 255), (box_x, box_y, box_width, box_height), 2)
            font = pygame.font.SysFont(None, 36)
            for i, option in enumerate(self.options):
                color = (255, 255, 0) if i == self.selected else (255, 255, 255)
                text_surf = font.render(option, True, color)
                screen.blit(text_surf, (box_x + 40, box_y + 20 + i * 40))
class BagMenu(Menu):
    def __init__(self, screen_width, screen_height):
        super().__init__(screen_width, screen_height)
        self.options = ["Key Items", "Items", "Medicine", "Berries", "TM/HM", "Pokeballs"]
        self.selected = 0
        self.open = False
        self.item_selected = 0
        self.mini_menu = MiniMenu(["Use", "Give", "Description", "Drop"])

        # Load bag data
        bag_data_path = os.path.join(os.path.dirname(__file__), "data", "menu", "bag_data.json")
        with open(bag_data_path, "r") as f:
            self.bag_data = json.load(f)

    def handle_event(self, event):
        if self.mini_menu.open:
            result = self.mini_menu.handle_event(event)
            if result:
                print(f"{result} {self.get_selected_item()}")
        elif self.open and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.open = False
            elif event.key == pygame.K_LEFT:
                self.selected = (self.selected - 1) % len(self.options)
                self.item_selected = 0
            elif event.key == pygame.K_RIGHT:
                self.selected = (self.selected + 1) % len(self.options)
                self.item_selected = 0
            elif event.key == pygame.K_UP:
                items = self.bag_data.get(self.options[self.selected], [])
                if items:
                    self.item_selected = (self.item_selected - 1) % len(items)
            elif event.key == pygame.K_DOWN:
                items = self.bag_data.get(self.options[self.selected], [])
                if items:
                    self.item_selected = (self.item_selected + 1) % len(items)
            elif event.key == pygame.K_RETURN:
                items = self.bag_data.get(self.options[self.selected], [])
                if items:
                    self.mini_menu.open = True
                    self.mini_menu.selected = 0

    def get_selected_item(self):
        items = self.bag_data.get(self.options[self.selected], [])
        if items:
            return items[self.item_selected]
        return None

    def draw(self, screen):
        if self.open:
            box_width, box_height = self.screen_width, self.screen_height
            box_x, box_y = 0, 0
            pygame.draw.rect(screen, (50, 50, 80), (box_x, box_y, box_width, box_height))
            pygame.draw.rect(screen, (255, 255, 255), (box_x, box_y, box_width, box_height), 4)
            font = pygame.font.SysFont(None, 48)
            title_surf = font.render("Bag", True, (255, 255, 0))
            screen.blit(title_surf, (box_x + box_width // 2 - title_surf.get_width() // 2, box_y + 40))

            # Category and arrows
            item_font = pygame.font.SysFont(None, 36)
            category = self.options[self.selected]
            category_surf = item_font.render(category, True, (255, 255, 0))
            category_y = box_y + 110
            screen.blit(category_surf, (box_x + box_width // 2 - category_surf.get_width() // 2, category_y))
            arrow_font = pygame.font.SysFont(None, 60)
            left_arrow = arrow_font.render("<", True, (200, 200, 200))
            right_arrow = arrow_font.render(">", True, (200, 200, 200))
            arrow_y = category_y + category_surf.get_height() // 2 - left_arrow.get_height() // 2
            screen.blit(left_arrow, (box_x + 60, arrow_y))
            screen.blit(right_arrow, (box_x + box_width - 100, arrow_y))

            # Show items in category, highlight selected
            items = self.bag_data.get(category, [])
            for i, item in enumerate(items):
                color = (255, 255, 0) if i == self.item_selected else (255, 255, 255)
                item_surf = item_font.render(item, True, color)
                item_y = category_y + 60 + i * 40
                item_x = box_x + box_width // 2 - item_surf.get_width() // 2
                screen.blit(item_surf, (item_x, item_y))
                # Draw mini menu next to selected item
                if i == self.item_selected and self.mini_menu.open:
                    menu_x = item_x + item_surf.get_width() + 30
                    menu_y = item_y
                    if menu_x + 160 > self.screen_width:
                        menu_x = item_x - 160 - 30
                    self.mini_menu.draw(screen, menu_x, menu_y)
            if not items:
                empty_surf = item_font.render("Empty", True, (180, 180, 180))
                screen.blit(empty_surf, (box_x + box_width // 2 - empty_surf.get_width() // 2, category_y + 60))
class MiniMenu:
    def __init__(self, options):
        self.options = options
        self.selected = 0
        self.open = False

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and self.open:
            if event.key == pygame.K_x:
                self.open = False
            elif event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                return self.options[self.selected]
        return None

    def draw(self, screen, x, y):
        if self.open:
            width, height = 160, 180
            pygame.draw.rect(screen, (20, 20, 60), (x, y, width, height))
            pygame.draw.rect(screen, (255, 255, 255), (x, y, width, height), 2)
            font = pygame.font.SysFont(None, 32)
            for i, opt in enumerate(self.options):
                color = (255, 255, 0) if i == self.selected else (255, 255, 255)
                surf = font.render(opt, True, color)
                screen.blit(surf, (x + 20, y + 20 + i * 38))