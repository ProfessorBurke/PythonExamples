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

# Game setup
screen = pygame.display.set_mode((600, 800))
pygame.display.set_caption("Brickout 1.0")
clock = pygame.time.Clock()

# Make a background and a square.
background = pygame.Surface((600, 800))
square = pygame.Surface((50, 50))
square.fill((255, 255, 255))

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
    screen.blit(square, (x, y))
    x += 2 + random.randint(-3, 3)
    y += 2 + random.randint(-3, 3)
    screen.blit(square, (x, y))

    pygame.display.flip()

pygame.quit()
