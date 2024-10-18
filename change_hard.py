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

    destantion_enter_n = (CENTER_WIDTH - enter_n.get_width() // 2, HEIGHT / 6)
    
    destantion_txt_easy = (CENTER_WIDTH - txt_easy.get_width() // 2, HEIGHT // 3)
    destantion_txt_medium = (CENTER_WIDTH - txt_medium.get_width() // 2, HEIGHT // 3 + 100)
    destantion_txt_hard = (CENTER_WIDTH - txt_hard.get_width() // 2, HEIGHT // 3 + 200)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()

                if (destantion_txt_easy[0] <= x <= destantion_txt_easy[0] + txt_easy.get_width()) and \
                        (destantion_txt_easy[1] <= y <= destantion_txt_easy[1] + txt_easy.get_height()):
                    active = True
                    TILE = 70
                    hard = 'Easy'
                elif (destantion_txt_medium[0] <= x <= destantion_txt_medium[0] + txt_medium.get_width()) and \
                        (destantion_txt_medium[1] <= y <= destantion_txt_medium[1] + txt_medium.get_height()):
                    active = True
                    TILE = 50
                    hard = 'Medium'
                elif (destantion_txt_hard[0] <= x <= destantion_txt_hard[0] + txt_hard.get_width()) and \
                     (destantion_txt_hard[1] <= y <= destantion_txt_hard[1] + txt_hard.get_height()):
                    active = True
                    TILE = 40
                    hard = 'Hard'

            if active:
                pygame.mixer.init()
                pygame.mixer.music.load('data/music\\Savkov_Igor_RiverTravel.mp3')
                pygame.mixer.music.set_volume(2.0)

                pygame.mixer.music.play()
                return TILE, hard

        sc.fill(pygame.color.Color(15, 0, 44))

        width_ramks = max(txt_easy.get_width() + 20,
                          txt_medium.get_width() + 20,
                          txt_hard.get_width() + 20)
        x_ramks = min(destantion_txt_easy[0] - 10,
                      destantion_txt_medium[0] - 10,
                      destantion_txt_hard[0] - 10)

        sc.blit(enter_n, destantion_enter_n)
        sc.blit(txt_easy, destantion_txt_easy)
        pygame.draw.rect(sc, 'gray', (
            x_ramks,
            destantion_txt_easy[1],
            width_ramks,
            txt_medium.get_height()), 3)

        sc.blit(txt_medium, destantion_txt_medium)
        pygame.draw.rect(sc, 'gray', (
            x_ramks,
            destantion_txt_medium[1],
            width_ramks,
            txt_medium.get_height()), 3)

        sc.blit(txt_hard, destantion_txt_hard)
        pygame.draw.rect(sc, 'gray', (
            x_ramks,
            destantion_txt_hard[1],
            width_ramks,
            txt_medium.get_height()), 3)

        pygame.display.flip()
        clock.tick(1000)
