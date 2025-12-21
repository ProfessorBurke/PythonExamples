"""
    A fog-of-war effect that reveals tiles as the player
    visits them.  Built on top of:
    Base program that allows a sprite to move around a terrain 
    limited to the window size by using the arrow keys.
"""

# Import the random library.
import random
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

    def __init__(self, image: pygame.Surface, x: int, y: int, speed: int) -> None:
        """Initialize the sprite."""
        super().__init__()
        self._face_right = image
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self._dx = 0
        self._dy = 0
        self._speed = speed

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

    # Object-level fields
    _tile: pygame.Surface         # The tile for grassy terrain
    _terrain: list[list[int]]     # The terrain map, a 2d list of integer
    ## NEW CODE
    _fog_tile: pygame.Surface     # The fog tile
    _fog: list[list[bool]]        # The fog map, a 2d list of bool, True is fog
    _changed: bool                # The background has changed since last update.
    ## END NEW CODE

    def __init__(self, width: int, height: int) -> None:
        """Create the terrain map and image.  The initial terrain fits in the window.
           Background begins not moving and left, top is 0,0 in the terrain map."""
        super().__init__()
        # Create the terrain map (all grass) and the fog map (all fog)
        self._terrain = [[2 for col in range(width//Background.TILE_SIZE)] for row in range(height//Background.TILE_SIZE)]

        ## NEW CODE 
        self._fog = [[True for col in range(width//Background.TILE_SIZE)] for row in range(height//Background.TILE_SIZE)]
        self._fog_tile = pygame.image.load("fog_tile2.png").convert_alpha()
        self._changed = False
        ## END NEW CODE
        # Create the starting image from the terrain,
        # located at (0,0).
        tiles_surf: pygame.Surface = pygame.image.load("terrain.jpg").convert()
        self._tile = pygame.Surface((Background.TILE_SIZE, Background.TILE_SIZE), flags = pygame.SRCALPHA)
        self._tile.blit(tiles_surf, (0, 0), pygame.Rect(Background.GRASS_LT,
                                                        (Background.TILE_SIZE, Background.TILE_SIZE)))
        self.image = self._get_surface(width, height)
        self.rect = self.image.get_rect()

    def _get_surface(self, width: int, height: int) -> pygame.Surface:
        """Creates a Surface from the tile and fog maps."""
        # The Surface to draw the tiles on.
        surf: pygame.Surface = pygame.Surface((width, height), flags = pygame.SRCALPHA)
        # row and col index into the two-dimensional list of map tile numbers.
        row: int
        col: int
        # x and y are the blit coordinates on surf -- they will stay between 0,0 and width, height.
        x: int = 0
        y: int = 0
        # Iterate through the 2D list of map tile numbers. Blit the grass.
        for row in range(height//Background.TILE_SIZE):
            for col in range(width//Background.TILE_SIZE):
                ## NEW CODE
                if not self._fog[row][col]:
                    surf.blit(self._tile, (x, y))
                ## END NEW CODE (previously it blitted, but didn't check fog)
                x += Background.TILE_SIZE
            y += Background.TILE_SIZE
            x = 0
        ## NEW CODE
        # Now blit the fog over it.
        x = 0
        y = 0
        diff: int = (self._fog_tile.get_width() - self._tile.get_width())//2
        for row in range(height//Background.TILE_SIZE):
            for col in range(width//Background.TILE_SIZE):
                if self._fog[row][col]:
                    surf.blit(self._fog_tile, (x-diff, y-diff))
                x += Background.TILE_SIZE
            y += Background.TILE_SIZE
            x = 0
        ## END NEW CODE

        return surf

    ## NEW CODE
    def unfog(self, player_x: int, player_y: int) -> None:
        """Player is in a location; unfog if fogged and set _changed field."""
        # Find the row, col of player location.
        col: int = player_x // Background.TILE_SIZE
        row: int = player_y // Background.TILE_SIZE
        # Expand that by 2 and unfog.
        for i in range(max(0, row-2), min(row+3, len(self._fog))):
            for j in range(max(0, col-2), min(col+3, len(self._fog[i]))):
                if self._fog[i][j]:
                    self._fog[i][j] = False
                    self._changed = True

    def update(self, screen: pygame.Surface) -> None:
        """Get a new surface if the background has changed and unset _changed field."""
        if self._changed:
            self.image = self._get_surface(screen.get_width(), screen.get_height())
            self._changed = False
    ## END NEW CODE
        

def main() -> None:
    """Allow the user to explore an infinite random space."""
    # Annotate and initialize window and background constants and variables.
    WIDTH: int = 800
    HEIGHT: int = 600
    SPEED: int = 10
    screen: pygame.Surface = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Use the arrow keys to explore")
    background: Background = Background(WIDTH, HEIGHT)
    background_group: pygame.sprite.Group = pygame.sprite.Group(background)

    # Annotate and initialize constants and variables for the sprite.
    player: Player = Player(pygame.image.load("class_dash_sprite.png").convert_alpha(),
                      25, 25, SPEED)
    player_group: pygame.sprite.Group = pygame.sprite.Group(player)
    direction: int = Player.STOP

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
        player_group.update(screen, background)
        ## NEW CODE
        background.unfog(player.rect.centerx, player.rect.centery)
        ## END NEW CODE
                    
        # Draw the player and background
        background_group.update(screen)
        background_group.draw(screen)
        player_group.draw(screen) 
                
        # Show the display.
        pygame.display.flip()
    pygame.quit()

main()
