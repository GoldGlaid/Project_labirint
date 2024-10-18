import os
import sys

import pygame

from parametrs import RES, WIDTH, HEIGHT, CENTER_WIDTH

pygame.init()
sc = pygame.display.set_mode(RES)
clock = pygame.time.Clock()

text = ''
font_range = 90
text_input_f = True
max_col_txt = 9

all_sprites = pygame.sprite.Group()


def load_image(name, colorkey=None):
    fullname = os.path.join('data/images', name)

    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()

    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Dino(pygame.sprite.Sprite):
    image = load_image("dinozavr.png")
    size = (500, 400)
    image = pygame.transform.scale(image, size)

    def __init__(self, group):
        super().__init__(group)
        self.image = Dino.image
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = HEIGHT - Dino.size[1]


class Dino2(pygame.sprite.Sprite):
    image = load_image("dinozavr2.png")
    size = (500, 400)
    image = pygame.transform.scale(image, size)
    image = pygame.transform.flip(image, True, False)

    def __init__(self, group):
        super().__init__(group)
        self.image = Dino2.image
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH - Dino2.size[0]
        self.rect.y = HEIGHT - Dino2.size[1]


class Coca(pygame.sprite.Sprite):
    image = load_image('coconut.png')
    size = (500, 600)
    image = pygame.transform.scale(image, size)
    image = pygame.transform.flip(image, True, False)

    def __init__(self, group):
        super().__init__(group)
        self.image = Coca2.image
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = HEIGHT - Coca.size[1]


class Coca2(pygame.sprite.Sprite):
    image = load_image('coconut.png')
    size = (500, 600)
    image = pygame.transform.scale(image, size)

    def __init__(self, group):
        super().__init__(group)
        self.image = Coca.image
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH - Coca2.size[0]
        self.rect.y = HEIGHT - Coca2.size[1]


Coca(all_sprites)
Coca2(all_sprites)
Dino(all_sprites)
Dino2(all_sprites)


def enter_name():
    global text_input_f, text, text_input_f, max_col_txt

    input_box_w = 10
    input_box_h = 100
    input_box_x = 0
    input_box_y = HEIGHT / 6

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return text
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                    input_box_w -= font_range
                    input_box_x += font_range / 2
                else:
                    if text_input_f:
                        text += event.unicode

        sc.fill(pygame.color.Color(15, 0, 44))

        font = pygame.font.Font('data/fonts/determinationmonorusbylyajk.otf', font_range)
        txt_surface = font.render(text, True, 'yellow')

        enter_n = font.render('Enter your name', True, 'white')

        if len(text) == max_col_txt:
            text_input_f = False
        else:
            text_input_f = True
        if input_box_w <= txt_surface.get_width():
            input_box_w += font_range
            input_box_x -= font_range / 2

        all_sprites.draw(sc)

        sc.blit(enter_n, (CENTER_WIDTH - enter_n.get_width() // 2, 60))
        sc.blit(txt_surface, (CENTER_WIDTH - txt_surface.get_width() // 2,
                              enter_n.get_height() + 80))

        pygame.draw.rect(sc, 'white', (CENTER_WIDTH - txt_surface.get_width() // 2 - 10,
                                       enter_n.get_height() + 80,
                                       input_box_w,
                                       input_box_h), 5)
        pygame.display.flip()
        clock.tick(1000)
