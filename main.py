import pygame
import os
import spritesheet
import random


pygame.init()

# Set up screen
SCREEN_WIDTH = 1088
SCREEN_HEIGHT = 640
screen_size = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Dino City Dodge")

# create text for screen
txt = pygame.font.SysFont("Arial", 20, True, False)


# Variables
clock = pygame.time.Clock()
FPS = 60
score = 0

# asteroid
ast = pygame.image.load(os.path.join(
    "assets", "objects", "asteroid3.png")).convert_alpha()

# Load background images
bg_img = pygame.transform.scale(pygame.image.load(
    os.path.join("assets", "bg", "bg.png")), screen_size).convert_alpha()
bg_img2 = pygame.transform.scale(pygame.image.load(
    os.path.join("assets", "bg", "buildings.png")), screen_size).convert_alpha()
bg_img3 = pygame.transform.scale(pygame.image.load(
    os.path.join("assets", "bg", "farbuildings.png")), screen_size).convert_alpha()
bg_img4 = pygame.transform.scale(pygame.image.load(
    os.path.join("assets", "bg", "foreground.png")), screen_size).convert_alpha()
ground = pygame.image.load(os.path.join(
    "assets", "bg", "ground2.png")).convert_alpha()

# power up images
speed_img = pygame.image.load(os.path.join(
    "assets", "objects", "speed.png")).convert_alpha()

# functions and classes


class Player(pygame.sprite.Sprite):

    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)

        self.scale_x = 12
        self.scale_y = 16
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.gravity = 0.2
        self.ground_y = 525
        self.scale = scale
        sprite_sheet_image = pygame.image.load(os.path.join(
            "assets", "player", "doux.png")).convert_alpha()
        self.sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)
        self.animation_list = []
        self.animation_steps = [4, 6, 3, 4, 7]
        self.action = 0
        self.last_update = pygame.time.get_ticks()
        self.animation_cooldown = 150
        self.frame = 0
        self.step_counter = 0
        self.rect = pygame.Rect(self.x, self.y, self.scale_x *
                                self.scale, self.scale_y * self.scale)
        self.mask = pygame.mask.from_surface(sprite_sheet_image)
        self.walk = 2
        self.run = 4
        self.update()

    def update(self):
        # player
        self.vy += self.gravity

        if self.y >= self.ground_y:
            self.vy = 0
            self.y = self.ground_y

        self.x += self.vx
        self.y += self.vy
        self.rect.x = self.x + 17
        self.rect.y = self.y + 13

        for animation in self.animation_steps:
            temp_img_list = []
            for _ in range(animation):
                temp_img_list.append(self.sprite_sheet.get_image(
                    self.step_counter, 24, 24, self.scale, (0, 0, 0)))
                self.step_counter += 1
            self.animation_list.append(temp_img_list)

        current_time = pygame.time.get_ticks()
        if current_time - self.last_update > self.animation_cooldown:
            self.last_update = current_time
            self.frame += 1
            if self.frame >= len(self.animation_list[self.action]):
                self.frame = 0

        keys = pygame.key.get_pressed()
        # if no keys are pressed action = 0
        if not keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
            self.rect.y = self.y + 20
            self.action = 0
            if self.frame >= len(self.animation_list[self.action]):
                self.frame = 0
            x = self.animation_list[self.action][self.frame]

        if keys[pygame.K_RIGHT]:
            self.action = 1
            if self.frame >= len(self.animation_list[self.action]):
                self.frame = 0
            x = self.animation_list[self.action][self.frame]
            if self.x < SCREEN_WIDTH - 24 * self.scale:
                self.x += self.walk

        if keys[pygame.K_LSHIFT] and keys[pygame.K_RIGHT]:
            self.rect.x = self.x + 40
            self.rect.y = self.y + 20
            self.scale_y = 28
            self.action = 4
            x = self.animation_list[self.action][self.frame]
            if self.x < SCREEN_WIDTH - 24 * self.scale:
                self.x += self.run

        if keys[pygame.K_LEFT]:
            self.action = 1
            if self.frame >= len(self.animation_list[self.action]):
                self.frame = 0
            x = self.animation_list[self.action][self.frame]
            if self.x > 0:
                self.x -= self.walk

        if keys[pygame.K_LSHIFT] and keys[pygame.K_LEFT]:
            self.rect.x = self.x + 27
            self.rect.y = self.y + 20
            self.action = 4
            x = self.animation_list[self.action][self.frame]
            if self.x > 0:
                self.x -= self.run

        if keys[pygame.K_SPACE]:
            self.rect.x = self.x + 20
            self.rect.y = self.y + 15
            self.scale_y = 5
            self.action = 2
            if self.frame >= len(self.animation_list[self.action]):
                self.frame = 0
            if self. y >= self.ground_y:
                self.vy = -5
                self.y -= 5
                self.frame = 2
            x = self.animation_list[self.action][self.frame]

        # animation
        screen.blit(x, (self.x, self.y))
        # pygame.draw.rect(screen, (255, 0, 0), self.rect, 3)


