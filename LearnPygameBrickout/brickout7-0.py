
# Pygame setup
import pygame
pygame.init()
pygame.display.init()
pygame.mixer.init()

# Import libraries
import random
from pathlib import Path

class Laser(pygame.sprite.Sprite):
    """A single laser that moves upward and disappears at the top of the screen."""
    def __init__(self, x: int, y: int, width = 5, height = 10,
                 color = (255, 255, 255), dy = -10) -> None:
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self._dy = dy
        sound_folder: Path = Path("sound")
        self._sound = pygame.mixer.Sound(sound_folder / "laser.wav")

    def play_sound(self) -> None:
        pygame.mixer.Sound.play(self._sound)

    def update(self) -> None:
        self.rect.y += self._dy
        if self.rect.bottom <= 0:
            self.kill()

class LaserManager:
    """Manages when and how lasers are fired, creates lasers"""
    def __init__(self):
        self._cooldown = 500
        self._last_shot_time = None

    def update(self, keys: pygame.key.ScancodeWrapper, paddle: "Paddle",
                   laser_group: pygame.sprite.Group) -> None:
        if keys[pygame.K_UP]:
            now: int = pygame.time.get_ticks()

            if (self._last_shot_time is None or
                now - self._last_shot_time >= self._cooldown):
                laser: Laser = Laser(paddle.rect.centerx, paddle.rect.top)
                laser_group.add(laser)
                laser.play_sound()
                self._last_shot_time = now

class Scoreboard(pygame.sprite.Sprite):
    """Displays the points and balls."""
    def __init__(self, balls: int, x: int, y: int, screen: pygame.Surface) -> None:
        super().__init__()
        self._points = 0
        self._balls = balls
        self._font = pygame.font.SysFont("Courier New", 32)
        self._create_surface(screen, x, y)

    def _create_surface(self, screen: pygame.Surface, x: int, y: int) -> None:
        left_score: pygame.Surface = self._font.render(f"score {self._points}",
                                       True, (255, 255, 255), (0, 0, 0))
        right_score: pygame.Surface = self._font.render(f"balls {self._balls}",
                                       True, (255, 255, 255), (0, 0, 0))

        self.image = pygame.Surface((screen.get_width() - x * 2,
                                     left_score.get_height()))
        self.image.blit(left_score, (0, 0))
        self.image.blit(right_score, (self.image.get_width() -
                                      right_score.get_width(), 0))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def add_points(self, points: int) -> None:
        self._points += points

    def lose_ball(self) -> None:
        self._balls = max(0, self._balls - 1)

    def game_over(self) -> None:
        return self._balls == 0

    def update(self, screen: pygame.Surface) -> None:
        self._create_surface(screen, self.rect.left, self.rect.top)

class Brick(pygame.sprite.Sprite):
    """An individual brick.  The goal of the game is to destroy all bricks.
       Bricks are rectangular colored Surfaces with a location.
    """
    def __init__(self, image: pygame.Surface, x: int, y: int, points: int) -> None:
        super().__init__()
        self.image = image
        self.rect = image.get_rect()
        self.rect.topleft = (x, y)
        self._points = points

    def get_points(self) -> int:
        return self._points

class Paddle(pygame.sprite.Sprite):
    """The player-controlled paddle.  It is controlled by the keyboard.
    """
    STILL: int = 0
    MOVING_RIGHT: int = 1
    MOVING_LEFT: int = 2

    def __init__(self, width: int, height: int, x: int, y: int, dx: int) -> None:
        super().__init__()
        self._dx = dx
        self.image = pygame.Surface((width, height))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self._moving = Paddle.STILL
        
    def update(self, screen: pygame.Surface) -> None:
        if self._moving == Paddle.MOVING_LEFT:
            self.rect.left -= self._dx
            if self.rect.left < 0:
                self.rect.left = 0
        elif self._moving == Paddle.MOVING_RIGHT:
            self.rect.left += self._dx
            if self.rect.right >= screen.get_width():
                self.rect.right = screen.get_width()

    def set_moving(self, keys: pygame.key.ScancodeWrapper)-> None:
        """Update motion according to what keys are pressed."""
        if keys[pygame.K_LEFT] and keys[pygame.K_RIGHT]:
            self._moving = Paddle.STILL
        elif keys[pygame.K_LEFT]:
            self._moving = Paddle.MOVING_LEFT
        elif keys[pygame.K_RIGHT]:
            self._moving = Paddle.MOVING_RIGHT
        else:
            self._moving = Paddle.STILL
        
