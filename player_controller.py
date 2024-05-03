import pygame

class PlayerController:
    def __init__(self, screen_width, screen_height, player_size, player_speed):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.player_size = player_size
        self.player_speed = player_speed
        self.initial_player_position = (self.screen_width // 2 - self.player_size // 2,
                                        self.screen_height - self.player_size - 10)
        self.player = pygame.Rect(*self.initial_player_position, self.player_size, self.player_size)
        self.score = 0

    def move_up(self):
        if self.player.top > 0:
            self.player.y -= self.player_speed
            self.score += 1

    def move_down(self):
        if self.player.bottom < self.screen_height:
            self.player.y += self.player_speed

    def move_left(self):
        if self.player.left > 0:
            self.player.x -= self.player_speed

    def move_right(self):
        if self.player.right < self.screen_width:
            self.player.x += self.player_speed