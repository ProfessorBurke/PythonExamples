"""Demonstration of the Vector2 class for vector motion."""

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

def main() -> None:
    """Add a function description."""
    # Annotate and initialize variables
    SIZE: int = 480
    screen: pygame.Surface
    background: pygame.Surface
    robot: pygame.Surface
    battery: pygame.Surface
    robot_vector: pygame.Vector2
    battery1_vector: pygame.Vector2
    battery2_vector: pygame.Vector2
    target_vector: pygame.Vector2
    counter: int = 0
    distance1: int
    distance2: int
    user_quit: bool = False
    e: pygame.event.Event
    caption: str = "Add a window caption here"

    # Set up assets.
    screen = make_window(SIZE, caption)
    background = pygame.Surface((SIZE, SIZE))
    background.fill((255, 255, 255))
    robot = pygame.image.load("robot.jpg").convert()
    battery = pygame.image.load("battery.jpg").convert()
    robot_vector = pygame.Vector2(random.randint(0, screen.get_width() - robot.get_width()),
                                  random.randint(0, screen.get_height() - robot.get_height()))
    battery1_vector = pygame.Vector2(random.randint(0, screen.get_width() - battery.get_width()),
                                     random.randint(0, screen.get_height() - battery.get_height()))
    battery2_vector = pygame.Vector2(random.randint(0, screen.get_width() - battery.get_width()),
                                     random.randint(0, screen.get_height() - battery.get_height()))
    clock: pygame.time.Clock = pygame.time.Clock()

    # Process events until the user chooses to quit.
    while not user_quit:
        # Count to two minutes
        counter += 1
        if counter  == 60:
            # Move robot to the closest battery
            distance1 = robot_vector.distance_to(battery1_vector)
            distance2 = robot_vector.distance_to(battery2_vector)
            if distance1 < distance2:
                target_vector = battery1_vector
            else:
                target_vector = battery2_vector
        elif counter == 120:
            counter = 0
            robot_vector = pygame.Vector2(random.randint(0, screen.get_width() - robot.get_width()),
                                          random.randint(0, screen.get_height() - robot.get_height()))
            battery1_vector = pygame.Vector2(random.randint(0, screen.get_width() - battery.get_width()),
                                             random.randint(0, screen.get_height() - battery.get_height()))
            battery2_vector = pygame.Vector2(random.randint(0, screen.get_width() - battery.get_width()),
                                             random.randint(0, screen.get_height() - battery.get_height()))
        elif counter > 60:
            robot_vector.move_towards_ip(target_vector, 5)
            
        # Loop 30 times per second
        clock.tick(30)
        for e in pygame.event.get():
            # Process a quit choice.
            if e.type == pygame.QUIT:
                user_quit = True
            elif e.type == pygame.MOUSEMOTION:
                pass
            elif e.type == pygame.MOUSEBUTTONDOWN:
                pass
            elif e.type == pygame.MOUSEBUTTONUP:
                pass
            elif e.type == pygame.KEYDOWN:
                pass
            elif e.type == pygame.KEYUP:
                pass
            elif e.type == pygame.ACTIVEEVENT:
                pass
                    
        # Draw the background.
        screen.blit(background, (0, 0))
        screen.blit(robot, robot_vector)
        screen.blit(battery, battery1_vector)
        screen.blit(battery, battery2_vector)
                
        # Show the display.
        pygame.display.flip()
    pygame.quit()

main()
