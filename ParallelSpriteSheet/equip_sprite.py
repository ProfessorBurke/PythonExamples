"""
    Demonstrate how to load in a sprite sheet animation, along
    with sprite equipment that can be swapped out in parallel
    lists with the sprite sheet.
"""

# Import and initialize pygame.
import pygame
pygame.init()

# Import the enum type and define constants.
from enum import Enum

# Hat type constants.
class HatType(Enum):
    PITH = 0
    HIPSTER = 1
    NONE = 2

    def __next__(self) -> "HatType":
        """Return the next element in the enum, or first element if at the end."""
        members: list[HatType]
        index: int
        next_index: int
        
        members = list(type(self))
        index = members.index(self)
        next_index = (index + 1) % len(members)
        return members[next_index]

# Movement constants.
class Motion(Enum):
    LEFT = 0
    RIGHT = 1
    NOT_MOVING = 2

class EquippedSprite(pygame.sprite.Sprite):
    """A player-controlled character with swappable gear."""

    # Annotate object-level fields
    _images: list[pygame.Surface]
    _pith: list[pygame.Surface]
    _hipster: list[pygame.Surface]
    _dx: int
    _facing_right: bool
    _image_index: int
    _hat_type: HatType

    def _create_image(self) -> None:
        """Create the image without doing any rectangle changes."""
        self.image: pygame.Surface = self._images[self._image_index].copy()        
        if self._current_hat == HatType.PITH:
            self.image.blit(self._pith[self._image_index], (0,0))
        elif self._current_hat == HatType.HIPSTER:
            self.image.blit(self._hipster[self._image_index], (0,0))

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
        # Load in the sprite sheets
        self._current_hat = HatType.PITH
        self._images = []
        self._pith = []
        self._hipster = []
        for i in range(6):
            image = pygame.image.load("sprite_images/"+str(i)+".png").convert_alpha()
            self._images.append(image)
            image = pygame.image.load("sprite_images/hat"+str(i)+".png").convert_alpha()
            self._pith.append(image)
            image = pygame.image.load("sprite_images/greenhat"+str(i)+".png").convert_alpha()
            self._hipster.append(image)
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

    def change_hat(self) -> None:
        """Toggle through hat changes."""
        self._current_hat = next(self._current_hat)
        self._update_image()

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
                    player.change_hat()
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