class Asteroid(pygame.sprite.Sprite):

    def __init__(self, x, y, scale, hitbox_scale):
        pygame.sprite.Sprite.__init__(self)

        self.x = x
        self.y = y
        self.image = pygame.transform.scale(
            ast, (int(ast.get_width()*scale), int(ast.get_height()*scale)))
        self.rect = self.image.get_rect()
        self.speed = 9
        self.gravity = 0.5
        self.counter = 0
        self.hitbox = self.rect.inflate(-int(self.rect.width * (
            1 - hitbox_scale)), -int(self.rect.height * (1 - hitbox_scale)))

    def spawn(self):
        self.rect.y += self.speed*self.gravity
        self.hitbox.y = self.rect.y

        if self.rect.y > SCREEN_HEIGHT:
            self.rect.y = -150
            self.hitbox.y = -125
            self.rect.x = random.randrange(0, SCREEN_WIDTH)
            self.hitbox.x = self.rect.x
            self.counter += 1
            if self.counter % 5 == 0:
                self.speed += 3

    def draw_score(self):
        score_count = self.score_txt = txt.render(
            "Score: " + str(self.counter), True, (255, 255, 255))
        speed_count = self.speed_txt = txt.render(
            "Speed: " + str(self.speed + 1), True, (255, 255, 255))
        screen.blit(score_count, (10, 10))
        # screen.blit(speed_count, (10, 30))

    def update(self):
        self.spawn()
        screen.blit(self.image, self.rect)

        pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 3)


class PowerUp:

    def __init__(self):
        self.image1 = pygame.transform.scale(speed_img, (50, 50))
        self.rect1 = self.image1.get_rect()
        self.counter = 0
        self.x = 0
        self.y = 435

    def update(self):
        if self.counter >= 1:
            self.x = random.randrange(0, SCREEN_WIDTH - self.rect1.width)
            self.counter = 0
        self.rect1.x = self.x
        self.rect1.y = self.y
        screen.blit(self.image1, (self.x, self.y))
    # show the hitbox
    # pygame.draw.rect(screen, (255, 0, 0), self.rect1, 3)


def draw_bg():

    screen.blit(bg_img, (0, 0))
    screen.blit(bg_img2, (0, 0))
    screen.blit(bg_img3, (0, 0))


# more variables
bg_scroll = 0
ground_scroll = 0
power_up_counter = 0


