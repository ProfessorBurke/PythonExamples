# Note: this program loads a jpeg that I haven't included.  Either create
# the background as a plain Surface, or load in your own image.

# Pygame setup
import pygame
pygame.init()
pygame.display.init()

# Import libraries
import random

# Annotate variables
screen: pygame.Surface
square: pygame.Surface
background: pygame.Surface
clock: pygame.time.Clock
e: pygame.event.Event
running: bool
x: int = 98
y: int = 98
dx: int = 5
dy: int = 5

# Game setup
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Brickout 2.0")
clock = pygame.time.Clock()

# Make a background and a square.
background = pygame.image.load("pool_leaves.jpg")
background = background.convert()
square = pygame.Surface((50, 50))
square.set_colorkey((0, 0, 0))
pygame.draw.circle(square, (255, 255, 255),
                   (square.get_width() // 2, square.get_height() // 2),
                   square.get_width() // 2)

# Game loop
running = True
while running:
    clock.tick(30)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        elif e.type == pygame.MOUSEBUTTONUP:
            x, y = e.pos

    screen.blit(background, (0, 0))
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
        dy *= -1
    screen.blit(square, (x, y))

    pygame.display.flip()

pygame.quit()
