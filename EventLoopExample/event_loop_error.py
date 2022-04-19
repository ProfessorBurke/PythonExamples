"""Example of what not to do with an event loop."""

# Imports and initialize pygame.
import random
import pygame
pygame.init()

def make_window(width: int, height: int, caption: str) -> pygame.Surface:
    """Create and return a pygame window."""
    screen: pygame.Surface
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(caption)
    return screen

def main() -> None:
    """Add a function description."""
    # Annotate and initialize variables
    screen: pygame.Surface
    background: pygame.Surface
    rocket: pygame.Surface
    rocket_x: int = 0
    rocket_y: int = 100
    rocket_dx: int = 10
    rocket_dy: int = 0
    stars: list = []
    i: int
    max_height: int
    max_width: int
    
    user_quit: bool = False
    e: pygame.event.Event
    caption: str = "Click for a landing"

    # Set up assets.
    background = pygame.image.load("moonNASA.JPG")
    screen = make_window(background.get_width(), background.get_height(), caption)
    rocket = pygame.image.load("rocket.png").convert_alpha()

    # Create the stars
    max_height = background.get_height() -100
    max_width = background.get_width()
    for i in range(50):
        stars.append((random.randint(0, max_width), random.randint(0, max_height)))
    
    # Process events until the user chooses to quit.
    clock: pygame.time.Clock = pygame.time.Clock()
    while not user_quit:
        # Loop 30 times per second
        clock.tick(30)
        for e in pygame.event.get():
            # Process a quit choice.
            if e.type == pygame.QUIT:
                user_quit = True
            elif e.type == pygame.MOUSEBUTTONUP:
                rocket_dy = 5
                rocket_dx = 0                

        
        # Float the rocket right and boundary check.
        rocket_x += rocket_dx
        if rocket_x >= screen.get_width():
            rocket_x = 0 - rocket.get_width()

        rocket_y += rocket_dy
        if rocket_y + rocket.get_height() >= screen.get_height():
            rocket_y = 0
            rocket_y = screen.get_height() - rocket.get_height()
                    
        # Draw the background, stars, and robot.
        screen.blit(background, (0, 0))
        for star in stars:
            pygame.draw.circle(screen, (255, 255, 255), star,
                              random.randint(1, 3))
        screen.blit(rocket, (rocket_x, rocket_y))

        # Show the display.
        pygame.display.flip()
    pygame.quit()

main()
