"""Top-down game demonstrating scoring."""

# Imports and initialize pygame.
import pygame
import io
import math
import random
pygame.init()

class Brick(pygame.sprite.Sprite):
    """Just another brick..."""

    def __init__(self, x: int, y: int, length: int, width: int) -> None:
        """Create an invisible sprite."""
        super().__init__()
        self.image = pygame.Surface((width, length))
        self.image.fill((0,0,0))
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

class Gold(pygame.sprite.Sprite):
    """A goal in the game."""

    # Annotate object-level fields
    _images: list
    _current_image: int
    _timer: int

    def __init__(self, x: int, y: int) -> None:
        """Create a spinning coin."""
        super().__init__()
        i: int
        self._images = []
        for i in range(6):
            self._images.append(pygame.image.load("coin" + str(i) + ".png").convert_alpha())
        self._current_image = 0
        self.image = self._images[self._current_image]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self._timer = 0

    def update(self) -> None:
        """Update the spinning animation."""
        self._timer += 1
        if self._timer % 3 == 0:
            self._current_image += 1
            self.image = self._images[self._current_image % len(self._images)]
            loc: tuple = self.rect.topleft
            self.rect = self.image.get_rect()
            self.rect.topleft = loc


class Background(pygame.sprite.Sprite):
    """A tile-based background."""

    # Annotate object-level fields
    _bricks: list
    _gold: list

    def __init__(self, tile_files: list, terrain_file: str,
                 bricks: list, gold: list) -> None:
        """Load map and build Surface."""
        # Annotate and initialize local variables
        name: str
        line: str
        tile_size: int
        width: int
        height: int
        x: int = 0
        y: int = 0
        terrain: io.TextIOWrapper
        # Superclass init.
        super().__init__()
        # Load the images to pygame Surfaces.
        tiles: list = []
        for name in tile_files:
            tiles.append(pygame.image.load(name).convert())
        # Load the terrain map into a 2D list.
        terrain_map: list = []
        with open(terrain_file) as terrain:
            line = terrain.readline()
            while line != "":
                terrain_map.append(line.split())
                line = terrain.readline()
        # Calculate the size of the Surface and create.
        tile_size = tiles[0].get_width()
        width = len(terrain_map[0]) * tile_size
        height = len(terrain_map) * tile_size
        self.image = pygame.Surface((width, height)) 
        # Blit the images to the Surface.
        # Create a Brick if necessary.
        self._bricks = []
        self._gold = []
        for row in terrain_map:
            for i in row:
                self.image.blit(tiles[int(i)], (x, y))
                if int(i) in bricks:
                    self._bricks.append(Brick(x, y, tile_size, tile_size))
                elif int(i) in gold:
                    self._gold.append(Gold(x, y))
                x += tile_size
            y += tile_size
            x = 0
        # Complete initialization
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)
        self._speed = 5

    def get_bricks(self) -> list:
        """Return the bricks."""
        return self._bricks

    def get_gold(self) -> list:
        """Return the gold."""
        return self._gold

    def get_size(self) -> tuple:
        """Return the Surface size."""
        return self.image.get_size()

