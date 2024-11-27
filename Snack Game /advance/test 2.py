import pygame
import time
import random
import math

pygame.init()

# স্ক্রীনের আকার (আরও বড় স্ক্রিন)
WIDTH = 1600
HEIGHT = 900

# মিনিমাল রং স্কিম
BACKGROUND = (20, 20, 20)
SNAKE_COLOR = (0, 200, 100)
FOOD_COLOR = (200, 50, 50)
TEXT_COLOR = (220, 220, 220)

# স্নেকের আকার এবং গতি
SNAKE_SIZE = 25
SNAKE_SPEED = 15

# ফন্ট
font_style = pygame.font.SysFont("consolas", 35)
score_font = pygame.font.SysFont("consolas", 50)

# স্ক্রীন সেটআপ
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('মিনিমাল স্নেক গেম')

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
foodx = round(random.randrange(0, WIDTH - SNAKE_SIZE) / SNAKE_SIZE) * SNAKE_SIZE
foody = round(random.randrange(0, HEIGHT - SNAKE_SIZE) / SNAKE_SIZE) * SNAKE_SIZE

# স্কোর
score = 0

# গেমের শেষে বার্তা
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, [WIDTH / 6, HEIGHT / 3])

# স্টাইলিশ খাবার এনিমেশন
def animate_food(foodx, foody):
    for i in range(20):
        size = SNAKE_SIZE + 5 * math.sin(i * 0.3)
        alpha = int(255 * math.sin(i * 0.1))
        food_surface = pygame.Surface((SNAKE_SIZE, SNAKE_SIZE), pygame.SRCALPHA)
        pygame.draw.circle(food_surface, (*FOOD_COLOR, alpha), (SNAKE_SIZE//2, SNAKE_SIZE//2), size//2)
        screen.blit(food_surface, (foodx, foody))
        pygame.display.update()
        pygame.time.delay(20)

# স্নেক আঁকা (গ্রেডিয়েন্ট রঙ সহ)
def our_snake(snake_size, snake_list):
    for i, x in enumerate(snake_list):
        color = (SNAKE_COLOR[0], SNAKE_COLOR[1] - i * 2 if SNAKE_COLOR[1] - i * 2 > 0 else 0, SNAKE_COLOR[2])
        pygame.draw.rect(screen, color, [x[0], x[1], snake_size, snake_size])

# খাবার আঁকা (পালসিং এফেক্ট সহ)
def draw_food(foodx, foody):
    pulse = math.sin(pygame.time.get_ticks() * 0.01) * 3
    pygame.draw.circle(screen, FOOD_COLOR, (int(foodx + SNAKE_SIZE/2), int(foody + SNAKE_SIZE/2)), int(SNAKE_SIZE/2 + pulse))

# ডিজিটাল স্কোরবোর্ড
def Your_score(score):
    value = score_font.render(f"{score:04d}", True, TEXT_COLOR)
    text_rect = value.get_rect(center=(WIDTH/2, 50))
    pygame.draw.rect(screen, (40, 40, 40), (text_rect.x - 10, text_rect.y - 10, text_rect.width + 20, text_rect.height + 20))
    pygame.draw.rect(screen, TEXT_COLOR, (text_rect.x - 10, text_rect.y - 10, text_rect.width + 20, text_rect.height + 20), 2)
    screen.blit(value, text_rect)

# মিনিমাল পটভূমি এনিমেশন
def animate_background():
    t = pygame.time.get_ticks() * 0.001
    for x in range(0, WIDTH, 100):
        for y in range(0, HEIGHT, 100):
            color = (
                int(25 + 5 * math.sin(x * 0.01 + t)),
                int(25 + 5 * math.sin(y * 0.01 + t)),
                int(25 + 5 * math.sin((x+y) * 0.01 + t))
            )
            pygame.draw.rect(screen, color, [x, y, 100, 100])

# গেম লুপ
def gameLoop():
    global x1, y1, x1_change, y1_change, foodx, foody, score, Length_of_snake, snake_List

    game_over = False
    game_close = False

    while not game_over:
        while game_close:
            screen.fill(BACKGROUND)
            message("You Lost! Press C-Play Again or Q-Quit", TEXT_COLOR)
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

        animate_background()
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
            foodx = round(random.randrange(0, WIDTH - SNAKE_SIZE) / SNAKE_SIZE) * SNAKE_SIZE
            foody = round(random.randrange(0, HEIGHT - SNAKE_SIZE) / SNAKE_SIZE) * SNAKE_SIZE
            Length_of_snake += 1
            score += 1
            animate_food(foodx, foody)

        clock = pygame.time.Clock()
        clock.tick(SNAKE_SPEED)

    pygame.quit()
    quit()

if __name__ == "__main__":
    gameLoop()