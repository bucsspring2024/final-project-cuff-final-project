import random
import pygame
import sys



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
        self.player_controller = PlayerController(self.screen_width, self.screen_height, self.player_size, self.player_speed)
        self.running = False
        self.game_over = False

    def generate_enemy(self):
        lane = random.randint(1, 3)  # Randomly select a lane (1, 2, or 3)
        direction = random.choice(["LEFT", "RIGHT"])
        if direction == "LEFT":
            enemy_x = self.screen_width
        else:
            enemy_x = -self.enemy_size
        enemy_y = (self.screen_height // 3) * lane - self.enemy_size
        self.enemies.append((enemy_x, enemy_y, direction))

    def handle_events(self):
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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not self.running and not self.game_over:
                    if 300 <= event.pos[0] <= 500 and 400 <= event.pos[1] <= 450:
                        self.running = True
                        self.game_over = False
                        self.enemies.clear()
                        # Reset player position to initial starting point and score to 0
                        self.player_controller.player.topleft = self.player_controller.initial_player_position
                        self.player_controller.score = 0
                elif self.game_over:
                    if 300 <= event.pos[0] <= 500 and 400 <= event.pos[1] <= 450:
                        self.running = True
                        self.game_over = False
                        self.enemies.clear()
                        # Reset player position to initial starting point and score to 0
                        self.player_controller.player.topleft = self.player_controller.initial_player_position
                        self.player_controller.score = 0

    def move_enemies(self):
        for i, (enemy_x, enemy_y, direction) in enumerate(self.enemies):
            if direction == "LEFT":
                self.enemies[i] = (enemy_x - self.enemy_speed, enemy_y, direction)
            else:
                self.enemies[i] = (enemy_x + self.enemy_speed, enemy_y, direction)

    def run_game(self):
        while True:
            self.handle_events()

            if self.running:
                # Generate enemies
                if random.random() < 0.02:  # Adjust enemy generation frequency
                    self.generate_enemy()

                # Move enemies
                self.move_enemies()

                # Check collisions
                for enemy_x, enemy_y, _ in self.enemies:
                    if self.player_controller.player.colliderect(pygame.Rect(enemy_x, enemy_y, self.enemy_size, self.enemy_size)):
                        print("Game Over")  # Replace this with your game over logic
                        self.running = False
                        self.game_over = True

                # Draw everything
                self.screen.fill((255, 255, 255))  # Fill screen with white color
                pygame.draw.rect(self.screen, pygame.Color("blue"), self.player_controller.player)  # Draw player
                for enemy_x, enemy_y, _ in self.enemies:
                    pygame.draw.rect(self.screen, pygame.Color("red"), (enemy_x, enemy_y, self.enemy_size, self.enemy_size))  # Draw enemies

            else:
                # Draw start button and game over text
                self.screen.fill((255, 255, 255))
                if self.game_over:
                    font = pygame.font.Font(None, 36)
                    game_over_text = font.render("Game Over", True, pygame.Color("red"))
                    self.screen.blit(game_over_text, (340, 200))
                    # Display final score
                    final_score_text = font.render("Final Score: " + str(self.player_controller.score), True, pygame.Color("black"))
                    self.screen.blit(final_score_text, (320, 250))
                    play_again_button = pygame.Rect(300, 400, 200, 50)
                    pygame.draw.rect(self.screen, pygame.Color("green"), play_again_button)
                    play_again_text = font.render("Play Again", True, pygame.Color("black"))
                    self.screen.blit(play_again_text, (340, 410))
                else:
                    start_button = pygame.Rect(300, 400, 200, 50)
                    pygame.draw.rect(self.screen, pygame.Color("green"), start_button)
                    font = pygame.font.Font(None, 36)
                    start_text = font.render("Start", True, pygame.Color("black"))
                    self.screen.blit(start_text, (370, 410))

            pygame.display.update()
            self.clock.tick(60)

if __name__ == "__main__":
    game = CrossyRoadController()
    game.run_game()
    
   