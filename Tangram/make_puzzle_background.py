
import pygame
import random
import math

pygame.init()


def apply_gaussian_blur(surface: pygame.Surface, repeats: int) -> pygame.Surface:
    """ Approximate a Gaussian blur by repeated smoothscaling (repeats times)."""
    i: int
    # Smoothscale down (halve / average) and then up (double / interpolate) to blur the edges.
    for i in range(repeats):
        surface = pygame.transform.smoothscale(surface, (surface.get_width() // 2, surface.get_height() // 2))
        surface = pygame.transform.smoothscale(surface, (surface.get_width() * 2, surface.get_height() * 2))
    return surface

def make_blob_surface(width: int, height: int, num_blobs: int,
                      min_size: int, max_size: int) -> pygame.Surface:
    """Create a surface of black blobs with variations in transparency."""
    # Make a surface for the blobs.
    rect_surface = pygame.Surface((width, height), pygame.SRCALPHA)

    # Randomly generate blobs on the Surface.
    for i in range(num_blobs):

        points: list = [(random.randint(0, width * 2), random.randint(0, height * 2))]
        points.append((points[0][0] + random.randint(0, width//2), points[0][1] + random.randint(0, height//2)))
        points.append((points[0][0], points[0][1] + random.randint(0, height//2)))
        points.append((points[0][0] - random.randint(0, width//2), points[0][1]))
        points.append((points[0][0] - random.randint(0, width//2), points[0][1] + random.randint(0, height//2)))
        # Less distance between the alpha values gives for muted changes between shapes
        pygame.draw.polygon(rect_surface, (0,0,0, random.randint(125, 150)), points) # 125, 200; 110, 170; 100, 150 (invisible)
        
    # Blur the shapes
    rect_surface = apply_gaussian_blur(rect_surface, 10)    

    return rect_surface

def grow_mask(mask, kernel_size):
    # Define a small kernel to grow the mask (3x3 square kernel grows by ~1 pixel)
    kernel = pygame.Mask((kernel_size, kernel_size), fill=True)

    # Convolve the mask to grow it
    grown_mask = mask.convolve(kernel)

    return grown_mask
    
def make_mask_border(mask, kernel_size):
    """Make a border for the mask that is blurry and has a brushstroke effect."""
    
    # Grow the mask
    grown_mask = grow_mask(mask, kernel_size)

    # Make a slightly larger mask with pixels removed to give a messy edge.
    blurry_mask = grow_mask(mask, kernel_size+4)

    # Now randomly remove some pixels from that
    width, height = blurry_mask.get_size()
    for y in range(height):
        for x in range(width):
            if int(random.triangular(1, 6, 3)) == 3:
                blurry_mask.set_at((x, y), 0)

    # Merge the masks
    grown_mask.draw(blurry_mask, (0, 0))  
    
    # Subtract the original mask from the grown mask to create the border
    border_mask = grown_mask.copy()
    border_mask.erase(mask, ((kernel_size // 2), (kernel_size // 2)))

    # Offset for the border (shift it so it's correctly positioned)
    # Offset by half the kernel size to center the border around the original
    offset = (-(kernel_size//2), -(kernel_size//2))

    return offset, border_mask

def make_parchment(width, height):
    parchment = pygame.Surface((width, height), pygame.SRCALPHA)
    tan = pygame.Color(220, 212, 189)
    light_tan = pygame.Color(227, 221, 199)
    for y in range(-10, height):
        for x in range(-10, width):
            parchment.set_at((x, y), (227, 221, 189, random.randint(210, 255)))
    big_parchment = pygame.transform.scale_by(parchment, 6)
    parchment.blit(big_parchment, (0, 0))
    return parchment


def make_parchment_brushes(width, height):
    parchment = pygame.Surface((width, height), pygame.SRCALPHA)
    brush = pygame.Surface((10,10), pygame.SRCALPHA)
    brush.fill((220, 212, 189, 150))
    for y in range(10):
        for x in range(20):
            if int(random.triangular(1, 10, 5)) == 5:
                brush.set_at((x, y), (235, 227, 206, 250))
    for y in range(-10, height):
        for x in range(-10, width):
            if random.randint(1, 10) == 10:
                parchment.blit(brush, (x, y))
    big_parchment = pygame.transform.smoothscale_by(parchment, 1.5)
    parchment.blit(big_parchment, (0, 0))
    return parchment

def make_puzzle_image(image: pygame.Surface) -> pygame.Surface:
    """Generate a background from a puzzle shape."""
    # Create the parchment background
    destination_surface = make_parchment_brushes(1024, 1024)
    
    # Make the puzzle image.
    surface = pygame.image.load(image).convert_alpha()
    mask = pygame.mask.from_surface(surface)
    grown_mask = grow_mask(mask, 6)
    mask_surface = grown_mask.to_surface(setcolor=(255, 255, 255, 255), unsetcolor=(0, 0, 0, 0))

    # Create a Surface with a little variation
    paint_surface = make_blob_surface(1024, 1024, 1800, 10, 50)

    # Mask out the puzzle, blit and blur.
    paint_surface.blit(mask_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    paint_surface = apply_gaussian_blur(paint_surface, 2)
   
    # Make a border
    offset, border_mask = make_mask_border(mask, 8)
    border_mask_surface = border_mask.to_surface(setcolor=(0, 0, 0, 255), unsetcolor=(0, 0, 0, 0))
    border_mask_surface = apply_gaussian_blur(border_mask_surface, 5)

    # Blit the puzzle and its border to the parchment.
    destination_surface.blit(border_mask_surface, offset)
    destination_surface.blit(paint_surface, (0, 0))

    return destination_surface

def main() -> None:
    # Set up the screen.
    screen = pygame.display.set_mode((1024, 1024))
    destination_surface = make_puzzle_image("rabbit_background_transparent.png")

    screen.fill((255, 255, 255))
    screen.blit(destination_surface, (0, 0))
    user_quit = False
    while not user_quit:
        # Process events
        for event in pygame.event.get():
            # Process a quit choice.
            if event.type == pygame.QUIT:
                user_quit = True

               
        # Show the drawing.
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()








