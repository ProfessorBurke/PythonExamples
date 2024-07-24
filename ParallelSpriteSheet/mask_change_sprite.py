"""
    Demonstrate how to load in a sprite sheet animation,
    and create a mask for the hair that will allow us to
    change the pixel values for the hair.
"""

# Import and initialize pygame and the random library.
import random
import pygame
pygame.init()

# Import the enum type and define constants.
from enum import Enum

# Movement constants.
class Motion(Enum):
    LEFT = 0
    RIGHT = 1
    NOT_MOVING = 2

class EquippedSprite(pygame.sprite.Sprite):
    """A player-controlled character with swappable gear."""

    # Annotate object-level fields
    _images: list[pygame.Surface]
    _dx: int
    _facing_right: bool
    _image_index: int
    _hair_masks: list[pygame.mask.Mask]

    def _create_image(self) -> None:
        """Create the image without doing any rectangle changes."""
        self.image: pygame.Surface = self._images[self._image_index].copy()

    def _update_image(self) -> None:
        """Set the character's image according to the type of hat."""
        self._create_image()
        if not self._facing_right:
            self.image = pygame.transform.flip(self.image, True, False)
        center: tuple = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center

    def __init__(self) -> None:
        """Initialize from parameters."""
        super().__init__()
        # Load in the sprite sheet
        self._images = []
        self._hair_masks = []

        for i in range(6):
            image = pygame.image.load("sprite_images/"+str(i)+".png").convert_alpha()
            self._images.append(image)
            self._hair_masks.append(pygame.mask.from_threshold(image, (254, 206, 0),
                                                     (25, 100, 5, 0)))

        self._image_index = 5

        # Create the image and rectangle.
        self._create_image()
        # Locate the sprite.
        self.rect = self.image.get_rect()
        self.rect.topleft = (10, 300)
        # Set the walking speed and direction.
        self._facing_right = True
        self._dx = 0

    def process_move_command(self, move_command: int) -> None:
        """Process a command from the user."""
        if move_command == Motion.LEFT:
            self._dx = -5
            self._facing_right = False
            self.image = pygame.transform.flip(self.image, True, False)
        elif move_command == Motion.RIGHT:
            self._dx = 5
            self._facing_right = True
        elif move_command == Motion.NOT_MOVING:
            self._dx = 0

    def change_hair(self) -> None:
        """Toggle through hair changes."""
        # For every image in the sprite sheet, change
        # the hair color to a new random color.
        new_hair: tuple = (random.randint(0, 255),
                           random.randint(0, 255),
                           random.randint(0, 255), 255)
        for i in range(len(self._images)):
            image = self._images[i]
            # Create a new surface to hold the modified image
            new_image = image.copy()

            # Iterate over every pixel in the surface
            for x in range(image.get_width()):
                for y in range(image.get_height()):
                    # If the pixel is within the hair mask for this sprite,
                    # change it to the new random color.
                    if self._hair_masks[i].get_at((x, y)):
                        new_image.set_at((x, y), new_hair)
            self._images[i] = new_image


    def update(self) -> None:
        """Change location by dx and update image according to animation."""
        self.rect.x += self._dx
        if self._dx != 0:
            self._image_index  = (self._image_index + 1) % len(self._images)
        else:
            self._image_index = 5
        self._update_image()


def make_window(width: int, height: int, caption: str) -> pygame.Surface:
    """Create and return a pygame window."""
    screen: pygame.Surface
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(caption)
    return screen

def main() -> None:
    """The arrow keys move the character, the space bar changes its appearance."""
    
    # Annotate and initialize variables.
    # Screen and character variables.
    SCREEN_WIDTH: int = 800
    SCREEN_HEIGHT: int = 600
    screen: pygame.Surface
    background: pygame.Surface
    player: EquippedSprite
    player_group: pygame.sprite.Group

    # Game loop variables.
    user_quit: bool = False
    e: pygame.event.Event

    
    # Set up assets.
    # Create the window and give it a white background.
    screen = make_window(SCREEN_WIDTH, SCREEN_HEIGHT, "Arrow keys to move; space bar for appearance")
    background: pygame.Surface = pygame.Surface((800, 600))
    background.fill((255, 255, 255))
    
    # Load base player image and put it in a group.
    player = EquippedSprite()
    player_group = pygame.sprite.Group(player)

    # Run the game loop.
    clock: pygame.time.Clock = pygame.time.Clock()
    while not user_quit:
        # Loop 30 times per second
        clock.tick(30)

        # What does the player want to do?  Grab the events.
        for e in pygame.event.get():
            # Process a quit choice.
            if e.type == pygame.QUIT:
                user_quit = True
            elif e.type == pygame.KEYDOWN:
                # Process movement arrow keys.
                if e.__dict__["key"] == pygame.K_LEFT:
                    player.process_move_command(Motion.LEFT)
                elif e.__dict__["key"] == pygame.K_RIGHT:
                    player.process_move_command(Motion.RIGHT)
                # Process a space bar press by changing hats.
                elif e.__dict__["key"] == pygame.K_SPACE:
                    player.change_hair()
            elif e.type == pygame.KEYUP:
                if (not pygame.key.get_pressed()[pygame.K_LEFT] 
                        and not pygame.key.get_pressed()[pygame.K_RIGHT]):
                    player.process_move_command(Motion.NOT_MOVING)


        # Redraw and show.
        screen.blit(background, (0, 0))
        player_group.update()
        player_group.draw(screen)
        pygame.display.flip()

         
    pygame.quit()

main()
