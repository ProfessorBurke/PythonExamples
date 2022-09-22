"""Example of the new transparency settings in pygame 2.0."""

# Import and initialize pygame.
import pygame
pygame.init()


def change_center_alphas(star: pygame.Surface,
                         star_colorkey: pygame.Surface,
                         alpha_star: pygame.Surface) -> None:
    """Change the alpha channel at the center of each star."""
    stars: list = [star, star_colorkey, alpha_star]
    color: tuple
    new_alpha: int
    row: int
    col: int
    for star in stars:
        for row in range(40, 60):
            for col in range(40, 60):
                color = star.get_at((row, col))
                new_alpha = color[3] - 50 if color[3] - 50 > 0 else 0
                star.set_at((row, col), (color[0], color[1], color[2], new_alpha))

def blit_stars(star: pygame.Surface,
               star_colorkey: pygame.Surface,
               alpha_star: pygame.Surface,
               screen: pygame.Surface) -> None:
    """Blit the stars to the background."""
    # Blit the stars to the screen
    # Star from 100, 100 to 200, 200
    # Star with colorkey from 300, 100 to 400, 200
    # Alpha star from 300, 300 to 400, 400
    screen.blit(star, (100, 100))
    screen.blit(star_colorkey, (300, 100))
    screen.blit(alpha_star, (300, 300))
    
def print_color_table(star: pygame.Surface,
                      star_colorkey: pygame.Surface,
                      alpha_star: pygame.Surface) -> None:
    """Print a table of colors at top left and top middle."""
    print("{:<20s}{:<20s}{:<20s}{:<20s}".format("Star", "Top left", "Top point", "Center point"))
    print("{:<20s}{:<20s}{:<20s}{:<20s}".format("jpg star",
                                         str(star.get_at((0,0))),
                                         str(star.get_at((50, 5))),
                                         str(star.get_at((50, 50)))))
    print("{:<20s}{:<20s}{:<20s}{:<20s}".format("colorkey star",
                                         str(star_colorkey.get_at((0,0))),
                                         str(star_colorkey.get_at((50,5))),
                                         str(star_colorkey.get_at((50,50)))))
    print("{:<20s}{:<20s}{:<20s}{:<20s}".format("alpha channel star",
                                         str(alpha_star.get_at((0,0))),
                                         str(alpha_star.get_at((50,5))),
                                         str(alpha_star.get_at((50,50)))))

def main() -> None:
    """Demonstrate transparency."""
    # Annotate and initialize variables
    SIZE: int = 480
    screen: pygame.Surface
    background: pygame.Surface
    star: pygame.Surface
    star_colorkey: pygame.Surface
    alpha_star: pygame.Surface
    user_quit: bool = False
    e: pygame.event.Event
    clock: pygame.time.Clock = pygame.time.Clock()

    # Create a window.
    screen = pygame.display.set_mode((SIZE, SIZE))
    pygame.display.set_caption("Transparency Example")

    # Open the checkerboard background and blit to the screen.
    background = pygame.image.load("checkerboard.jpg").convert()
    screen.blit(background, (0, 0))
    
    # Load the star images.
    star = pygame.image.load("star.jpg").convert_alpha()
    star_colorkey = pygame.image.load("star.gif").convert_alpha()
    star_colorkey.set_colorkey((255, 255, 255))
    alpha_star = pygame.image.load("alpha_star.png").convert_alpha()

    # Blit the stars to the screen.
    blit_stars(star, star_colorkey, alpha_star, screen)

    # Display information about the star colors
    print_color_table(star, star_colorkey, alpha_star)
    
    # Process events until the user chooses to quit.
    while not user_quit:
        # Loop 30 times per second
        clock.tick(30)
        for e in pygame.event.get():
            # Process a quit choice.
            if e.type == pygame.QUIT:
                user_quit = True
            elif e.type == pygame.KEYDOWN:
                # Change overall alpha and display the table
                if e.__dict__["key"] == pygame.K_KP_PLUS:
                    screen.blit(background, (0, 0))
                    star.set_alpha(star.get_alpha() + 10)
                    star_colorkey.set_alpha(star_colorkey.get_alpha() + 10)
                    alpha_star.set_alpha(alpha_star.get_alpha() + 10)
                    blit_stars(star, star_colorkey, alpha_star, screen)
                    print_color_table(star, star_colorkey, alpha_star)
                elif e.__dict__["key"] == pygame.K_KP_MINUS:
                    screen.blit(background, (0, 0))
                    screen.blit(background, (0, 0))
                    star.set_alpha(star.get_alpha() - 10)
                    star_colorkey.set_alpha(star_colorkey.get_alpha() - 10)
                    alpha_star.set_alpha(alpha_star.get_alpha() - 10)
                    blit_stars(star, star_colorkey, alpha_star, screen)
                    print_color_table(star, star_colorkey, alpha_star)
    
                # Change the individual alpha values at the center
                # of each star
                elif e.__dict__["key"] == pygame.K_SPACE:
                    screen.blit(background, (0, 0))
                    change_center_alphas(star, star_colorkey, alpha_star)
                    blit_stars(star, star_colorkey, alpha_star, screen)
                    print_color_table(star, star_colorkey, alpha_star)

        # Show the display.
        pygame.display.flip()

    pygame.quit()

main()
