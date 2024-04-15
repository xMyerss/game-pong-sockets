import pygame

import pygame

class Paddle:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = pygame.Rect(x, y, width, height)
        self.vel = 10

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)

    def move(self, direction):
        if direction == "up":
            self.rect.y -= self.vel
        elif direction == "down":
            self.rect.y += self.vel

        # Limitar las paletas dentro de los límites de la ventana
        self.rect.y = max(0, min(self.rect.y, 500 - self.height))  # 500 es la altura de la ventana

class Ball:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.rect = pygame.Rect(x - radius, y - radius, 2 * radius, 2 * radius)
        self.velX = 2  # Velocidad horizontal de la pelota
        self.velY = 2  # Velocidad vertical de la pelota

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.velX
        self.y += self.velY

        # Verificar si la pelota golpea los límites de la ventana
        if self.y - self.radius <= 0 or self.y + self.radius >= 500:
            self.velY = -self.velY

        self.rect.x = self.x - self.radius
        self.rect.y = self.y - self.radius