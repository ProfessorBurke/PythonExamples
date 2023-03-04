"""
    Tangram shape rotation.
"""
# Import libraries and initialize pygame.
import math
import pygame
pygame.init()


class Click(pygame.sprite.Sprite):
    """ Represents a click location as a sprite for collision detection."""
    
    def __init__(self, pos: tuple) -> None:
        """Initialize from the location tuple."""
        super().__init__()
        self.image = pygame.Surface((1, 1))
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def get_pos(self) -> tuple:
        """Return the location of the click."""
        return self.rect.center

    def set_pos(self, pos: tuple) -> None:
        """Set the location of the click to the new position."""
        self.rect.center = pos

class RotationControl(pygame.sprite.Sprite):
    """ A rotation control on a shape."""

    # Annotate object-level fields.
    _raw_image: pygame.Surface
    _radius: float
    _angle: float
    
    def __init__(self, image: pygame.Surface, shape_center: tuple,
                 radius: float, angle: float) -> None:
        """Initialize from image parameter and set location."""
        super().__init__()
        self.image = image
        self._raw_image = image
        self._radius = radius
        self._angle = angle
        self.rect = image.get_rect()
        self.rect.center = (shape_center[0] + radius * math.cos(math.radians(angle)),
                            shape_center[1] - radius * math.sin(math.radians(angle)))
        
        
    def rotate(self, by: int, shape_center: tuple) -> None:
        """Rotate and locate some magical values from center of shape, need
           to come up with a general algorithm for this."""
        self.image = pygame.transform.rotate(self._raw_image, by)
        self.rect = self.image.get_rect()
        self.rect.center = (shape_center[0] + self._radius * math.cos(math.radians(self._angle + by)),
                            shape_center[1] - self._radius * math.sin(math.radians(self._angle + by)))
        
    def move_by(self, diff: tuple) -> None:
        """Move by diff."""
        self.rect.top += diff[1]
        self.rect.left += diff[0]
        

class Shadow(pygame.sprite.Sprite):
    """ A shape's shadow."""

    # Annotate object-level variables
    _raw_image: pygame.Surface
    
    def __init__(self, image: pygame.Surface, x: int, y: int,
                 rotation: int) -> None:
        """Initialize from parameters, locate, and rotate."""
        super().__init__()
        image.set_alpha(100)
        self.image = image
        self._raw_image = image
        self.rect = image.get_rect()
        self.rect.topleft = (x, y)
        self.rotate(rotation)

    def rotate(self, rotation: float) -> None:
        """Rotate raw image by rotation and set."""
        center: tuple = self.rect.center
        self.image = pygame.transform.rotate(self._raw_image, rotation)
        self.rect = self.image.get_rect()
        self.rect.center = center

    def move_by(self, diff: tuple) -> None:
        """Move by diff."""
        self.rect.top += diff[1]
        self.rect.left += diff[0]
        

