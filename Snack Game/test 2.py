import pygame
import time
import random

pygame.init()

# স্ক্রীনের আকার
WIDTH = 800
HEIGHT = 600

# রং
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# স্নেকের আকার এবং গতি
SNAKE_SIZE = 20
SNAKE_SPEED = 15

# ফন্ট
font_style = pygame.font.SysFont(None, 50)

# স্ক্রীন সেটআপ
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('স্নেক গেম')

# স্নেকের শুরু পজিশন
x1 = WIDTH / 2
y1 = HEIGHT / 2

# স্নেকের গতি
x1_change = 0
y1_change = 0

# স্নেকের শরীর
snake_List = []
Length_of_snake = 1

# খাবার (এলোমেলোভাবে)
foodx = round(random.randrange(0, WIDTH - SNAKE_SIZE) / 20.0) * 20.0
foody = round(random.randrange(0, HEIGHT - SNAKE_SIZE) / 20.0) * 20.0

# স্কোর
score = 0

# গেমের শেষে বার্তা
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, [WIDTH / 6, HEIGHT / 3])

# খাবারের সাথে এনিমেশন (লাফানো ও রঙ পরিবর্তন)
def animate_food(foodx, foody):
    for i in range(5):
        pygame.draw.circle(screen, (255, 255 - i * 40, 0), (int(foodx), int(foody)), SNAKE_SIZE // 2 + i)
        pygame.display.update()
        time.sleep(0.1)

# স্নেক আঁকা
def our_snake(snake_size, snake_list):
    for x in snake_list:
        pygame.draw.rect(screen, GREEN, [x[0], x[1], snake_size, snake_size])

# খাবার আঁকা
def draw_food(foodx, foody):
    pygame.draw.rect(screen, RED, [foodx, foody, SNAKE_SIZE, SNAKE_SIZE])

# স্কোর দেখানো
def Your_score(score):
    value = font_style.render("Your Score: " + str(score), True, WHITE)
    screen.blit(value, [0, 0])

# গেম লুপ
def gameLoop():
    global x1, y1, x1_change, y1_change, foodx, foody, score, Length_of_snake, snake_List

    game_over = False
    game_close = False

    while not game_over:
        while game_close:
            screen.fill(BLACK)
            message("You Lost! Press C-Play Again or Q-Quit", RED)
            Your_score(score)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -SNAKE_SIZE
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = SNAKE_SIZE
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -SNAKE_SIZE
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = SNAKE_SIZE
                    x1_change = 0

        if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        screen.fill(BLACK)
        draw_food(foodx, foody)
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        our_snake(SNAKE_SIZE, snake_List)
        Your_score(score)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, WIDTH - SNAKE_SIZE) / 20.0) * 20.0
            foody = round(random.randrange(0, HEIGHT - SNAKE_SIZE) / 20.0) * 20.0
            Length_of_snake += 1
            score += 1
            animate_food(foodx, foody)

        clock = pygame.time.Clock()
        clock.tick(SNAKE_SPEED)

    pygame.quit()
    quit()

if __name__ == "__main__":
    gameLoop()