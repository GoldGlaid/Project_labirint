import sqlite3

import pygame

from parametrs import RES, WIDTH, HEIGHT, CENTER_WIDTH, CENTER_HEIGHT

pygame.init()
sc = pygame.display.set_mode(RES)
clock = pygame.time.Clock()

text = ''
font_range_menu = 75
font_range_text = 80


def get_result(board):
    con = sqlite3.connect('Leader_board.db')
    cur = con.cursor()
    result = cur.execute('''SELECT * FROM {} WHERE winorloss like "WIN"'''.format(board)).fetchall()
    con.commit()
    con.close()
    return result


def leader_board(board):
    list_leaders = sorted(get_result(board), key=lambda x: int(x[1][:2]) * 60 + int(x[1][3:]))
    rerun = False
    while True:
        if rerun:
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                rerun = True
                break
        sc.fill(pygame.color.Color(20, 20, 20))
        font1 = pygame.font.Font('data/fonts/determinationmonorusbylyajk.otf', font_range_menu)
        font2 = pygame.font.Font('data/fonts/determinationmonorusbylyajk.otf', font_range_text)

        leader_board_text = font1.render('LEADER BOARD TOP 10 ({})'.format(board[:-6].upper()), True, 'gold')

        next_step = 120
        st = 1
        for name, time, wl in list_leaders:
            player = font2.render(f"{st}. {name.upper()}", True, 'white')
            sc.blit(player, (WIDTH // 6, next_step))

            pl_time = font2.render(f"{time.upper()}", True, 'white')
            sc.blit(pl_time, (WIDTH // 6 + 600, next_step))

            next_step += 75
            st += 1
            if st > 10:
                break

        sc.blit(leader_board_text, (CENTER_WIDTH - leader_board_text.get_width() // 2, 20))
        pygame.draw.rect(sc, 'gold', (WIDTH // 8, 90, WIDTH - WIDTH // 4, HEIGHT - 120), 2)
        pygame.display.flip()
        clock.tick(1000)
