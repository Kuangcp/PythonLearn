import sys

import pygame

from alien_settings import Settings
from ship import Ship


def run_game():
    # 初始化游戏并创建一个屏幕对象
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height)
    )
    # screen = pygame.display.set_mode((600, 400))
    pygame.display.set_caption("Alien Invasion")
    ship = Ship(screen)
    # bg_color = (230,230,230)

    # 开始游戏的循环
    while True:
        # 监视键盘和鼠标事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        # 重绘屏幕
        # screen.fill(bg_color)
        screen.fill(ai_settings.bg_color)
        ship.blitme()
        # 让最近绘制的屏幕可见 重绘
        pygame.display.flip()


run_game()
