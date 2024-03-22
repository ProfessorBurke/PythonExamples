""" Dystopian face blimp
    A blimp running a video of your face drifts across the screen.
"""

# Imports and initialize pygame.
import random
import pygame
pygame.init()

# Import and initialize the camera.
import cv2

# Import facial recognition library.
import face_recognition

# Import numpy for manipulating the image.
import numpy as np

class VideoFeed():
    """A rectangular face image that updates from the webcam,
       glitching at random intervals to an advertisement."""

    # Object-level fields
    _video_capture: cv2.VideoCapture
    _default_image: pygame.Surface
    _glitch_interval: int
    _glitch_count: int
    _image: pygame.Surface

    def __init__(self) -> None:
        """Create the video capture object, init image
           to the default, set up glitch interval."""
        self._default_image = pygame.image.load("smaller_default.png").convert_alpha()
        self._video_capture = cv2.VideoCapture(0)
        self._image = self._default_image.copy()
        self._glitch_interval = random.randint(10, 20)
        self._glitch_count = 0
        if pygame.mixer:
            interference = pygame.mixer.Sound(file = "interference.mp3")
            interference.play()
            pygame.mixer.pause()

    def update(self) -> pygame.Surface:
        """Grab a new image from the webcam, resize, return."""
        self._glitch_count += 1
        # Glitch to the advertisement at random intervals,
        # play the glitch sound, reset the interval and count.
        if self._glitch_count == self._glitch_interval:
            self._glitch_count = 0
            self._glitch_interval = random.randint(10, 20)
            self._image = self._default_image
            if pygame.mixer:
                pygame.mixer.unpause()

        # Otherwise, get the camera image, find a face, if a face
        # is found, grab it, distort it, pause the glitch sound,
        # put the face on a surface.  If no face is found, glitch.
        else:
            ret, frame = self._video_capture.read()
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = small_frame[:, :, ::-1]
            face_locations = face_recognition.face_locations(rgb_small_frame)
            # Turn that into a Surface.  Some manipulation required.
            rgb_small_frame = np.swapaxes(rgb_small_frame, 0, 1)
            image = pygame.surfarray.make_surface(rgb_small_frame)
            if face_locations:
                if pygame.mixer:
                    pygame.mixer.pause()
                # Find one face, pull it out of the image, scale to screen size.
                face = face_locations[0]
                self._image = image.subsurface((face[3], face[0], face[1]-face[3],face[2]-face[0]))
                self._image = pygame.transform.scale(self._image, (133, 75))
            else:
                self._image = self._default_image
                if pygame.mixer:
                    pygame.mixer.unpause()
        return self._image
                
    def release_resources(self) -> None:
        """Release the video resources."""
        self._video_capture.release()


class Blimp(pygame.sprite.Sprite):
    """Blimp with your face."""

    # Annotate object-level fields
    _dx: int
    _reset_x: int
    _frame_image: pygame.Surface
    _video_feed: VideoFeed
    _default_image: pygame.Surface

    def __init__(self, dx: int, x: int, y: int) -> None:
        """Load the image and set location and motion."""
        super().__init__()
        # Load the blimp and frame images.
        self.image = pygame.image.load("blimp.png").convert_alpha()
        self._default_image = self.image.copy()
        self._frame_image = pygame.image.load("frame.png").convert_alpha()
        # Set location and motion variables
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self._dx = dx
        self._reset_x = x
        # Create the video feed
        self._video_feed = VideoFeed()

    def update(self, screen: pygame.Surface) -> None:
        """Move the blimp and update the image."""
        feed_surface: pygame.Surface
        # Move the blimp.
        self.rect.left += self._dx
        if self.rect.right < 0:
            self.rect.left = self._reset_x
        # Create the image.
        self.image = self._default_image.copy()
        feed_surface = self._video_feed.update()
        self.image.blit(feed_surface, (124, 68))
        self.image.blit(self._frame_image, (118, 66))

    def release_resources(self) -> None:
        """Release the video resources."""
        self._video_feed.release_resources()


class Background(pygame.sprite.Sprite):
    """Just the background."""

    def __init__(self, image: pygame.Surface) -> None:
        """Load the image and set dx."""
        super().__init__()
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()


def make_window(width: int, height: int, caption: str) -> pygame.Surface:
    """Create and return a pygame window."""
    screen: pygame.Surface
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(caption)
    return screen

def main() -> None:
    """Add a function description."""
    # Annotate and initialize variables
    WIDTH: int = 512
    HEIGHT: int = 512
    screen: pygame.Surface
    blimp: Blimp
    background_group: pygame.sprite.Group
    blimp_group: pygame.sprite.Group
    user_quit: bool = False
    e: pygame.event.Event
    caption: str = "Is that you?"
    
    # Set up assets.
    screen = make_window(WIDTH, HEIGHT, caption)
    background_group = pygame.sprite.Group(Background("background.jpg"))
    blimp = Blimp(-2, WIDTH + 30, 10)
    blimp_group = pygame.sprite.Group(blimp)
    clock: pygame.time.Clock = pygame.time.Clock()

    # Play the blimp's traveling hum.
    if pygame.mixer:
        pygame.mixer.music.load("low_hum.mp3")
        pygame.mixer.music.play()

    # Process events until the user chooses to quit.
    while not user_quit:
        # Loop 30 times per second
        clock.tick(30)

        for e in pygame.event.get():
            # Process a quit choice.
            if e.type == pygame.QUIT:
                user_quit = True

                    
        # Draw robot and background.
        background_group.update(screen)
        blimp_group.update(screen)
        background_group.draw(screen)
        blimp_group.draw(screen)
                
        # Show the display.
        pygame.display.flip()

    if pygame.mixer:
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()

    blimp.release_resources()
    pygame.quit()

main()
