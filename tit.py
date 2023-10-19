import pygame
from copy import deepcopy
from random import choice, randrange

from time import sleep
import pygame_menu
from pygame_menu import themes

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, wight, height):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(player_image), (600, 400))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        

pygame.init()
surface = pygame.display.set_mode((600, 400))

global score
score = 0

def start_the_game():
    W, H = 10, 15
    TILE = 45
    GAME_RES = W * TILE, H * TILE
    FPS = 15

    game_sc = pygame.display.set_mode(GAME_RES)
    score = 0
    pygame.display.set_caption('TETRIS')
    clock = pygame.time.Clock()

    pygame.font.init()
    font_score = pygame.font.Font(None, 36)

    grid = [pygame.Rect(x * TILE, y * TILE, TILE, TILE) for x in range(W) for y in range(H)]

    figures_pos = [[(-1, 0), (-2,0), (0, 0), (1, 0)],
                    [(0, -1), (-1, -1), (-1, 0), (0, 0)],
                    [(-1, 0), (-1, 1), (0, 0), (0, -1)],
                    [(0, 0), (-1, 0), (0, 1), (-1, -1)],
                    [(0, 0), (0, -1), (0, 1), (-1, -1)],
                    [(0, 0), (0, -1), (0, 1), (-1, -1)],
                    [(0, 0), (0, -1), (0, 1), (-1, 0)]]

    figures = [[pygame.Rect(x + W // 2, y +1, 1, 1) for x, y in fig_pos] for fig_pos in figures_pos]
    figure_rect = pygame.Rect(0, 0, TILE - 2, TILE - 2)
    field = [[0 for i in range(W)] for j in range(H)]

    anim_count, anim_speed, anim_limit = 0, 60, 2000
    figure = deepcopy(choice(figures))


    def check_borders():
            if figure[i].x < 0 or figure[i].x > W - 1:
                    return False
            elif figure[i].y > H - 1 or field[figure[i].y][figure[i].x]:
                    return False
            return True


    get_color = lambda : (randrange(30, 256), randrange(30, 256), randrange(30, 256))
    color = get_color()
    game = True
    while game:
            for i in field[0]:
                if i != 0:
                    game = False
            dx, rotate = 0, False
            game_sc.fill(pygame.Color('black'))

            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                            exit()
                    if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_LEFT:
                                    dx = -1
                            elif event.key == pygame.K_RIGHT:
                                    dx = 1
                            elif event.key == pygame.K_DOWN:
                                    anim_limit = 100
                            elif event.key == pygame.K_UP:
                                    rotate = True
            figure_old = deepcopy(figure)
            for i in range(4):
                    figure[i].x += dx
                    if not check_borders():
                            figure = deepcopy(figure_old)
                            break

            anim_count += anim_speed
            if anim_count > anim_limit:
                    anim_count = 0
                    figure_old = deepcopy(figure)
                    for i in range(4):
                            figure[i].y += 1
                            if not check_borders():
                                    for i in range(4):
                                            field[figure_old[i].y][figure_old[i].x] = color
                                    color = get_color()
                                    figure = deepcopy(choice(figures))
                                    anim_limit = 2000
                                    score += 100
                                    break

            center = figure[0]
            figure_old = deepcopy(figure)
            if rotate:
                    for i in range(4):
                            x = figure[i].y - center.y
                            y = figure[i].x - center.x
                            figure[i].x = center.x - x
                            figure[i].y = center.y + y
                            if not check_borders():
                                    figure = deepcopy(figure_old)
                                    break

            line = H - 1
            for row in range(H - 1, -1, -1):
                    count = 0
                    for i in range(W):
                            if field[row][i]:
                                    count += 1
                            field[line][i] = field[row][i]
                    if count < W:
                        line -= 1
            [pygame.draw.rect(game_sc, (40, 40, 40), i_rect, 1) for i_rect in grid]

            for i in range(4):
                    figure_rect.x = figure[i].x * TILE
                    figure_rect.y = figure[i].y * TILE
                    pygame.draw.rect(game_sc, color, figure_rect)

            for y, raw in enumerate(field):
                    for x, col in enumerate(raw):
                            if col:
                                    figure_rect.x, figure_rect.y = x * TILE, y * TILE
                                    pygame.draw.rect(game_sc, col, figure_rect)
            score_text = font_score.render('Счёт: ' + str(score), 1, (255,255,255))
            game_sc.blit(score_text, (10, 20))

            pygame.display.flip()
            clock.tick(FPS)
    finish = True
    win_player1 = GameSprite('cat.jpg', 0, 0, 0, 600, 400)
    surface_end = pygame.display.set_mode((600, 400))
    score_text = font_score.render('Ваш счёт!!! ' + str(score), 1, (0,0,0))
    while finish:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
                
        pygame.display.flip()
        clock.tick(FPS)
        surface_end.blit(win_player1.image, (win_player1.rect.x, win_player1.rect.y))
        surface_end.blit(score_text, (120, 80))


    
    mainmenu._exit()

mainmenu = pygame_menu.Menu('Привет!', 600, 400, theme=themes.THEME_ORANGE)
mainmenu.add.text_input('Как настроение? ', default=' ', maxchar=20)
mainmenu.add.button('Начать игру', start_the_game)
mainmenu.add.button('Выйти', pygame_menu.events.EXIT)

mainmenu.mainloop(surface)