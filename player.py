import pygame
from utils import load_spritesheet
from config import HEIGHT

class Player:
    def __init__(self, x, y):
        # Posición y características físicas
        self.x = x
        self.y = y
        self.width = 32
        self.height = 32
        self.speed = 5
        self.jump_power = -20
        self.gravity = 1
        self.velocity_y = 0
        self.on_ground = True
        self.alive = True  # Variable para saber si el jugador está "vivo" o "muerto"

        # Cargar animaciones
        self.run_frames = load_spritesheet("assets/player/run.png", self.width, self.height)
        self.jump_frames = load_spritesheet("assets/player/jump.png", self.width, self.height)
        self.death_frames = load_spritesheet("assets/player/death.png", self.width, self.height)

        # Índice y velocidad de animación
        self.frame_index = 0
        self.animation_speed = 0.3

    def update(self):
        if self.alive:
            # Movimiento y física del jugador
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE] and self.on_ground:
                self.velocity_y = self.jump_power
                self.on_ground = False

            # Actualización de posición vertical con gravedad
            self.velocity_y += self.gravity
            self.y += self.velocity_y

            # Limita el jugador al suelo
            if self.y >= HEIGHT - self.height:
                self.y = HEIGHT - self.height
                self.velocity_y = 0
                self.on_ground = True

    def draw(self, surface):
        # Determinar qué animación mostrar
        if not self.alive:
            # Animación de muerte
            self.frame_index += self.animation_speed
            if self.frame_index >= len(self.death_frames):
                self.frame_index = len(self.death_frames) - 1  # Mantiene el último frame
            frame = self.death_frames[int(self.frame_index)]
        elif self.on_ground:
            # Animación de correr
            self.frame_index += self.animation_speed
            if self.frame_index >= len(self.run_frames):
                self.frame_index = 0
            frame = self.run_frames[int(self.frame_index)]
        else:
            # Animación de salto
            frame = self.jump_frames[0]

        # Dibujar el frame correspondiente
        surface.blit(frame, (self.x, self.y))

    def die(self):
        """Activa la animación de muerte del jugador."""
        self.alive = False
        self.frame_index = 0  # Reiniciar la animación de muerte

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
