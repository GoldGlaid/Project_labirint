import sqlite3

import pygame

pygame.init()

RES = WIDTH, HEIGHT = 1202, 902

pygame.init()
sc = pygame.display.set_mode(RES)
clock = pygame.time.Clock()

text = ''
font_range_menu = 45
font_range_text = 50


def get_result(board):
    con = sqlite3.connect('Leader_board.db')
    cur = con.cursor()
    result = cur.execute('''SELECT * FROM {} WHERE winorloss like "WIN"'''.format(board)).fetchall()
    con.commit()
    con.close()
    return result


def leader_board(board):
    list_leaders = sorted(get_result(board), key=lambda x: int(x[1][:2]) * 60 + int(x[1][3:]))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                exit()
        sc.fill(pygame.color.Color(20, 20, 20))
        font1 = pygame.font.Font('MonsterFriendFore.otf', font_range_menu)
        font2 = pygame.font.Font('MonsterFriendBack.otf', font_range_text)

        enter_n = font1.render('Leader board TOP 10 ({})'.format(board[:-6]), True, 'white')

        next_step = 120
        st = 1
        for name, time, wl in list_leaders:
            player = font2.render(f"{st}. {name}", True, 'white')
            sc.blit(player, (WIDTH // 6, next_step))

            pl_time = font2.render(f"{time}", True, 'white')
            sc.blit(pl_time, (WIDTH // 6 + 600, next_step))

            next_step += 75
            st += 1
            if st > 10:
                break

        sc.blit(enter_n, (WIDTH // 15, 20))
        pygame.draw.rect(sc, 'gray', (WIDTH // 8, 80, WIDTH - WIDTH // 4, HEIGHT - 90), 2)
        pygame.display.flip()
        clock.tick(1000)
