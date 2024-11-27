import pygame
import time
import random
import math

pygame.init()

# স্ক্রীনের আকার (আরও বড় স্ক্রিন)
WIDTH = 1600
HEIGHT = 900

# অ্যাডভান্সড মিনিমাল রং স্কিম
BACKGROUND = (10, 10, 15)
SNAKE_COLOR = (0, 200, 100)
FOOD_COLOR = (200, 50, 50)
BIG_FOOD_COLOR = (220, 180, 0)
TEXT_COLOR = (220, 220, 220)
GRID_COLOR = (30, 30, 35)

# স্নেকের আকার এবং গতি
SNAKE_SIZE = 25
SNAKE_SPEED = 9

# খাবারের আকার
FOOD_SIZE = 20
BIG_FOOD_SIZE = 40

# ফন্ট
font_style = pygame.font.SysFont("consolas", 35)
score_font = pygame.font.SysFont("consolas", 50)

# স্ক্রীন সেটআপ
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('অ্যাডভান্সড মিনিমাল স্নেক গেম')

# গ্রিড ফাংশন
def draw_grid():
    for x in range(0, WIDTH, SNAKE_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, SNAKE_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (WIDTH, y))

# অ্যাডভান্সড স্কোরবোর্ড
def draw_scoreboard(score, high_score):
    pygame.draw.rect(screen, (30, 30, 35), (10, 10, 300, 80))
    pygame.draw.rect(screen, TEXT_COLOR, (10, 10, 300, 80), 2)
    score_text = score_font.render(f"Score: {score:04d}", True, TEXT_COLOR)
    high_score_text = font_style.render(f"High: {high_score:04d}", True, TEXT_COLOR)
    screen.blit(score_text, (20, 20))
    screen.blit(high_score_text, (20, 60))

# অ্যানিমেটেড খাবার
def draw_food(foodx, foody, is_big):
    size = BIG_FOOD_SIZE if is_big else FOOD_SIZE
    color = BIG_FOOD_COLOR if is_big else FOOD_COLOR
    pulse = math.sin(pygame.time.get_ticks() * 0.01) * 3
    glow_size = size + pulse
    
    # গ্লো ইফেক্ট
    for i in range(3):
        alpha = 100 - i * 30
        glow_surface = pygame.Surface((glow_size*2, glow_size*2), pygame.SRCALPHA)
        pygame.draw.circle(glow_surface, (*color, alpha), (glow_size, glow_size), glow_size - i*2)
        screen.blit(glow_surface, (foodx + SNAKE_SIZE//2 - glow_size, foody + SNAKE_SIZE//2 - glow_size))
    
    # মূল খাবার
    pygame.draw.circle(screen, color, (int(foodx + SNAKE_SIZE/2), int(foody + SNAKE_SIZE/2)), int(size/2))

# অ্যাডভান্সড স্নেক রেন্ডারিং
def our_snake(snake_size, snake_list):
    for i, x in enumerate(snake_list):
        color = (
            max(0, SNAKE_COLOR[0] - i * 2),
            min(255, SNAKE_COLOR[1] + i * 2),
            max(0, SNAKE_COLOR[2] - i * 2)
        )
        pygame.draw.rect(screen, color, [x[0], x[1], snake_size, snake_size])
        pygame.draw.rect(screen, (255, 255, 255), [x[0], x[1], snake_size, snake_size], 1)

# গেম লুপ
def gameLoop():
    global x1, y1, x1_change, y1_change, foodx, foody, score, Length_of_snake, snake_List

    game_over = False
    game_close = False

    x1 = WIDTH / 2
    y1 = HEIGHT / 2
    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx = round(random.randrange(0, WIDTH - SNAKE_SIZE) / SNAKE_SIZE) * SNAKE_SIZE
    foody = round(random.randrange(0, HEIGHT - SNAKE_SIZE) / SNAKE_SIZE) * SNAKE_SIZE

    score = 0
    high_score = 0
    is_big_food = False
    big_food_timer = 0

    clock = pygame.time.Clock()

    while not game_over:
        while game_close:
            screen.fill(BACKGROUND)
            message("You Lost! Press C-Play Again or Q-Quit", TEXT_COLOR)
            draw_scoreboard(score, high_score)
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
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -SNAKE_SIZE
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = SNAKE_SIZE
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -SNAKE_SIZE
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = SNAKE_SIZE
                    x1_change = 0

        if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change

        screen.fill(BACKGROUND)
        draw_grid()
        draw_food(foodx, foody, is_big_food)
        
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
        draw_scoreboard(score, high_score)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, WIDTH - SNAKE_SIZE) / SNAKE_SIZE) * SNAKE_SIZE
            foody = round(random.randrange(0, HEIGHT - SNAKE_SIZE) / SNAKE_SIZE) * SNAKE_SIZE
            Length_of_snake += 1
            if is_big_food:
                score += 5
                is_big_food = False
            else:
                score += 1
            
            if score > high_score:
                high_score = score

            # বড় খাবারের জন্য টাইমার
            big_food_timer += 1
            if big_food_timer >= 5:  # প্রতি 5টি সাধারণ খাবারের পর একটি বড় খাবার
                is_big_food = True
                big_food_timer = 0

        clock.tick(SNAKE_SPEED)

    pygame.quit()
    quit()

if __name__ == "__main__":
    gameLoop()