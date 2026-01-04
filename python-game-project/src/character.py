import pygame
class Character:
    def __init__(self, image_path, x, y, width=50, height=50):
        # Load and scale the image
        original_image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(original_image, (width, height))
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.toggle_state = False  # To track the toggle state for alternating images

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def change_image(self, image_path):
        # Change the character's image and scale it
        self.image = pygame.transform.scale(pygame.image.load(image_path), (self.width, self.height))

    def toggle_image(self, image_path1, image_path2):
        # Alternate between two images
        if self.toggle_state:
            self.change_image(image_path1)
        else:
            self.change_image(image_path2)
        self.toggle_state = not self.toggle_state

    def get_rect(self):
        hitbox_width = int(self.width * 0.6)  # 60% of image width
        hitbox_x = self.x + (self.width - hitbox_width) // 2  # center the hitbox
        # return pygame.Rect(hitbox_x, self.y, hitbox_width, self.height)
        return pygame.Rect(hitbox_x, self.y, hitbox_width, self.height)

    def draw(self, screen, offset=(0, 0)):
        screen.blit(self.image, (self.x + offset[0], self.y + offset[1]))

    def handle_movement(self, keys, obstacles, screen_width, screen_height):
        move_x, move_y = 0, 0
        if keys[pygame.K_UP]:
            self.change_image("assets/Up.png")
            move_y = -10
        if keys[pygame.K_DOWN]:
            self.change_image("assets/Down.png")
            move_y = 10
        if keys[pygame.K_LEFT]:
            self.toggle_image("assets/Left1.png", "assets/Left2.png")
            move_x = -10
        if keys[pygame.K_RIGHT]:
            self.toggle_image("assets/Right1.png", "assets/Right2.png")
            move_x = 10

        if move_x != 0 or move_y != 0:
            new_rect = self.get_rect().move(move_x, move_y)
            # You can use a can_move function or inline the logic here
            if (
                0 <= new_rect.left and new_rect.right <= screen_width and
                0 <= new_rect.top and new_rect.bottom <= screen_height and
                not any(new_rect.colliderect(rect) for rect in obstacles)
            ):
                self.move(move_x, move_y)

    