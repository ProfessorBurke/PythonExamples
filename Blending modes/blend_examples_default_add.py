"""
    pygame blending modes demo: default and the add modes.
"""

import pygame

def main() -> None:
    """Illustration of pygame blending modes"""
    # Annotate and initialize window and image constants and variables.
    i: int
    j: int

    # Create the screen.
    SIZE: int = 512
    screen: pygame.Surface = pygame.display.set_mode((SIZE, SIZE))
    pygame.display.set_caption("Blending examples")

    # Load in the two primary images.
    background: pygame.Surface = pygame.image.load("background.jpg").convert_alpha()
    blimp: pygame.Surface = pygame.image.load("blimp.png").convert_alpha()

    # Create some special effects Surfaces.
    working: pygame.Surface = pygame.Surface((SIZE, SIZE), pygame.SRCALPHA)
    filter_surf: pygame.Surface = pygame.Surface((SIZE, SIZE), pygame.SRCALPHA)
    spotlight: pygame.Surface = pygame.image.load("spotlight.jpg").convert_alpha()
    searchlight: pygame.Surface

    # Create a searchlight
    searchlight: pygame.Surface = pygame.Surface((SIZE, SIZE), pygame.SRCALPHA)
    searchlight.fill((255, 255, 0))
    for i in range(SIZE):
        for j in range(SIZE):
            alpha: int = max(255 - (abs((SIZE // 2) - i) + abs((SIZE // 2) - j)) // 2, 0)

            searchlight.set_at((i, j), pygame.Color(255, 255, 0, alpha))
    pygame.image.save(searchlight, "searchlight.png")

    # Annotate and initialize event and game loop variables.
    user_quit: bool = False
    e: pygame.event.Event

    # Create the clock for timing the game loop.
    clock: pygame.time.Clock = pygame.time.Clock()

    # Printing pixels from the images we're blitting.
    print("Working pixel at (232, 107): " + str(working.get_at((232, 107))))
    print("Background pixel at (232, 107): " + str(background.get_at((232, 107))))
    print("Background pixel at (185, 280): " + str(background.get_at((185, 280))))
    print("Opaque Blimp pixel at (132, 7): "  + str(blimp.get_at((132, 7))))
    print("Opaque Blimp pixel at (85, 180): "  + str(blimp.get_at((85, 180))))
    print("Background pixel at (220, 102): " + str(background.get_at((220, 102))))
    print("Transparent Blimp pixel at (120, 2): "  + str(blimp.get_at((120, 2))))
    print("Searchlight pixel at (220, 102): " + str(searchlight.get_at((220, 102))))
    

##    # ###################################################
##    # Default blending mode -- standard alpha compositing
##    # ###################################################
##    working.blit(background, (0, 0))
##    working.blit(blimp, (100, 100))
##    pygame.image.save(working, "background_and_blimp.jpg")
##    print("Blended pixel at (232, 107) : " + str(working.get_at((232, 107))))
##    print("Blended pixel at (220, 102) : " + str(working.get_at((220, 102))))
##
##    working.blit(searchlight, (0, 0))
##    pygame.image.save(working, "background_and_blimp_and_searchlight.jpg")
##    print("Blended pixel at (220, 102) : " + str(working.get_at((220, 102))))

##    # ###################################################
##    # BLEND_RGB_ADD
##    # ###################################################
##    # Blitting to working, which is 0,0,0,0, with this mode will leave the alpha at 0.
##    working.blit(background, (0, 0), special_flags = pygame.BLEND_RGB_ADD)
##    
##    # Fill working with black with full opacity.
##    working.fill((0,0,0,255))
##    # And now blit.
##    working.blit(background, (0, 0), special_flags = pygame.BLEND_RGB_ADD)
##    
##    # Blit a dark grey over that.
##    filter_surf.fill((100,100,100,0))
##    pygame.image.save(filter_surf, "filter_surf.jpg")
##    # And now blit.
##    working.blit(filter_surf, (0, 0), special_flags = pygame.BLEND_RGB_ADD)
##
##    # Blit the spotlight over that.
##    working.blit(spotlight, (0, 0), special_flags = pygame.BLEND_RGB_ADD)
##    pygame.image.save(working, "background_and_spotlight.jpg")
    

    # ###################################################
    # BLEND_RGBA_ADD
    # ###################################################
##    working.fill((0,0,0,0))
##    working.blit(background, (0, 0), special_flags = pygame.BLEND_RGBA_ADD)
##    working.blit(spotlight, (0, 0), special_flags = pygame.BLEND_RGBA_ADD)
##    print("After background blit, working pixel at (232, 107): " + str(working.get_at((232, 107))))
##    #working.blit(blimp, (100, 100), special_flags = pygame.BLEND_RGBA_ADD)
##    print("After blimp blit, working pixel at (232, 107): " + str(working.get_at((232, 107))))
##    print("After blimp blit, working pixel at (185, 280): " + str(working.get_at((185, 280))))

##    # Create a transparent Surface and a light blob
##    filter_surf.fill((0, 0, 0, 0))
##    spotlight = pygame.Surface((100, 100), pygame.SRCALPHA)
##    pygame.draw.circle(spotlight, (255, 255, 100, 60), (50, 50), 50)
##    pygame.image.save(spotlight, "spotlight.png")
##    
##    # Draw lights onto the transparent surface.
##    filter_surf.blit(spotlight, (100, 100), special_flags=pygame.BLEND_RGBA_ADD)
##    filter_surf.blit(spotlight, (120, 110), special_flags=pygame.BLEND_RGBA_ADD)
##    pygame.image.save(filter_surf, "overlapping_spotlights.png")
##    # Print overlapping and non-overlapping spotlight pixels.
##    print("An overlapping spotlight pixel (150, 150): " + str(filter_surf.get_at((150, 150))))
##    print("A non-overlapping spotlight pixel (120, 120): " + str(filter_surf.get_at((120, 120))))
##
##    # Blit the lights onto the background
##    print("Background pixel before overlapping spotlight (150, 150): " + str(working.get_at((150, 150))))
##    print("Background pixel before spotlight (120, 120): " + str(working.get_at((120, 120))))    
##    working.blit(filter_surf, (0, 0))
##    print("An overlapping spotlight pixel on the background (150, 150): " + str(working.get_at((150, 150))))
##    print("A non-overlapping spotlight pixel on the background (120, 120): " + str(working.get_at((120, 120))))
##    pygame.image.save(working, "working_with_spotlights.png")

##    # Third image from the quiz:
##    working.blit(blimp, (100,100), special_flags = pygame.BLEND_RGBA_ADD)
##    pygame.image.save(working, "oops.png")


    # ###################################################
    # Game loop
    # ###################################################  
    # Show the display.
    screen.blit(working, (0, 0))
    pygame.display.flip()

    # Wait for the user to quit
    while not user_quit:
        # Loop 30 times per second
        clock.tick(30)
        for e in pygame.event.get():
            # Process a quit choice.
            if e.type == pygame.QUIT:
                user_quit = True
    pygame.quit()

main()
