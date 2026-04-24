import sys
import time
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button
from game_stats import GameStats
from scoreboard import Scoreboard


class AlienInvasion:
    def __init__(self):
        pygame.init()
        self.ai_settings = Settings()
        self.screen = pygame.display.set_mode((self.ai_settings.screen_width, self.ai_settings.screen_height))
        pygame.display.set_caption("Alien Invasion")
        self.clock = pygame.time.Clock()
        self.stats = GameStats(self.ai_settings)
        self.stats.game_active = False
        self.ship = Ship(self.ai_settings, self.screen)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.play_button = Button(self.screen)
        self.sb = Scoreboard(self)
        self._create_fleet()

    def run_game(self):
        while True:
            self._check_events()
            if self.stats.game_active:
                self._check_fleet_edges()
                self.ship.update()
                self.aliens.update(self.ai_settings.fleet_direction)
                self._update_bullets()
                self._check_ship_alien_collisions()
                self._check_aliens_bottom()
            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._check_play_button(event.pos)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_q:
            pygame.quit()
            sys.exit()
        if not self.stats.game_active:
            return

        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            if len(self.bullets) < self.ai_settings.bullets_allowed:
                new_bullet = Bullet(self.ai_settings, self.screen, self.ship)
                self.bullets.add(new_bullet)

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _check_play_button(self, mouse_pos):
        if not self.stats.game_active and self.play_button.rect.collidepoint(mouse_pos):
            self.stats.reset_stats()
            self.ai_settings.initialize_dynamic_settings()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            self.aliens.empty()
            self.bullets.empty()
            self._create_fleet()
            self.ship.rect.centerx = self.screen.get_rect().centerx
            self.ship.rect.bottom = self.screen.get_rect().bottom
            self.ship.center = float(self.ship.rect.centerx)
            pygame.mouse.set_visible(False)

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self.ai_settings.fleet_direction *= -1
                for alien in self.aliens.sprites():
                    alien.rect.y += self.ai_settings.fleet_drop_speed
                break

    def _create_fleet(self):
        alien = Alien(self.ai_settings, self.screen)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.ai_settings.screen_width - 2 * alien_width
        number_aliens_x = available_space_x // (2 * alien_width)
        available_space_y = (self.ai_settings.screen_height - (3 * alien_height) - self.ship.rect.height)
        number_rows = available_space_y // (2 * alien_height)
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                alien = Alien(self.ai_settings, self.screen)
                alien.x = alien_width + 2 * alien_width * alien_number
                alien.rect.x = alien.x
                alien.rect.y = alien_height + 2 * alien_height * row_number
                self.aliens.add(alien)

    def _ship_hit(self):
        self.stats.ships_left -= 1
        self.sb.prep_ships()
        self.aliens.empty()
        self.bullets.empty()
        if self.stats.ships_left > 0:
            self._create_fleet()
            self.ship.rect.centerx = self.screen.get_rect().centerx
            self.ship.rect.bottom = self.screen.get_rect().bottom
            self.ship.center = float(self.ship.rect.centerx)
            time.sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_ship_alien_collisions(self):
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

    def _check_aliens_bottom(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.ai_settings.alien_points * len(aliens)
            self.sb.check_high_score()
            self.sb.prep_score()

        if not self.aliens:
            self.bullets.empty()
            self.ai_settings.increase_speed()
            self.stats.level += 1
            self.sb.prep_level()
            self._create_fleet()

    def _update_screen(self):
        print(f"Bullet count: {len(self.bullets)}")
        self.screen.fill(self.ai_settings.bg_color)
        if self.stats.game_active:
            for bullet in self.bullets.sprites():
                self.screen.blit(bullet.image, bullet.rect)
            self.ship.blitme()
            self.aliens.draw(self.screen)
        else:
            self.play_button.draw_button()
        self.sb.show_score()
        pygame.display.flip()


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()

