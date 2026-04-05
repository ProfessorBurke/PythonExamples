# Pygame setup
import pygame
pygame.init()
pygame.display.init()

# Import libraries
import random

# Annotate variables
screen: pygame.Surface
square: pygame.Surface
square2: pygame.Surface
background: pygame.Surface
clock: pygame.time.Clock
e: pygame.event.Event
running: bool
x: int = 98
y: int = 98
square2_x: int = 300
square2_y: int = 300

# Game setup
screen = pygame.display.set_mode((600, 800))
pygame.display.set_caption("Brickout 1.0")
clock = pygame.time.Clock()

# Make a background and a square.
background = pygame.Surface((600, 800))
background.fill((random.randint(0, 255),
                 random.randint(0, 255),
                 random.randint(0, 255)))
square = pygame.Surface((50, 50))
square.fill((random.randint(0,255),
             random.randint(0,255),
             random.randint(0,255)))
color_change_timer: int = 0
square2 = pygame.Surface((100, 100))
square2.fill((random.randint(0,255),
             random.randint(0,255),
             random.randint(0,255)))
                
# Game loop
running = True
while running:
    clock.tick(30)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        elif e.type == pygame.MOUSEBUTTONUP:
            x, y = e.pos
            square2_x = 600-x
            square2_y = 800-y

    color_change_timer += 1
    if color_change_timer == 90:
        color_change_timer = 0
        background.fill((random.randint(0, 255),
                         random.randint(0, 255),
                         random.randint(0, 255)))
        square.fill((random.randint(0,255), random.randint(0,255), random.randint(0,255)))
        square2.fill((random.randint(0,255), random.randint(0,255), random.randint(0,255)))
        square2_x = random.randint(0, 500)
        square2_y = random.randint(0, 300)

    screen.blit(background, (0, 0))
    screen.blit(square, (x, y))
    screen.blit(square2, (square2_x, square2_y))
    x += 2 + random.randint(-3, 3)
    y += 2 + random.randint(-3, 3)
    square2_x -= 5
    square2_y -= 5
    screen.blit(square, (x, y))

    pygame.display.flip()

pygame.quit()
