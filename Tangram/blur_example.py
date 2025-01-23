import pygame
from make_puzzle_background import apply_gaussian_blur

pygame.init()

def main() -> None:
    # Set up the screen.
    screen = pygame.display.set_mode((1024, 1024))
    image = pygame.image.load("fox_background.png").convert_alpha()
    raw_image = image.copy()
    count = 0
    screen.fill((255, 255, 255))
    screen.blit(image, (0, 0))

    user_quit = False
    while not user_quit:
        # Process events
        for event in pygame.event.get():
            # Process a quit choice.
            if event.type == pygame.QUIT:
                user_quit = True
            if event.type == pygame.MOUSEBUTTONUP:
                if count < 5:
                    image = apply_gaussian_blur(image, 10)
                    screen.fill((255, 255, 255))
                    screen.blit(image, (0, 0))
                    count += 1
                else:
                    image = raw_image.copy()
                    screen.fill((255, 255, 255))
                    screen.blit(image, (0, 0))
                    count = 0

               
        # Show the drawing.
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
