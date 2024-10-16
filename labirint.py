import random
import sqlite3
import time
from random import choice

import pygame

from change_hard import choise_hard
from leader_bord import leader_board
from name_entering import enter_name
from name_entering import load_image
from parametrs import RES, WIDTH, HEIGHT

TILE = None

MILLISEC, SEC, MINUTE = 0, 0, 0
time_flag_start = False

TEXT_TIME = ''
WL = 'LOSS'

pygame.init()
sc = pygame.display.set_mode(RES)
clock = pygame.time.Clock()
pygame.display.set_caption('Лабиринт')

FPS = 90

all_sprites = pygame.sprite.Group()


def insert_result(board, names, game_time, wl):
    con = sqlite3.connect('Leader_board.db')
    cur = con.cursor()
    cur.execute("""INSERT INTO {} (name, result, winorloss) \
                    VALUES('{}', '{}', '{}')""".format(board, names, game_time, wl))
    con.commit()
    con.close()


def music(flag):
    if flag:
        print('m')
        pygame.mixer.music.load('data/music/Savkov_Igor_RiverTravel.mp3')
        pygame.mixer.music.set_volume(10.0)

        pygame.mixer.music.play()


def start_screen():
    intro_text = ["Лабиринт", "",
                  "На языке Pythone"]

    fon = pygame.transform.scale(load_image('fon(1).jpg'), (WIDTH, HEIGHT))
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
                exit()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return

        pygame.display.flip()
        clock.tick(FPS)


def label_steps(steps):
    font = pygame.font.Font(None, 30)
    text = font.render(f"Осталось шагов {steps}", True, (100, 255, 100))

    text_x = COLS * TILE + 30
    text_y = 30
    text_w = text.get_width()
    text_h = text.get_height()

    pygame.draw.rect(sc, (0, 0, 0), (text_x - 10, text_y - 10,
                                     text_w + 20, text_h + 20), 0)
    pygame.draw.rect(sc, (0, 255, 0), (text_x - 10, text_y - 10,
                                       text_w + 20, text_h + 20), 2)
    sc.blit(text, (text_x, text_y))


def label_time():
    global MINUTE, SEC, MILLISEC, TEXT_TIME
    MILLISEC += clock.get_time()
    font = pygame.font.Font(None, 40)
    if time_flag_start:
        if MILLISEC > 1000:
            SEC += 1
            MILLISEC = 0
        if SEC >= 60:
            SEC = 0
            MINUTE += 1
    if SEC >= 10 and MINUTE >= 10:
        TEXT_TIME = f"{MINUTE}:{SEC}"
    elif SEC >= 10 > MINUTE:
        TEXT_TIME = f"0{MINUTE}:{SEC}"
    elif SEC < 10 and MINUTE < 10:
        TEXT_TIME = f"0{MINUTE}:0{SEC}"
    elif SEC < 10 <= MINUTE:
        TEXT_TIME = f"{MINUTE}:0{SEC}"

    lab_time = font.render(TEXT_TIME, True, (100, 230, 200))

    text_x = COLS * TILE + 30
    text_y = 80
    text_w = lab_time.get_width()
    text_h = lab_time.get_height()

    pygame.draw.rect(sc, (0, 0, 0), (text_x - 10, text_y - 10,
                                     text_w + 20, text_h + 20), 0)
    pygame.draw.rect(sc, (0, 255, 0), (text_x - 10, text_y - 10,
                                       text_w + 20, text_h + 20), 2)
    sc.blit(lab_time, (text_x, text_y))


def Game_time(game):
    if game == 'Game_win.png':
        step_y = 150
    else:
        step_y = 300
    font = pygame.font.Font(None, 100)
    text_time = TEXT_TIME
    game_time = font.render(text_time, True, (100, 230, 200))
    text_x = WIDTH // 2 - game_time.get_width() // 2
    text_y = HEIGHT // 2 - game_time.get_height() // 2 + step_y
    text_w = game_time.get_width()
    text_h = game_time.get_height()

    pygame.draw.rect(sc, (0, 255, 0), (text_x - 10, text_y - 10,
                                       text_w + 20, text_h + 20), 2)
    sc.blit(game_time, (text_x, text_y))