# game running
game_over = False
asteroid = Asteroid(0, 0, 0.2, 0.95)
asteroid2 = Asteroid(0, 0, 0.22, .95)
asteroid3 = Asteroid(0, 0, 0.24, .95)
player = Player(500, 500, 3.5)
power_up = PowerUp()
running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                player.walk = 2
                player.run = 4
                asteroid.counter = 0
                asteroid.speed = 9
                asteroid2.counter = 0
                asteroid2.speed = 9
                asteroid3.counter = 0
                asteroid3.speed = 9
                power_up_counter = 0
                player.x = 500
                player.y = 500
                power_up.x = random.randrange(0, SCREEN_WIDTH)
                asteroid.rect.y = -150
                asteroid2.rect.y = -150
                asteroid3.rect.y = -150
                asteroid.hitbox.y = -125
                asteroid2.hitbox.y = -125
                asteroid3.hitbox.y = -125
                asteroid.rect.x = random.randrange(0, SCREEN_WIDTH)
                asteroid2.rect.x = random.randrange(0, SCREEN_WIDTH)
                asteroid3.rect.x = random.randrange(0, SCREEN_WIDTH)
                asteroid.hitbox.x = asteroid.rect.x
                asteroid2.hitbox.x = asteroid2.rect.x
                asteroid3.hitbox.x = asteroid3.rect.x
                game_over = False
                screen.fill((0, 0, 0))
            draw_bg()
            screen.blit(bg_img4, (bg_scroll, 0))
            screen.blit(bg_img4, (bg_scroll + SCREEN_WIDTH, 0))
            screen.blit(ground, (ground_scroll, 590))
            screen.blit(ground, (ground_scroll + SCREEN_WIDTH, 590))
            power_up_counter_txt = txt.render(
                "Speed up: + " + str(power_up_counter), True, (255, 255, 255))
            screen.blit(power_up_counter_txt, (10, 30))
            restart_txt = txt.render(
                "Press R to restart, Q to quit", True, (255, 255, 255))
            screen.blit(restart_txt, (SCREEN_WIDTH/2 - 100, 10))
            if ground_scroll <= -SCREEN_WIDTH:
                ground_scroll = 0
            ground_scroll -= 2
            if bg_scroll <= -SCREEN_WIDTH:
                bg_scroll = 0
            bg_scroll -= 1
            # functions
            player.update()
            asteroid.update()
            asteroid.draw_score()
            power_up.update()
            if asteroid.counter >= 5:
                asteroid2.update()
            if asteroid.counter >= 10:
                asteroid3.update()
            elif event.key == pygame.K_q:
                running = False

    if player.rect.colliderect(asteroid.hitbox) or player.rect.colliderect(asteroid2.hitbox) or player.rect.colliderect(asteroid3.hitbox):
        game_over = True
        screen.fill((0, 0, 0))
        game_over_txt = txt.render("Game Over", True, (255, 255, 255))
        screen.blit(game_over_txt, (SCREEN_WIDTH/2 - game_over_txt.get_width() /
                    2, SCREEN_HEIGHT/2 - game_over_txt.get_height()/2))

    # if player collides with powerup
    if player.rect.colliderect(power_up.rect1):
        power_up_counter += 1
        power_up.x = random.randrange(0, SCREEN_WIDTH)
        player.walk += 0.1
        player.run += 0.1

    if not game_over:
        screen.fill((0, 0, 0))
        draw_bg()
        screen.blit(bg_img4, (bg_scroll, 0))
        screen.blit(bg_img4, (bg_scroll + SCREEN_WIDTH, 0))
        screen.blit(ground, (ground_scroll, 590))
        screen.blit(ground, (ground_scroll + SCREEN_WIDTH, 590))
        power_up_counter_txt = txt.render(
            "Speed up: + " + str(power_up_counter), True, (255, 255, 255))
        screen.blit(power_up_counter_txt, (10, 30))
        restart_txt = txt.render(
            "Press R to restart, Q to quit", True, (255, 255, 255))
        screen.blit(restart_txt, (SCREEN_WIDTH/2 - 100, 10))
        if ground_scroll <= -SCREEN_WIDTH:
            ground_scroll = 0
        ground_scroll -= 2
        if bg_scroll <= -SCREEN_WIDTH:
            bg_scroll = 0
        bg_scroll -= 1
        # functions
        player.update()
        asteroid.update()
        asteroid.draw_score()
        power_up.update()
        if asteroid.counter >= 5:
            asteroid2.update()
        if asteroid.counter >= 10:
            asteroid3.update()

    pygame.display.update()


pygame.quit()
