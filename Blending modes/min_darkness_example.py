"""
    Demonstrating a night effect with BLEND_RGB_MIN.
    Requires background.jpg in the same folder.
    Requires lighter_filter.png in the same folder.
"""
import pygame

# Annotate and initialize variables
# Drawing surfaces.
screen: pygame.Surface
background: pygame.Surface
dark_overlay: pygame.Surface
working: pygame.Surface
# Event handling.
running: bool = True
event: pygame.event.Event

# Initialize pygame and create the window.
pygame.init()
screen = pygame.display.set_mode((512, 512))
pygame.display.set_caption("Night effect with BLEND_RGB_MIN")

# Load the city image.
background = pygame.image.load("background.jpg").convert_alpha()

# Create a general darkness overlay with a moon light source.
dark_overlay = pygame.image.load("lighter_filter.png").convert_alpha()

# Show the image with the effect.
working = pygame.Surface((background.get_size()))
working.blit(background, (0, 0))
working.blit(dark_overlay, (0, 0), special_flags=pygame.BLEND_RGB_MIN)
pygame.image.save(working, "min_quiz.jpg")
screen.blit(working, (0, 0))
pygame.display.flip()

# Wait for the user to quit.
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
