import pygame


class Scoreboard:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        self.ships = pygame.sprite.Group()
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        rounded_score = int(round(self.game.stats.score, -1))
        score_str = f"{rounded_score:,}"
        self.score_image = self.font.render(score_str, True, self.text_color, None)

        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        rounded_high_score = int(round(self.game.stats.high_score, -1))
        high_score_str = f"High Score: {rounded_high_score:,}"
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, None)

        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = 20

    def prep_level(self):
        level_str = f"Level {self.game.stats.level}"
        self.level_image = self.font.render(level_str, True, self.text_color, None)

        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.screen_rect.right - 20
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        self.ships.empty()
        for ship_number in range(self.game.stats.ships_left):
            ship_image = pygame.image.load('images/ship.bmp')
            ship_image = pygame.transform.scale(ship_image, (20, 15))
            ship_rect = ship_image.get_rect()
            ship_rect.x = 10 + ship_number * 30
            ship_rect.y = 10
            
            ship_sprite = pygame.sprite.Sprite()
            ship_sprite.image = ship_image
            ship_sprite.rect = ship_rect
            self.ships.add(ship_sprite)

    def check_high_score(self):
        if self.game.stats.score > self.game.stats.high_score:
            self.game.stats.high_score = self.game.stats.score
            self.prep_high_score()

    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)
