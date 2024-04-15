import socket
from _thread import *
from player import Paddle, Ball
import pickle
import sys

server = "10.10.0.37"  # Dirección IP del servidor
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clients = []

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

paddle1 = Paddle(50, 225, 10, 100, (255, 0, 0))  # Paleta izquierda
paddle2 = Paddle(440, 225, 10, 100, (0, 0, 255))  # Paleta derecha
ball = Ball(250, 250, 10, (255, 255, 255))  # Pelota inicial

def threaded_client(conn, player):
    global ball
    conn.send(pickle.dumps((paddle1, paddle2, ball)))
    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            direction = data[3]  # La dirección de movimiento de la paleta
            ball_moving = data[4]  # Si la pelota está en movimiento

            if player == 1:
                paddle1.move(direction)
            else:
                paddle2.move(direction)

            # Mover la pelota solo si ball_moving es True
            if ball_moving:
                ball.move()

            # Colisiones con las paletas
            if ball.rect.colliderect(paddle1.rect) or ball.rect.colliderect(paddle2.rect):
                ball.velX = -ball.velX
                
                # Ajustar la posición de la pelota para evitar que atraviese las paletas
                if ball.rect.colliderect(paddle1.rect):
                    if ball.velX < 0:  # Asegurarse de que la pelota se mueva hacia la derecha
                        ball.x = paddle1.rect.right + ball.radius + 1  # Ajustar la posición x
                elif ball.rect.colliderect(paddle2.rect):
                    if ball.velX > 0:  # Asegurarse de que la pelota se mueva hacia la izquierda
                        ball.x = paddle2.rect.left - ball.radius - 1  # Ajustar la posición x

            # Colisiones con los bordes superior e inferior
            if ball.y <= 0 or ball.y >= 500:
                ball.velY = -ball.velY
                
            if ball.x <= 0 or ball.x >= 500:
                ball = Ball(250, 250, 10, (255, 255, 255))
                # [conn.close() for c in clients]


            # Actualizar la posición de la pelota en todos los clientes
            reply = (paddle1, paddle2, ball)
            conn.sendall(pickle.dumps(reply))
        except:
            break

    print("Lost connection")
    conn.close()

currentPlayer = 0
while True:
    conn, addr = s.accept()
    clients.append(conn)
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1
