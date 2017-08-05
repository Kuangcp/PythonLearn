"""
    设置类
"""


class Settings:
    def __init__(self):
        self.screen_width = 800
        self.screen_height = 500
        self.bg_color = (230, 230, 230)
        # 飞船速度的设置，因为rect的centerx等属性只能放整数，所以还要进行修改
        # self.ship_speed_factor = 1.5
        self.ship_limit = 3
        # 子弹设置
        # self.bullet_speed_factor = 3
        self.bullet_width = 5
        self.bullet_height = 10
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 3
        self.quit_alt_flag = False
        # 外星人设置
        # self.alien_speed_factor = 0.6
        # self.fleet_drop_speed = 3
        # self.alien_points = 50

        # 1表示右， -1表示左
        # self.fleet_direction = 1

        self.speedup_scale = 1.1
        self.score_scale = 1.3
        self.initialize_dynamic()

    def initialize_dynamic(self):
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 0.8

        self.fleet_direction = 1
        # 下落速度
        self.fleet_drop_speed = 5
        self.alien_points = 50

    def increase_speed(self):
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.fleet_drop_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
        # print(self.alien_points)
