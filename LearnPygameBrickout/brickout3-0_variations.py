
# Pygame setup
import pygame
pygame.init()
pygame.display.init()

# Import libraries
import random

# Annotate variables
PADDLE_WIDTH: int = 100
PADDLE_HEIGHT: int = 20
PADDLE_MAX: int = 200
screen: pygame.Surface
square: pygame.Surface
paddle: pygame.Surface
sparkles: pygame.Surface
background: pygame.Surface
clock: pygame.time.Clock
e: pygame.event.Event
running: bool
x: int = 98
y: int = 98
dx: int = 5
dy: int = 5
paddle_x: int
paddle_y: int
paddle_dx: int = 10
keys: pygame.key.ScancodeWrapper # like list[bool]
i: int

# Game setup
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Brickout 3.0")
clock = pygame.time.Clock()

# Asset setup.
background = pygame.Surface((600, 400))
square = pygame.Surface((50, 50))
square.set_colorkey((0, 0, 0))
pygame.draw.circle(square, (255, 255, 255),
                   (square.get_width() // 2, square.get_height() // 2),
                   square.get_width() // 2)
paddle = pygame.Surface((PADDLE_WIDTH, PADDLE_HEIGHT))
paddle.fill((0, 0, 255))
paddle_x = screen.get_width() // 2 - paddle.get_width() // 2
paddle_y = screen.get_height() - paddle.get_height() * 2
sparkles = pygame.Surface((paddle.get_width(), paddle.get_height()))
sparkles.set_colorkey((0, 0, 0))

# Game loop
running = True
while running:
    clock.tick(30)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        elif e.type == pygame.MOUSEBUTTONUP:
            x, y = e.pos
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_UP:
                background.fill((random.randint(0, 255),
                                 random.randint(0, 255),
                                 random.randint(0, 255)))
            elif e.key == pygame.K_DOWN:
                pygame.draw.circle(square, (random.randint(0, 255),
                                            random.randint(0, 255),
                                            random.randint(0, 255)),
                                   (square.get_width() // 2, square.get_height() // 2),
                                   square.get_width() // 2)                

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        paddle_x -= paddle_dx
        if paddle_x < 0:
            paddle_x = 0
    if keys[pygame.K_RIGHT]:
        paddle_x += paddle_dx
        if paddle_x + paddle.get_width() >= screen.get_width():
            paddle_x = screen.get_width() - paddle.get_width()
    if keys[pygame.K_SPACE]:
        paddle_width: int = min(paddle.get_width() + 1, PADDLE_MAX)
        paddle = pygame.Surface((paddle_width, paddle.get_height()))
        paddle.fill((0, 0, 255))
        #sparkles.fill((0, 0, 0))
##        for i in range(50):
##            pygame.draw.circle(sparkles, (random.randint(0, 255),
##                                          random.randint(0, 255),
##                                          random.randint(0, 255)),
##                               (random.randint(0, sparkles.get_width()-1),
##                                random.randint(0, sparkles.get_height()-1)),
##                               random.randint(1, sparkles.get_height()//6))
        
    else:
##        sparkles.fill((0, 0, 0))
        paddle = pygame.Surface((PADDLE_WIDTH, PADDLE_HEIGHT))
        paddle.fill((0, 0, 255))
    
    x += dx
    y += dy

    # Boundary checking
    if x <= 0:
        x = 0
        dx *= -1
    elif x + square.get_width() >= screen.get_width():
        x = screen.get_width() - square.get_width()
        dx *= -1
    if y <= 0:
        y = 0
        dy *= -1
    elif y + square.get_height() >= screen.get_height():
        y = screen.get_height() - square.get_height()
        dy = 0
        dx = 0

    # Boundary checking with paddle
    if (dy > 0 and (y + square.get_height() >= paddle_y) and
        (x + square.get_width() >= paddle_x and x <= paddle_x + paddle.get_width())):
        y = paddle_y - square.get_height()
        dy *= -1
    
    screen.blit(background, (0, 0))
    screen.blit(square, (x, y))
    screen.blit(paddle, (paddle_x, paddle_y))
    screen.blit(sparkles, (paddle_x, paddle_y))

    pygame.display.flip()

pygame.quit()
