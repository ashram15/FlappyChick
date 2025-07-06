import random
import sys


import pygame
from pygame import font

from utils import load_high_score, save_high_score

pygame.init()

screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 40)

chicken_img = pygame.image.load("assets/flappychick.png").convert_alpha()
chicken_img = pygame.transform.scale(chicken_img, (150, 160))  # match bird size

total_score = 0
high_score = load_high_score()

bird = pygame.Rect(100, 250, 40, 40)  # x, y, width, height
gravity = 0.5
bird_movement: int = 0
jump_strength = -10

# Game state
game_over = False

# Ground scroll setup
ground_img = pygame.Surface((600, 120))
ground_img.fill((46, 204, 113))
ground_x = 0

# Pipe scroll setup
pipe_width = 80
pipe_gap = random.randint(180,230)
pipe_x = 600
pipe_height = random.randint(100, 300)

#score
pipe_scored = False

# Clouds
clouds = [
    {"x": 140, "y": 70},
    {"x": 250, "y": 80},
    {"x": 50,  "y": 150}
]


def draw_game_over():

    screen.fill((215, 189, 226))  #  background

    global high_score

    text_surface = font.render("Game Over!", True, (118, 68, 138))
    text_rect = text_surface.get_rect(center=(300, 280))
    screen.blit(text_surface, text_rect)

    # "Final Score" text
    score_surface = font.render(f"Final Score: {total_score}", True, (118, 68, 138))
    score_rect = score_surface.get_rect(center=(300, 320))  # slightly lower
    screen.blit(score_surface, score_rect)

    # Restart button
    restart_button = pygame.Rect(225, 360, 150, 50)
    pygame.draw.rect(screen, (255, 255, 255), restart_button)
    restart_text = font.render("Restart", True, (0, 0, 0))
    screen.blit(restart_text, restart_button.move(25, 10))

    # Update high score
    if total_score > high_score:
        high_score = total_score
        save_high_score(high_score)

    pygame.display.flip()

    # Wait for keypress or quit
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.collidepoint(event.pos):
                    waiting = False

def reset_game():
    # Reset game state

    global bird_movement, pipe_x, pipe_height, total_score, game_over, pipe_scored

    bird.y = 250
    bird_movement = 0
    pipe_x = 600
    pipe_height = random.randint(120, 300)
    total_score = 0
    game_over = False

def draw_cloud(surface, x, y):
    cloud_color = (255, 255, 255)
    # Main puff
    pygame.draw.circle(surface, cloud_color, (x, y), 20)
    pygame.draw.circle(surface, cloud_color, (x + 20, y - 10), 25)
    pygame.draw.circle(surface, cloud_color, (x + 40, y), 20)
    pygame.draw.circle(surface, cloud_color, (x + 20, y + 10), 18)



def start_screen():
    waiting = True
    button_rect = pygame.Rect(220, 280, 160, 60)

    while waiting:
        screen.fill((215, 189, 226))

        # Title
        title_surface = font.render("Flappy Chick!", True, (118, 68, 138))
        title_rect = title_surface.get_rect(center=(300, 150))
        screen.blit(title_surface, title_rect)

        # Draw start button
        pygame.draw.rect(screen, (255, 255, 255), button_rect)
        button_text = font.render("Start", True, (0, 0, 0))
        button_text_rect = button_text.get_rect(center=button_rect.center)
        screen.blit(button_text, button_text_rect)

        #Draw high score
        high_score_text = font.render(f"High Score: { high_score}", True, (118, 68, 138))
        screen.blit(high_score_text, high_score_text.get_rect(center=(300, 200)))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    waiting = False

#start game
start_screen()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Jump on space key
        if not game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_movement = jump_strength


    if not game_over:
        # Apply gravity
        bird_movement += gravity
        bird.y += int(bird_movement)

        # Scroll ground
        ground_x -= 4
        if ground_x <= -600:
            ground_x = 0

        # Scroll pipe
        pipe_x -= 4

        # Check if bird has passed the pipe
        if not pipe_scored and bird.x > pipe_x + pipe_width:
            total_score += 1
            pipe_scored = True

        if pipe_x < -pipe_width:
            pipe_x = 600
            pipe_height = random.randint(100, 300)
            pipe_gap = random.randint(120,210)
            pipe_scored = False

        # Scroll clouds
        for cloud in clouds:
            cloud["x"] -= 1
            if cloud["x"] < -60:
                cloud["x"] = 640  # reset to right
                cloud["y"] = random.randint(50, 150)



        screen.fill((135, 206, 235))  # Sky blue background

        #display Sun
        pygame.draw.circle(screen, (247, 220, 111), (45,50), 30)
        pygame.draw.circle(screen, (255, 255, 143), (52, 50), 30)

        #display grass on ground
        pygame.draw.rect(screen, (46, 204, 113), (0, 480, 700, 200), 0)
        pygame.draw.rect(screen, (39, 174, 96), (0, 580, 700, 100), 0)

        #display score while playing
        score_surface = font.render("Score: " + str(total_score), True, (0,0,0))
        screen.blit(score_surface, (20, 500))

        # Clouds
        for cloud in clouds:
            draw_cloud(screen, cloud["x"], cloud["y"])


        # Pipe (top and bottom)
        pygame.draw.rect(screen, (52, 152, 219), (pipe_x, 0, pipe_width, pipe_height))
        pygame.draw.rect(screen, (52, 152, 219), (pipe_x, pipe_height + pipe_gap, pipe_width, 600))

        # Draw bird
        #pygame.draw.rect(screen, (255, 255, 0), bird)  # Yellow bird
        # Draw chicken image
        # Offset image so it's centered over the bird rect
        image_rect = chicken_img.get_rect(center=bird.center)
        screen.blit(chicken_img, image_rect)


        #Game end conditions
        if bird. y >= 480 or \
        bird.colliderect(pygame.Rect(pipe_x, 0, pipe_width, pipe_height)) or \
        bird.colliderect(pygame.Rect(pipe_x, pipe_height + pipe_gap, pipe_width, 600)):
            game_over = True
            draw_game_over()
            reset_game()
            start_screen()

        pygame.display.flip()
        clock.tick(60)
