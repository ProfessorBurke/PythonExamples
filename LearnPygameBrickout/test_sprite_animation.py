"""Test a sprite animation."""

import random

# Import and initialize pygame.
import pygame
pygame.init()

# Define constants and annotate variables
WINDOW_SIZE: int = 480
NUM_SPRITES: int = 4
SPRITE_WIDTH: int = 32
SPRITE_HEIGHT: int = 32
screen: pygame.Surface
sprite_sheet: pygame.Surface
background: pygame.Surface
offset_w: float
offset_h: float
user_quit: bool
event: pygame.event.Event
sheet_x: int = 0
sheet_y: int = 0
sprite_dy: int = 5
sprite_width: int = 32
sprite_height: int = 32
animation_count: int = 0
x: int = WINDOW_SIZE // 2 - SPRITE_WIDTH // 2
y: int = 0
clock: pygame.time.Clock = pygame.time.Clock()

# Create a pygame window.
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Sprite animation test")

# Create the background and color it blue.
background = pygame.Surface((WINDOW_SIZE, WINDOW_SIZE))
background.fill((185, 208, 215))

# Load the sprite sheet image.
sprite_sheet = pygame.image.load("animales3.png")

# Draw a star for each click.
user_quit = False
while not user_quit:
    clock.tick(30)
    for event in pygame.event.get():
        # Process a quit choice.
        if event.type == pygame.QUIT:
            user_quit = True

    # Animate the sprite.
    animation_count += 1
    #y += sprite_dy
    y = (y + sprite_dy) % (WINDOW_SIZE + SPRITE_HEIGHT)
    if animation_count == 10:
        animation_count = 0
        sheet_x = (sheet_x + SPRITE_WIDTH) % (SPRITE_WIDTH * NUM_SPRITES)
        print("sheet_x after calculation,", sheet_x)
    screen.blit(background, (0, 0))
    screen.blit(sprite_sheet, (x, y), area=(sheet_x, sheet_y,
                                            SPRITE_WIDTH, SPRITE_HEIGHT))
    
  
    # Show the drawing.
    pygame.display.flip()

pygame.quit()
            
