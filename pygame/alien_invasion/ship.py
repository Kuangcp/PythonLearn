import pygame


class Ship():
    def __init__(self, screen: object) -> object:
        self.screen = screen

        # 加载船图像 load 出不来使用load_basic
        self.image = pygame.image.load_basic('images/ico.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # 将新的船放置在底部中央
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

    def blitme(self):
        # 指定位置绘制飞船
        self.screen.blit(self.image,self.rect)