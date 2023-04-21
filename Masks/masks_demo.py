"""
    Masks demo.
"""
# Import libraries and initialize pygame.
import typing
import pathlib
import pygame
import random
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

class Shadow(pygame.sprite.Sprite):
    """ An item's shadow."""
    
    def __init__(self, image: pygame.Surface, loc: tuple) -> None:
        """Initialize from parameters, locate, and rotate."""
        super().__init__()
        self.image = image
        self.rect = image.get_rect()
        self.rect.topleft = loc

    def move_by(self, diff: tuple) -> None:
        """Move by diff."""
        self.rect.top += diff[1]
        self.rect.left += diff[0]

class Glow(Shadow):
    """A glow -- an alternative to a shadow."""
    def __init__(self, image: pygame.Surface, loc: tuple) -> None:
        """Initialize from parameters, locate, and rotate."""
        super().__init__(image, loc)
        self.rect.center = loc
        

class Item(pygame.sprite.Sprite):
    """An item.  It can be picked up and dropped."""

    def _make_glow(self) -> Glow:
        """Make a glow for the item."""
        
        mask_surface: pygame.Surface
        glow: pygame.Surface
        inner_glow: pygame.Surface
        scale: float
        i: int

        # Create a surface from the mask that's almost transparent yellow
        # and scale to the outer size of the glow.
        mask_surface = self.mask.to_surface(setcolor = (255, 255, 0, 25),
                                            unsetcolor = None)
        glow = pygame.transform.scale(mask_surface, (self.rect.width * 1.3,
                                                     self.rect.height * 1.3))
        # Scale ten times and blit to the outer glow for a gradient.
        for i in range(1, 11):
            scale = 1 + i * 0.029
            inner_glow = pygame.transform.scale(mask_surface, (self.rect.width * scale,
                                                               self.rect.height * scale))
            glow.blit(inner_glow, ((glow.get_width() - inner_glow.get_width())/2,
                                   (glow.get_height() - inner_glow.get_height())/2))
        return Glow(glow, self.rect.center)
        
    
    def __init__(self, image: pygame.Surface,
                 x: int, y: int) -> None:
        """Initialize the image from parameters, create the Shadow and controls."""
        super().__init__()
        self.image = image
        self.rect = image.get_rect()
        self.mask = pygame.mask.from_surface(image)
        self._shadow = Shadow(self.mask.to_surface(setcolor = (0, 0, 0, 150), unsetcolor = None),
                              (x + 10, y + 10))
        self.rect.topleft = (x, y)
        self._moving = False
        self._glow = self._make_glow()

    def handle_mouse_down(self, click: Click, effect_group: pygame.sprite.Group) -> None:
        """Change state to moving or rotating, add shadow to sprite group for shadows."""
        # Add the shadow or the glow to the shadow group so it can be drawn.
        effect_group.add(self._glow)
        # Set the moving flag.
        self._moving = True

    def handle_mouse_up(self, shapes: pygame.sprite.Group) -> None:
        """Change state to not moving on mouse release."""
        self._moving = False
        loc: tuple = self.rect.center
        self.image = pygame.transform.scale(self.image,
                                            (self.rect.width * .5, self.rect.height * .5))
        self.rect = self.image.get_rect()
        self.rect.center = loc
        self.mask = pygame.mask.from_surface(self.image)
        self._shadow = Shadow(self.mask.to_surface(setcolor = (0, 0, 0, 150), unsetcolor = None),
                              (self.rect.x + 5, self.rect.y + 5))
        self._glow = self._make_glow()


    def handle_mouse_motion(self, diff: tuple, mouse_loc: tuple) -> None:
        """Handle moving or rotating."""
        if self._moving:
            self.rect.top += diff[1]
            self.rect.left += diff[0]
            self._shadow.move_by(diff)
            self._glow.move_by(diff)


