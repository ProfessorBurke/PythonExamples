"""
    Illustration of BLEND_RGBA_MAX mode.
    Requires background.jpg in the same folder.
"""

import pygame
import math

def create_spotlight(size: tuple, color: tuple, radius: int, position: tuple):
    """
    Create a radial gradient spotlight surface.
    - size: (width, height) of the surface
    - color: (R, G, B) color of the spotlight
    - radius: radius in pixels of the bright center
    - position: (x, y) center position of the spotlight on the surface
    """
    # Annotate locals.
    w: int
    h: int
    surf: pygame.Surface
    cx: int
    cy: int
    y: int
    dx: int
    dy: int
    dist: float

    # Create the gradient.
    w, h = size
    surf = pygame.Surface(size, pygame.SRCALPHA)
    cx, cy = position
    for y in range(h):
        for x in range(w):
            dx = x - cx
            dy = y - cy
            dist = math.hypot(dx, dy)
            if dist <= radius:
                # Alpha falls off from center to edge
                alpha = max(0, int(255 * (1 - dist / radius)))
                surf.set_at((x, y), (*color, alpha))
    return surf

# Annotate and initialize variables.
SIZE: int = 512
running: bool = True
event: pygame.event.Event
screen: pygame.Surface
background: pygame.Surface
spotlight1: pygame.Surface
spotlight2: pygame.Surface
glow_composite: pygame.Surface

# Initialize pygame and create the screen.
pygame.init()
screen = pygame.display.set_mode((SIZE, SIZE))
pygame.display.set_caption("BLEND_RGBA_MAX: Dual Spotlights")

# Load the background.
background = pygame.image.load("background.jpg").convert()

# Create two colored spotlights.
spotlight1 = create_spotlight((SIZE, SIZE), color=(255, 200, 50), radius=128, position=(192, 255))
spotlight2 = create_spotlight((SIZE, SIZE), color=(50, 200, 255), radius=100, position=(320, 170))

# Composite them with BLEND_RGBA_MAX onto a transparent surface.
glow_composite = pygame.Surface((SIZE, SIZE), pygame.SRCALPHA)
glow_composite.blit(spotlight1, (0, 0), special_flags=pygame.BLEND_RGBA_MAX)
glow_composite.blit(spotlight2, (0, 0), special_flags=pygame.BLEND_RGBA_MAX)
pygame.image.save(glow_composite, "glow_composite.png")

# Draw background, then default-blit the composite glow.
screen.blit(background, (0, 0))
screen.blit(glow_composite, (0, 0))  
pygame.display.flip()

# Wait for the user to quit.
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()

