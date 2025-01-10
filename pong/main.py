import pygame
import time
from sys import exit

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((800, 500))
pygame.display.set_caption("PONG!")
pygame_icon = pygame.image.load('graphics/arts/Ball.png')
pygame.display.set_icon(pygame_icon)

# Text
teko_font = pygame.font.Font("fonts/Teko.ttf", 50)
title_font = pygame.font.Font("fonts/prstart.ttf", 60)
enter_font = pygame.font.Font("fonts/prstart.ttf", 30)

# Menu
pong_menu = title_font.render("PONG!", False, "White")
pong_menu_rect = pong_menu.get_rect(center=(420, 150))

enter_menu = enter_font.render("Press Space to Start", False, "White")
enter_menu_rect = pong_menu.get_rect(center=(250, 300))

# Time
total_time = 99
start_time = time.time()

# Players
player1_sur = pygame.image.load("graphics/arts/Player1.png").convert_alpha()
player1_rect = player1_sur.get_rect(midleft = (50, screen.get_height() / 2))
player1_score = 0

player2_sur = pygame.image.load("graphics/arts/Player2.png").convert_alpha()
player2_rect = player2_sur.get_rect(midright = (screen.get_width() - 50, screen.get_height() / 2))
player2_score = 0

# Ball
ball_surf = pygame.image.load("graphics/arts/Ball.png").convert_alpha()
ball_rect = ball_surf.get_rect(center = (400, 250))
ball_speedx = 9
ball_speedy = 9
ball_sfx =pygame.mixer.Sound('graphics/hit.mp3')

# Score and Board:
board = pygame.image.load("graphics/arts/Board.png")

score_surf1 = pygame.image.load("graphics/arts/ScoreBar.png")
score_rect1 = score_surf1.get_rect(topleft = (0, 0))
score_surf2 = pygame.transform.flip(score_surf1, True, False)
score_rect2 = score_surf2.get_rect(topleft = (459, 0))

is_running = True
game_active = False
player_speed = 6

while is_running:
    if game_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        keys = pygame.key.get_pressed()

        # Player 1 Movement
        if keys[pygame.K_w] and player1_rect.top > 50:
            player1_rect.y -= player_speed
        if keys[pygame.K_s] and player1_rect.bottom < 495:
            player1_rect.y += player_speed

        # Player 2 Movement
        if keys[pygame.K_UP] and player2_rect.top > 50:
            player2_rect.y -= player_speed
        if keys[pygame.K_DOWN] and player2_rect.bottom < 495:
            player2_rect.y += player_speed

        # Ball Movement and Collision
        ball_rect.x += ball_speedx
        ball_rect.y += ball_speedy

        if ball_rect.top <= 50 or ball_rect.bottom >= 495:
            ball_speedy *= -1
            ball_sfx.play()
        if ball_rect.colliderect(player1_rect) or ball_rect.colliderect(player2_rect):
            ball_speedx *= -1
            ball_sfx.play()


        if ball_rect.right >= 900:
            player1_score += 1
            player1_rect = player1_sur.get_rect(midleft=(50, screen.get_height() / 2))
            player2_rect = player2_sur.get_rect(midright=(screen.get_width() - 50, screen.get_height() / 2))
            ball_rect = ball_surf.get_rect(center = (400, 250))
            pygame.time.delay(500)

        if ball_rect.left <= -100:
            player2_score += 1
            player1_rect = player1_sur.get_rect(midleft=(50, screen.get_height() / 2))
            player2_rect = player2_sur.get_rect(midright=(screen.get_width() - 50, screen.get_height() / 2))
            ball_rect = ball_surf.get_rect(center=(400, 250))
            pygame.time.delay(500)

        elapsed_time = time.time() - start_time
        remaining_time = total_time - int(elapsed_time)

        if remaining_time <= 0:
            pygame.time.delay(500)
            game_active = False

        screen.fill((0, 0, 0))
        screen.blit(board, (0,45))

        screen.blit(score_surf1, score_rect1.topleft)
        screen.blit(score_surf2, score_rect2.topleft)

        screen.blit(player1_sur, player1_rect.topleft)
        screen.blit(player2_sur, player2_rect.topleft)
        screen.blit(ball_surf, ball_rect.topleft)

        timer_surface = teko_font.render(str(remaining_time), True, "White")
        timer_rect = timer_surface.get_rect(center = (400, 25))
        screen.blit(timer_surface, timer_rect.topleft)

        score_text1 = teko_font.render(str(player1_score), True, "Black")
        score_text2 = teko_font.render(str(player2_score), True, "Black")
        screen.blit(score_text1, (180, -5))
        screen.blit(score_text2, (620, -5))

        pygame.display.update()
        clock.tick(60)

    else:
        screen.fill((0, 0, 0))
        screen.blit(pong_menu, pong_menu_rect)
        screen.blit(enter_menu, enter_menu_rect)

        winner1 = enter_font.render("Player 1 wins!", False, "#281825")
        winner_rect1 = winner1.get_rect(center=(420, 400))
        winner2 = enter_font.render("Player 2 wins!", False, "#281825")
        winner_rect2 = winner2.get_rect(center=(420, 400))

        if player1_score > player2_score:
            screen.blit(winner1, winner_rect1)
        elif player1_score < player2_score:
            screen.blit(winner2, winner_rect2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.time.delay(500)

                    player1_score = 0
                    player2_score = 0
                    total_time = 99
                    player1_rect = player1_sur.get_rect(midleft=(50, screen.get_height() / 2))
                    player2_rect = player2_sur.get_rect(midright=(screen.get_width() - 50, screen.get_height() / 2))
                    ball_rect = ball_surf.get_rect(center=(400, 250))

                    game_active = True

        pygame.display.update()
        clock.tick(60)