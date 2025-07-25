"""
    Compare min and max blending modes.
    Requires background.jpg in the same folder.
"""
import pygame

# Annotate and initialize variables.
# Drawing surfaces.
screen: pygame.Surface
image: pygame.Surface
image_A: pygame.Surface
image_B: pygame.Surface
# Text display variables.
font: pygame.font.SysFont
label_left: pygame.Surface
label_right: pygame.Surface
# Window variables.
SIZE: int = 512
WIDTH: int = SIZE
HEIGHT: int = SIZE + 50
# Slider variables.
right_rect: pygame.Rect
slider_x: int = SIZE // 2
dragging: bool = False
# Event variables.
running: bool = True
event: pygame.event.Event
mx: int
my: int

# Initialize pygame and set up the window.
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Blending Mode Comparison Slider")

# Load the city image and create the medium light grey overlay.
image = pygame.image.load("background.jpg").convert_alpha()  
overlay = pygame.Surface((SIZE, SIZE), pygame.SRCALPHA)
overlay.fill((150, 150, 150))
pygame.image.save(overlay, "grey150.jpg")

# Image A: BLEND_RGB_MIN
image_A = image.copy()
image_A.blit(overlay, (0, 0), special_flags=pygame.BLEND_RGB_MIN)

# Image B: BLEND_RGB_MAX
image_B = image.copy()
image_B.blit(overlay, (0, 0), special_flags=pygame.BLEND_RGB_MAX)
pygame.image.save(image_B, "blend_max.jpg")

# Allow the user to move the slider until they choose to quit.
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            if HEIGHT - 40 < my and my < HEIGHT - 10:
                dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False
        elif event.type == pygame.MOUSEMOTION and dragging:
            mx, _ = event.pos
            slider_x = max(0, min(SIZE, mx))

    # Draw background white.
    screen.fill((255, 255, 255))

    # Draw images with slider split
    screen.blit(image_A, (0, 0))
    right_rect = pygame.Rect(slider_x, 0, SIZE - slider_x, SIZE)
    screen.blit(image_B, (slider_x, 0), right_rect)

    # Draw slider track
    pygame.draw.rect(screen, (200, 200, 200), (0, HEIGHT - 25, SIZE, 5))
    # Draw slider handle
    pygame.draw.rect(screen, (0, 0, 0), (slider_x - 5, HEIGHT - 40, 10, 30))

    # Draw the labels.
    font = pygame.font.SysFont(None, 24)
    label_left = font.render("BLEND_RGB_MIN", True, (0, 0, 0))
    label_right = font.render("BLEND_RGB_MAX", True, (0, 0, 0))
    screen.blit(label_left, (10, SIZE + 5))
    screen.blit(label_right, (SIZE - label_right.get_width() - 10, SIZE + 5))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