class Enemy(pygame.sprite.Sprite):

    # Annotate object-level fields
    _dx: int
    _dy: int
    _timer: int
    _freeze_counter: int

    def _change_direction(self) -> None:
        if random.randint(0, 1):
            self._dx = random.randint(-3, 3)
        else:
            self._dy = random.randint(-3, 3)
        self._timer = 0

    def __init__(self, image: pygame.Surface, x: int, y: int) -> None:
        """Initialize the sprite."""
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self._dx = 0
        self._dy = 0
        self._timer = 0
        self._change_direction()
        self._frozen = False
        self._freeze_counter = 0

    def freeze(self, enemy_group: pygame.sprite.Group,
               frozen_group: pygame.sprite.Group) -> None:
        self._frozen = True
        self._freeze_counter = 150
        enemy_group.remove(self)
        frozen_group.add(self)
        self.image.set_alpha(150)

    def update(self, bricks: pygame.sprite.Group,
               enemy_group: pygame.sprite.Group,
               frozen_group: pygame.sprite.Group ) -> None:
        if not self._frozen:
            self.rect.top += self._dy
            self.rect.left += self._dx
            self._timer += 1
            if pygame.sprite.spritecollide(self, bricks, False):
                self.rect.top -= self._dy
                self.rect.left -= self._dx
                self._change_direction()
            elif self._timer >= 60:
                self._change_direction()
        else:
            self._freeze_counter -= 1
            if self._freeze_counter <= 30:
                if self._freeze_counter == 0:
                    enemy_group.add(self)
                    frozen_group.remove(self)
                    self._frozen = False
                    self.image.set_alpha(255)
                elif self._freeze_counter % 10 == 0:
                    self.image.set_alpha(150)
                elif self._freeze_counter % 5 == 0:
                    self.image.set_alpha(255)

            
class Student(pygame.sprite.Sprite):

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
    _coins: int

    def __init__(self, image: pygame.Surface, x: int, y: int) -> None:
        """Initialize the sprite."""
        super().__init__()
        self._face_right = image
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self._dx = 0
        self._dy = 0
        self._speed = 2
        self._coins = 0

    def get_coins(self) -> int:
        """Return the number of coins."""
        return self._coins

    def add_coins(self, num_coins: int) -> None:
        """Add num_coins to coins total."""
        self._coins += num_coins

    def move(self, direction: int) -> None:
        self._dx = 0
        self._dy = 0
        if direction != Student.STOP:
            rotation: int = direction * 90
            x: int = self.rect.centerx
            y: int = self.rect.centery
            self.image = pygame.transform.rotate(self._face_right, rotation)
            self.rect.centerx = x
            self.rect.centery = y
            if direction == Student.LEFT:
                self._dx = -self._speed
            elif direction == Student.RIGHT:
                self._dx = self._speed
            if direction == Student.UP:
                self._dy = -self._speed
            elif direction == Student.DOWN:
                self._dy = self._speed

    def update(self, bricks: pygame.sprite.Group) -> None:
        self.rect.top += self._dy
        self.rect.left += self._dx
        while pygame.sprite.spritecollide(self, bricks, False):
            # Calculate a unit vector
            distance: float = math.sqrt(self._dx ** 2 + self._dy ** 2)
            x: float = self._dx / distance
            y: float = self._dy / distance
            # Backup
            self.rect.top -= y
            self.rect.left -= x

class Level():
    """Stub for level."""
    def get_level(self) -> int:
        return 1

class Scorekeeper(pygame.sprite.Sprite):
    """Responsible for displaying an updated score."""

    # Annotate object-level fields
    _player: Student
    _level: Level
    _font: pygame.font.Font

    def __init__(self, player: Student, level: Level) -> None:
        """Initialize from parameters."""
        super().__init__()
        self._player = player
        self._level = level
        if pygame.font:
            self._font = pygame.font.SysFont("Bauhaus 93", 24)
        self.image = pygame.Surface((0, 0)) 
        self.rect = self.image.get_rect()

    def update(self, screen: pygame.Surface) -> None:
        """Get information from player, level and render."""
        coins: int = self._player.get_coins()
        level: int = self._level.get_level()
        if pygame.font:
            level_surf: pygame.Surface = self._font.render("Level " + str(level), True, (0, 0, 0))
            coins_surf: pygame.Surface = self._font.render("Coins " + str(coins), True, (0, 0, 0))
            self.image = pygame.Surface((screen.get_width(), self._font.get_height()))
            self.image.fill((222, 237, 244))
            self.image.blit(level_surf, (0, 0))
            self.image.blit(coins_surf, (screen.get_width() - coins_surf.get_width(), 0))
            self.rect = self.image.get_rect()
        else:
            pygame.display.set_caption("Level " + str(level) + " Coins " + str(coins))
            
