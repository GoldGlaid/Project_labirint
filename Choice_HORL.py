import pygame

from parametrs import RES, WIDTH, HEIGHT, CENTER_WIDTH

pygame.init()
sc = pygame.display.set_mode(RES)
clock = pygame.time.Clock()

TILE = 0


def choise_hard():
    global TILE
    active = False
    hard = 'Easy'

    font_b = pygame.font.Font('data/fonts/determinationmonorusbylyajk.otf', 90)
    font_m = pygame.font.Font('data/fonts/determinationmonorusbylyajk.otf', 90)

    enter_n = font_b.render('Choice a hard level:', True, 'white')

    txt_easy = font_m.render('Easy', True, 'green')
    txt_medium = font_m.render('Medium', True, 'yellow')
    txt_hard = font_m.render('Hard', True, 'red')

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
                pygame.mixer.music.load('data/music\\Savkov_Igor_RiverTravel.mp3')
                pygame.mixer.music.play()
                return TILE, hard
        sc.fill(pygame.color.Color(15, 0, 44))

        sc.blit(enter_n, (CENTER_WIDTH - enter_n.get_width() // 2, HEIGHT / 6))
        sc.blit(txt_easy, (CENTER_WIDTH - txt_easy.get_width() // 2, HEIGHT // 3))

        width_ramks = max(txt_easy.get_width(),
                          txt_medium.get_width(),
                          txt_hard.get_width())

        pygame.draw.rect(sc, 'gray', (
            CENTER_WIDTH - width_ramks // 2,
            HEIGHT // 3,
            txt_medium.get_width(),
            txt_medium.get_height()), 3)

        sc.blit(txt_medium, (CENTER_WIDTH - txt_medium.get_width() // 2, HEIGHT // 3 + 100))
        pygame.draw.rect(sc, 'gray', (
            CENTER_WIDTH - width_ramks // 2,
            HEIGHT // 3 + 100,
            txt_medium.get_width(),
            txt_medium.get_height()), 3)

        sc.blit(txt_hard, (CENTER_WIDTH - txt_hard.get_width() // 2, HEIGHT // 3 + 200))
        pygame.draw.rect(sc, 'gray', (
            CENTER_WIDTH - width_ramks // 2,
            HEIGHT // 3 + 200,
            txt_medium.get_width(),
            txt_medium.get_height()), 3)

        pygame.display.flip()
        clock.tick(1000)
