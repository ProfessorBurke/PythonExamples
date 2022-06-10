"""Top-down game demonstrating scoring."""

# Imports and initialize pygame.
import pygame
import io
import math
import random
pygame.init()


class Fish(pygame.sprite.Sprite):
    """The fish swims and has a love/hate relationship with bubbles."""

    # Annotate class-level fields
    _BUBBLE_MIN = -5
    _BUBBLE_MAX = 5
    
    # Annotate object-level fields
    _bubble_affinity: int
    _dx: int
    _dy: int
    _treasure: "Treasure"

    def __init__(self, image: pygame.Surface, left: int, right: int,
                 top: int, bottom: int, treasure: "Treasure") -> None:
        """Create a spinning coin."""
        x: int = random.randint(left, right)
        y: int = random.randint(top, bottom)
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self._dx = random.randint(-2, 2)
        self._dy = random.randint(-2, 2)
        self._bubble_affinity = random.randint(Fish._BUBBLE_MIN, Fish._BUBBLE_MAX)
        self._treasure = treasure
        treasure.attach(self)
        
    def move_to_treasure(self, treasure_x: int, treasure_y: int) -> None:
        """Change dx and dy to move toward the treasure."""
        x: float = self.rect.centerx - treasure_x
        y: float = self.rect.centery - treasure_y
        distance: float = math.sqrt(x**2 + y**2)
        x /= distance
        y /= distance
        self._dx = -x * self._bubble_affinity
        self._dy = -y * self._bubble_affinity

    def update(self, screen: pygame.Surface) -> None:
        """Update the fish's location."""
        change_direction: bool = False
        self.rect.left += self._dx
        self.rect.top += self._dy
        if self.rect.left <= 0:
            self.rect.left = 0
            change_direction = True
        elif self.rect.right >= screen.get_width():
            self.rect.right = screen.get_width()
            change_direction = True
        if self.rect.top <= 0:
            self.rect.top = 0
            change_direction = True
        elif self.rect.bottom >= screen.get_height():
            self.rect.bottom = screen.get_height()
            change_direction = True
        if change_direction:
            self._dx = random.randint(-2, 2)
            self._dy = random.randint(-2, 2)

    def subject_update(self) -> None:
        """Update direction based on treasure chest activity."""
        if self._treasure.bubbling():
            self.move_to_treasure(self._treasure.get_x(),
                                  self._treasure.get_y())
        else:
            self._dx = random.randint(-2, 2)
            self._dy = random.randint(-2, 2)            
            

class Treasure(pygame.sprite.Sprite):
    """A treasure chest that can make bubbles."""

    # Annotate object-level fields
    _MAX_BUBBLES: int = 2
    _bubble_image: pygame.Surface
    _image: pygame.Surface
    _bubbling_timer: int
    _bubbling: bool
    _observers: list

    def __init__(self, image: pygame.Surface, bubble_image: pygame.Surface,
                 x: int, y: int) -> None:
        """Init a treasure chest from parameters, begin in non-bubbling state."""
        super().__init__()
        self.image = image
        self._image = image
        self._bubble_image = bubble_image
        self._bubbling = False
        self._bubbling_timer = 0
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self._observers = []

    def attach(self, observer: object) -> None:
        """Attach an observer to this object."""
        self._observers.append(observer)

    def detach(self, observer: object) -> None:
        """Detach an observer from this object."""
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self) -> None:
        """Notify observers that this object's state has changed."""
        for observer in self._observers:
            observer.subject_update()

    def bubbling(self) -> bool:
        """Return the bubbling state."""
        return self._bubbling

    def get_x(self) -> int:
        """Return center x."""
        return self.rect.centerx

    def get_y(self) -> int:
        """Return center y."""
        return self.rect.centery

    def bubble(self) -> None:
        """Make some bubbles."""
        self._bubbling = True
        self.image = self._bubble_image
        self.notify()

    def update(self) -> None:
        """Update the spinning animation."""
        if not self._bubbling:
            self._bubbling = random.randint(1, 300) == 1
            if self._bubbling:
                self.bubble()
        else:
            self._bubbling_timer += 1
            # Reset after _MAX_BUBBLES + 1 seconds
            if self._bubbling_timer % (30 * self._MAX_BUBBLES) == 0:
                self.image = self._image
                self._bubbling = False
                self._bubbling_timer = 0
                self.notify()
            
def make_window(width: int, height: int, caption: str) -> pygame.Surface:
    """Create and return a pygame window."""
    screen: pygame.Surface
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(caption)
    return screen

def main() -> None:
    """The arrow keys move the student or scroll."""
    # Annotate and initialize variables.
    screen: pygame.Surface = make_window(800, 800, "Virtual Fish!")
    background: pygame.Surface = pygame.Surface((800, 800))
    background.fill((0,150,200))
    screen.blit(background, (0,0))
    
    user_quit: bool = False
    e: pygame.event.Event
    key: int
    i: int
    
    # Set up assets.
    chest = Treasure(pygame.image.load("treasure_chest.png").convert_alpha(),
                     pygame.image.load("treasure_chest_bubbles.png").convert_alpha(),
                     350, 650)
    chest_group: pygame.sprite.Group = pygame.sprite.Group(chest)

    fish_group: pygame.sprite.Group = pygame.sprite.Group()
    for i in range(10):
        fish = Fish(pygame.image.load("small_fish.png").convert_alpha(),
                    0, 600, 0, 600, chest)
        fish_group.add(fish)
    
    clock: pygame.time.Clock = pygame.time.Clock()

    while not user_quit:
        # Loop 30 times per second
        clock.tick(30)

        for e in pygame.event.get():
            # Process a quit choice.
            if e.type == pygame.QUIT:
                user_quit = True
            elif e.type == pygame.KEYDOWN:
                # Process arrow keys to produce bubbles.
                key = e.__dict__["key"]
                if key == pygame.K_SPACE:
                    chest.bubble()

        # Clear, animate, redraw, and show.
        chest_group.clear(screen, background)
        fish_group.clear(screen, background)
        chest_group.update()
        fish_group.update(screen)
        chest_group.draw(screen)
        fish_group.draw(screen)
        pygame.display.flip()
         
    pygame.quit()

main()
