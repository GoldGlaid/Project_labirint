import os
import sys

import pygame

pygame.init()

RES = WIDTH, HEIGHT = 1202, 902
pygame.init()
sc = pygame.display.set_mode(RES)
clock = pygame.time.Clock()


def choise_hard():
    global TILE
    active = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if (WIDTH / 3 - 20 <= x <= WIDTH / 3 - 20 + txt_medium.get_width() + 40) and \
                    (HEIGHT // 3 - 20 <= y <= HEIGHT // 3 - 20 + txt_medium.get_height() + 30):
                    active = True
                    TILE = 70
                    hard = 'Easy'
                elif (WIDTH / 3 - 20 <= x <= WIDTH / 3 - 20 + txt_medium.get_width() + 40) and \
                    (HEIGHT // 2 - 20 <= y <= HEIGHT // 2 - 20 + txt_medium.get_height() + 30):
                    active = True
                    TILE = 50
                    hard = 'Medium'
                elif (WIDTH / 3 - 20 <= x <= WIDTH / 3 - 20 + txt_medium.get_width() + 40) and \
                    (HEIGHT // 2 + 150 <= y <= HEIGHT // 2 + 150 + txt_medium.get_height() + 30):
                    active = True
                    TILE = 40
                    hard = 'Hard'
            if active:
                pygame.mixer.init()
                pygame.mixer.music.load('music\Savkov_Igor_RiverTravel.mp3')
                pygame.mixer.music.play()
                return TILE, hard
        sc.fill(pygame.color.Color(15, 0, 44))
        font_b = pygame.font.Font('MonsterFriendBack.otf', 50)
        font_m = pygame.font.Font('MonsterFriendBack.otf', 60)

        enter_n = font_b.render('Choice a hard level:', True, 'white')

        txt_easy = font_m.render('Easy', True, 'green')
        txt_medium = font_m.render('Medium', True, 'yellow')
        txt_hard = font_m.render('Hard', True, 'red')

        sc.blit(enter_n, (WIDTH // 5 - 50, HEIGHT / 6))

        sc.blit(txt_easy, (WIDTH / 3 + 55, HEIGHT // 3))
        pygame.draw.rect(sc, 'gray', (WIDTH / 3 - 20,
                                      HEIGHT // 3 - 20,
                                      txt_medium.get_width() + 40,
                                      txt_medium.get_height() + 30), 2)

        sc.blit(txt_medium, (WIDTH / 3, HEIGHT // 2))
        pygame.draw.rect(sc, 'gray', (WIDTH / 3 - 20,
                                      HEIGHT // 2 - 20,
                                      txt_medium.get_width() + 40,
                                      txt_medium.get_height() + 30), 2)

        sc.blit(txt_hard, (WIDTH / 3 + 60, HEIGHT // 2 + 150 + 20))
        pygame.draw.rect(sc, 'gray', (WIDTH / 3 - 20,
                                      HEIGHT // 2 + 150,
                                      txt_medium.get_width() + 40,
                                      txt_medium.get_height() + 30), 2)

        pygame.display.flip()
        clock.tick(1000)
