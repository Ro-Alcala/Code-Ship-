import pygame


class Bullet(pygame.sprite.Sprite):
    def __init__(self, ai_settings, screen, ship):
        super().__init__()
        self.screen = screen

        self.image = pygame.Surface((ai_settings.bullet_width, ai_settings.bullet_height))
        self.image.fill(ai_settings.bullet_color)
        self.rect = self.image.get_rect()

        self.rect.midtop = ship.rect.midtop
        self.y = float(self.rect.y)
        self.speed = ai_settings.bullet_speed

    def update(self):
        self.y -= self.speed
        self.rect.y = self.y
