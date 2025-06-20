"""
    pygame blending modes demo: sub modes.
"""

import pygame

def main() -> None:
    """Illustration of pygame blending modes"""
    # Create the screen.
    SIZE: int = 512
    screen: pygame.Surface = pygame.display.set_mode((SIZE, SIZE))
    pygame.display.set_caption("Blending examples")

    # Load in the two primary images.
    background: pygame.Surface = pygame.image.load("background.jpg").convert_alpha()
    blimp: pygame.Surface = pygame.image.load("blimp.png").convert_alpha()

    # Create some special effects Surfaces.
    working_alpha: pygame.Surface = pygame.Surface((SIZE, SIZE), pygame.SRCALPHA)
    working_opaque: pygame.Surface = pygame.Surface((SIZE, SIZE))
    reverse_spotlight: pygame.Surface = pygame.image.load("reverse_spotlight.jpg").convert_alpha()
    filter_surf: pygame.Surface = pygame.Surface((SIZE, SIZE), pygame.SRCALPHA)

    # Define a flag for when we should blit either the working_opaque or working_alpha Surface.
    blit_opaque: bool = True

    # Annotate and initialize event and game loop variables.
    user_quit: bool = False
    e: pygame.event.Event

    # Create the clock for timing the game loop.
    clock: pygame.time.Clock = pygame.time.Clock()


    # ###################################################
    # BLEND_RGB_SUB
    # ###################################################
    # Blitting to working_opaque, which is 0,0,0,255.
##    print("Blitting the background to working_opaque with BLEND_RGB_SUB:")
##    print("Background pixel at (232, 107): " + str(background.get_at((232, 107))))
##    print("Working_opaque pixel at (232, 107) before: " + str(working_opaque.get_at((232, 107))))
##    working_opaque.blit(background, (0, 0), special_flags = pygame.BLEND_RGB_SUB)
##    print("Working_opaque pixel at (232, 107) after: " + str(working_opaque.get_at((232, 107))))
  
##    # Fill working_opaque with white and blit.
##    working_opaque.fill((255,255,255))
##    print("Blitting the background to WHITE working_opaque with BLEND_RGB_SUB:")
##    print("Background pixel at (232, 107): " + str(background.get_at((232, 107))))
##    print("Working_opaque pixel at (232, 107) before: " + str(working_opaque.get_at((232, 107))))
##    working_opaque.blit(background, (0, 0), special_flags = pygame.BLEND_RGB_SUB)
##    print("Working_opaque pixel at (232, 107) after: " + str(working_opaque.get_at((232, 107))))
##    pygame.image.save(working_opaque, "inverted.jpg")

##    # Blit yellow and then sub background over
##    working_opaque.fill((255, 255, 0))
##    working_opaque.blit(background, (0, 0), special_flags = pygame.BLEND_RGB_SUB)

##    # Blit the background in the default blending mode and then sub a grey over.
##    working_opaque.blit(background, (0, 0))
##    filter_surf.fill((100, 100, 100))
##    working_opaque.blit(filter_surf, (0, 0), special_flags = pygame.BLEND_RGB_SUB)

##    # Blit the background in the default blending mode and then sub reverse_spotlight over.
##    working_opaque.blit(background, (0, 0))
##    working_opaque.blit(reverse_spotlight, (0, 0), special_flags = pygame.BLEND_RGB_SUB)
##    pygame.image.save(working_opaque, "reverse_spotlight_blitted.jpg")

 
    # ###################################################
    # BLEND_RGBA_SUB
    # ###################################################
    # We're going to use the transparent working surface for this example.
##    blit_opaque = False
##    # Create a Mask from the blimp and then turn it into a Surface that we can use to
##    # fade the blimp and tinge it red as it fades.
##    blimp_mask: pygame.Mask = pygame.mask.from_surface(blimp)
##    blimp_fader: pygame.Surface = blimp_mask.to_surface(setcolor = (0,20,20,2), unsetcolor = (0,0,0,0))
##    faded_blimp: pygame.Surface = blimp.copy()
##    faded_blimp.blit(blimp_fader, (0, 0), special_flags = pygame.BLEND_RGBA_SUB)    
##    # Blit the background and the blimp in default mode.
##    working_alpha.blit(background, (0, 0))
##    working_alpha.blit(blimp, (100, 100))
##    print("Faded blimp pixel at (132, 7): " + str(faded_blimp.get_at((132, 7))))
##    print("Working alpha pixel at (232, 107): " + str(working_alpha.get_at((232, 107))))
    

    # ###################################################
    # Game loop
    # ###################################################  
    # Show the display.
    # Blit either working_alpha or working_opaque
    if blit_opaque:
        screen.blit(working_opaque, (0, 0))
    else:
        screen.blit(working_alpha, (0, 0))
    pygame.display.flip()

    count = 0
    # Wait for the user to quit
    while not user_quit:
        count += 1
        # Loop 30 times per second
        clock.tick(30)
        for e in pygame.event.get():
            # Process a quit choice.
            if e.type == pygame.QUIT:
                user_quit = True
            elif e.type == pygame.MOUSEBUTTONUP:
                # Check effects slowly with mouse clicks.
                working_alpha.blit(background, (0, 0))
                working_alpha.blit(faded_blimp, (100, 100))
                faded_blimp.blit(blimp_fader, (0, 0), special_flags = pygame.BLEND_RGBA_SUB)
                screen.blit(working_alpha, (0, 0))
                print("Faded blimp pixel at (132, 7): " + str(faded_blimp.get_at((132, 7))))
                print("Working alpha pixel at (232, 107): " + str(working_alpha.get_at((232, 107))))
                pygame.display.flip()
            elif e.type == pygame.MOUSEWHEEL:
                pygame.image.save(working_alpha, "red_blimp.png")
                
        # Uncomment this code for animated effects.
##        working_alpha.blit(background, (0, 0))
##        working_alpha.blit(faded_blimp, (100, 100))
##        faded_blimp.blit(blimp_fader, (0, 0), special_flags = pygame.BLEND_RGBA_SUB)
##        screen.blit(working_alpha, (0, 0))
##        pygame.display.flip()

    pygame.quit()

main()
