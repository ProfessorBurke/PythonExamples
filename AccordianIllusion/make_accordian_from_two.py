"""Get two images from the user and make the accordian-fold image."""

# Import and initialize pygame.
import pygame
import tkinter
import tkinter.filedialog

pygame.init()

def prompt_file() -> str:
    """Create a Tk file dialog, clean up, and return the
       file name."""
    top = tkinter.Tk()
    top.withdraw()  
    file_name = tkinter.filedialog.askopenfilename(parent=top)
    top.destroy()
    return file_name

def make_window(width: int, height: int, caption: str) -> pygame.Surface:
    """Create and return a pygame window."""
    screen: pygame.Surface
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(caption)
    return screen

def main() -> None:
    """Obtain two file names from the user, open and slice up
       so the resulting image can be folded, accordian style,
       to create an optical illusion."""
    # Annotate and initialize variables
    SIZE: int = 480
    NUM_SLICES: int = 12
    screen: pygame.Surface
    background: pygame.Surface
    user_quit: bool = False
    e: pygame.event.Event
    clock: pygame.time.Clock = pygame.time.Clock()
    file_name_left: str
    file_name_right: str
    done: bool = False

    # Make a dummy window.
    screen = make_window(SIZE, SIZE, "Choose two faces, facing forward, 5.5 by 8")

    # Get the file names from the user.
    file_name_left = prompt_file()
    file_name_right = prompt_file()

    # Load the images.
    image_left = pygame.image.load(file_name_left).convert()
    image_right = pygame.image.load(file_name_right).convert()
    
    # Process events until the user chooses to quit.
    while not user_quit:
        # Loop 30 times per second
        clock.tick(30)
        for e in pygame.event.get():
            # Process a quit choice.
            if e.type == pygame.QUIT:
                user_quit = True

        if not done:
            done = True
            # Get size of the user's image.
            width: float = image_left.get_width() 
            height: float = image_left.get_height()
        
            slice_width = width / NUM_SLICES
            image_width = 2 * width + NUM_SLICES - 1
            image = pygame.Surface((image_width, height))

            x = 0
            for i in range(NUM_SLICES):
                # Blit a slice for the left image and slide image left
                image.blit(image_left, (x, 0))
                image_left.scroll(-int(slice_width))
                # Add tick marks
                pygame.draw.line(image, (0, 0, 0), (x+slice_width - 1, 0), (x+slice_width - 1, 10), 2)
                pygame.draw.line(image, (0, 0, 0), (x+slice_width - 1, height-10), (x+slice_width - 1, height), 2)
                # Blit a slice for the right image and slide image left
                x += slice_width + 1
                image.blit(image_right, (x, 0))
                image_right.scroll(-int(slice_width))
                # Add tick marks
                pygame.draw.line(image, (0, 0, 0), (x+slice_width - 1, 0), (x+slice_width - 1, 10), 2)
                pygame.draw.line(image, (0, 0, 0), (x+slice_width - 1, height-10), (x+slice_width - 1, height), 2)
                x += slice_width + 1
                
            # Resize the screen and blit the sliced image.
            screen = make_window(image_width, height, "Your finished image")
            screen.blit(image, (0, 0))

            pygame.image.save(image, "sliced_image.jpg")

        # Show the display.
        pygame.display.flip()

    pygame.quit()

main()
