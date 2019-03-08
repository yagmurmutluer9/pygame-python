import pygame
import random
import sys

pygame.init()

# background music
pygame.mixer.init()
pygame.mixer.music.load('nyancat.mp3')
pygame.mixer.music.play(-1)

# background size
Width = 800
Height = 600
# colors
Red = (255, 0, 0)
Blue = (0, 0, 255)
Yellow = (239, 239, 239)
background_color = (0, 0, 0)

player_size = 50
player_pos = [Width / 2, Height - 2 * player_size]

enemy_size = 50
enemy_Pos = [random.randint(0, Width - enemy_size), 0]
enemy_List = [enemy_Pos]


BACKGROUND = pygame.image.load("background_image.png")

character = pygame.image.load("cha2.png")
character = pygame.transform.scale(character, (player_size, player_size))


enemy = pygame.image.load("enemy.png")
enemy = pygame.transform.scale(enemy, (enemy_size, enemy_size))

SPEED = 5
second_screen = pygame.display.set_mode((Width-740, Height-500))
screen = pygame.display.set_mode((Width, Height))

game_over = False
score_ = 0
clock = pygame.time.Clock()

myFont = pygame.font.SysFont("Arial", 15)


def set_level(score, _speed):
    if score < 30:
        _speed = 10

    elif score < 50:
        _speed = 15

    elif score < 70:
        _speed = 20
    else:
        _speed = 30
    return _speed


def drop_enemies(enemy_list):
    delay = random.random()  # it generates a random num between 0-1
    if len(enemy_list) < 10 and delay < 0.1:
        x_pos = random.randint(0, Width - enemy_size)
        y_pos = 0
        enemy_list.append([x_pos, y_pos])


def draw_enemies(enemy_list):
    for enemy_pos in enemy_list:
        # pygame.draw.rect(screen, Blue, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))
        screen.blit(enemy, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))


def update_enemy_positions(enemy_list, score):
    for idx, enemy_pos in enumerate(enemy_list):
        if (enemy_pos[1] >= 0) and enemy_pos[1] < Height:
            enemy_pos[1] += SPEED
        else:
            enemy_list.pop(idx)
            score += 1
    return score


def collision_check(enemy_list, player_p):
    for enemy_pos in enemy_list:
        if detect_collision(enemy_pos, player_p):
            return True
    return False


def detect_collision(player_p, enemy_pos):
    p_x = player_p[0]
    p_y = player_p[1]
    e_x = enemy_pos[0]
    e_y = enemy_pos[1]

    if ((e_x >= p_x) and e_x < (p_x + player_size)) or (p_x >= e_x and (p_x < e_x + enemy_size)):
        if ((e_y >= p_y) and e_y < (p_y + player_size)) or (p_y >= e_y and (p_y < e_y + enemy_size)):
            return True
    return False


while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            x = player_pos[0]
            y = player_pos[1]
            if event.key == pygame.K_LEFT:
                x -= player_size

            elif event.key == pygame.K_RIGHT:
                x += player_size

            player_pos = [x, y]

    # screen.fill(background_color)
    screen.blit(BACKGROUND, (0, 0))

    drop_enemies(enemy_List)
    score_ = update_enemy_positions(enemy_List, score_)
    SPEED = set_level(score_, SPEED)
    # BACKGROUND = set_background(score_, BACKGROUND)

    print(score_)
    text = "Score:  " + str(score_)
    label = myFont.render(text, 3, Blue)
    second_screen.blit(label, (Width - 200, Height - 40))
    if collision_check(enemy_List, player_pos):
        game_over = True
        break
    draw_enemies(enemy_List)
    # pygame.draw.rect(screen, Yellow, (Width - 200, Height - 40, 40, 80))
    screen.blit(character, (player_pos[0], player_pos[1], player_size, player_size))
    # pygame.draw.rect(screen, Red, (player_pos[0], player_pos[1], player_size, player_size))
    clock.tick(30)
    pygame.display.update()
