import os
import random
import time
from random import choice

import pygame


def music(flag):
    if flag:
        print('m')
        pygame.mixer.music.load('music\Savkov_Igor_RiverTravel.mp3')
        pygame.mixer.music.play()


RES = WIDTH, HEIGHT = 1202, 902
TILE = 60
cols, rows = WIDTH // TILE - 5, HEIGHT // TILE
MINUTE = 0
N = 0

pygame.init()
sc = pygame.display.set_mode(RES)
clock = pygame.time.Clock()
pygame.display.set_caption('Лабиринт')

pygame.display.set_caption('Лабиринт')
FPS = 90

all_sprites = pygame.sprite.Group()


def start_screen():
    intro_text = ["Лабиринт", "",
                  "На языке Pythone",
                  ]

    fon = pygame.transform.scale(load_image('fon(1).jpg'), (1202, 902))
    sc.blit(fon, (0, 0))
    font = pygame.font.Font(None, 90)
    text_coord = 10
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        sc.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                pygame.mixer.init()
                pygame.mixer.music.load('music\Savkov_Igor_RiverTravel.mp3')
                pygame.mixer.music.play()
                return
        pygame.display.flip()
        clock.tick(FPS)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
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


def label_steps(steps):
    font = pygame.font.Font(None, 30)
    text = font.render(f"Осталось шагов {steps}", True, (100, 255, 100))
    text_x = cols * TILE + 30
    text_y = 30
    text_w = text.get_width()
    text_h = text.get_height()
    pygame.draw.rect(sc, (0, 0, 0), (text_x - 10, text_y - 10,
                                     text_w + 20, text_h + 20), 0)
    pygame.draw.rect(sc, (0, 255, 0), (text_x - 10, text_y - 10,
                                       text_w + 20, text_h + 20), 2)
    sc.blit(text, (text_x, text_y))


def label_time(time):
    minut, sec = 0, time
    font = pygame.font.Font(None, 40)
    if sec == 60:
        minut += 1
        sec = 0
    if sec >= 10 and minut >= 10:
        text = font.render(f"{minut}:{sec}", True, (100, 230, 200))
    elif sec >= 10 > minut:
        text = font.render(f"0{minut}:{sec}", True, (100, 230, 200))
    elif sec < 10 and minut < 10:
        text = font.render(f"0{minut}:0{sec}", True, (100, 230, 200))
    elif sec < 10 <= minut:
        text = font.render(f"{minut}:0{sec}", True, (100, 230, 200))
    text_x = cols * TILE + 30
    text_y = 80
    text_w = text.get_width()
    text_h = text.get_height()
    pygame.draw.rect(sc, (0, 0, 0), (text_x - 10, text_y - 10,
                                     text_w + 20, text_h + 20), 0)
    pygame.draw.rect(sc, (0, 255, 0), (text_x - 10, text_y - 10,
                                       text_w + 20, text_h + 20), 2)
    sc.blit(text, (text_x, text_y))


def Game_time(time, game):
    if game == 'Game_win.png':
        step_y = 150
    else:
        step_y = 300
    minut, sec = 0, time
    font = pygame.font.Font(None, 100)
    if sec > 60:
        minut += sec // 60
        sec = sec - 60 * minut
    if sec >= 10 and minut >= 10:
        text = font.render(f"{minut}:{sec}", True, (100, 230, 200))
    elif sec >= 10 > minut:
        text = font.render(f"0{minut}:{sec}", True, (100, 230, 200))
    elif sec < 10 and minut < 10:
        text = font.render(f"0{minut}:0{sec}", True, (100, 230, 200))
    elif sec < 10 <= minut:
        text = font.render(f"{minut}:0{sec}", True, (100, 230, 200))
    text_x = WIDTH // 2 - text.get_width() // 2
    text_y = HEIGHT // 2 - text.get_height() // 2 + step_y
    text_w = text.get_width()
    text_h = text.get_height()
    pygame.draw.rect(sc, (0, 255, 0), (text_x - 10, text_y - 10,
                                       text_w + 20, text_h + 20), 2)
    sc.blit(text, (text_x, text_y))


''' оптимизировать over_time'''


class Cell:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.visited = False
        self.colors, self.color = [], 40
        self.colors.append((min(self.color, 255), 10, 100))
        self.step = 1

    def draw_current_cell(self):
        x, y = self.x * TILE, self.y * TILE
        pygame.draw.rect(sc, pygame.Color('saddlebrown'), (x + 2, y + 2, TILE - 2, TILE - 2))

    def draw(self):
        x, y = self.x * TILE, self.y * TILE
        if self.visited:
            pygame.draw.rect(sc, pygame.Color('black'), (x, y, TILE, TILE))

        if self.walls['top']:
            pygame.draw.line(sc, self.colors[-1], (x, y), (x + TILE, y), 3)
        if self.walls['right']:
            pygame.draw.line(sc, self.colors[-1], (x + TILE, y), (x + TILE, y + TILE), 3)
        if self.walls['bottom']:
            pygame.draw.line(sc, self.colors[-1], (x + TILE, y + TILE), (x, y + TILE), 3)
        if self.walls['left']:
            pygame.draw.line(sc, self.colors[-1], (x, y + TILE), (x, y), 3)
        self.colors.append((100, min(self.color, 255), 10))
        self.color += self.step
        if self.color == 255:
            self.step *= -1
        elif self.color == 40:
            self.step *= -1

    def check_cell(self, x, y):
        find_index = lambda x, y: x + y * cols
        if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
            return False
        return grid_cells[find_index(x, y)]

    def check_neighbors(self):
        neighbors = []
        top = self.check_cell(self.x, self.y - 1)
        right = self.check_cell(self.x + 1, self.y)
        bottom = self.check_cell(self.x, self.y + 1)
        left = self.check_cell(self.x - 1, self.y)
        if top and not top.visited:
            neighbors.append(top)
        if right and not right.visited:
            neighbors.append(right)
        if bottom and not bottom.visited:
            neighbors.append(bottom)
        if left and not left.visited:
            neighbors.append(left)
        return choice(neighbors) if neighbors else False


