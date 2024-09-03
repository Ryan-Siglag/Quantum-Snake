import pygame
import random

pygame.init()

# Set up display
width, height = 900, 600
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Quantum Snake")

# Colors (still used for text)
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# Updated snake settings
snake_block = 50  # Size of the blocks
snake_speed = 10  

clock = pygame.time.Clock()

font_style = pygame.font.Font('PixelFont.ttf', 30)

# Load sprites
snake_body_sprite = pygame.image.load('snake_body_sprite.png')
snake_head_sprite = pygame.image.load('snake_head_sprite.png')
snake_tail_sprite = pygame.image.load('snake_tail_sprite.png')
apple_sprite = pygame.image.load('apple_sprite.png')
barrier_sprite = pygame.image.load('barrier_sprite.png')

# Resize sprites to match the snake_block size
snake_body_sprite = pygame.transform.scale(snake_body_sprite, (snake_block, snake_block))
snake_head_sprite = pygame.transform.scale(snake_head_sprite, (snake_block, snake_block))
snake_tail_sprite = pygame.transform.scale(snake_tail_sprite, (snake_block, snake_block))
apple_sprite = pygame.transform.scale(apple_sprite, (snake_block, snake_block))
barrier_sprite = pygame.transform.scale(barrier_sprite, (snake_block, snake_block))


def message(msg, color, y_displace=0):
    mesg = font_style.render(msg, True, color)
    win.blit(mesg, [width / 2 - mesg.get_width() / 2, height / 2 + y_displace])

def display_score(score):
    score_text = font_style.render(f"Score: {score}", True, white)
    win.blit(score_text, [10, 10])  # Display score at top-left corner

def splash_screen():
    splash = True
    while splash:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Press SPACE to start game
                    splash = False

        win.fill(black)
        message("Welcome to Quantum Snake!", white, -250)
        message("This is a world where apples", white, -200)
        message("exist in a quantum superposition.", white, -150)
        message("When eaten (measured),", white, -100)
        message("they undergo wave function collapse", white, -50)
        message("into either a tasty treat for growth", white, 0)
        message("or a rotten hazard to avoid.", white, 50)
        message("Press SPACE to Start", green, 150)
        message("(Arrow keys to move)", green, 200)
        pygame.display.update()

def is_collision(position, barriers):
    return position in barriers

def place_food(barriers, width, height, snake_block):
    while True:
        foodx = round(random.randrange(0, width - snake_block) / snake_block) * snake_block
        foody = round(random.randrange(0, height - snake_block) / snake_block) * snake_block
        if not is_collision([foodx, foody], barriers):
            return foodx, foody

def game_loop():
    game_over = False
    game_close = False

    x1 = round(width / 2 / snake_block) * snake_block
    y1 = round(height / 2 / snake_block) * snake_block

    x1_change = 0
    y1_change = 0

    snake_List = []
    length_of_snake = 1

    barriers = []
    foodx, foody = place_food(barriers, width, height, snake_block)

    score = 0
    direction = 'RIGHT'

    while not game_over:

        while game_close:
            win.fill(black)
            message("You Lost! Press Q-Quit or C-Play Again", red, -50)
            display_score(score)
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
                    if direction != 'RIGHT':
                        x1_change = -snake_block
                        y1_change = 0
                        direction = 'LEFT'
                elif event.key == pygame.K_RIGHT:
                    if direction != 'LEFT':
                        x1_change = snake_block
                        y1_change = 0
                        direction = 'RIGHT'
                elif event.key == pygame.K_UP:
                    if direction != 'DOWN':
                        y1_change = -snake_block
                        x1_change = 0
                        direction = 'UP'
                elif event.key == pygame.K_DOWN:
                    if direction != 'UP':
                        y1_change = snake_block
                        x1_change = 0
                        direction = 'DOWN'

        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        win.fill(black)

        # Draw apple sprite
        win.blit(apple_sprite, (foodx, foody))

        # Draw barrier sprites
        for barrier in barriers:
            win.blit(barrier_sprite, (barrier[0], barrier[1]))

        snake_Head = [x1, y1]
        snake_List.append(snake_Head)

        if len(snake_List) > length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        for barrier in barriers:
            if snake_Head == barrier:
                game_close = True

        # Rotate head sprite based on the direction
        if direction == 'UP':
            rotated_head = pygame.transform.rotate(snake_head_sprite, 90)
        elif direction == 'DOWN':
            rotated_head = pygame.transform.rotate(snake_head_sprite, -90)
        elif direction == 'LEFT':
            rotated_head = pygame.transform.rotate(snake_head_sprite, 180)
        else:  # RIGHT
            rotated_head = snake_head_sprite

        # Draw snake head
        win.blit(rotated_head, (snake_List[-1][0], snake_List[-1][1]))

        # Draw snake body
        for block in snake_List[1:-1]:
            win.blit(snake_body_sprite, (block[0], block[1]))

        # Determine the direction of the tail
        tail_direction = None
        if len(snake_List) > 1:
            if snake_List[0][0] < snake_List[1][0]:
                tail_direction = 'LEFT'
            elif snake_List[0][0] > snake_List[1][0]:
                tail_direction = 'RIGHT'
            elif snake_List[0][1] < snake_List[1][1]:
                tail_direction = 'UP'
            elif snake_List[0][1] > snake_List[1][1]:
                tail_direction = 'DOWN'

            # Rotate tail sprite based on the direction
            if tail_direction == 'UP':
                rotated_tail = pygame.transform.rotate(snake_tail_sprite, 90)
            elif tail_direction == 'DOWN':
                rotated_tail = pygame.transform.rotate(snake_tail_sprite, -90)
            elif tail_direction == 'LEFT':
                rotated_tail = pygame.transform.rotate(snake_tail_sprite, 180)
            else:  # RIGHT
                rotated_tail = snake_tail_sprite

            # Draw snake tail
            win.blit(rotated_tail, (snake_List[0][0], snake_List[0][1]))

        display_score(score)

        pygame.display.update()

        # Collision detection with food
        if x1 == foodx and y1 == foody:
            score += 1
            if random.choice([True, False]):  # 50% chance
                length_of_snake += 1
            else:
                barriers.append([foodx, foody])

            foodx, foody = place_food(barriers, width, height, snake_block)

        clock.tick(snake_speed)
    pygame.quit()
    quit()

splash_screen()
game_loop()
