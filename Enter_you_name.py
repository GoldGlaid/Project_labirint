import pygame

pygame.init()

RES = WIDTH, HEIGHT = 1202, 902
TILE = 60

pygame.init()
sc = pygame.display.set_mode(RES)
clock = pygame.time.Clock()

text = ''
active = False
font_range = 50

input_box_w = 50
input_box_h = 100
input_box_x = WIDTH / 2 - input_box_w
input_box_y = HEIGHT / 2 - input_box_h

input_box = pygame.Rect(input_box_x, input_box_y, input_box_w, input_box_h)
text_input_f = True
max_col_txt = 9


def enter_name():
    global active, text_input_f, text, text_input_f, max_col_txt
    global input_box_x, input_box_y, input_box_w, input_box_h, NAME
    active = True

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                exit()
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        pygame.mixer.init()
                        pygame.mixer.music.load('music\Savkov_Igor_RiverTravel.mp3')
                        pygame.mixer.music.play()
                        return text

                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                        input_box_w -= font_range
                        input_box_x += font_range / 2
                    else:
                        if text_input_f:
                            text += event.unicode
        sc.fill(pygame.color.Color(20, 20, 20))
        font = pygame.font.Font('MonsterFriendBack.otf', font_range)

        enter_n = font.render('Enter your name', True, 'white')
        txt_surface = font.render(text, True, 'white')

        if len(text) == max_col_txt:
            text_input_f = False
        else:
            text_input_f = True
        if input_box_w <= txt_surface.get_width():
            input_box_w += font_range
            input_box_x -= font_range / 2

        sc.blit(txt_surface, (input_box_x + 10, input_box_y))
        sc.blit(enter_n, (WIDTH / 5, HEIGHT / 6))
        pygame.draw.rect(sc, 'gray', (input_box_x, input_box_y - font_range // 2, input_box_w, input_box_h), 2)
        pygame.display.flip()
        clock.tick(1000)
