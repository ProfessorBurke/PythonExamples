"""Mess around with the facial recognition."""

# Import and initialize pygame, tkinter, and face recognition.
import pygame
import tkinter
import tkinter.filedialog
import PIL.Image
import PIL.ImageDraw
import face_recognition

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
    """Obtain images from the user, superimpose one over the other and then
       slice the two together.  Save both."""
    # Annotate and initialize variables
    SIZE: int = 480
    NUM_SLICES: int = 12
    screen: pygame.Surface
    background: pygame.Surface
    sprite: GenericSprite
    group: pygame.sprite.Group
    user_quit: bool = False
    e: pygame.event.Event
    clock: pygame.time.Clock = pygame.time.Clock()
    file_name_left: str
    done: bool = False

    # Make a dummy window.
    screen = make_window(SIZE, SIZE, "Choose a picture with at least one face")

    # Get the file name from the user.
    file_name = prompt_file()

    # Show the image and prompt for the skull image.
    image: pygame.Surface = pygame.image.load(file_name).convert_alpha()
    screen = make_window(image.get_width(), image.get_height(), "Now we'll have some fun")
    screen.blit(image, (0, 0))

    
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

            # Load the image and find facial landmarks.
            facial_rec_image = face_recognition.load_image_file(file_name)
            face_landmarks = face_recognition.face_landmarks(facial_rec_image)
            face_locations = face_recognition.face_locations(facial_rec_image)

            print(face_landmarks)
            for face in face_landmarks:
                pygame.draw.polygon(image, (255, 0, 0), face["left_eye"], width = 2)
                pygame.draw.polygon(image, (255, 0, 0), face["right_eye"], width = 2)
                pygame.draw.polygon(image, (255, 0, 0), face["left_eyebrow"], width = 2)
                pygame.draw.polygon(image, (255, 0, 0), face["right_eyebrow"], width = 2)
                pygame.draw.polygon(image, (255, 0, 0), face["nose_tip"], width = 2)
            for face in face_locations:
                pygame.draw.rect(image, (0, 255, 0),
                                 (face[3], face[0], face[1]-face[3],face[2]-face[0]),
                                  width = 2)
            screen.blit(image, (0, 0))
                


        # Show the display.
        pygame.display.flip()

    pygame.quit()

main()
