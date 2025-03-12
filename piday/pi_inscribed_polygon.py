"""
    Approximating pi using the inscribed polygon method, illustrated with
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


def inscribed_polygon_pi(n: int) -> float:
    """Return the approximation of pi given an inscribed n-sided polygon."""
    return n * math.sin(math.pi / n)

def draw_polygon(n: int, screen: pygame.Surface) -> None:
    """Draw an n-sided polygon inscribed within a circle of RADIUS size."""
    # Fill the screen with white and draw the circle.
    screen.fill((255, 255, 255))
    pygame.draw.circle(screen, (0, 0, 0), CENTER, RADIUS, 2)
    # Calculate the angle between each point.
    angle_step = 2 * math.pi / n
    # Create a list of the n points of the polygon and draw.
    points = []
    for i in range(n):
        angle = i * angle_step
        x = CENTER[0] + RADIUS * math.cos(angle)
        y = CENTER[1] + RADIUS * math.sin(angle)
        points.append((x, y))
    pygame.draw.polygon(screen, (0, 0, 255), points, 2)

def main():
    # Game loop variable
    running = True

    # Simulation variable
    num_sides = 6

    # Create the window, clock, and font.
    screen: pygame.surface.Surface = pygame.display.set_mode((SIZE, SIZE))
    clock: pygame.time.Clock = pygame.time.Clock()
    font: pygame.font.SysFont = pygame.font.SysFont("arialrounded", 24)

    # Draw the first inscribed polygon and calculate and display the pi approximation.
    draw_polygon(num_sides, screen)
    text = font.render("Polygon π ≈ {:.5f}".format(inscribed_polygon_pi(num_sides)),
                       True, (0, 0, 0))
    screen.blit(text, (CENTER[0] - text.get_width()//2,
                       CENTER[1] - text.get_height()//2))
    
    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Increase the number of sides of the polygon
                # and recalculate pi.
                num_sides = min(num_sides + 1, 100)
                draw_polygon(num_sides, screen)
                text = font.render("Polygon π ≈ {:.5f}".format(inscribed_polygon_pi(num_sides)),
                                    True, (0, 0, 0))
                screen.blit(text, (CENTER[0] - text.get_width()//2,
                                   CENTER[1] - text.get_height()//2))

        pygame.display.set_caption("Polygon pi is {:.5f}; Number of sides = {}".
                                    format(inscribed_polygon_pi(num_sides), num_sides))
        pygame.display.flip()


    pygame.quit()

if __name__ == "__main__":
    main()
