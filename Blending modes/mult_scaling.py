"""
    Demonstrating that the MULT modes scale the color of an image.
    Requires background.jpg in the same folder.
"""

import pygame

# Annotate and initialize variables
# Drawing surfaces.
screen: pygame.Surface
background: pygame.Surface
shadow: pygame.Surface
blit_background: pygame.Surface
# Color and alpha values.
red: int = 155
green: int = 155
blue: int = 155
alpha: int = 155
# Event handling.
event: pygame.event.Event
running: bool = True
alpha_on: bool = False
# Text display variables.
text_surf: pygame.Surface
text_box: pygame.Surface
font: pygame.font.SysFont
blend_mode: str

# Initialize pygame and create the window
pygame.init()
screen = pygame.display.set_mode((512, 512))
pygame.display.set_caption("Arrows to change scale; space to toggle alpha")

# Initialize font
pygame.font.init()
font = pygame.font.SysFont(None, 22)

# Load the background image
background = pygame.image.load("background.jpg").convert_alpha()

# Create a grey Surface for color scaling
shadow = pygame.Surface(background.get_size(), pygame.SRCALPHA)
shadow.fill((red, green, blue, alpha))  

# Process user choices until the user chooses to quit.
while running:
    for event in pygame.event.get():
        # Process a close box click.
        if event.type == pygame.QUIT:
            running = False
        # Process arrow key up and down by changing the darkness of the scale.
        elif event.type == pygame.KEYUP:
            if event.dict["key"] == pygame.K_UP:
                red = min(255, red + 25)
                green = min(255, green + 25)
                blue = min(255, blue + 25)
                alpha = min(255, alpha + 25)
                shadow.fill((red, green, blue, alpha))
            elif event.dict["key"] == pygame.K_DOWN:
                red = max(0, red - 25)
                green = max(0, green - 25)
                blue = max(0, blue - 25)
                alpha = max(0, alpha - 25)
                shadow.fill((red, green, blue, alpha))
            elif event.dict["key"] == pygame.K_SPACE:
                alpha_on = not alpha_on
            blit_background = background.copy()
            blit_background.blit(shadow, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            print("Background pixel at (232, 107): " + str(blit_background.get_at((232, 107))))

    # Apply MULT blending to darken.
    blit_background = background.copy()
    if alpha_on:
        blend_mode = "BLEND_RGBA_MULT"
        blit_background.blit(shadow, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    else:
        blend_mode = "BLEND_RGB_MULT"
        blit_background.blit(shadow, (0, 0), special_flags=pygame.BLEND_RGB_MULT)
        
    # Render text showing RGBA values and mode.
    info_text = f"Shadow RGBA: ({red}, {green}, {blue}, {alpha}) | Mode: {blend_mode}"
    text_surf = font.render(info_text, True, (0, 0, 0))

    # Create a semi-transparent white box behind the text.
    text_box = pygame.Surface((text_surf.get_width() + 10, text_surf.get_height() + 10), pygame.SRCALPHA)
    text_box.fill((255, 255, 255, 180))  

    # Blit the text box and then the text.
    blit_background.blit(text_box, (10, blit_background.get_height() - text_surf.get_height() - 20))
    blit_background.blit(text_surf, (15, blit_background.get_height() - text_surf.get_height() - 15))

    # Display the result.
    screen.fill((255, 0, 0))
    screen.blit(blit_background, (0, 0))
    pygame.display.flip()

            
pygame.quit()












