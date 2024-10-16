import os
import sys

import pygame

from parametrs import RES, WIDTH, HEIGHT

TILE = 60

pygame.init()
sc = pygame.display.set_mode(RES)
clock = pygame.time.Clock()

text = ''
font_range = 90

input_box_w = 50
input_box_h = 100
input_box_x = WIDTH / 2 - input_box_w
input_box_y = HEIGHT / 2 - input_box_h

input_box = pygame.Rect(input_box_x, input_box_y, input_box_w, input_box_h)
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
    image = pygame.transform.scale(image, (250 * 2, 200 * 2))

    def __init__(self, group):
        super().__init__(group)
        self.image = Dino.image
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH // 80
        self.rect.y = 500


class Dino2(pygame.sprite.Sprite):
    image = load_image("dinozavr2.png")
    image = pygame.transform.scale(image, (250 * 2, 200 * 2))
    image = pygame.transform.flip(image, True, False)

    def __init__(self, group):
        super().__init__(group)
        self.image = Dino2.image
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH - 500
        self.rect.y = 500


class Coca(pygame.sprite.Sprite):
    image = load_image('coconut.png')
    image = pygame.transform.scale(image, (500, 600))
    image = pygame.transform.flip(image, True, False)

    def __init__(self, group):
        super().__init__(group)
        self.image = Coca.image
        self.rect = self.image.get_rect()
        self.rect.x = 740
        self.rect.y = 290


class Coca2(pygame.sprite.Sprite):
    image = load_image('coconut.png')
    image = pygame.transform.scale(image, (500, 600))

    def __init__(self, group):
        super().__init__(group)
        self.image = Coca2.image
        self.rect = self.image.get_rect()
        self.rect.x = -50
        self.rect.y = 290


Coca(all_sprites)
Coca2(all_sprites)
Dino(all_sprites)
Dino2(all_sprites)


def enter_name():
    global text_input_f, text, text_input_f, max_col_txt
    global input_box_x, input_box_y, input_box_w, input_box_h

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

        enter_n = font.render('Enter your name', True, 'white')
        txt_surface = font.render(text, True, 'yellow')

        if len(text) == max_col_txt:
            text_input_f = False
        else:
            text_input_f = True
        if input_box_w <= txt_surface.get_width():
            input_box_w += font_range
            input_box_x -= font_range / 2

        all_sprites.draw(sc)

        sc.blit(txt_surface, (input_box_x, input_box_y - 40))
        sc.blit(enter_n, (WIDTH / 5, HEIGHT / 6))
        pygame.draw.rect(sc, 'gray', (input_box_x, input_box_y - font_range // 2, input_box_w, input_box_h), 2)
        pygame.display.flip()
        clock.tick(1000)
