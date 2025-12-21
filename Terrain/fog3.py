"""
    A flashlight effect that is a cone in the direction the player
    is facing.  Built on top of:
    A flashlight effect that reveals only tiles around the player.
    Built on top of:
    Base program that allows a sprite to move around a terrain 
    limited to the window size by using the arrow keys.
"""

# Import Python libraries.
import random
from math import sin, cos, pi, radians ## NEW CODE
# Import and initialize pygame.
import pygame
pygame.init()


class Player(pygame.sprite.Sprite):
    """A player can move around the terrain with the arrow keys."""

    # Annotate class-level constants
    UP: int = 1
    DOWN: int = 3
    LEFT: int = 2
    RIGHT: int = 0
    STOP: int = 4

    # Annotate object-level fields
    _dx: int
    _dy: int
    _speed: int
    _face_right: pygame.Surface
    ## NEW CODE
    direction_facing: int
    ## END NEW CODE

    def __init__(self, image: pygame.Surface, loc: tuple[int], speed: int) -> None:
        """Initialize the sprite."""
        super().__init__()
        self._face_right = image
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = loc
        self._dx = 0
        self._dy = 0
        self._speed = speed
        ## NEW CODE
        self.direction_facing = Player.RIGHT
        ## END NEW CODE

    def turn(self, direction: int) -> None:
        """Turn the player sprite to face the direction of movement."""
        if direction != Player.STOP:
            rotation: int = direction * 90
            x: int = self.rect.centerx
            y: int = self.rect.centery
            self.image = pygame.transform.rotate(self._face_right, rotation)
            self.rect.centerx = x
            self.rect.centery = y

    def move(self, direction: int) -> None:
        self._dx = 0
        self._dy = 0
        if direction != Player.STOP:
            ## NEW CODE
            self.direction_facing = direction
            ## END NEW CODE
            self.turn(direction)
            if direction == Player.LEFT:
                self._dx = -self._speed
            elif direction == Player.RIGHT:
                self._dx = self._speed
            if direction == Player.UP:
                self._dy = -self._speed
            elif direction == Player.DOWN:
                self._dy = self._speed

    def update(self, screen: pygame.Surface, background: "Background") -> None:
        """Move sprite by _dx, _dy."""
        self.rect.top += self._dy
        self.rect.left += self._dx
        if self.rect.right > screen.get_width():
            self.rect.right = screen.get_width() - int(self.rect.width / 4)
        elif self.rect.left < 0:
            self.rect.left = int(self.rect.width / 4)
        if self.rect.bottom > screen.get_height():
            self.rect.bottom = screen.get_height() - int(self.rect.height / 4)
        elif self.rect.top < 0:
            self.rect.top = int(self.rect.height / 4)
        
 