def make_window(width: int, height: int, caption: str) -> pygame.Surface:
    """Create and return a pygame window."""
    screen: pygame.Surface
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(caption)
    return screen

def main() -> None:
    """The arrow keys move the student or scroll."""
    # Annotate and initialize variables.
    screen: pygame.Surface = pygame.display.set_mode((400, 400)) # temporary window
    background: Background
    bkgd_group: pygame.sprite.Group
    bricks: pygame.sprite.Group
    gold: pygame.sprite.Group
    sam: Student
    group: pygame.sprite.Group = pygame.sprite.Group()
    user_quit: bool = False
    e: pygame.event.Event
    level1: Level = Level()
    scorekeeper: Scorekeeper
    score_group: pygame.sprite.Group
    enemies: pygame.sprite.Group
    frozen_enemies: pygame.sprite.group = pygame.sprite.Group()
    enemy_image: pygame.Surface
    
    # Set up assets.
    image_files: list = ["barrier.jpg", "floor.jpg", "floor.jpg"]
    background = Background(image_files, "castle.txt", [0], [2])
    background_size: tuple = background.get_size()
    screen = make_window(background_size[0], background_size[1], "Scoring Demo")
    bkgd_group = pygame.sprite.Group(background)
    bricks = pygame.sprite.Group(background.get_bricks())
    gold = pygame.sprite.Group(background.get_gold())
    sam = Student(pygame.image.load("class_dash_sprite.png").convert_alpha(), 50, 50)
    group.add(sam)
    
    clock: pygame.time.Clock = pygame.time.Clock()
    scorekeeper = Scorekeeper(sam, level1)
    score_group = pygame.sprite.Group(scorekeeper)
    coins: list
    enemies = pygame.sprite.Group()
    for i in range(10):
        enemies.add(Enemy(pygame.image.load("enemy.png").convert_alpha(), 350, 230))
    

    while not user_quit:
        # Loop 30 times per second
        clock.tick(30)

        for e in pygame.event.get():
            # Process a quit choice.
            if e.type == pygame.QUIT:
                user_quit = True
            elif e.type == pygame.KEYDOWN:
                # Process movement arrow keys.
                key = e.__dict__["key"]
                if key == pygame.K_UP:
                    sam.move(Student.UP)
                elif key == pygame.K_DOWN:
                    sam.move(Student.DOWN)
                elif key == pygame.K_RIGHT:
                    sam.move(Student.RIGHT)
                elif key == pygame.K_LEFT:
                    sam.move(Student.LEFT)
            elif e.type == pygame.KEYUP:
                if (not pygame.key.get_pressed()[pygame.K_LEFT] 
                        and not pygame.key.get_pressed()[pygame.K_RIGHT]
                        and not pygame.key.get_pressed()[pygame.K_UP]
                        and not pygame.key.get_pressed()[pygame.K_DOWN]):
                     sam.move(Student.STOP)

        # Check for collisions with gold.
        coins = pygame.sprite.spritecollide(sam, gold, True)
        sam.add_coins(len(coins))

        # Check for collisions with spiders.
        bites = pygame.sprite.groupcollide(group, enemies, False, False)
        if bites:
            for enemy in enemies:
                enemy.freeze(enemies, frozen_enemies)

        # Move, redraw, and show.
        group.update(bricks)
        gold.update()
        score_group.update(screen)
        enemies.update(bricks, enemies, frozen_enemies)
        frozen_enemies.update(bricks, enemies, frozen_enemies)
        bkgd_group.draw(screen)
        gold.draw(screen)
        group.draw(screen)
        enemies.draw(screen)
        frozen_enemies.draw(screen)
        score_group.draw(screen)
        pygame.display.flip()
         
    pygame.quit()

main()
