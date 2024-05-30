import pygame
import os
import random

pygame.init()

WIDTH, HEIGHT = 800, 600

BLACK = (0, 0, 0)
WHITE = 255, 255, 255
RED = (255, 0, 0)
ORANGE = (255, 175, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 150, 255)
PURPLE = (255, 0, 255)

VEL = 4
FPS = 60

hit = 0

idle = True
right = False
left = False

power_up_fall = False
slime_fall = False
question_fall = False

question_good = False
question_bad = False

font = pygame.font.SysFont(None, 50)

FAR_LEFT, FAR_RIGHT = 60, 740
FAR_LEFT_POWER, FAR_RIGHT_POWER = 160, 650

SLIME_IDLE_WIDTH, SLIME_IDLE_HEIGHT = 100, 75
SLIME_RIGHT_WIDTH, SLIME_RIGHT_HEIGHT = 100, 75
SLIME_LEFT_WIDTH, SLIME_LEFT_HEIGHT = 100, 75

SLIME_BALL_WIDTH, SLIME_BALL_HEIGHT = 60, 60
ACID_BALL_WIDTH, ACID_BALL_HEIGHT = 60, 60
ACID_BALL_WIDTH2, ACID_BALL_HEIGHT2 = 60, 60
POWER_UP_WIDTH, POWER_UP_HEIGHT = 40, 40
QUESTION_COIN_WIDTH, QUESTION_COIN_HEIGHT = 60, 60

SLIME_IDLE = pygame.image.load(os.path.join('slime_idle.png'))
SLIME_IDLE = pygame.transform.rotate(pygame.transform.scale(
    SLIME_IDLE, (SLIME_IDLE_WIDTH, SLIME_IDLE_HEIGHT)), 0)
SLIME_RIGHT = pygame.image.load(os.path.join('slime_right.png'))
SLIME_RIGHT = pygame.transform.rotate(pygame.transform.scale(
    SLIME_RIGHT, (SLIME_RIGHT_WIDTH, SLIME_RIGHT_HEIGHT)), 0)
SLIME_LEFT = pygame.image.load(os.path.join('slime_left.png'))
SLIME_LEFT = pygame.transform.rotate(pygame.transform.scale(
    SLIME_LEFT, (SLIME_LEFT_WIDTH, SLIME_LEFT_HEIGHT)), 0)
SLIME_BALL = pygame.image.load(os.path.join('slime_ball.png'))
SLIME_BALL = pygame.transform.rotate(pygame.transform.scale(
    SLIME_BALL, (SLIME_BALL_WIDTH, SLIME_BALL_HEIGHT)), 180)
ACID_BALL = pygame.image.load(os.path.join('acid.png'))
ACID_BALL = pygame.transform.rotate(pygame.transform.scale(
    ACID_BALL, (ACID_BALL_WIDTH, ACID_BALL_HEIGHT)), 0)
ACID_BALL2 = pygame.image.load(os.path.join('acid.png'))
ACID_BALL2 = pygame.transform.rotate(pygame.transform.scale(
    ACID_BALL2, (ACID_BALL_WIDTH2, ACID_BALL_HEIGHT2)), 0)
POWER_UP = pygame.image.load(os.path.join('power_up.png'))
POWER_UP = pygame.transform.rotate(pygame.transform.scale(
    POWER_UP, (POWER_UP_WIDTH, POWER_UP_HEIGHT)), 0)
QUESTION_COIN = pygame.image.load(os.path.join('question_coin.png'))
QUESTION_COIN = pygame.transform.rotate(pygame.transform.scale(
    QUESTION_COIN, (QUESTION_COIN_WIDTH, QUESTION_COIN_HEIGHT)), 0)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
random_x = random.randint(FAR_LEFT, FAR_RIGHT)
acid_x1 = random.randint(FAR_LEFT, FAR_RIGHT)
acid_x2 = random.randint(FAR_LEFT, FAR_RIGHT)
power_up_x = random.randint(FAR_LEFT_POWER, FAR_RIGHT_POWER)
question_coin_x = random.randint(FAR_LEFT_POWER, FAR_RIGHT_POWER)
chose_fall = random.randint(1, 10)
chose_question = random.randint(1, 2)
slime = pygame.Rect(400, 535, 70, 55)
slime_ball = pygame.Rect(random_x, -100, 60, 60)
acid1 = pygame.Rect(acid_x1, -100, 60, 60)
acid2 = pygame.Rect(acid_x2, -100, 60, 60)
power_up = pygame.Rect(power_up_x, -100, 40, 40)
question_coin = pygame.Rect(question_coin_x, -100, 60, 60)
pygame.display.set_caption('Dodge Up')

if chose_question == 1:
    question_good = True
else:
    question_good = False
if chose_question == 2:
    question_bad = True
else:
    question_bad = False


if chose_fall <= 7:
    slime_fall = True
else:
    slime_fall = False
if chose_fall == 8 or chose_fall == 9:
    power_up_fall = True
else:
    power_up_fall = False
if chose_fall == 10:
    question_fall = True
else:
    question_fall = False


# For restarting the game use the R key
def reset(keys_press):
    global hit, SLIME_BALL_WIDTH, SLIME_BALL_HEIGHT
    if keys_press[pygame.K_r]:
        slime.x = 400
        slime.y = 535
        slime_ball.y = -50
        acid1.y = -50
        acid2.y = -50
        power_up.y = -50
        hit = 0


