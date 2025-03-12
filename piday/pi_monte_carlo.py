"""
    Approximating pi using the Monte Carlo method, illustrated with
    pygame.

"""
import pygame
import random
import math

# Initialize pygame
pygame.init()

# Define window and drawing constants.
SIZE: int = 600
CENTER: tuple = (SIZE // 2, SIZE // 2)
RADIUS: int = SIZE // 2 - 20


def approximate_pi_monte_carlo(num_samples: int) -> tuple[float, list]:
    """ Approximate pi using the Monte Carlo method and return a list of tuples
        (x, y, True if inside the circle) and the approximation. """
    # Annotate variables
    inside: int = 0
    points: list = []
    i: int
    x: float
    y: float

    # Generate a point and append to the list, count the number of points
    # inside the circle.
    for i in range(num_samples):
        x = random.uniform(-1, 1)
        y = random.uniform(-1, 1)
        if x**2 + y**2 <= 1:
            inside += 1
            points.append((x, y, True))  
        else:
            points.append((x, y, False))
            
    # Return the approximation of pi and the list of points.
    return (4 * inside / num_samples, points)

def draw_monte_carlo(points: list, screen: pygame.Surface) -> None:
    """ Given the list of points and the screen, draw the square with
        the inscribed circle and then draw the randomly generated points."""
    # Annotate variables
    x: float
    y: float
    color: tuple
    screen_x: int
    screen_y: int

    # Clear the screen by filling with white, then draw the circle and square.
    screen.fill((255, 255, 255))
    pygame.draw.circle(screen, (0, 0, 0), CENTER, RADIUS, 2)
    pygame.draw.rect(screen, (0, 0, 0), (20, 20, SIZE - 40, SIZE - 40), 2)
    # Draw each point, blue if in the circle, red if outside.
    for x, y, inside in points:
        screen_x = int(CENTER[0] + x * RADIUS)
        screen_y = int(CENTER[1] + y * RADIUS)
        color = (0, 0, 255) if inside else (255, 0, 0)
        pygame.draw.circle(screen, color, (screen_x, screen_y), 2)

def main() -> None:

    # Game loop variable
    running: bool = True

    # Simulation variables
    num_samples: int = 500
    text: pygame.Surface
    pi_monte: float
    monte_points: list

    # Create the window, clock, and font.
    screen: pygame.surface.Surface = pygame.display.set_mode((SIZE, SIZE))
    clock: pygame.time.Clock = pygame.time.Clock()
    font: pygame.font.SysFont = pygame.font.SysFont("arialrounded", 24)

    # Draw a Monte Carlo approximation.
    screen.fill((255, 255, 255))
    pi_monte, monte_points = approximate_pi_monte_carlo(num_samples)
    draw_monte_carlo(monte_points, screen)
    text = font.render("Monte Carlo π ≈ {:.5f}".format(pi_monte),
                        True, (0, 0, 0))
    screen.blit(text, (20, SIZE - 45))
    
    while running:
        
        for event in pygame.event.get():
            # Process a quit
            if event.type == pygame.QUIT:
                running = False
            # Draw a new Monte Carlo approximation on click.
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pi_monte, monte_points = approximate_pi_monte_carlo(num_samples)
                draw_monte_carlo(monte_points, screen)
                text = font.render("Monte Carlo π ≈ {:.5f}".format(pi_monte),
                                   True, (0, 0, 0))
                screen.blit(text, (20, SIZE - 45))
            # Increase or decrease the number of samples
            elif event.type == pygame.KEYUP:
                if event.__dict__["key"] == pygame.K_UP:
                    num_samples += 100
                elif event.__dict__["key"] == pygame.K_DOWN:
                    num_samples = num_samples - 100 if (num_samples > 100) else 100
        pygame.display.set_caption("Monte Carlo pi is {:.5f}; Number of samples = {}".
                                    format(pi_monte, num_samples))
                
        pygame.display.flip()
        
    pygame.quit()

if __name__ == "__main__":
    main()
