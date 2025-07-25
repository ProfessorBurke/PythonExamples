"""
    Demonstrate an alpha effect with BLEND_RGBA_MIN.
    Requires background.jpg in the same folder.
"""

import pygame
import math

# Annotate and initialize variables.
screen: pygame.Surface
background: pygame.Surface
shadow: pygame.Surface
shadowed_scene: pygame.Surface
size: int = 512
x: int
y: int
dx: int
dy: int
dist: float
alpha: int
running: bool = True
event: pygame.event.Event

# Initialize pygame and load the background and create the
# dimming overlay.
pygame.init()
screen = pygame.display.set_mode((512, 512))
background = pygame.image.load("background.jpg").convert_alpha()
shadow = pygame.Surface((size, size), pygame.SRCALPHA)

for y in range(size):
    for x in range(size):
        dx = x - size // 2
        dy = y - size // 2
        dist = math.hypot(dx, dy)
        alpha = max(0, min(255, int(255 - (dist / (size // 2)) * 255)))
        shadow.set_at((x, y), (255, 255, 255, alpha))

# Apply BLEND_RGBA_MIN to create a dimming effect with transparency preserved.
shadowed_scene = background.copy()
shadowed_scene.blit(shadow, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
screen.blit(shadowed_scene, (0, 0))
pygame.display.flip()

# Wait for the user to quit.
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()

