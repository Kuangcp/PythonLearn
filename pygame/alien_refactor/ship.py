import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    def __init__(self, ai_settings, screen):
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # 加载船图像 load 出不来使用load_basic
        self.image = pygame.image.load_basic('images/ico.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # 将新的船放置在底部中央
        self.center = float(self.rect.centerx)
        # self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom


        # 移动标识
        self.moving_right = False
        self.moving_left = False

    def update(self):
        # 更新center值而不是rect值
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor
        # 根据self.center更新 rect对象
        self.rect.centerx = self.center

    def blitme(self):
        # 指定位置绘制飞船
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """让飞船居中"""
        self.center = self.screen_rect.centerx