class Shape(pygame.sprite.Sprite):
    """A tangram shape.  It can be picked up, dropped, and rotated."""

    # Annotate fields

    def _draw_to_image(self) -> None:
        """Private method to draw the shape at its current rotation and location
           to its image and obtain and recenter its rectangle."""
        center: tuple = self.rect.center
        self.image = pygame.transform.rotate(self._raw_image, self._rotation)
        self.rect = self.image.get_rect()
        self.rect.center = center

    def _calculate_angle_arctan2(self, loc: tuple) -> None:
        """Use arctan2 to calculate the angle of a location."""
        # x1, y1 is the center of the shape; x2, y2 is the mouse location
        y1 = self.rect.centery
        y2 = loc[1]
        x1 = self.rect.centerx
        x2 = loc[0]
        # Calculate the angle
        angle: float
        if x2 - x1 == 0:
            # If we're on the y axis, rotation is 90 or -90
            angle = 90 if y2 < y1 else -90
        else:
            print(-math.degrees(math.atan2((y2-y1),(x2-x1))))
            print(-math.degrees(math.atan((y2-y1)/(x2-x1))))
            print()
            angle = -math.degrees(math.atan2((y2-y1),(x2-x1))) 
        return angle
        
    
    def __init__(self, image: pygame.Surface,
                 shadow: Shadow,
                 controls: list,
                 x: int, y: int) -> None:
        """Initialize the image from parameters, create the Shadow and controls."""
        super().__init__()
        self._raw_image = image
        self.image = image
        self.rect = image.get_rect()
        self.rect.topleft = (x, y)
        self._rotation = 0
        self._shadow = shadow
        self._start_rotation_angle = 0
        self._moving = False
        self._controls = controls
        self._controls_group = pygame.sprite.Group(controls)
        self._rotating = False

    def handle_mouse_down(self, click: Click, shadow_group: pygame.sprite.Group) -> None:
        """Change state to moving or rotating, add shadow to sprite group for shadows."""
        shadow_group.add(self._shadow)
        clicked_shape = pygame.sprite.spritecollide(click, self._controls_group, False,
                             collided = pygame.sprite.collide_mask)
        if clicked_shape:
            self._rotating = True
            self._start_rotation_angle = (self._calculate_angle_arctan2(click.get_pos())
                                          - self._rotation)
        else:
            self._moving = True

    def handle_mouse_up(self) -> None:
        """Change state to not moving, not rotating on mouse release."""
        self._moving = False
        self._rotating = False
        self._start_rotation_angle = 0

    def handle_mouse_motion(self, diff: tuple, mouse_loc: tuple) -> None:
        """Handle moving or rotating."""
        if self._moving:
            self.rect.top += diff[1]
            self.rect.left += diff[0]
            self._shadow.move_by(diff)
            for control in self._controls:
                control.move_by(diff)
        elif self._rotating:
            # Calculate the angle between the mouse at the start 
            # of the rotation and the current location of the mouse
            self._rotation = (self._calculate_angle_arctan2(mouse_loc)
                              - self._start_rotation_angle)
            self._draw_to_image()
            # Send the rotation message to the shadow and the control(s).
            self._shadow.rotate(self._rotation)
            for control in self._controls:
                control.rotate(self._rotation, self.rect.center)


# Define constants and annotate variables.
LARGE_TRIANGLE_UPPER_CONTROL_RADIUS: int = 190
LARGE_TRIANGLE_UPPER_LEFT_CONTROL_ANGLE: int = 153
LARGE_TRIANGLE_UPPER_RIGHT_CONTROL_ANGLE: int = 27
LARGE_TRIANGLE_LOWER_CONTROL_RADIUS: int = 84
LARGE_TRIANGLE_LOWER_CONTROL_ANGLE: int = 270

SQUARE_LOWER_RIGHT_CONTROL_ANGLE: int = 315
SQUARE_LOWER_LEFT_CONTROL_ANGLE: int = 225
SQUARE_UPPER_RIGHT_CONTROL_ANGLE: int = 45
SQUARE_UPPER_LEFT_CONTROL_ANGLE: int = 135
SQUARE_RADIUS: int = 82


screen: pygame.Surface
user_quit: bool
event: pygame.event.Event
background: pygame.Surface
shapes: list
shapes_group: pygame.sprite.Group
shadow_group: pygame.sprite.Group
current_shape: Shape = None
large_triangle_shadow_image: pygame.Surface 
large_triangle_control_image: pygame.Surface
large_triangle_image: pygame.Surface
large_triangle_center: tuple
square_shadow_image: pygame.Surface 
square_control_image: pygame.Surface
square_image: pygame.Surface
square_center: tuple

# Create a pygame window.
screen = pygame.display.set_mode((1024, 1024))
pygame.display.set_caption("Tangrams")

# Load large triangle assets.
large_triangle_shadow_image = pygame.image.load("large_triangle_shadow.png")
large_triangle_control_image = pygame.transform.scale(large_triangle_shadow_image,(70,35))
large_triangle_image = pygame.image.load("large_triangle.png")
large_triangle_center = (20 + large_triangle_image.get_width() / 2,
                         20 + large_triangle_image.get_height() / 2)

