"""
    Tangram -- implementing snap to puzzle prototype.
"""
# Import libraries and initialize pygame.
import math
import pygame
pygame.init()

class Puzzle(pygame.sprite.Sprite):
    """Represents a puzzle (configuration of pieces) that the user is solving."""

    # Annotate object-level fields
    _pieces: pygame.sprite.Group
    
    def __init__(self, pieces: pygame.sprite.Group, pos: tuple) -> None:
        """Initialize the puzzle from parameters."""
        super().__init__()
        self.image = pygame.Surface(pieces[0].rect.size)
        self.image.fill((255, 255, 255))
        self.image.blit(pieces[0].image, (0, 0))
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self._pieces = pieces

    def get_adjusted_rect(self, shape: "Shape") -> pygame.Rect:
        """Return a new rectangle if the piece overlaps enough with a piece
           in the puzzle."""
        return_rect: pygame.Rect = shape.rect
        piece_mask: pygame.mask
        area: float
        shape_mask: pygame.mask = pygame.mask.from_surface(shape.image)
        collided_pieces: list = pygame.sprite.spritecollide(shape,
                                                            self._pieces,
                                                            False,
                                                            collided = pygame.sprite.collide_mask)
        for piece in collided_pieces:
            piece_mask = pygame.mask.from_surface(piece.image)
            area = shape_mask.overlap_area(piece_mask, (shape.rect.x - piece.rect.x,
                                                        shape.rect.y - piece.rect.y))
            area = area / shape_mask.overlap_area(shape_mask, (0, 0)) * 100
            print(area)
            if area >= 90:
                print("snapping")
                return_rect = piece.rect.copy()
            
        return return_rect

            
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

class Shadow(pygame.sprite.Sprite):
    """ A shape's shadow."""

    # Annotate object-level variables
    _raw_image: pygame.Surface
    
    def __init__(self, image: pygame.Surface, x: int, y: int) -> None:
        """Initialize from parameters, locate, and rotate."""
        super().__init__()
        image.set_alpha(100)
        self.image = image
        self._raw_image = image
        self.rect = image.get_rect()
        self.rect.topleft = (x, y)

    def move_by(self, diff: tuple) -> None:
        """Move by diff."""
        self.rect.top += diff[1]
        self.rect.left += diff[0]
        

class Shape(pygame.sprite.Sprite):
    """A tangram shape.  It can be picked up and dropped."""
    
    def __init__(self, image: pygame.Surface,
                 shadow: Shadow,
                 x: int, y: int) -> None:
        """Initialize the image from parameters, create the Shadow and controls."""
        super().__init__()
        self.image = image
        self.rect = image.get_rect()
        self.rect.topleft = (x, y)
        self._shadow = shadow
        self._moving = False

    def handle_mouse_down(self, click: Click, shadow_group: pygame.sprite.Group) -> None:
        """Change state to moving or rotating, add shadow to sprite group for shadows."""
        # Add the shadow to the shadow group so it can be drawn.
        shadow_group.add(self._shadow)
        # Set the moving flag.
        self._moving = True

    def handle_mouse_up(self, shapes: pygame.sprite.Group, puzzle: Puzzle) -> None:
        """Change state to not moving on mouse release."""
        self._moving = False
        self.rect = puzzle.get_adjusted_rect(self)

    def handle_mouse_motion(self, diff: tuple, mouse_loc: tuple) -> None:
        """Handle moving or rotating."""
        if self._moving:
            self.rect.top += diff[1]
            self.rect.left += diff[0]
            self._shadow.move_by(diff)


screen: pygame.Surface
user_quit: bool
event: pygame.event.Event
background: pygame.Surface
shapes_group: pygame.sprite.Group
shadow_group: pygame.sprite.Group
active_shape_group: pygame.sprite.Group
current_shape: Shape = None
large_triangle_shadow_image: pygame.Surface 
large_triangle_image: pygame.Surface
large_triangle_center: tuple

# Create a pygame window.
screen = pygame.display.set_mode((1024, 1024))
pygame.display.set_caption("Tangrams")

# Load large triangle assets.
large_triangle_shadow_image = pygame.image.load("large_triangle_shadow.png")
large_triangle_image = pygame.image.load("large_triangle.png")
large_triangle_center = (20 + large_triangle_image.get_width() / 2,
                         20 + large_triangle_image.get_height() / 2)

# Load and blit the background.
background = pygame.image.load("rabbit_background.png")
screen.blit(background, (0, 0))

# Create the shapes.
shapes = [Shape(large_triangle_image,
          Shadow(large_triangle_shadow_image, 20+10, 20+10),
          20,20)]
shapes_group = pygame.sprite.Group(shapes)
shadow_group = pygame.sprite.Group()
active_shape_group = pygame.sprite.Group()

# Create the puzzle and puzzle group.
puzzle: Puzzle = Puzzle([Shadow(large_triangle_shadow_image, 500, 500)], (500, 500))
puzzle_group: pygame.sprite.Group = pygame.sprite.Group(puzzle)

# Process dragging to move the shape, or quit.
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
            # Remove the shape from the shapes group and add to the
            # active shapes group.
            click = Click(event.__dict__["pos"]) 
            clicked_shape = pygame.sprite.spritecollide(click, shapes, False,
                             collided = pygame.sprite.collide_mask)
            if clicked_shape:
                current_shape = clicked_shape[0]
                active_shape_group.add(current_shape)
                shapes_group.remove(current_shape)
                current_shape.handle_mouse_down(click, shadow_group)
        elif event.type == pygame.MOUSEBUTTONUP:
            # Inform the selected shape of the mouse release,
            # then remove the selected shape from the active shape group
            # and add it back in to the shapes group
            # and empty the shadow group.
            if current_shape != None:
                current_shape.handle_mouse_up(shapes_group, puzzle)
                shapes_group.add(current_shape)
                active_shape_group.empty()
                current_shape = None
                shadow_group.empty()
        elif event.type == pygame.MOUSEMOTION:
            # Move or rotate depending on where the mousedown was.
            if current_shape != None:
                current_shape.handle_mouse_motion(event.__dict__["rel"],
                                               event.__dict__["pos"])

    # Draw
    puzzle_group.clear(screen, background)
    shadow_group.clear(screen, background)
    shapes_group.clear(screen, background)
    active_shape_group.clear(screen, background)

    puzzle_group.update()
    shadow_group.update()
    shapes_group.update()
    active_shape_group.update()

    puzzle_group.draw(screen)
    shadow_group.draw(screen)
    shapes_group.draw(screen)
    active_shape_group.draw(screen)
    
           
    # Show the drawing.
    pygame.display.flip()

pygame.quit()




