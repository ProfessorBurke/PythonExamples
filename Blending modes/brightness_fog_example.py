"""
    Demonstrating a fog effect with BLEND_RGB_MAX.
    Requires background.jpg in the same folder.
"""
import pygame

# Annotate and initialize variables
# Drawing surfaces.
screen: pygame.Surface
background: pygame.Surface
fog_overlay: pygame.Surface
working: pygame.Surface
# Event handling.
running: bool = True
event: pygame.event.Event

# Initialize pygame and create the window.
pygame.init()
screen = pygame.display.set_mode((512, 512))
pygame.display.set_caption("Fog effect with BLEND_RGB_MAX")

# Load your background
background = pygame.image.load("background.jpg").convert()

# Create a fog overlay (gray with slight blue tint)
fog_overlay = pygame.Surface((512, 512))
fog_overlay.fill((150, 150, 170))

# Show the image with the effect.
working = pygame.Surface((background.get_size()))
working.blit(background, (0, 0))
working.blit(fog_overlay, (0, 0), special_flags=pygame.BLEND_RGB_MAX)
screen.blit(working, (0, 0))
pygame.display.flip()

# Wait for the user to quit.
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


pygame.quit()
