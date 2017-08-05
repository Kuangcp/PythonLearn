import sys
from time import sleep
import pygame

from bullet import Bullet
from alien import Alien

'''
     一些使用的的方法, 就是处理逻辑的公共方法代码
'''


def check_keydown_events(event, ai_settings, screen, stats,board, aliens, ship, bullets):
    # print("按下，采用的是ascii编码按键", event.key)
    """响应按键"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key in (pygame.K_LALT, pygame.K_RALT, pygame.K_q):
        check_quit(event, ai_settings)
    elif event.key == pygame.K_p and not stats.game_active:
        start_game(ai_settings, screen, stats, board, ship, aliens, bullets)


def check_quit(event, ai_settings):
    """退出快捷键"""
    if event.key in (pygame.K_LALT, pygame.K_RALT):
        ai_settings.quit_alt_flag = True
    if ai_settings.quit_alt_flag and event.key == pygame.K_q:
        print("再见 *.* ")
        sys.exit(1)


def check_keyup_events(event, ship):
    """响应松开"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_play_button(ai_settings, screen, stats, board, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    if play_button.rect.collidepoint(mouse_x, mouse_y):
        button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
        if button_clicked and not stats.game_active:
            start_game(ai_settings, screen, stats, board, ship, aliens, bullets)

# 重置游戏状态，开始游戏
def start_game(ai_settings, screen, stats, board, ship, aliens, bullets):
    pygame.mouse.set_visible(False)
    ai_settings.initialize_dynamic()
    # 重置游戏状态
    stats.reset_stats()
    stats.game_active = True
    aliens.empty()
    bullets.empty()
    # 重置显示板
    board.prep_high_score()
    board.prep_score()
    board.prep_level()
    board.prep_ships()

    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()
    # 应该使用常量的
    # ai_settings.fleet_drop_speed = 3
    # ai_settings.alien_speed_factor = 0.6


def check_events(ai_settings, screen, stats, board, play_button, ship, aliens, bullets):
    """ 响应按键，更新ship对象的标识属性，ship根据标识属性自更新状态"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, stats,board, aliens, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, board, play_button, ship, aliens, bullets, mouse_x, mouse_y)

"""子弹"""


def fire_bullet(ai_settings, screen, ship, bullets):
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def update_screen(ai_settings, screen, stats, board, ship, aliens, bullets, play_button):
    screen.fill(ai_settings.bg_color)
    # 在飞船和外星人后面重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    board.show_score()
    # alien.blitme()
    # 如果游戏是非活动状态，就绘制按钮
    if not stats.game_active:
        play_button.draw_button()

    # 让最近绘制的屏幕可见 重绘
    pygame.display.flip()


def update_bullets(ai_settings, screen, stats, board, ship, aliens, bullets):
    bullets.update()
    # 删除超出屏幕的子弹， 不应从列表或编组中删除条目，应该从副本删除
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
            # print("子弹集合长度：", len(bullets))
    check_bullet_alien_collisions(ai_settings, screen, stats, board, ship, aliens, bullets)


def check_bullet_alien_collisions(ai_settings, screen, stats, board, ship, aliens, bullets):
    # 检查是否有子弹击中了外星人，如果有就删除对应的子弹和外星人， 这666了一个方法搞定
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            board.prep_score()
        check_high_score(stats, board)

    if len(aliens) == 0:
        # 删除现有子弹新建外星人群,并提高下落速度
        bullets.empty()
        ai_settings.increase_speed()
        stats.level += 1
        board.prep_level()
        create_fleet(ai_settings, screen, ship, aliens)


"""外星人"""


def create_fleet(ai_settings, screen, ship, aliens):
    """创建外星人群"""
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def get_number_aliens_x(ai_settings, alien_width):
    """计算行容纳的外星人数量"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """创建一个外星人，放在当前行"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * row_number * alien_width
    aliens.add(alien)


def get_number_rows(ai_settings, ship_height, alien_height):
    """计算屏幕容纳外星人行数"""
    available_space_y = ai_settings.screen_height - (3 * alien_height) - ship_height
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def update_aliens(ai_settings, stats, board, screen, ship, aliens, bullets):
    """检查是否有外星人在边缘"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # 监测外星人和飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, board,  screen, ship, aliens, bullets)
    check_aliens_bottom(ai_settings, stats, board, screen, ship, aliens, bullets)


def ship_hit(ai_settings, stats, board, screen, ship, aliens, bullets):
    if stats.ships_left > 0:
        # 减一
        stats.ships_left -= 1
        # 重置游戏
        aliens.empty()
        bullets.empty()
        board.prep_ships()
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        # 暂停
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_fleet_edges(ai_settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def check_aliens_bottom(ai_settings, stats, board, screen, ship, aliens, bullets):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, stats, board, screen, ship, aliens, bullets)
            break


def change_fleet_direction(ai_settings, aliens):
    """下落"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def check_high_score(stats, board):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        board.prep_high_score()