# Load square assets.
square_shadow_image = pygame.image.load("square_shadow.png")
square_control_image = pygame.transform.scale(square_shadow_image,(30,30))
square_image = pygame.image.load("square.png")
square_center = (20 + square_image.get_width() / 2,
                         200 + square_image.get_height() / 2)

# Load and blit the background.
background = pygame.image.load("rabbit_background.png")
screen.blit(background, (0, 0))

# Create the shapes.
shapes = [Shape(large_triangle_image,
          Shadow(large_triangle_shadow_image, 20+10, 20+10, 0),
          [RotationControl(large_triangle_control_image,
                            large_triangle_center , LARGE_TRIANGLE_UPPER_CONTROL_RADIUS,
                            LARGE_TRIANGLE_UPPER_LEFT_CONTROL_ANGLE),
           RotationControl(large_triangle_control_image,
                            large_triangle_center, LARGE_TRIANGLE_UPPER_CONTROL_RADIUS,
                            LARGE_TRIANGLE_UPPER_RIGHT_CONTROL_ANGLE),
           RotationControl(large_triangle_control_image,
                            large_triangle_center, LARGE_TRIANGLE_LOWER_CONTROL_RADIUS,
                            LARGE_TRIANGLE_LOWER_CONTROL_ANGLE)],
          20,20),
          Shape(square_image,
          Shadow(square_shadow_image, 20+10, 200+10, 0),
          [RotationControl(square_control_image,
                            square_center , SQUARE_RADIUS,
                            SQUARE_UPPER_LEFT_CONTROL_ANGLE),
           RotationControl(square_control_image,
                            square_center, SQUARE_RADIUS,
                            SQUARE_UPPER_RIGHT_CONTROL_ANGLE),
           RotationControl(square_control_image,
                            square_center, SQUARE_RADIUS,
                            SQUARE_LOWER_LEFT_CONTROL_ANGLE),
           RotationControl(square_control_image,
                            square_center, SQUARE_RADIUS,
                            SQUARE_LOWER_RIGHT_CONTROL_ANGLE)],
          20,200)]
shapes_group = pygame.sprite.Group(shapes)
shadow_group = pygame.sprite.Group()

# Process dragging to move and rotate the shape, or quit.
user_quit = False
while not user_quit:
    # Process events
    for event in pygame.event.get():
        # Process a quit choice.
        if event.type == pygame.QUIT:
            user_quit = True
        # Process a mousedown by picking up the shape.
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # If the click is in a shape, let the shape handle the click.
            click = Click(event.__dict__["pos"]) 
            clicked_shape = pygame.sprite.spritecollide(click, shapes, False,
                             collided = pygame.sprite.collide_mask)
            if clicked_shape:
                current_shape = clicked_shape[0]
                current_shape.handle_mouse_down(click, shadow_group)
        elif event.type == pygame.MOUSEBUTTONUP:
            # Inform the selected shape of the mouse release and empty the shadow group.
            if current_shape != None:
                current_shape.handle_mouse_up()
                current_shape = None
                shadow_group.empty()
        elif event.type == pygame.MOUSEMOTION:
            # Move or rotate depending on where the mousedown was.
            if current_shape != None:
                current_shape.handle_mouse_motion(event.__dict__["rel"],
                                               event.__dict__["pos"])

    # Draw
    shadow_group.clear(screen, background)
    shapes_group.clear(screen, background)
    # Temporary measure -- controls won't be drawn in the final game.
    for shape in shapes:
        shape._controls_group.clear(screen, background)
    shadow_group.update()
    shapes_group.update()
    shadow_group.draw(screen)
    shapes_group.draw(screen)
    for shape in shapes:
        shape._controls_group.draw(screen)#temporary
           
    # Show the drawing.
    pygame.display.flip()

pygame.quit()




