import pygame
import random
import sys
from config import HEIGHT, WIDTH, FPS, WHITE, BLACK
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

        # Configuración de puntuación y vidas
        self.score = 0
        self.collision_count = 0
        self.max_collisions = 3
        self.heart_image = pygame.image.load("assets/heart.png").convert_alpha()
        self.heart_image = pygame.transform.scale(self.heart_image, (32, 32))  

    def run(self):
        running = True
        while running:
            self.clock.tick(FPS)
            self.screen.fill(WHITE)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.USEREVENT and not self.player.alive:
                    running = False  

            self.update()
            self.draw()

            pygame.display.flip()

        pygame.quit()

    def update(self):
        if self.player.alive:
           
            self.player.update()
            self.background_scroll -= self.background_speed
            self.score += 0.1  # Incremento de puntuación continuo

            
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
                    if self.player.alive:
                        self.collision_count += 1
                        self.obstacles.remove(obstacle)
                        if self.collision_count >= self.max_collisions:
                            self.player.die()  # Activa la animación de muerte
                            pygame.time.set_timer(pygame.USEREVENT, 1500)  # Temporizador para cierre

    def draw(self):
    
        self.screen.blit(self.background_image, (self.background_scroll, 0))
        self.screen.blit(
            self.background_image,
            (self.background_scroll + self.background_image.get_width(), 0),
        )

        self.player.draw(self.screen)

        for obstacle in self.obstacles:
            obstacle.draw(self.screen)

        # Mostrar puntuación
        self.draw_text(f"{int(self.score)}", font, BLACK, self.screen, WIDTH - 60, 30)

        # Dibujar corazones para las vidas
        for i in range(self.max_collisions - self.collision_count):
            x = 20 + i * 40
            y = 20
            self.screen.blit(self.heart_image, (x, y))

    def draw_text(self, text, font, color, surface, x, y):
        textobj = font.render(text, True, color)
        textrect = textobj.get_rect()
        textrect.center = (x, y)
        surface.blit(textobj, textrect)