def check_cell(x, y):
    find_index = lambda a, b: a + b * COLS
    if x < 0 or x > COLS - 1 or y < 0 or y > ROWS - 1:
        return False
    return grid_cells[find_index(x, y)]


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

    def check_neighbors(self):
        neighbors = []
        top = check_cell(self.x, self.y - 1)
        right = check_cell(self.x + 1, self.y)
        bottom = check_cell(self.x, self.y + 1)
        left = check_cell(self.x - 1, self.y)
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
        top = check_cell(self.x, self.y - 1)
        right = check_cell(self.x + 1, self.y)
        bottom = check_cell(self.x, self.y + 1)
        left = check_cell(self.x - 1, self.y)
        if top:
            neighbors.append(['top', top])
        if right:
            neighbors.append(['right', right])
        if bottom:
            neighbors.append(['bottom', bottom])
        if left:
            neighbors.append(['left', left])
        return neighbors if neighbors else False

    @staticmethod
    def move(direction):
        for i in hero.check_neighbors():
            if i[0] == direction:
                if not grid_cells[hero_x + hero_y * COLS].walls[direction]:
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


rerun = False


def main():
    global TILE, MINUTE, MILLISEC, SEC, TEXT_TIME, WL, \
        time_flag_start, FPS, COLS, ROWS, grid_cells, rerun, hero, hero_x, hero_y

    res = RES
    TILE = None
    rerun = False
    MILLISEC, SEC, MINUTE = 0, 0, 0
    time_flag_start = False

    c = 0

    TEXT_TIME = ''
    WL = 'LOSS'

    pygame.display.set_caption('Лабиринт')

    sc = pygame.display.set_mode(res)
    clock = pygame.time.Clock()

    FPS = 90

    all_sprites = pygame.sprite.Group()

    stack = []
    colors, color = [], 40

    bag_fix = 0

    game_start = 0
    end_game = 0
    image_over = "Game_win.png"

    start_screen()
    user_name = enter_name()
    TILE, hard = choise_hard()
    if hard == 'Easy':
        board = 'easy_board'
    elif hard == 'Medium':
        board = 'medium_board'
    else:
        board = 'hard_board'

    COLS, ROWS = WIDTH // TILE - 5, HEIGHT // TILE
    hero_y, hero_x = random.randint(5, ROWS - 2), random.randint(5, COLS - 2)
    step_count = COLS * ROWS // 2 + 50
    grid_cells = [Cell(col, row) for row in range(ROWS) for col in range(COLS)]
    current_cell = grid_cells[0]

    while True:
        sc.fill(pygame.Color('darkslategray'))
        music(pygame.mixer.music.get_endevent())

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                rerun = True
                break

            if bag_fix and step_count:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                    if hero.move('left'):
                        hero_x -= 1
                        step_count -= 1
                        time_flag_start = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                    if hero.move('right'):
                        hero_x += 1
                        step_count -= 1
                        time_flag_start = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                    if hero.move('top'):
                        hero_y -= 1
                        step_count -= 1
                        time_flag_start = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                    if hero.move('bottom'):
                        hero_y += 1
                        step_count -= 1
                        time_flag_start = True
            if not step_count:
                image_over = "Game_over.png"
                end_game = True
                WL = 'LOSS'

        [cell.draw() for cell in grid_cells]
        current_cell.visited = True
        current_cell.draw_current_cell()

        [pygame.draw.rect(sc, colors[i], (
            cell.x * TILE + 2,
            cell.y * TILE + 2,
            TILE - 4,
            TILE - 4)) for i, cell in enumerate(stack)]

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
            bag_fix = 1
            hero = Hero(hero_x, hero_y)
            hero.draw()
            label_steps(step_count)
            label_time()

        if hero_x == 0 and hero_y == 0:
            end_game = True
            WL = 'WIN'

        if end_game and not c:
            Game(all_sprites, image_over)
            c += 1
        pl_mn = 1
        if end_game:
            sc.fill(pygame.color.Color(20, 20, 20))
            for i in all_sprites:
                if i.rect.x + 5 + WIDTH > WIDTH:
                    pl_mn = 0
                    time.sleep(3)
                    insert_result(board, user_name, TEXT_TIME, WL)
                    leader_board(board)
                i.rect.x += 20 * pl_mn
            all_sprites.draw(sc)
            Game_time(image_over)
            game_start = 2

        pygame.display.flip()
        clock.tick(10000)

        if rerun:
            main()


if __name__ == '__main__':
    main()

# (ВЫПОЛНЕНО) Сделать начало таймера с 1 хода игрока либо через какой-то промежуток времени,
# чтобы игрок мог запомнить и соорентироваться на местности'''

# '''Сделать доп.режим "Туман Войны", идея заключается в том, чтобы со временем стены теряли бы цвет, и
# было бы необходимо запомнить строение лабиринта'''
#
# '''(ВЫПОЛНЕНО)Сделать начальный экран с выбором уровня сложности
# (Просто добавить кнопки с изменением параметра TILE) '''

# '''(ВЫПОЛНЕНО)Сделать перезагрузку игры на кнопку "R"'''