class SharpItem(Item):
    """An item you shouldn't pick up by the sharp edge."""

    # Annotate object-level field
    _sharp_mask: pygame.mask

    def __init__(self, image: pygame.Surface, threshold_image: pygame.Surface, 
                 x: int, y: int) -> None:
        """Initialize the image from parameters, create the Shadow and controls."""
        super().__init__(image, x, y)
        # Create the mask for the sharp part.
        self._sharp_mask = pygame.mask.from_threshold(threshold_image, (255, 0, 0), (1, 1, 1))

    def handle_mouse_down(self, click: Click, effect_group: pygame.sprite.Group) -> None:
        """Change state to moving or rotating, add shadow to sprite group for shadows."""
        old_mask: pygame.mask = self.mask
        self.mask = self._sharp_mask
        if pygame.sprite.spritecollide(click, pygame.sprite.Group(self), False,
                                       collided = pygame.sprite.collide_mask):
            print("Ouch!")
        else:
            # Add the shadow or the glow to the shadow group so it can be drawn.
            effect_group.add(self._glow)
            # Set the moving flag.
            self._moving = True
        self.mask = old_mask

    def handle_mouse_up(self, shapes: pygame.sprite.Group) -> None:
        """Change state to not moving on mouse release."""
        self._moving = False
 

screen: pygame.Surface
user_quit: bool
event: pygame.event.Event
background: pygame.Surface
items_group: pygame.sprite.Group
effect_group: pygame.sprite.Group
active_item_group: pygame.sprite.Group
current_item: Item = None
current: pathlib.Path
filepath: pathlib.Path

# Create a pygame window.
screen = pygame.display.set_mode((1500, 800))
pygame.display.set_caption("Masks demo")

# Load and blit the background.
background = pygame.Surface((1500, 800))
background.fill((255, 255, 255))
screen.blit(background, (0, 0))

# Create the items by getting all files from the items directory
# and using them for Item images.
items_group = pygame.sprite.OrderedUpdates()

# Make the axe and add it to the items group.
items_group.add(SharpItem(pygame.image.load("axe.png"),
                          pygame.image.load("axe_thresholds.png"),
                          random.randint(0, 1000), random.randint(0, 400)))
# Create the other items.
current = pathlib.Path("items")
for filepath in current.iterdir():
    items_group.add(Item(pygame.image.load(filepath), random.randint(0, 1000),
                         random.randint(0, 400)))
                    
# Crate the shadow group and active item group for picking up items.
effect_group = pygame.sprite.Group()
active_item_group = pygame.sprite.Group()

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
            # If the click is in an item, let the item handle the click.
            # Remove the item from the items group and add to the
            # active items group.
            click = Click(event.__dict__["pos"]) 
            clicked_item = pygame.sprite.spritecollide(click, items_group, False,
                                                       collided = pygame.sprite.collide_mask)
            if clicked_item:
                current_item = clicked_item[0]
                active_item_group.add(current_item)
                items_group.remove(current_item)
                current_item.handle_mouse_down(click, effect_group)
        elif event.type == pygame.MOUSEBUTTONUP:
            # Inform the selected item of the mouse release,
            # then remove the selected item from the active item group
            # and add it back in to the items group
            # and empty the shadow group.
            if current_item != None:
                current_item.handle_mouse_up(items_group)
                items_group.add(current_item)
                active_item_group.empty()
                current_item = None
                effect_group.empty()
        elif event.type == pygame.MOUSEMOTION:
            # Move the item.
            if current_item != None:
                current_item.handle_mouse_motion(event.__dict__["rel"],
                                               event.__dict__["pos"])

    # Draw
    items_group.clear(screen, background)
    effect_group.clear(screen, background)
    active_item_group.clear(screen, background)
    
    items_group.update()
    effect_group.update()
    active_item_group.update()
    
    items_group.draw(screen)
    effect_group.draw(screen)
    active_item_group.draw(screen)
              
    # Show the drawing.
    pygame.display.flip()

pygame.quit()




