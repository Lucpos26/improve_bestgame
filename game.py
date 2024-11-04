import pygame
import random
import sys
from config import HEIGHT, FPS, WHITE, WIDTH, BLACK
from player import Player
from obstacle import Obstacle

pygame.font.init()
font = pygame.font.SysFont(None, 48)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Speedrunner")

        self.clock = pygame.time.Clock()
        self.player = Player(100, HEIGHT - 50)
        self.obstacles = []
        self.background_image = pygame.image.load("assets/background.png").convert()
        self.background_scroll = 0
        self.background_speed = 2
        self.collision_count = 0
        self.max_collisions = 3
        self.score = 0  # Iniciar la puntuación del juego
        self.lives = 3  # Iniciar las vidas que hay 

    def run(self):
        running = True
        while running:
            self.clock.tick(FPS)
            self.screen.fill(WHITE)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.update()
            self.draw()

            pygame.display.flip()

        pygame.quit()

    def update(self):
        self.player.update()

        # Incrementar la puntuación con el tiempo
        self.score += 1  # Incremento constante de la puntuación

        self.background_scroll -= self.background_speed
        if self.background_scroll <= -self.background_image.get_width():
            self.background_scroll = 0

        if random.randint(0, 100) < 1:
            obstacle_x = WIDTH
            obstacle_y = HEIGHT - 50
            self.obstacles.append(Obstacle(obstacle_x, obstacle_y))

        for obstacle in self.obstacles:
            obstacle.update()

        self.obstacles = [
            obstacle
            for obstacle in self.obstacles
            if obstacle.rect.x + obstacle.rect.width > 0
        ]

        player_rect = self.player.get_rect()
        for obstacle in self.obstacles:
            if player_rect.colliderect(obstacle.rect):
                self.collision_count += 1
                self.lives -= 1  # Restar una vida al momento colisionar con un obstáculo
                
                
                self.obstacles.remove(obstacle)

                # Comprobar si se han perdido todas las vidas
                if self.lives <= 0:
                    self.game_over()

    def draw(self):
        # .
        self.screen.blit(self.background_image, (self.background_scroll, 0))
        self.screen.blit(
            self.background_image,
            (self.background_scroll + self.background_image.get_width(), 0),
        )

        # ..
        self.player.draw(self.screen)
        
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)

        # Mostrar la puntuación en pantalla
        self.draw_text(
            f"Puntuación: {self.score}", font, BLACK, self.screen, WIDTH // 2, 30
        )
        
        self.draw_text(
            f"Colisiones: {self.collision_count}", font, BLACK, self.screen, 100, 30
        )

        # Mostrar el número de vidas restantes en pantalla
        self.draw_text(
            f"Vidas: {self.lives}", font, BLACK, self.screen, WIDTH - 100, 30
        )

    def draw_text(self, text, font, color, surface, x, y):
        textobj = font.render(text, True, color)
        textrect = textobj.get_rect()
        textrect.center = (x, y)
        surface.blit(textobj, textrect)

    def game_over(self):
        # Mostrar mensaje de fin del juego y la puntuación final
        final_score_text = f"¡Perdiste! Puntuación Final: {self.score}"
        
        # ...
        self.draw_text(final_score_text, font, BLACK, self.screen, WIDTH // 2, HEIGHT // 2)
        
        pygame.display.flip()
        pygame.time.wait(2000)
        pygame.quit()
        sys.exit() 

      

