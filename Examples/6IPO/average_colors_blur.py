"""
    Load in an image.
    On each click, blur each pixel in the image by averaging the pixel color
    with the pixels immediately surrounding it.

"""

# Import and initialize pygame.
import pygame
pygame.init()

# Define constants and annotate variables.
SIZE: int = 417
screen: pygame.Surface
user_quit: bool
event: pygame.event.Event
background: pygame.Surface
blurry: pygame.Surface
x: int
y: int
splat_choice: int
caption_choice: int
count: int = 0
splatter: pygame.Surface
current_caption: str = "Click to blur!"
draw_splatter: bool = False
reset_canvas: bool = True

# Create a pygame window.
screen = pygame.display.set_mode((SIZE, SIZE))
pygame.display.set_caption(current_caption)

# Load assets.
background = pygame.image.load("YouTubeLogo.jpg")

screen.blit(background, (0, 0))

# Every time the user clicks, blur the image.
user_quit = False
while not user_quit:
    # Process events
    for event in pygame.event.get():
        # Process a quit choice.
        if event.type == pygame.QUIT:
            user_quit = True
        # Process a click by (inefficiently) blurring pixels with surrounding pixels.
        elif event.type == pygame.MOUSEBUTTONUP:
            blurry = screen.copy()
            for x in range(blurry.get_width()):
                for y in range(blurry.get_height()):
                    total_red = 0
                    total_green = 0
                    total_blue = 0
                    count = 0
                    for i in range(max(x-1, 0), min(x+1, blurry.get_width())):
                        for j in range(max(y-1, 0), min(y+1, blurry.get_height())):
                            color = screen.get_at((i,j))
                            total_red += color[0]
                            total_green += color[1]
                            total_blue += color[2]
                            count += 1
                    new_color = pygame.Color(total_red/count, total_green/count, total_blue/count, 255)
                    blurry.set_at((x,y), new_color)

            screen.blit(blurry, (0, 0))
        
    # Show the drawing.
    pygame.display.flip()

pygame.quit()
            