def remove_walls(current, next_ceil):
    dx = current.x - next_ceil.x
    if dx == 1:
        current.walls['left'] = False
        next_ceil.walls['right'] = False
    elif dx == -1:
        current.walls['right'] = False
        next_ceil.walls['left'] = False
    dy = current.y - next_ceil.y
    if dy == 1:
        current.walls['top'] = False
        next_ceil.walls['bottom'] = False
    elif dy == -1:
        current.walls['bottom'] = False
        next_ceil.walls['top'] = False


class Hero(Cell):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.x, self.y = x, y
        self.color = pygame.color.Color(10, 100, 10)

    def draw(self):
        x, y = self.x * TILE, self.y * TILE
        pygame.draw.rect(sc, self.color, (x + 6, y + 6, TILE - 12, TILE - 12))

    def check_neighbors(self):
        neighbors = []
        top = self.check_cell(self.x, self.y - 1)
        right = self.check_cell(self.x + 1, self.y)
        bottom = self.check_cell(self.x, self.y + 1)
        left = self.check_cell(self.x - 1, self.y)
        if top:
            neighbors.append(['top', top])
        if right:
            neighbors.append(['right', right])
        if bottom:
            neighbors.append(['bottom', bottom])
        if left:
            neighbors.append(['left', left])
        return neighbors if neighbors else False

    def move(self, direction):
        for i in hero.check_neighbors():
            if i[0] == direction:
                if not grid_cells[hero_x + hero_y * cols].walls[direction]:
                    return True
        return False


class Game(pygame.sprite.Sprite):
    def __init__(self, group, image_2):
        image = load_image(image_2)
        image = pygame.transform.scale(image, (WIDTH, HEIGHT))
        super().__init__(group)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = -WIDTH
        self.rect.y = self.rect[1]


grid_cells = [Cell(col, row) for row in range(rows) for col in range(cols)]
current_cell = grid_cells[0]
stack = []
colors, color = [], 40

hero_y, hero_x = random.randint(5, rows - 2), random.randint(5, cols - 2)
bag_Fix = 0
step_count = cols * rows // 2 + 20

game_start = 0
End_Game = 0
image_over = "Game_win.png"
time_over = 0

start_screen()
while True:
    sc.fill(pygame.Color('darkslategray'))
    music(pygame.mixer.music.get_endevent())

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            exit()
        if bag_Fix and step_count:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                if hero.move('left'):
                    hero_x -= 1
                    step_count -= 1
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                if hero.move('right'):
                    hero_x += 1
                    step_count -= 1
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                if hero.move('top'):
                    hero_y -= 1
                    step_count -= 1
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                if hero.move('bottom'):
                    hero_y += 1
                    step_count -= 1
        if not step_count:
            image_over = "Game_over.png"
            End_Game = True

    [cell.draw() for cell in grid_cells]
    current_cell.visited = True
    current_cell.draw_current_cell()
    [pygame.draw.rect(sc, colors[i], (cell.x * TILE + 2, cell.y * TILE + 2,
                                      TILE - 4, TILE - 4)) for i, cell in enumerate(stack)]

    next_cell = current_cell.check_neighbors()
    if next_cell:
        next_cell.visited = True
        stack.append(current_cell)
        colors.append((min(color, 255), 10, 100))
        color += 1
        remove_walls(current_cell, next_cell)
        current_cell = next_cell
    elif stack:
        current_cell = stack.pop()
    if current_cell.x == 0 and current_cell.y == 0 and not game_start:
        game_start += 1
    if game_start == 1:
        bag_Fix = 1
        hero = Hero(hero_x, hero_y)
        hero.draw()
        label_steps(step_count)

        start_time = pygame.time.get_ticks() // 1000
        label_time(start_time)

    if hero_x == 0 and hero_y == 0:
        End_Game = True

    pl_mn = 1
    speed = 20
    if End_Game and not time_over:
        Game(all_sprites, image_over)
        time_over = start_time
    if End_Game:
        sc.fill(pygame.color.Color(20, 20, 20))
        for i in all_sprites:
            if i.rect.x + 5 + WIDTH > WIDTH:
                pl_mn = 0
            i.rect.x += speed * pl_mn
        all_sprites.draw(sc)
        Game_time(time_over, image_over)

    pygame.display.flip()
    clock.tick(10000)
