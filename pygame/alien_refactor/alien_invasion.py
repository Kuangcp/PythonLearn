import pygame

from alien_settings import Settings
from scoreboard import Scoreboard
from ship import Ship
from alien import Alien
from pygame.sprite import Group
from game_stats import GameStats
from button import Button

import game_functions as gf

''' 
    运行入口 主类,创建一系列整个游戏都要使用的对象
'''


def run_game():
    # 初始化游戏并创建一个屏幕对象
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height)
    )
    pygame.display.set_caption("Alien Invasion")
    play_button = Button(ai_settings, screen, "Play")
    # 创建一个飞船
    ship = Ship(ai_settings, screen)
    # 创建一个编组
    bullets = Group()
    aliens = Group()
    # 创建外星人群
    gf.create_fleet(ai_settings, screen, ship, aliens)
    # alien = Alien(ai_settings, screen)
    stats = GameStats(ai_settings)
    board = Scoreboard(ai_settings, screen, stats)

    # 开始游戏的循环
    while True:
        gf.check_events(ai_settings, screen, stats, board, play_button, ship, aliens, bullets)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, board, ship, aliens, bullets)
            gf.update_aliens(ai_settings, stats, board, screen, ship, aliens, bullets)

        gf.update_screen(ai_settings, screen, stats, board, ship, aliens, bullets, play_button)


run_game()