class Background(pygame.sprite.Sprite):
    """ A tile-based background the size of the window."""

    # Size of a tile.
    TILE_SIZE: int = 25
    # Locations of the grass tile within the tiles Surface.
    GRASS_LT: tuple[int] = (25, 25)
    LIGHT_RADIUS: int = 180

    # Object-level fields
    _tile: pygame.Surface         # The tile for grassy terrain
    _terrain: list[list[int]]     # The terrain map, a 2d list of integer

    ## NEW CODE
    def __init__(self, width: int, height: int, player: Player) -> None:
    ## END NEW CODE
        """Create the terrain map and image.  The initial terrain fits in the window.
           Background begins not moving and left, top is 0,0 in the terrain map."""
        super().__init__()
        # Create the terrain map (all grass)
        self._terrain = [[2 for col in range(width//Background.TILE_SIZE)] for row in range(height//Background.TILE_SIZE)]
        # Create the starting image from the terrain,
        # located at (0,0).
        tiles_surf: pygame.Surface = pygame.image.load("terrain.jpg").convert_alpha()
        self._tile = pygame.Surface((Background.TILE_SIZE, Background.TILE_SIZE), flags = pygame.SRCALPHA)
        self._tile.blit(tiles_surf, (0, 0), pygame.Rect(Background.GRASS_LT, (Background.TILE_SIZE, Background.TILE_SIZE)))
        ## NEW CODE
        self.image = self._get_surface(width, height, player.rect.center, player.direction_facing)
        ## END NEW CODE
        self.rect = self.image.get_rect()

    ## NEW CODE
    def _get_surface(self, width: int, height: int, player_center: tuple[int],
                     direction: int) -> pygame.Surface:
    ## END NEW CODE
        # The Surface to draw the tiles on.
        surf: pygame.Surface = pygame.Surface((width, height), flags = pygame.SRCALPHA)
        # row and col index into the two-dimensional list of map tile numbers.
        row: int
        col: int
        # x and y are the blit coordinates on surf -- they will stay between 0,0 and width, height.
        x: int = 0
        y: int = 0
        # Iterate through the 2D list of map tile numbers for the part that's showing,
        # which begins at self._left_top.  Blit the correct tile for the map from the _tiles.
        for row in range(height//Background.TILE_SIZE):
            for col in range(width//Background.TILE_SIZE):
                surf.blit(self._tile, (x, y))
                x += Background.TILE_SIZE
            y += Background.TILE_SIZE
            x = 0
        ## NEW CODE
        # Add the flashlight effect.
        darkness: pygame.Surface
        darkness = pygame.Surface((width, height), pygame.SRCALPHA)
        darkness.fill((0, 0, 0, 180))
        # Draw a cone.
        # These variables are just to shorten the calculation code.
        lr: int = Background.LIGHT_RADIUS
        cx: int = player_center[0]
        cy: int = player_center[1]
        angle_adjustment: float

        # Starting point of the polygon is the player center.
        points: list[tuple] = [player_center]

        # Adjust the angle based on the player's direction and the
        # clockwise unit circle (because y increases down).
        if direction == Player.RIGHT:
            angle_adjustment = 0        # radians and degrees
        elif direction == Player.LEFT:
##            angle_adjustment = pi       # radians
            angle_adjustment = 180      # degrees
        elif direction == Player.UP:
##            angle_adjustment = 3*pi/2   # radians
            angle_adjustment = 270      #degrees
        elif direction == Player.DOWN:
##            angle_adjustment = pi/2     # radians
            angle_adjustment = 90       # degrees

        # Calculate the curvy points for our wedge.
        # Radians:
##        for angle in [i * 0.05 for i in range(-11, 12)]:
##            x = cx + lr * cos(angle_adjustment + angle)
##            y = cy + lr * sin(angle_adjustment + angle)
##            points.append((x, y))
        # Degrees:
        for angle in range(-30, 31, 3):
            x = cx + lr * cos(radians(angle_adjustment + angle))
            y = cy + lr * sin(radians(angle_adjustment + angle))
            points.append((x, y))

        pygame.draw.polygon(darkness, (0, 0, 0, 0), points)
        surf.blit(darkness, (0, 0))
        ## END NEW CODE
        return surf
        
    ## NEW CODE       
    def update(self, screen: pygame.Surface, player: Player) -> None:
        """Update the background sprite to be dimmed except for a radius
           around the player."""
        self.image = self._get_surface(screen.get_width(), screen.get_height(),
                                        player.rect.center, player.direction_facing)          
    ## END NEW CODE


def main() -> None:
    """Allow the user to explore an infinite random space."""
    # Annotate and initialize window and background constants and variables.
    WIDTH: int = 800
    HEIGHT: int = 600
    SPEED: int = 10
    ## NEW CODE
    PLAYER_START: tuple[int] = (25, 25)
    screen: pygame.Surface = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Use the arrow keys to explore")
 
    # Annotate and initialize constants and variables for the sprite.
    player: Player = Player(pygame.image.load("class_dash_sprite.png").convert_alpha(),
                      PLAYER_START, SPEED)
    player_group: pygame.sprite.Group = pygame.sprite.Group(player)
    background: Background = Background(WIDTH, HEIGHT, player)
    background_group: pygame.sprite.Group = pygame.sprite.Group(background)
    direction: int = Player.STOP
    ## END NEW CODE

    # Annotate and initialize event and game loop variables.
    user_quit: bool = False
    e: pygame.event.Event
    keys: tuple
    key: int

    # Create the clock for timing the game loop.
    clock: pygame.time.Clock = pygame.time.Clock()

    # Process events until the user chooses to quit.
    while not user_quit:
        # Loop 30 times per second
        clock.tick(30)
        for e in pygame.event.get():
            # Process a quit choice.
            if e.type == pygame.QUIT:
                user_quit = True
            elif e.type == pygame.KEYDOWN:
                key = e.__dict__["key"]
                if key == pygame.K_UP:
                    direction = Player.UP
                elif key == pygame.K_DOWN:
                    direction = Player.DOWN
                elif key == pygame.K_RIGHT:
                    direction = Player.RIGHT
                elif key == pygame.K_LEFT:
                    direction = Player.LEFT
            # If all arrow keys are up, stop the player.
            elif e.type == pygame.KEYUP:
                keys = pygame.key.get_pressed()
                if not (keys[pygame.K_UP] or keys[pygame.K_DOWN] or
                        keys[pygame.K_RIGHT] or keys [pygame.K_LEFT]):
                    direction = Player.STOP

        # Move the sprite if needed.
        player.move(direction)
                    
        # Draw the player and background.
        player_group.update(screen, background)
        ## NEW CODE
        background_group.update(screen, player)
        ## END NEW CODE
        background_group.draw(screen)
        player_group.draw(screen)
                
        # Show the display.
        pygame.display.flip()
    pygame.quit()

main()
