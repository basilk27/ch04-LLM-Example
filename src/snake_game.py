import pygame
import time
import random
# Initialize Pygame
pygame.init()
# Define colors
WHITE = (255, 255, 255)
YELLOW = (255, 255, 102)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)
# Display properties
WIDTH = 600
HEIGHT = 400
DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')
# Game settings
SNAKE_BLOCK = 10
SNAKE_SPEED = 15
# Clock
CLOCK = pygame.time.Clock()
# Fonts
FONT_STYLE = pygame.font.SysFont("bahnschrift", 25)
SCORE_FONT = pygame.font.SysFont("comicsansms", 35)
def display_score(score):
    value = SCORE_FONT.render("Your Score: " + str(score), True, BLUE)
    DISPLAY.blit(value, [0, 0])
def draw_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(DISPLAY, BLACK, [x[0], x[1], snake_block, snake_block])
def message(msg, color):
    mesg = FONT_STYLE.render(msg, True, color)
    DISPLAY.blit(mesg, [WIDTH / 6, HEIGHT / 3])
def game_loop():
    game_over = False
    game_close = False
    x1 = WIDTH / 2
    y1 = HEIGHT / 2
    x1_change = 0
    y1_change = 0
    snake_list = []
    snake_length = 1
    food_x = round(random.randrange(0, WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
    food_y = round(random.randrange(0, HEIGHT - SNAKE_BLOCK) / 10.0) * 10.0
    while not game_over:
        while game_close:
            DISPLAY.fill(WHITE)
            message("You Lost! Press Q-Quit or C-Play Again", RED)
            display_score(snake_length - 1)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -SNAKE_BLOCK
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = SNAKE_BLOCK
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -SNAKE_BLOCK
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = SNAKE_BLOCK
                    x1_change = 0
        if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        DISPLAY.fill(WHITE)
        pygame.draw.rect(DISPLAY, GREEN, [food_x, food_y, SNAKE_BLOCK, SNAKE_BLOCK])
        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_list.append(snake_head)
        if len(snake_list) > snake_length:
            del snake_list[0]
        for block in snake_list[:-1]:
            if block == snake_head:
                game_close = True
        draw_snake(SNAKE_BLOCK, snake_list)
        display_score(snake_length - 1)
        pygame.display.update()
        if x1 == food_x and y1 == food_y:
            food_x = round(random.randrange(0, WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
            food_y = round(random.randrange(0, HEIGHT - SNAKE_BLOCK) / 10.0) * 10.0
            snake_length += 1
        CLOCK.tick(SNAKE_SPEED)
    pygame.quit()
    quit()
game_loop()
