import pygame
import time
import random

class Battler:
    def __init__(self, name, level, hp, hp_max, attack, defense, moves, move_info):
        self.name = name
        self.level = level
        self.hp = hp
        self.hp_max = hp_max
        self.attack = attack
        self.defense = defense
        self.moves = moves
        self.move_info = move_info
class Player(Battler):
    def __init__(self, data):
        super().__init__(
            name=data["name"],
            level=data["level"],
            hp=data["hp"],
            hp_max=data["hp_max"],
            attack=data["attack"],
            defense=data["defense"],
            moves=data["moves"],
            move_info=data["move_info"]
        )
        # Player-specific fields
        self.exp = data.get("exp", 0)
        self.exp_max = data.get("exp_max", 100)
        # Add more player-specific fields if needed
class Enemy(Battler):
    def __init__(self, data):
        super().__init__(
            name=data["name"],
            level=data["level"],
            hp=data["hp"],
            hp_max=data["hp_max"],
            attack=data["attack"],
            defense=data["defense"],
            moves=data["moves"],
            move_info=data["move_info"]
        )
        # Enemy-specific fields
        self.expyield = data.get("expyield", 0)
        # Add more enemy-specific fields if needed

class Battle:
    def __init__(self, screen_width, screen_height, player, enemy):
        self.just_opened = False 
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.open = False
        self.player = player
        self.enemy = enemy
        self.selected = 0
        self.blink_start = time.time()
        self.blink_on = True
        self.turn = "player"  # "player" or "enemy"
        self.last_action_text = ""
        self.last_damage = 0
        self.action_display_time = 0  # in seconds
        self.action_display_start = None
        self.player_sprite = pygame.image.load(f"assets/pokemonsprites/{player.name.lower()}.png").convert_alpha()
        self.enemy_sprite = pygame.image.load(f"assets/pokemonsprites/{enemy.name.lower()}.png").convert_alpha()
        # Resize sprites (adjust sizes as needed)
        self.player_sprite = pygame.transform.scale(self.player_sprite, (170, 155))
        self.enemy_sprite = pygame.transform.scale(self.enemy_sprite, (160, 160))
        self.player_dead = False
        self.death_message_start = None
        self.death_message_duration = 2  # seconds
        self.showing_message = False

    def show_death_message(self):
        self.player_dead = True
        self.death_message_start = time.time()

    def set_enemy(self, enemy):
        self.enemy = enemy
        self.enemy_sprite = pygame.image.load(f"assets/pokemonsprites/{enemy.name.lower()}.png").convert_alpha()
        self.enemy_sprite = pygame.transform.scale(self.enemy_sprite, (160, 160))
    def update_blink(self):
        # Call this once per frame before draw
        if time.time() - self.blink_start > 0.35:  # blink every 0.35s
            self.blink_on = not self.blink_on
            self.blink_start = time.time()

    def handle_event(self, event):
        if self.showing_message and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.showing_message = False
            self.last_action_text = ""
            self.action_display_start = None
            # Only switch turn if it was enemy's move
            if self.turn == "enemy":
                self.turn = "player"
            return
        if self.turn == "player" and event.type == pygame.KEYDOWN:
            row = self.selected // 2
            col = self.selected % 2
            if event.key == pygame.K_ESCAPE:
                self.open = False
            elif event.key == pygame.K_LEFT:
                if col > 0:
                    self.selected -= 1
            elif event.key == pygame.K_RIGHT:
                if col < 1 and self.selected + 1 < len(self.player.moves):
                    self.selected += 1
            elif event.key == pygame.K_UP:
                if row > 0:
                    self.selected -= 2
            elif event.key == pygame.K_DOWN:
                if row < 1 and self.selected + 2 < len(self.player.moves):
                    self.selected += 2
            elif event.key == pygame.K_RETURN:
                # print(f"Selected action: {self.player.moves[self.selected]}")
                # Player attacks
                move_idx = self.selected
                move_name = self.player.moves[move_idx]
                basebasedamage = self.player.move_info[move_idx]["damage"]
                level = self.player.level
                crit = random.uniform(0,1)
                attack = self.player.attack
                defense = self.player.defense
                accuracy = (self.player.move_info[move_idx]["accuracy"])
                if self.player.move_info[move_idx]["stab"]==1:
                    stab=1.5
                else:
                    stab=1
                basedamage = ((2*level/5+2)*basebasedamage*(attack/defense))/50+2
                if crit<0.04:
                    basedamage=basedamage*1.7
                    crit_text=" A critical hit!"
                else:
                    crit_text=""
                damage = int(basedamage * stab * random.uniform(0.85, 1.0))   
                if random.uniform(0,99) > accuracy:
                    damage = 0  # Missed attack
                    self.last_action_text = f"{self.player.name} used {move_name}! But it missed!"
                    self.showing_message = True
                else:
                    self.enemy.hp = max(0, self.enemy.hp - damage)
                    self.last_action_text = f"{self.player.name} used {move_name}! {crit_text} Damage: {damage}"
                    self.showing_message = True
                self.action_display_time = 2
                self.action_display_start = time.time()
                self.last_damage = damage
                self.turn = "enemy"

    def enemy_turn(self):
        # Enemy attacks
        move_idx = random.randint(0, len(self.enemy.moves) - 1)
        move_name = self.enemy.moves[move_idx]
        basebasedamage = self.enemy.move_info[move_idx]["damage"]
        level = self.enemy.level
        attack = self.enemy.attack
        defense = self.enemy.defense
        accuracy = (self.enemy.move_info[move_idx]["accuracy"])

        if self.enemy.move_info[move_idx]["stab"]==1:
            stab=1.5
        else:
            stab=1
        basedamage = ((2*level/5+2)*basebasedamage*(attack/defense))/50+2
        damage = int(basedamage * stab * random.uniform(0.85, 1.0))
        if random.uniform(0,99) > accuracy:
            damage = 0  # Missed attack
            self.last_action_text = f"{self.enemy.name} used {move_name}! But it missed!"
            self.showing_message = True
        else:
            self.player.hp = max(0, self.player.hp - damage)
            self.last_action_text = f"{self.enemy.name} used {move_name}! Damage: {damage}"
            self.showing_message = True
        self.action_display_time = 2
        self.action_display_start = time.time()
        self.last_damage = damage
        self.turn = "player"
     
    def update(self):
        # Call this once per frame in your main loop
        if self.turn == "enemy":
            self.enemy_turn()
            
    def action_text_showing(self):
        return self.last_action_text and self.action_display_start and \
            time.time() - self.action_display_start < self.action_display_time
    
    def draw(self, screen):
        # Grassland gradient background (top lighter, bottom deeper green)
        for y in range(self.screen_height):
            t = y / self.screen_height
            r = int(70 + 30 * t)      # subtle shift
            g = int(160 + 60 * t)     # richer green toward bottom
            b = int(70 + 25 * t)
            pygame.draw.line(screen, (r, g, b), (0, y), (self.screen_width, y))

        # Outer decorative borders (dark moss + light highlight)
        pygame.draw.rect(screen, (30, 60, 35), (8, 8, self.screen_width - 16, self.screen_height - 16), 10)
        pygame.draw.rect(screen, (200, 235, 205), (18, 18, self.screen_width - 36, self.screen_height - 36), 2)

        # Enemy info box (pale leaf green)
        upper_rect = pygame.Rect(40, 40, self.screen_width - 80, 80)
        pygame.draw.rect(screen, (210, 235, 195), upper_rect, border_radius=18)
        pygame.draw.rect(screen, (40, 80, 45), upper_rect, 4, border_radius=18)

        font = pygame.font.SysFont(None, 40)
        enemy_text = f"{self.enemy.name}♂   Lv{self.enemy.level}"
        enemy_surf = font.render(enemy_text, True, (25, 55, 30))
        screen.blit(enemy_surf, (upper_rect.x + 20, upper_rect.y + 15))

        # Enemy HP bar
        hp_bar_w = 200
        hp_bar_h = 16
        hp_x = upper_rect.x + 20
        hp_y = upper_rect.y + 50
        pygame.draw.rect(screen, (25, 55, 30), (hp_x - 2, hp_y - 2, hp_bar_w + 4, hp_bar_h + 4), border_radius=8)
        hp_ratio = self.enemy.hp / self.enemy.hp_max
        pygame.draw.rect(screen, (90, 200, 90), (hp_x, hp_y, int(hp_bar_w * hp_ratio), hp_bar_h), border_radius=8)

        # Lower part: Player info + actions (soft meadow panel)
        lower_rect = pygame.Rect(0, self.screen_height - 200, self.screen_width, 200)
        pygame.draw.rect(screen, (205, 230, 190), lower_rect, border_radius=28)
        pygame.draw.rect(screen, (40, 80, 45), lower_rect, 5, border_radius=28)

        player_font = pygame.font.SysFont(None, 32)
        player_text = f"{self.player.name}♂   Lv{self.player.level}"
        player_surf = player_font.render(player_text, True, (25, 55, 30))
        screen.blit(player_surf, (lower_rect.x + 30, lower_rect.y + 20))

        player_hp_x = lower_rect.x + 30
        player_hp_y = lower_rect.y + 60
        pygame.draw.rect(screen, (25, 55, 30), (player_hp_x - 2, player_hp_y - 2, hp_bar_w + 4, hp_bar_h + 4), border_radius=8)
        player_hp_ratio = self.player.hp / self.player.hp_max
        if player_hp_ratio<=0.2:
            hp_color=(200, 40, 40)
        elif player_hp_ratio<=0.5:
            hp_color=(240, 220, 60)
        else:
            hp_color=(90, 200, 90)
        pygame.draw.rect(screen, hp_color, (player_hp_x, player_hp_y, int(hp_bar_w * player_hp_ratio), hp_bar_h), border_radius=8)

        hp_text = f"{self.player.hp}/{self.player.hp_max}"
        hp_surf = player_font.render(hp_text, True, (25, 55, 30))
        screen.blit(hp_surf, (player_hp_x + hp_bar_w + 20, player_hp_y - 4))
                # EXP bar (above HP bar)
        exp_bar_w = hp_bar_w
        exp_bar_h = 10
        exp_x = player_hp_x
        exp_y = player_hp_y - 18  # 18 pixels above HP bar
        pygame.draw.rect(screen, (25, 55, 120), (exp_x, exp_y, exp_bar_w, exp_bar_h), border_radius=6)  # border
        pygame.draw.rect(screen, (80, 160, 255), (exp_x, exp_y, int(exp_bar_w * (self.player.exp/self.player.exp_max)), exp_bar_h), border_radius=6)  # filled 25%
        pygame.draw.rect(screen, (25, 55, 30), (exp_x-2, exp_y-2, exp_bar_w+4, exp_bar_h+4), 2, border_radius=8)  # outline
        # Actions (leaf tiles)
        action_font = pygame.font.SysFont(None, 36)
        action_w = 220
        action_h = 50
        action_x0 = lower_rect.x + 40
        action_y0 = lower_rect.y + 83

        for i, action in enumerate(self.player.moves):
            col = i % 2
            row = i // 2
            surf = action_font.render(action, True, (25, 55, 30))
            rect_x = action_x0 + col * (action_w + 30)
            rect_y = action_y0 + row * (action_h + 12)
            rect = pygame.Rect(rect_x, rect_y, action_w, action_h)

            # Blinking highlight (sunlit grass) else light leaf
            if self.selected == i and self.blink_on:
                fill_color = (250, 245, 160)  # sunny flash
            elif self.selected == i:
                fill_color = (235, 225, 140)
            else:
                fill_color = (225, 240, 205)

            pygame.draw.rect(screen, fill_color, rect, border_radius=14)
            pygame.draw.rect(screen, (40, 80, 45), rect, 3, border_radius=14)

            text_x = rect.x + 18
            text_y = rect.y + (rect.height - surf.get_height()) // 2
            screen.blit(surf, (text_x, text_y))

        # Move detail (type + PP) panel (small bush patch)
        if 0 <= self.selected < len(self.player.moves):
            move = self.player.move_info[self.selected]
            info_box = pygame.Rect(self.screen_width - 230, lower_rect.y + 95, 190, 80)
            pygame.draw.rect(screen, (195, 220, 180), info_box, border_radius=16)
            pygame.draw.rect(screen, (40, 80, 45), info_box, 3, border_radius=16)

            pp_surf = player_font.render(f"PP  {move['pp']}", True, (25, 55, 30))
            type_surf = player_font.render(f"TYPE/{move['type']}", True, (25, 55, 30))
            screen.blit(pp_surf, (info_box.x + 16, info_box.y + 12))
            screen.blit(type_surf, (info_box.x + 16, info_box.y + 42))
        
        # Draw player sprite (bottom left, above menu)
        player_sprite_x = 60
        player_sprite_y = self.screen_height - 200 - 145  # above the menu panel
        screen.blit(self.player_sprite, (player_sprite_x, player_sprite_y))
        # Draw enemy sprite (top right, below enemy info)
        enemy_sprite_x = self.screen_width - 200
        enemy_sprite_y = 130  # below enemy info box
        screen.blit(self.enemy_sprite, (enemy_sprite_x, enemy_sprite_y))
        
        # Show last action and damage
        info_font = pygame.font.SysFont(None, 28)
        if self.showing_message and self.last_action_text:
            # Draw message box over action area, but not over HP/EXP
            msg_box_rect = pygame.Rect(lower_rect.x + 30, lower_rect.y + 75, self.screen_width - 60, 120)
            pygame.draw.rect(screen, (245, 245, 220), msg_box_rect, border_radius=18)
            pygame.draw.rect(screen, (40, 80, 45), msg_box_rect, 3, border_radius=18)
            info_font = pygame.font.SysFont(None, 32)
            lines = self.last_action_text.split('\n')
            for i, line in enumerate(lines):
                msg_surf = info_font.render(line, True, (30, 30, 30))
                screen.blit(msg_surf, (msg_box_rect.x + 20, msg_box_rect.y + 20 + i * 36))
            prompt_surf = info_font.render("Press Enter to continue...", True, (80, 80, 80))
            screen.blit(prompt_surf, (msg_box_rect.x + 20, msg_box_rect.y + 80))
        if self.player_dead:
            death_surf = info_font.render(f"{self.player.name} has fainted!", True, (200, 30, 30))
            screen.blit(death_surf, (40, self.screen_height - 270))
            