# The player "Slime" this is its movement code
def slime_moving(keys_press):
    global right, idle, left, slime
    if keys_press[pygame.K_RIGHT] and slime.x < WIDTH - 85:
        slime.x += VEL
        right = True
        idle = False
        left = False
    else:
        if keys_press[pygame.K_LEFT] and slime.x > - 15:
            slime.x -= VEL
            right = False
            idle = False
            left = True
        else:
            right = False
            idle = True
            left = False


# The movement code for the slime ball falling
def slime_ball_moving():
    global hit, chose_fall
    if slime_fall:
        if slime.colliderect(slime_ball):
            hit += 1
            reset_slime_ball()
            choosing_what_falls()
            print(chose_fall)
        elif slime_ball.y < HEIGHT:
            slime_ball.y += VEL * 1.5
        else:
            reset_slime_ball()
            choosing_what_falls()
            print(chose_fall)
            if hit != 0:
                hit = hit - 1


# The movement code for the acid ball falling
def acid_ball_moving1():
    global hit, acid1, acid_x1
    if slime.colliderect(acid1):
        if hit != 0:
            hit -= 1
        reset_acid_ball()
    elif acid1.y < HEIGHT:
        acid1.y += VEL * 1.5
    else:
        reset_acid_ball()


# The movement code for the second acid ball falling
def acid_ball_moving2():
    global hit, acid2, acid_x2
    if slime.colliderect(acid2):
        if hit != 0:
            hit -= 1
        reset_acid_ball2()
    elif acid2.y < HEIGHT:
        acid2.y += VEL * 1.5
    else:
        reset_acid_ball2()


# This movement code is for the power up that will sometimes appear
def power_up_moving():
    global hit, power_up, power_up_x, chose_fall
    if power_up_fall:
        if slime.colliderect(power_up):
            # What this power up does isn't final
            hit += 10
            reset_power_up()
            choosing_what_falls()
            print(chose_fall)
        elif power_up.y < HEIGHT:
            power_up.y += VEL * 1.6
        else:
            if hit < 10:
                hit = 0
            else:
                hit -= 10
            reset_power_up()
            choosing_what_falls()
            print(chose_fall)


def question_coin_moving():
    global hit, question_coin, question_coin_x, chose_fall, question_good, question_bad
    if question_fall:
        if slime.colliderect(question_coin):
            # What this question coin does this isn't final as well
            if question_good:
                hit += 50
                question_good = False
            if question_bad:
                hit = 0
                question_bad = False
            reset_question_coin()
            choosing_what_falls()
            question_action()
            print(chose_fall)
        elif question_coin.y < HEIGHT:
            question_coin.y += VEL
        else:
            reset_question_coin()
            choosing_what_falls()
            print(chose_fall)


def question_action():
    global question_coin, question_good, question_bad, chose_question
    chose_question = random.randint(1, 2)
    if chose_question == 1:
        question_good = True
    else:
        question_good = False
    if chose_question == 2:
        question_bad = True
    else:
        question_bad = False


def choosing_what_falls():
    global chose_fall, slime_fall, power_up_fall, question_fall
    chose_fall = random.randint(1, 10)
    if chose_fall <= 7:
        slime_fall = True
    else:
        slime_fall = False
    if chose_fall == 8 or chose_fall == 9:
        power_up_fall = True
    else:
        power_up_fall = False
    if chose_fall == 10:
        question_fall = True
    else:
        question_fall = False


def reset_acid_ball():
    global acid_x1, acid1
    acid1.y = -100
    acid_x1 = random.randint(FAR_LEFT, FAR_RIGHT)
    acid1.x = acid_x1


def reset_acid_ball2():
    global acid_x2, acid2
    acid2.y = -100
    acid_x2 = random.randint(FAR_LEFT, FAR_RIGHT)
    acid2.x = acid_x2


def reset_slime_ball():
    global random_x
    slime_ball.y = -100
    random_x = random.randint(FAR_LEFT, FAR_RIGHT)
    slime_ball.x = random_x


def reset_power_up():
    global power_up_x
    power_up.y = -100
    power_up_x = random.randint(FAR_LEFT, FAR_RIGHT)
    power_up.x = power_up_x


def reset_question_coin():
    global question_coin_x
    question_coin.y = -100
    question_coin_x = random.randint(FAR_LEFT, FAR_RIGHT)
    question_coin.x = question_coin_x


def draw_txt():
    global hit
    win_text = "Points " + str(hit)
    win_img = font.render(win_text, True, BLACK)
    WIN.blit(win_img, (10, 20))


def draw():
    global right, idle, left, slime, slime_ball, acid_x1, acid_x2, acid1, acid2
    if idle:
        WIN.blit(SLIME_IDLE, (slime.x - 15, slime.y - 8))
    if right:
        WIN.blit(SLIME_RIGHT, (slime.x - 15, slime.y - 8))
    if left:
        WIN.blit(SLIME_LEFT, (slime.x - 15, slime.y - 8))
    WIN.blit(SLIME_BALL, (slime_ball.x, slime_ball.y))
    WIN.blit(ACID_BALL, (acid1.x, acid1.y))
    WIN.blit(ACID_BALL2, (acid2.x, acid2.y))
    WIN.blit(POWER_UP, (power_up.x, power_up.y))
    WIN.blit(QUESTION_COIN, (question_coin.x, question_coin.y))
# Incase I need to see the entire rect
#    pygame.draw.rect(WIN, BLACK, slime)


def main():
    global hit
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        WIN.fill(BLUE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys_press = pygame.key.get_pressed()
        slime_moving(keys_press)
        slime_ball_moving()
        acid_ball_moving1()
        acid_ball_moving2()
        power_up_moving()
        question_coin_moving()
        draw_txt()
        reset(keys_press)
        draw()
        pygame.display.update()

    pygame.quit()


main()
