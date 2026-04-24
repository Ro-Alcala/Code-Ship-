import pygame


class Alien(pygame.sprite.Sprite):
    def __init__(self, ai_settings, screen):
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        self.image = pygame.Surface((40, 30))
        self.image.fill((0, 255, 0))  # Green rectangle
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.y = 10

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.speed = ai_settings.alien_speed

    def update(self, direction):
        self.x += self.speed * direction
        self.rect.x = self.x

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
        return False

    def draw_alien(self):
        self.screen.blit(self.image, self.rect)
