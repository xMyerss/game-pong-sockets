import pygame
from network import Network
from player import Paddle, Ball
import sys

width = 500
height = 500
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pong")
# isExit = None


def redrawWindow(win, player1, player2, ball):
    win.fill((0, 0, 0))
    player1.draw(win)
    player2.draw(win)
    ball.draw(win)
    pygame.display.update()


def main():
    run = True
    n = Network()
    player1, player2, ball = n.getP()
    clock = pygame.time.Clock()

    ball_moving = False  # La pelota no se mueve al principio

    while run:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Enviar la dirección de movimiento de la paleta al servidor
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            direction = "up"
            ball_moving = True  # La pelota comienza a moverse cuando el jugador mueve la paleta
        elif keys[pygame.K_DOWN]:
            direction = "down"
            ball_moving = True  # La pelota comienza a moverse cuando el jugador mueve la paleta
        else:
            direction = None

        player1, player2, ball = n.send((player1, player2, ball, direction, ball_moving))

        redrawWindow(win, player1, player2, ball)

        # if(isExit):
        #     pygame.quit()
        #     sys.exit()
        #     break

    


if __name__ == "__main__":
    main()
