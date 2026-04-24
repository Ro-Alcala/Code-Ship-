import sys
import pygame
from settings import Settings
from ship import Ship


def run_game():
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    bg_color = ai_settings.bg_color
    clock = pygame.time.Clock()
    ship = Ship(ai_settings, screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(bg_color)
        ship.blitme()
        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    run_game()
