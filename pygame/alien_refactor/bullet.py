import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """对飞船子弹管理的类"""

    def __init__(self, ai_settings, screen, ship):
        """一个对飞船所处位置创建子弹的对象"""
        super(Bullet, self).__init__()
        self.screen = screen

        # 先在 0，0处创建一个表示子弹的矩形，然后再设置正确的位置？？？ 为什么不是ship的坐标
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top
        # 存储使用小数表示的位置
        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        """向上移动子弹"""
        # 更新表示子弹位置的小数值
        self.y -= self.speed_factor
        self.rect.y = self.y

    def draw_bullet(self):
        """在屏幕绘制子弹"""
        pygame.draw.rect(self.screen, self.color, self.rect)