"""Obtain a portrait and a skull image from the user and
   scale and superimpose the skull over the portrait,
   save and then create an accordian image of both for an optical
   illusion and save."""

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

def make_right_image(width: int, height: int, image: pygame.Surface, file_name_left: str,
                     skull: pygame.Surface,
                     screen: pygame.Surface) -> pygame.Surface:
    """Scale the skull and blit to a surface with appropriate transparency and
       return that surface."""

    # Load the image and find facial landmarks.
    facial_rec_image = face_recognition.load_image_file(file_name_left)
    face_landmarks_dict = face_recognition.face_landmarks(facial_rec_image)

    ##Calculate horizontal scale factor
    # Find the distance between the eye centers.
    throwaway_surf: pygame.Surface = pygame.Surface((width, height))
    left_eye_rect: pygame.Rect = pygame.draw.polygon(throwaway_surf,
                                                     (255, 0, 0), face_landmarks_dict[0]['left_eye'])
    right_eye_rect: pygame.Rect = pygame.draw.polygon(throwaway_surf,
                                                      (255, 0, 0), face_landmarks_dict[0]['right_eye'])
    portrait_eye_diff: int = right_eye_rect.centerx - left_eye_rect.centerx

    # Hard-coded value for the skull.  
    skull_eye_diff:int = 380
    # Use the eye difference as a scale factor to horizontally scale the skull
    width_scale_factor = portrait_eye_diff / skull_eye_diff
    skull_width = width_scale_factor * skull.get_width()

    ##Calculate vertical scale factor
    # Find the distance between the eyebrow tops and the chin bottom
    eyebrow_rect: pygame.Rect = pygame.draw.polygon(throwaway_surf,
                                                    (255, 0, 0), face_landmarks_dict[0]['left_eyebrow'])
    chin_rect: pygame.Rect = pygame.draw.polygon(throwaway_surf,
                                                    (255, 0, 0), face_landmarks_dict[0]['chin'])
    portrait_face_diff: int = chin_rect.bottom - eyebrow_rect.top

    # Hard-coded value for the skull.
    skull_face_diff:int = 870
    # Use the eyebrow-to-chin difference as a scale factor to vertically  scale the skull
    height_scale_factor = portrait_face_diff / skull_face_diff
    skull_height = height_scale_factor * skull.get_height()
    
    # Create a copy of the original image onto our final (return) surface.
    skull_image: pygame.Surface = pygame.Surface((width, height), pygame.SRCALPHA)
    skull_image.blit(image, (0,0))

    # Let's bug out the eyes
    left_eye = pygame.Surface(left_eye_rect.size, pygame.SRCALPHA)
    right_eye = pygame.Surface(right_eye_rect.size, pygame.SRCALPHA)
    bigger_left_eye = pygame.Surface((left_eye_rect.width * 1.5, left_eye_rect.height * 1.5), pygame.SRCALPHA)
    bigger_right_eye = pygame.Surface((right_eye_rect.width * 1.5, right_eye_rect.height * 1.5), pygame.SRCALPHA)
    left_eye.blit(image, (0,0), left_eye_rect)
    right_eye.blit(image, (0,0), right_eye_rect)
    pygame.transform.smoothscale(left_eye, (left_eye_rect.width * 1.5, left_eye_rect.height * 1.5), bigger_left_eye)
    pygame.transform.smoothscale(right_eye, (right_eye_rect.width * 1.5, right_eye_rect.height * 1.5), bigger_right_eye)
    leftx = left_eye_rect.left - ((bigger_left_eye.get_width() - left_eye.get_width()))
    lefty = left_eye_rect.top - ((bigger_left_eye.get_height() - left_eye.get_height()))
    rightx = right_eye_rect.left - ((bigger_right_eye.get_width() - right_eye.get_width()))
    righty = right_eye_rect.top - ((bigger_right_eye.get_height() - right_eye.get_height()))
    skull_image.blit(bigger_left_eye, (leftx, lefty))
    skull_image.blit(bigger_right_eye, (rightx, righty))
    
    # Scale the skull image to the correct size.
    scaled_skull_surface: pygame.Surface = pygame.Surface((skull_width, skull_height), pygame.SRCALPHA)

    # The newer smoothsale algorithm works much better to scale the image!
    pygame.transform.smoothscale(skull, (skull_width, skull_height), scaled_skull_surface)

# This code is useful if your image doesn't have an alpha channel.
##    # Unfortunately, once scaled, the white areas weren't white.  Messes with our colorkey.
##    # Fortunately, there is a "threshold" function that allows us to find all sorta-white pixels
##    # and make them white.
##    pygame.transform.threshold(scaled_skull_surface, scaled_skull_surface, (255, 255, 255, 255),
##                               (10,10,10, 10), (255, 255, 255, 255), inverse_set = True)
##
##    # Blit the skull with transparency to the skull image and return.
##    scaled_skull_surface.set_colorkey((255, 255, 255))
##    scaled_skull_surface.set_alpha(120)

    # Scale the skull blitting distance from the center left eye
    skull_left_eye_centerx: int = 253
    skull_left_eye_centery: int = 578
    scaled_x_distance = skull_left_eye_centerx * width_scale_factor
    scaled_y_distance = skull_left_eye_centery * height_scale_factor
    # Calculate the coordinate that's the scaled distance from the center of the left eye
    blit_x = left_eye_rect.centerx - scaled_x_distance
    blit_y = left_eye_rect.centery - scaled_y_distance
    skull_image.blit(scaled_skull_surface, (blit_x, blit_y))

    return skull_image

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
    screen = make_window(SIZE, SIZE, "Choose a face, facing forward, 5.5 by 8")

    # Get the file name from the user.
    file_name_left = prompt_file()

    # Show the image and prompt for the skull image.
    image_left: pygame.Surface = pygame.image.load(file_name_left).convert_alpha()
    screen = make_window(image_left.get_width(), image_left.get_height(), "Choose your preferred skull")
    screen.blit(image_left, (0, 0))

    # Get the skull file name from the user.
    file_name_skull = prompt_file()

    # Load the preferred skull.
    skull: pygame.Surface = pygame.image.load(file_name_skull).convert_alpha()

    
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

            # Create the superimposed skull image.
            image_right = make_right_image(width, height, image_left, file_name_left,
                                           skull,
                                           screen)
            pygame.image.save(image_right, "superimposed skull image.jpg")


            # Slice the two images together (with tick marks) and save.
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
