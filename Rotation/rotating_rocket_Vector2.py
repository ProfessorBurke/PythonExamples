"""Demonstration of the Vector2 class for rotation motion."""

# Imports and initialize pygame.
import random
import math
import pygame
pygame.init()

def make_window(size: int, caption: str) -> pygame.Surface:
    """Create and return a pygame window."""
    screen: pygame.Surface
    screen = pygame.display.set_mode((size, size))
    pygame.display.set_caption(caption)
    return screen

def in_bounds(image_center: tuple, click_loc: tuple,
              image: pygame.Surface) -> bool:
    """Return True if the click is within the bounds of the image."""
    half_width: float = image.get_width()/2
    half_height: float = image.get_height()/2
    return (image_center[0] - half_width <= click_loc[0]
            and image_center[1] - half_height <= click_loc[1]
            and image_center[0] + half_width >= click_loc[0]
            and image_center[1] + half_height >= click_loc[1])

def draw_from_center(center: tuple,
                     image: pygame.Surface,
                     screen: pygame.Surface) -> None:
    """Blit the image to the screen given the image and its center point."""
    screen.blit(image, (center[0] - image.get_width() / 2,
                        center[1] - image.get_height() / 2))

def main() -> None:
    """Allow the user to rotate a rocket by clicking in the rocket
       and moving the mouse."""
    # Annotate and initialize variables
    SIZE: int = 480
    screen: pygame.Surface
    background: pygame.Surface
    raw_image: pygame.Surface
    image: pygame.Surface
    image_center: tuple
    current_rotation: float = 0
    start_angle: float = 0
    start_vector: pygame.Vector2
    current_vector: pygame.Vector2
    turning: bool = False
    user_quit: bool = False
    e: pygame.event.Event
    caption: str = "Spin the rocket"
    
    # Set up assets.
    screen = make_window(SIZE, caption)
    background = pygame.Surface((SIZE, SIZE))
    background.fill((255, 255, 255))
    raw_image = pygame.image.load("rocket_small.jpg").convert()
    image = raw_image
    image_center = (screen.get_width()/2, screen.get_height()/2)
    clock: pygame.time.Clock = pygame.time.Clock()

    # Process events until the user chooses to quit.
    while not user_quit:
        # Loop 30 times per second
        clock.tick(30)
        for e in pygame.event.get():
            # Process a quit choice.
            if e.type == pygame.QUIT:
                user_quit = True
            elif e.type == pygame.MOUSEMOTION:
                # If we're turning, then calculate the vector from
                # coordinates and take the delta from the original
                # mouse down vector, then draw the image at the delta.
                # Note that the coordinates need to be shifted to origin.
                if turning:
                    current_vector = pygame.Vector2(e.__dict__["pos"][0]-image_center[0],
                                                  e.__dict__["pos"][1]-image_center[1])
                    angle = -start_vector.angle_to(current_vector)
                    image = pygame.transform.rotate(raw_image, angle)
                    current_rotation = angle
            elif e.type == pygame.MOUSEBUTTONDOWN:
                # If the mouse down is within the image, 
                # set the turning flag and the start vector
                # for rotation
                if in_bounds(image_center, e.__dict__["pos"], image):
                    turning = True
                    start_vector = pygame.Vector2(e.__dict__["pos"][0]-image_center[0],
                                                  e.__dict__["pos"][1]-image_center[1])
                    start_vector.rotate_ip(current_rotation)
            elif e.type == pygame.MOUSEBUTTONUP:
                # We're not turning if we've released the mouse.
                turning = False
                    
        # Draw the background.
        screen.blit(background, (0, 0))
        draw_from_center(image_center, image, screen)
                
        # Show the display.
        pygame.display.flip()
    pygame.quit()

main()