class Ball(pygame.sprite.Sprite):
    """
        A ball that bounces around the screen, off the paddle and bricks, and is
        destroyed if it reaches the bottom of the screen.
    """
        
    def __init__(self, size: int, x: int, y: int, dx: int, dy: int) -> None:
        """Create a Surface with dimensions (size, size), set colorkey to
           black and draw a circle.  Set fields from remaining parameters."""
        super().__init__()
        self._dx = dx
        self._dy = dy
        self.image = pygame.Surface((size, size))
        self.image.set_colorkey((0, 0, 0))
        pygame.draw.circle(self.image, (255, 255, 255),
                           (size // 2, size // 2), size // 2)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self._in_play = True
        sound_folder: Path = Path("sound")
        self._wall_bounce = pygame.mixer.Sound(sound_folder / "boink.wav")
        self._brick_hit = pygame.mixer.Sound(sound_folder / "square-blip-non-fade.wav")
        self._paddle_bounce = pygame.mixer.Sound(sound_folder / "paddle_boink.wav")
        self._out_of_play = pygame.mixer.Sound(sound_folder / "game-over.wav")


    def play_wall_bounce(self) -> None:
        pygame.mixer.Sound.play(self._wall_bounce)

    def play_brick_bounce(self) -> None:
        pygame.mixer.Sound.play(self._brick_hit)

    def play_paddle_bounce(self) -> None:
        pygame.mixer.Sound.play(self._paddle_bounce)

    def play_out_of_play(self) -> None:
        pygame.mixer.Sound.play(self._out_of_play)

        
    def update(self, screen: pygame.Surface, scoreboard: Scoreboard) -> None:
        """Change x and y by dx and dy and boundary check with screen."""
        self.rect.left += self._dx
        self.rect.top += self._dy

        # Boundary checking
        if self.rect.left <= 0:
            self.rect.left = 0
            self._dx *= -1
            self.play_wall_bounce()
        elif self.rect.right >= screen.get_width():
            self.rect.right = screen.get_width()
            self._dx *= -1
            self.play_wall_bounce()
        if self.rect.top <= 0:
            self.rect.top = 0
            self._dy *= -1
            self.play_wall_bounce()
        elif self.rect.bottom >= screen.get_height():
            self.rect.bottom = screen.get_height()
            self._dy = 0
            self.play_out_of_play()
            scoreboard.lose_ball()
            self._in_play = False
            self.kill()

    def in_play(self) -> bool:
        """Return True if the ball is still in play; False otherwise."""
        return self._in_play

    def bounce(self) -> None:
        """Bounce the ball."""
        self._dy *= -1

class Droppable(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface,
                 sound: pygame.mixer.Sound,
                 x: int, y: int, dy: int = 8) -> None:
        super().__init__()
        self.image = image
        self._sound = sound
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y
        self._dy = dy

    def play_sound(self) -> None:
        if self._sound is not None:
            pygame.mixer.Sound.play(self._sound)

    def update(self, screen: pygame.Surface) -> None:
        self.rect.y += self._dy
        if self.rect.top >= screen.get_height():
            self.kill()

class PaintDroppable(Droppable):
    def __init__(self, image: pygame.Surface,
                 sound: pygame.mixer.Sound,
                 x: int, y: int, dy: int = 8) -> None:
        super().__init__(image, sound, x, y, dy)
        # Overwrite the image with a copy of the image and color it in
        self.image = image.copy()
        # Generate a random color
        self._color = (random.randint(5, 255), random.randint(5, 255), random.randint(5, 255))
        self.mask = pygame.mask.from_surface(image)
        width, height = self.mask.get_size()
        for y_pixel in range(height):
            for x_pixel in range(width):
                if self.mask.get_at((x_pixel, y_pixel)):
                    self.image.set_at((x_pixel, y_pixel), self._color)
       
    def get_color(self) -> tuple[int]:
        return self._color


class DroppableFactory:
    def __init__(self) -> None:
        sound_folder: Path = Path("sound")
        image_folder: Path = Path("images")
        self._droppable_dict = {"coin": {"callable": Droppable,
                                         "image": pygame.image.load(image_folder / "Coin.png"),
                                         "sound": pygame.mixer.Sound(sound_folder / "coin.wav")},
                                "gem": {"callable": Droppable,
                                         "image": pygame.image.load(image_folder / "Gem.png"),
                                         "sound": pygame.mixer.Sound(sound_folder / "gem.wav")},
                                "paint_drop": {"callable": PaintDroppable,
                                         "image": pygame.image.load(image_folder / "drop.png"),
                                         "sound": pygame.mixer.Sound(sound_folder / "droplet.wav")}
                                }

    def get_random_droppable_type(self) -> str:
        return random.choice(list(self._droppable_dict.keys()))

    def drop(self, droppable_type: str, x: int, y: int) -> Droppable | None:
        droppable: Droppable | None = None
        if droppable_type in self._droppable_dict:
            attributes: dict = self._droppable_dict[droppable_type]
            droppable = attributes["callable"](attributes["image"], attributes["sound"],
                                               x, y)
        return droppable
        
# Annotate variables
screen: pygame.Surface
background: pygame.Surface
bricks: list[Brick]
clock: pygame.time.Clock
e: pygame.event.Event
running: bool

keys: pygame.key.ScancodeWrapper # like list[bool]
i: int
ball: Ball
ball_group: pygame.sprite.Group
brick: Brick
brick_group: pygame.sprite.Group
brick_x: int = 0
brick_y: int = 0

# Game setup
screen = pygame.display.set_mode((600, 450))
pygame.display.set_caption("Brickout 7.0")
clock = pygame.time.Clock()

# Asset setup.
background = pygame.Surface((600, 450))

# Create the paddle
PADDLE_WIDTH: int = 100
PADDLE_HEIGHT: int = 20
paddle_dx: int = 10
paddle_x: int = screen.get_width() // 2 - PADDLE_WIDTH // 2
paddle_y: int = screen.get_height() - PADDLE_HEIGHT * 2
paddle: Paddle = Paddle(PADDLE_WIDTH, PADDLE_HEIGHT, paddle_x, paddle_y, paddle_dx)
paddle_group: pygame.sprite.Group = pygame.sprite.Group(paddle)

# Create the ball
ball = Ball(25, 100, 150, 5, 5)
ball_group = pygame.sprite.Group(ball)

# Create the bricks
NUM_BRICKS: int = 15
OFFSET: int = 2
BRICK_HEIGHT: int = 20
brick_colors: list[tuple] = [(255, 100, 100), (100, 255, 100), (100, 100, 255),
                             (255, 255, 100), (100, 255, 255)]
brick_group = pygame.sprite.Group()
brick_width: int = screen.get_width() // NUM_BRICKS - OFFSET * 2
points: int = 15
points_decrease: int = points // len(brick_colors)

x: float = OFFSET
y: int = BRICK_HEIGHT * 2.5
for color in brick_colors:
    brick_surf = pygame.Surface((brick_width, BRICK_HEIGHT))
    brick_surf.fill((color))
    for i in range(NUM_BRICKS):
        brick_group.add(Brick(brick_surf, x, y, points))
        x += brick_width + OFFSET * 2
    y += BRICK_HEIGHT + OFFSET
    x = OFFSET
    points -= points_decrease

# Create the Scoreboard.
scoreboard: Scoreboard = Scoreboard(5, 5, 5, screen) # balls, x, y, screen
scoreboard_group: pygame.sprite.Group = pygame.sprite.Group(scoreboard)

# Create laser assets.
laser_manager: LaserManager = LaserManager()
laser_group: pygame.sprite.Group = pygame.sprite.Group()

# Create droppable assets.
droppable_group: pygame.sprite.Group = pygame.sprite.Group()
droppable_factory: DroppableFactory = DroppableFactory()

# Game loop
running = True
while running:
    clock.tick(30)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        elif e.type == pygame.KEYDOWN:
            if (e.key == pygame.K_SPACE and not ball.in_play()
                and not scoreboard.game_over()):
                ball = Ball(25, random.randint(10, screen.get_width() - 10),
                            150, 5, 5)
                ball_group.add(ball)
            

    # Clear the location of bricks, paddle, and ball.
    brick_group.clear(screen, background)
    ball_group.clear(screen, background)
    paddle_group.clear(screen, background)
    scoreboard_group.clear(screen, background)
    laser_group.clear(screen, background)
    droppable_group.clear(screen, background)

    # Update the paddle and lasers according to what keys are pressed.
    keys = pygame.key.get_pressed()
    paddle.set_moving(keys)
    paddle_group.update(screen)
    laser_manager.update(keys, paddle, laser_group)

    # Update the ball and check for brick and paddle collisions.
    ball_group.update(screen, scoreboard)
    balls = pygame.sprite.groupcollide(ball_group, brick_group, False, True)
    if balls:
        for ball in balls:
            ball.bounce()
            ball.play_brick_bounce()
        # Total up the collided bricks in a set (no duplicates) and add points to scoreboard.
        all_bricks_hit = set()
        for brick_hit in balls.values():
            all_bricks_hit.update(brick_hit)
        for brick in all_bricks_hit:
            scoreboard.add_points(brick.get_points())
            if random.random() < .8:
                droppable_type: str = droppable_factory.get_random_droppable_type()
                droppable: Droppable = droppable_factory.drop(droppable_type,
                                                              brick.rect.centerx,
                                                              brick.rect.centery)
                if droppable is not None:
                    droppable_group.add(droppable)

    balls = pygame.sprite.groupcollide(ball_group, paddle_group, False, False)
    for hit_ball in balls:
        hit_ball.rect.bottom = balls[hit_ball][0].rect.top
        hit_ball.bounce()
        hit_ball.play_paddle_bounce()


    # Check for laser-brick collisions.
    hits: dict[Brick, Laser]
    hits = pygame.sprite.groupcollide(brick_group, laser_group, True, True)
    if hits:
        for brick in hits:
            scoreboard.add_points(brick.get_points())

    # Check for paddle-droppable collisions.
    droppables = pygame.sprite.groupcollide(droppable_group, paddle_group, True, False)
    for droppable in droppables:
        droppable.play_sound()
            
    # Draw the new state of bricks, paddle, and ball.
    droppable_group.update(screen)
    scoreboard_group.update(screen)
    laser_group.update()
    scoreboard_group.draw(screen)
    brick_group.draw(screen)
    ball_group.draw(screen)
    laser_group.draw(screen)
    droppable_group.draw(screen)
    paddle_group.draw(screen)

    pygame.display.flip()

pygame.quit()
