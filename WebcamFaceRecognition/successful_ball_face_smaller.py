"""Obtain the user's face from the webcam using face_recognition
   and blit it to a bouncing ball."""

# Import and initialize pygame.
import pygame
pygame.init()

# Import and initialize the camera.
import cv2

# Import facial recognition libraries.
import face_recognition
import numpy as np

def make_window(width: int, height: int, caption: str) -> pygame.Surface:
    """Create and return a pygame window."""
    screen: pygame.Surface
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(caption)
    return screen

def main() -> None:
    """Move an image randomly on the screen."""
    # Annotate and initialize variables.
    SCREEN_SIZE: int = 480
    screen: pygame.Surface
    background: pygame.Surface
    ball = pygame.Surface((70,70))
    ball_mask: pygame.Surface
    ball_width: int = ball.get_width()
    ball_height: int = ball.get_height()
    user_quit: bool = False
    e: pygame.event.Event
    x: int = 0
    y: int = 0
    dx: int = 5
    dy: int = 5
    count: int = 0

    # Get a reference to webcam #0 (the default one)
    video_capture = cv2.VideoCapture(0)
    
    # Set up assets.
    screen = make_window(SCREEN_SIZE, SCREEN_SIZE, "Basic Motion")
    background = pygame.Surface((SCREEN_SIZE, SCREEN_SIZE))
    background.fill((222, 237, 244))
    clock: pygame.time.Clock = pygame.time.Clock()

    # Create the mask that we'll use to make the face round
    # and set the "face" to the mask until we have a camera image.
    ball_mask = pygame.image.load("ballMask.png").convert_alpha()
    face_image = ball_mask

    while not user_quit:
        # Loop 30 times per second
        clock.tick(30)

        for e in pygame.event.get():
            # Process a quit choice.
            if e.type == pygame.QUIT:
                user_quit = True

        # Using the pattern from the example at
        # https://github.com/ageitgey/face_recognition/blob/master/examples/facerec_from_webcam_faster.py
        # Processing every other frame and reducing the frame size
        # by 1/4 to speed processing.
        if count % 2 == 0:
            count = 0
            
            # When the camera's ready, get the camera image
            ret, frame = video_capture.read()

            # Reduce to 1/4 size, convert to rgb, and find the face.
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = small_frame[:, :, ::-1]
            face_locations = face_recognition.face_locations(rgb_small_frame)

            # Turn that into a Surface.  Some manipulation required.
            rgb_small_frame = np.swapaxes(rgb_small_frame, 0, 1)
            image = pygame.surfarray.make_surface(rgb_small_frame)
            # This code is equivalent to swapaxes but much, much slower:
            #image = pygame.transform.rotate(image, 270)
            #image = pygame.transform.flip(image, True, False)
            # Convert_alpha so we can use a mask to get a round shape
            image = image.convert_alpha()
            background.blit(image, (0, 0))

            # Find the first face and blit to a new Surface, then scale
            # to the size of the ball and blit.
            if face_locations:
                # Find one face, pull it out of the image, scale to ball size,
                # (apologies for magic numbers), and blit as a circle.
                face = face_locations[0]
                face_image = image.subsurface((face[3], face[0], face[1]-face[3],face[2]-face[0]))
                face_image = pygame.transform.scale(face_image, (70, 70))
                face_image.blit(ball_mask, (0, 0), None, pygame.BLEND_RGBA_MULT)
                
                
        count += 1
        
        # Move the ball.
        # Change x and y.
        x += dx
        y += dy
        
        # Check boundaries and adjust.
        if x < 0:
            x = 0
            dx *= -1
        elif x + ball.get_width() > screen.get_width():
            x = screen.get_width() - ball.get_width()
            dx *= -1
        if y < 0:
            y = 0
            dy *= -1
        elif y + ball.get_height() > screen.get_height():
            y = screen.get_height() - ball.get_height()
            dy *= -1

                 
        # Draw the ball to the screen and show.
        screen.blit(background, (0, 0))
        screen.blit(face_image, (x, y))
        pygame.display.flip()

    # Release the resources
    video_capture.release()
    cv2.destroyAllWindows() # probably not necessary?
    pygame.quit()

main()
