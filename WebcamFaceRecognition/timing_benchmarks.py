"""
    Test the image manipulation algorithms for speed.
"""
# Import timing.
import timeit

# Import and initialize pygame.
import pygame
pygame.init()

# Import and initialize cv2 camera support.
import cv2

# Import facial recognition libraries.
from PIL import Image
from PIL import ImageDraw
import pkg_resources
import face_recognition_models
import face_recognition
import numpy as np

# Define the functions to time
def reshape_numpy(frame: np.ndarray) -> None:
    """Reshape the array using numpy swapaxes."""
    frame = np.swapaxes(frame, 0, 1)

def reshape_pygame(image: pygame.Surface) -> None:
    """Reshape the array using pygame transform methods."""
    image = pygame.transform.rotate(image, 270)
    image = pygame.transform.flip(image, True, False)

# Set up pygame so we can make Surface objects.
pygame.display.set_mode((480, 480))

# Grab a frame from the camera.
video_capture = cv2.VideoCapture(0)
ret, frame = video_capture.read()

# Set up some variables to use in the timing.
small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
small_image = pygame.surfarray.make_surface(small_frame)
large_image = pygame.surfarray.make_surface(frame)

# Time with the large ndarray and small ndarray and numpy
# manipulations.
print("640 x 480 image, numpy: ", end="")
print(timeit.timeit("reshape_numpy(frame)", setup="from __main__ import reshape_numpy",
                    globals=globals(), number=1000))
print("180 x 120 image, numpy: ", end="")
print(timeit.timeit("reshape_numpy(small_frame)", setup="from __main__ import reshape_numpy",
                    globals=globals(), number=1000))

# Time with the large Surface and small Surface and
# pygame manipulations.
print("640 x 480 image, pygame: ", end="")
print(timeit.timeit("reshape_pygame(large_image)", setup="from __main__ import reshape_pygame",
                    globals=globals(), number=1000))
print("180 x 120 image, pygame: ", end="")
print(timeit.timeit("reshape_pygame(small_image)", setup="from __main__ import reshape_pygame",
                    globals=globals(),number=1000))


video_capture.release()
cv2.destroyAllWindows()
pygame.quit()



