import pygame
import random

class Enemy:
    def __init__(self, screen_width, screen_height, size, speed, direction, initial_y):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.size = size
        self.speed = speed
        self.direction = direction
        self.initial_y = initial_y
        self.rect = self.initialize_position()

    def initialize_position(self):
        if self.direction == "LEFT":
            x = self.screen_width
        else:
            x = -self.size
        y = self.initial_y
        return pygame.Rect(x, y, self.size, self.size)

    def move(self):
        if self.direction == "LEFT":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed