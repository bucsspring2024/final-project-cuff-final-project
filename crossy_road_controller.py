import pygame
import sys
import time
import random
from player_controller import PlayerController
from enemy import Enemy

class CrossyRoadController:
    def __init__(self):
        pygame.init()
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Crossy Road")
        self.clock = pygame.time.Clock()
        self.player_size = 50
        self.player_speed = 5
        self.enemy_size = 50
        self.enemy_speed = 3
        self.enemies = []
        self.player_controller = PlayerController(self.screen_width, self.screen_height, self.player_size,
                                                  self.player_speed)
        self.running = False
        self.game_over = False
        self.best_time = None
        self.start_time = 0

    def load_best_time(self):
        try:
            with open("besttime.txt", "r") as file:
                return float(file.read())
        except FileNotFoundError:
            return None

    def save_best_time(self):
        with open("besttime.txt", "w") as file:
            if self.best_time is not None:
                file.write(str(self.best_time))
            else:
                file.write("N/A")

    def generate_enemy(self):
        initial_y = random.randint(0, self.screen_height - self.enemy_size)
        direction = random.choice(["LEFT", "RIGHT"])
        enemy = Enemy(self.screen_width, self.screen_height, self.enemy_size, self.enemy_speed, direction, initial_y)
        self.enemies.append(enemy)

    def handle_keyboard_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.player_controller.move_up()
                elif event.key == pygame.K_DOWN:
                    self.player_controller.move_down()
                elif event.key == pygame.K_LEFT:
                    self.player_controller.move_left()
                elif event.key == pygame.K_RIGHT:
                    self.player_controller.move_right()

    def handle_mouse_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not self.running and not self.game_over:
                    if 300 <= event.pos[0] <= 500 and 400 <= event.pos[1] <= 450:
                        self.start_game()
                elif self.game_over:
                    if 300 <= event.pos[0] <= 500 and 400 <= event.pos[1] <= 450:
                        self.start_game()

    def start_game(self):
        self.running = True
        self.game_over = False
        self.enemies.clear()
        self.player_controller.player.topleft = self.player_controller.initial_player_position
        self.player_controller.score = 0
        self.start_time = time.time()

    def move_enemies(self):
        for enemy in self.enemies:
            enemy.move()

    def check_collisions(self):
        for enemy in self.enemies:
            if self.player_controller.player.colliderect(enemy.rect):
                self.game_over = True
                self.running = False

    def check_win_condition(self):
        if self.player_controller.player.top <= 0:
            self.running = False
            self.game_over = True
            time_taken = time.time() - self.start_time
            if self.best_time is None or time_taken < self.best_time:
                self.best_time = time_taken
                self.save_best_time()

    def draw_best_time(self):
        font = pygame.font.Font(None, 24)
        if self.best_time is None:
            best_time_text = font.render("Best Time: N/A", True, pygame.Color("black"))
        else:
            best_time_text = font.render("Best Time: " + "{:.2f}".format(self.best_time) + " seconds", True,
                                         pygame.Color("black"))
        self.screen.blit(best_time_text, (10, 30))

    def draw_start_screen(self):
        self.screen.fill((255, 255, 255))
        font = pygame.font.Font(None, 36)
        main_menu_text = font.render("Main Menu", True, pygame.Color("blue"))
        self.screen.blit(main_menu_text, (330, 100))
        adaptation_text = font.render("Crossy Road Adaptation: By Pat Cuff", True, pygame.Color("blue"))
        self.screen.blit(adaptation_text, (180, 150))
        start_button = pygame.Rect(300, 400, 200, 50)
        pygame.draw.rect(self.screen, pygame.Color("green"), start_button)
        start_text = font.render("Start", True, pygame.Color("black"))
        self.screen.blit(start_text, (370, 410))

    def draw_game_over_screen(self):
        self.screen.fill((255, 255, 255))
        font = pygame.font.Font(None, 36)
        game_over_text = font.render("Game Over", True, pygame.Color("red"))
        self.screen.blit(game_over_text, (340, 200))
        final_score_text = font.render("Best Time: " + ("N/A" if self.best_time is None else "{:.2f}".format(self.best_time)) + " seconds", True,
                                       pygame.Color("black"))
        self.screen.blit(final_score_text, (300, 250))
        play_again_button = pygame.Rect(300, 400, 200, 50)
        pygame.draw.rect(self.screen, pygame.Color("green"), play_again_button)
        play_again_text = font.render("Play Again", True, pygame.Color("black"))
        self.screen.blit(play_again_text, (340, 410))

    def draw_win_screen(self):
        self.screen.fill((255, 255, 255))
        font = pygame.font.Font(None, 36)
        win_text = font.render("You Win!", True, pygame.Color("green"))
        self.screen.blit(win_text, (340, 200))
        final_score_text = font.render("Best Time: " + ("N/A" if self.best_time is None else "{:.2f}".format(self.best_time)) + " seconds", True,
                                       pygame.Color("black"))
        self.screen.blit(final_score_text, (300, 250))
        play_again_button = pygame.Rect(300, 400, 200, 50)
        pygame.draw.rect(self.screen, pygame.Color("green"), play_again_button)
        play_again_text = font.render("Play Again", True, pygame.Color("black"))
        self.screen.blit(play_again_text, (340, 410))

    def run_game(self):
        while True:
            if self.running:
                self.handle_keyboard_events()
            else:
                self.handle_mouse_events()

            if self.running:
                if random.random() < 0.02:
                    self.generate_enemy()
                self.move_enemies()
                self.check_collisions()
                self.check_win_condition()  # Check if the player reached the highest point
                self.screen.fill((255, 255, 255))  # Clear screen before drawing
                self.draw_best_time()
                pygame.draw.rect(self.screen, pygame.Color("blue"), self.player_controller.player)
                for enemy in self.enemies:
                    pygame.draw.rect(self.screen, pygame.Color("red"), enemy.rect)
            else:
                if self.game_over:
                    if self.player_controller.player.top <= 0:  # Check if the player won
                        self.draw_win_screen()  # Draw the win screen
                    else:
                        self.draw_game_over_screen()  # Draw the game over screen
                else:
                    self.draw_start_screen()

            pygame.display.update()
            self.clock.tick(60)