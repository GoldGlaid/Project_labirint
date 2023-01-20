import pygame

pygame.init()

RES = WIDTH, HEIGHT = 1202, 902
TILE = 60

pygame.init()
sc = pygame.display.set_mode(RES)
clock = pygame.time.Clock()

text = ''
active = False
input_box = pygame.Rect(WIDTH // 4, HEIGHT // 3 - 150, 620, 250)
text_input_f = True


def enter_name():
    global active, text_input_f
    sc.fill(pygame.color.Color(20, 20, 20))
    font = pygame.font.Font('MonsterFriendBack.otf', 70)
    txt_surface = font.render(text, True, 'white')
    if max(input_box.w, txt_surface.get_width() + 40) == txt_surface.get_width() + 40:
        text_input_f = False
    else:
        text_input_f = True
    # input_box.w = width
    sc.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
    width = max(WIDTH // 4, txt_surface.get_width() + 40)
    input_box_x = width
    pygame.draw.rect(sc, 'green', (WIDTH // 4, HEIGHT // 4 - 150, input_box.w, 250), 1)

    active = True


while True:
    sc.fill(pygame.Color('darkslategray'))

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            exit()
        if event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_RETURN:
                    print(text)
                    text = ''
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    if text_input_f:
                        text += event.unicode
    enter_name()

    pygame.display.flip()
    clock.tick(100006)
