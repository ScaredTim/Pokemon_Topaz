import pygame

class Battle:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.open = False
        self.enemy_name = "TENTACOOL"
        self.enemy_level = 11
        self.player_name = "MARSHTOMP"
        self.player_level = 19
        self.player_hp = 58
        self.player_hp_max = 58
        self.enemy_hp = 30
        self.enemy_hp_max = 30
        self.actions = ["TACKLE", "MUD-SLAP", "MUD SHOT", "WATER GUN"]
        self.selected = 0
        self.move_info = [
            {"type": "NORMAL", "pp": "35/35"},
            {"type": "GROUND", "pp": "10/10"},
            {"type": "GROUND", "pp": "10/10"},
            {"type": "WATER", "pp": "25/25"},
        ]

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            row = self.selected // 2
            col = self.selected % 2
            if event.key == pygame.K_ESCAPE:
                self.open = False
            elif event.key == pygame.K_LEFT:
                if col > 0:
                    self.selected -= 1
            elif event.key == pygame.K_RIGHT:
                if col < 1 and self.selected + 1 < len(self.actions):
                    self.selected += 1
            elif event.key == pygame.K_UP:
                if row > 0:
                    self.selected -= 2
            elif event.key == pygame.K_DOWN:
                if row < 1 and self.selected + 2 < len(self.actions):
                    self.selected += 2
            elif event.key == pygame.K_RETURN:
                print(f"Selected action: {self.actions[self.selected]}")

    def draw(self, screen):
        # Fill background
        screen.fill((250, 240, 200))

        # Upper part: Enemy info
        upper_rect = pygame.Rect(40, 40, self.screen_width - 80, 80)
        pygame.draw.rect(screen, (255, 255, 230), upper_rect)
        pygame.draw.rect(screen, (80, 80, 80), upper_rect, 3)
        font = pygame.font.SysFont(None, 40)
        enemy_text = f"{self.enemy_name}♂   Lv{self.enemy_level}"
        enemy_surf = font.render(enemy_text, True, (30, 30, 30))
        screen.blit(enemy_surf, (upper_rect.x + 20, upper_rect.y + 15))
        # Enemy HP bar
        hp_bar_w = 200
        hp_bar_h = 16
        hp_x = upper_rect.x + 20
        hp_y = upper_rect.y + 50
        pygame.draw.rect(screen, (0, 0, 0), (hp_x-2, hp_y-2, hp_bar_w+4, hp_bar_h+4))
        hp_ratio = self.enemy_hp / self.enemy_hp_max
        pygame.draw.rect(screen, (80, 200, 80), (hp_x, hp_y, int(hp_bar_w * hp_ratio), hp_bar_h))

        # Lower part: Player info and actions
        lower_rect = pygame.Rect(0, self.screen_height - 200, self.screen_width, 200)
        pygame.draw.rect(screen, (220, 220, 240), lower_rect)
        pygame.draw.rect(screen, (80, 80, 80), lower_rect, 3)
        # Player info
        player_font = pygame.font.SysFont(None, 32)
        player_text = f"{self.player_name}♂   Lv{self.player_level}"
        player_surf = player_font.render(player_text, True, (30, 30, 30))
        screen.blit(player_surf, (lower_rect.x + 30, lower_rect.y + 20))
        # Player HP bar
        player_hp_x = lower_rect.x + 30
        player_hp_y = lower_rect.y + 60
        pygame.draw.rect(screen, (0, 0, 0), (player_hp_x-2, player_hp_y-2, hp_bar_w+4, hp_bar_h+4))
        player_hp_ratio = self.player_hp / self.player_hp_max
        pygame.draw.rect(screen, (80, 200, 80), (player_hp_x, player_hp_y, int(hp_bar_w * player_hp_ratio), hp_bar_h))
        # Player HP text
        hp_text = f"{self.player_hp}/{self.player_hp_max}"
        hp_surf = player_font.render(hp_text, True, (30, 30, 30))
        screen.blit(hp_surf, (player_hp_x + hp_bar_w + 20, player_hp_y - 4))

        # Actions grid (2x2)
        action_font = pygame.font.SysFont(None, 36)
        action_w = 220
        action_h = 50
        action_x0 = lower_rect.x + 40
        action_y0 = lower_rect.y + 110
        for i, action in enumerate(self.actions):
            col = i % 2
            row = i // 2
            rect = pygame.Rect(action_x0 + col * (action_w + 30), action_y0 + row * (action_h + 10), action_w, action_h)
            color = (255, 255, 255) if self.selected != i else (255, 255, 180)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (80, 80, 80), rect, 2)
            surf = action_font.render(action, True, (30, 30, 30))
            screen.blit(surf, (rect.x + 16, rect.y + 8))
        # Show PP/Type info for selected move
        if 0 <= self.selected < len(self.actions):
            move = self.move_info[self.selected]
            pp_surf = player_font.render(f"PP   {move['pp']}", True, (30, 30, 30))
            type_surf = player_font.render(f"TYPE/{move['type']}", True, (30, 30, 30))
            screen.blit(pp_surf, (self.screen_width - 200, lower_rect.y + 120))
            screen.blit(type_surf, (self.screen_width - 200, lower_rect.y + 150))