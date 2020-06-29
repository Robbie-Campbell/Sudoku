# Simple pygame program

# Import and initialize the pygame library
import pygame
import random
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT
)
pygame.mixer.init()
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

score = 0
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
black = (0, 0, 0)

gameDisplay = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Missile Dodgers!')
clock = pygame.time.Clock()


def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()


def game_intro():
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(white)
        large_text = pygame.font.Font('freesansbold.ttf', 115)
        TextSurf, TextRect = text_objects("Game On", large_text)
        TextRect.center = ((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))
        gameDisplay.blit(TextSurf, TextRect)
        pygame.display.update()
        clock.tick(15)
        pygame.time.wait(2000)
        main_game()


def game_outro():
    outro = True
    crash_sound = pygame.mixer.Sound("C:/Users/robbi/Python/sudoku/crash.wav")
    crash_sound.play()
    crash_sound.set_volume(0.2)
    while outro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(white)
        large_text = pygame.font.Font('freesansbold.ttf', 40)
        TextSurf, TextRect = text_objects("Good Job! You scored: " + str(score), large_text)
        TextRect.center = ((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))
        gameDisplay.blit(TextSurf, TextRect)
        pygame.display.update()


def main_game():
    class Cloud(pygame.sprite.Sprite):
        def __init__(self):
            super(Cloud, self).__init__()
            self.surf = pygame.image.load("C:/Users/robbi/Python/sudoku/cloud.png").convert_alpha()

            self.rect = self.surf.get_rect(
                center=(
                    random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                    random.randint(0, SCREEN_HEIGHT)
                )
            )

        def update(self):
            self.rect.move_ip(-5, 0)
            if self.rect.right < 0:
                self.kill()

    class Enemy(pygame.sprite.Sprite):
        def __init__(self):
            super(Enemy, self).__init__()
            self.surf = pygame.image.load("C:/Users/robbi/Python/sudoku/missile.png").convert_alpha()
            self.rect = self.surf.get_rect(
                center=(
                    random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                    random.randint(0, SCREEN_HEIGHT),
                )
            )
            self.speed = random.randint(5, 20)

        def update(self):
            self.rect.move_ip(-self.speed, 0)
            if self.rect.right < 0:
                self.kill()

    class Player(pygame.sprite.Sprite):
        def __init__(self):
            super(Player, self).__init__()
            self.surf = pygame.image.load("C:/Users/robbi/Python/sudoku/jet.png").convert_alpha()
            self.rect = self.surf.get_rect(
                center=(
                    0,
                    SCREEN_HEIGHT / 2
                )
            )

        def update(self, key_press):
            if key_press[K_UP]:
                self.rect.move_ip(0, -5)
                move_up_sound.play()
            if key_press[K_DOWN]:
                self.rect.move_ip(0, 5)
                move_down_sound.play()
            if key_press[K_LEFT]:
                self.rect.move_ip(-5, 0)
            if key_press[K_RIGHT]:
                self.rect.move_ip(5, 0)

            # Collision detection
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.right > SCREEN_WIDTH:
                self.rect.right = SCREEN_WIDTH
            if self.rect.top <= 0:
                self.rect.top = 0
            if self.rect.bottom >= SCREEN_HEIGHT:
                self.rect.bottom = SCREEN_HEIGHT

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    add_enemy_rate = 250
    ADDENEMY = pygame.USEREVENT + 1
    pygame.time.set_timer(ADDENEMY, add_enemy_rate)
    ADDCLOUD = pygame.USEREVENT + 2
    pygame.time.set_timer(ADDCLOUD, 1000)

    pygame.mixer.set_num_channels(8)
    pygame.mixer.music.load("theme.mp3")
    pygame.mixer.music.play(loops=-1)
    pygame.mixer.music.set_volume(0.5)
    move_up_sound = pygame.mixer.Sound("C:/Users/robbi/Python/sudoku/up.wav")
    move_down_sound = pygame.mixer.Sound("C:/Users/robbi/Python/sudoku/down.wav")

    move_up_sound.set_volume(0.2)
    move_down_sound.set_volume(0.2)

    player = Player()

    enemies = pygame.sprite.Group()
    clouds = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    clock = pygame.time.Clock()
    running = True
    while running:
        global score
        font = pygame.font.Font('freesansbold.ttf', 32)
        # on which text is drawn on it.
        text = font.render('Score: ' + str(score), True, green, blue)

        # create a rectangular object for the
        # text surface object
        textRect = text.get_rect()

        textRect.center = (120, 30)
        score += 1

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            elif event.type == QUIT:
                running = False

            elif event.type == ADDENEMY:
                add_enemy_rate += 1
                new_enemy = Enemy()
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)

            elif event.type == ADDCLOUD:
                new_cloud = Cloud()
                clouds.add(new_cloud)
                all_sprites.add(new_cloud)

        pressed_keys = pygame.key.get_pressed()

        player.update(pressed_keys)

        enemies.update()

        clouds.update()

        screen.fill((135, 206, 250))

        screen.blit(text, textRect)

        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)

        if pygame.sprite.spritecollideany(player, enemies):
            player.surf = pygame.image.load("C:/Users/robbi/Python/sudoku/explosion.png").convert_alpha()
            player.rect = player.surf.get_rect()
            player.kill()
            move_up_sound.stop()
            move_down_sound.stop()
            pygame.mixer.music.stop()
            game_outro()
            running = False

        screen.blit(player.surf, player.rect)
        pygame.display.flip()
        clock.tick(30)


game_intro()

