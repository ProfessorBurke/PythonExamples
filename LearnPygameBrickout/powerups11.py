import pygame
pygame.init()
pygame.display.init()
pygame.mixer.init()

from pathlib import Path
import random

class Droppable(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface,
                 sound: pygame.mixer.Sound,
                 powerup: str,
                 x: int, y: int, dy: int = 8) -> None:
        super().__init__()
        self.image = image
        self._sound = sound
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y
        self._dy = dy
        self._powerup = powerup
        self.mask = pygame.mask.from_surface(self.image)

    def play_sound(self) -> None:
        if self._sound is not None:
            pygame.mixer.Sound.play(self._sound)

    def get_powerup(self) -> str:
        return self._powerup

    def update(self, screen: pygame.Surface) -> None:
        self.rect.y += self._dy
        if self.rect.top >= screen.get_height():
            self.kill()


class PaintDroppable(Droppable):
    def __init__(self, image: pygame.Surface,
                 sound: pygame.mixer.Sound,
                 powerup: str,
                 x: int, y: int, dy: int = 8) -> None:
        super().__init__(image, sound, powerup, x, y, dy)
        # Overwrite the image with a copy of the image and color it in
        self.image = image.copy()
        # Generate a random color
        self._color = (random.randint(5, 255), random.randint(5, 255), random.randint(5, 255))
        #self.mask = pygame.mask.from_surface(image)
        image_color: tuple[int] = self.image.get_at((self.rect.width//2,
                                                     self.rect.height//2))
        pygame.transform.threshold(self.image, self.image.copy(),
                                   image_color,
                                   threshold = (10, 10, 10, 255),
                                   set_color = self._color,
                                   inverse_set = True)
##        self.mask = pygame.mask.from_threshold(image, image_color,
##                                               threshold = (10, 10, 10, 255))
##        
##        width, height = self.mask.get_size()
##        for y_pixel in range(height):
##            for x_pixel in range(width):
##                if self.mask.get_at((x_pixel, y_pixel)):
##                    self.image.set_at((x_pixel, y_pixel), self._color)
       
    def get_color(self) -> tuple[int]:
        return self._color
    
class FlippableDroppable(Droppable):
    def __init__(self, image: pygame.Surface,
                 sound: pygame.mixer.Sound,
                 powerup: str,
                 x: int, y: int, dy: int = 8) -> None:
        super().__init__(image, sound, powerup, x, y, dy)
        self._flip_timer = 0
        self._flip_count = 0
        self._flip_threshold = 10
        self._raw_image = image.copy()
        
    def update(self, screen: pygame.Surface) -> None:
        self._flip_timer += 1
        if (self._flip_timer == self._flip_threshold):
            self._flip_timer = 0
            self._flip_count += 1
            if self._flip_count % 2 == 1:
                self.image = pygame.transform.flip(self._raw_image, True, False)
            else:
                self.image = self._raw_image.copy()
            self.mask = pygame.mask.from_surface(self.image)
        super().update(screen)

class TransformDroppable(Droppable):
    def __init__(self, image: pygame.Surface,
                 sound: pygame.mixer.Sound,
                 powerup: str,
                 x: int, y: int, dy: int = 8) -> None:
        super().__init__(image, sound, powerup, x, y, dy)
        self._transform_timer = 0
        self._transform_count = 0
        self._transform_threshold = 10
        self._raw_image = image.copy()
        self.image = pygame.mask.from_surface(self.image).to_surface()
        
    def update(self, screen: pygame.Surface) -> None:
        self._transform_timer += 1
        if (self._transform_timer == self._transform_threshold):
            self._transform_timer = 0
            self._transform_count += 1
            size: tuple[int] = (int(self.rect.width
                                    - self.rect.width * (self._transform_count / 10)),
                                int(self.rect.height
                                    - self.rect.height * (self._transform_count / 10)))
            #self.image = pygame.transform.scale(self._raw_image, size)
##            self.image = pygame.transform.rotate(self._raw_image,
##                                                 30 * self._transform_count)
##            self.image = pygame.transform.rotozoom(self._raw_image,
##                                                   30 * self._transform_count,
##                                                   1 + self._transform_count /2.5)
##            if self._transform_count % 2 == 1:
##                self.image = pygame.transform.flip(self._raw_image, True, False)
##            else:
##                self.image = self._raw_image.copy()
            center: tuple[int] = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = center
            self.mask = pygame.mask.from_surface(self.image)
        super().update(screen)

class AnimatedDroppable(Droppable):
    def __init__(self, image: pygame.Surface,
                 sound: pygame.mixer.Sound,
                 powerup: str,
                 x: int, y: int, dy: int = 8) -> None:
        self._sprite_sheet = image
        self._num_sprites = 4
        self._sprite_size = 32
        self._sheet_x = 0
        image = pygame.Surface((self._sprite_size, self._sprite_size),
                               pygame.SRCALPHA)
        image.blit(self._sprite_sheet, (0, 0),
                   area = (self._sheet_x, 0,
                           self._sprite_size, self._sprite_size))
        super().__init__(image, sound, powerup, x, y, dy)
        self._transform_timer = 0
        self._transform_threshold = 10
        
    def update(self, screen: pygame.Surface) -> None:
        self._transform_timer += 1
        if (self._transform_timer == self._transform_threshold):
            self._transform_timer = 0
            self._sheet_x = ((self._sheet_x + self._sprite_size) %
                             (self._sprite_size * self._num_sprites))
            self.image.blit(self._sprite_sheet, (0, 0),
                            area = (self._sheet_x, 0,
                           self._sprite_size, self._sprite_size))
            self.mask = pygame.mask.from_surface(self.image)
        super().update(screen)
        
class DroppableFactory:
    def __init__(self) -> None:
        sound_folder: Path = Path("sound")
        image_folder: Path = Path("images")
        self._droppable_dict = {
                                "fish": {"callable": AnimatedDroppable,
                                         "image": pygame.image.load(image_folder / "animales3.png"),
                                         "sound": pygame.mixer.Sound(sound_folder / "coin.wav"),
                                         "powerup": None}
##                                "coin": {"callable": Droppable,
##                                         "image": pygame.image.load(image_folder / "Coin.png"),
##                                         "sound": pygame.mixer.Sound(sound_folder / "coin.wav"),
##                                         "powerup": "point_doubler"},
##                                "gem": {"callable": Droppable,
##                                         "image": pygame.image.load(image_folder / "Gem.png"),
##                                         "sound": pygame.mixer.Sound(sound_folder / "gem.wav"),
##                                         "powerup": "turbo_ball"},
##                                "santa": {"callable": TransformDroppable,
##                                         "image": pygame.image.load(image_folder / "one_santa.png"),
##                                         "sound": pygame.mixer.Sound(sound_folder / "santa.wav"),
##                                         "powerup": None}
##                                ,
##                                "paint_drop": {"callable": PaintDroppable,
##                                         "image": pygame.image.load(image_folder / "drop.png"),
##                                         "sound": pygame.mixer.Sound(sound_folder / "droplet.wav"),
##                                         "powerup": "color_paddle"}
##                                ,
##                                "gummy_bear": {"callable": PaintDroppable,
##                                         "image": pygame.image.load(image_folder / "gummy_bear.png"),
##                                         "sound": pygame.mixer.Sound(sound_folder / "bear.wav"),
##                                         "powerup": "color_paddle"},
##                                "bird": {"callable": FlippableDroppable,
##                                         "image": pygame.image.load(image_folder / "bird.png"),
##                                         "sound": pygame.mixer.Sound(sound_folder / "squawk.wav"),
##                                         "powerup": None}
                                    
                                }

    def get_random_droppable_type(self) -> str:
        return random.choice(list(self._droppable_dict.keys()))

    def drop(self, droppable_type: str, x: int, y: int) -> Droppable | None:
        droppable: Droppable | None = None
        if droppable_type in self._droppable_dict:
            attributes: dict = self._droppable_dict[droppable_type]
            droppable = attributes["callable"](attributes["image"], attributes["sound"],
                                               attributes["powerup"],
                                               x, y)
        return droppable

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface,
                 effect_manager: "EffectManager",
                 droppable: Droppable,
                 centerx: int, centery: int,
                 caught_x: int, caught_y: int) -> None:
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.centerx = centerx
        self.rect.centery = centery
        self._start_time = pygame.time.get_ticks()
        self._duration = 3000
        self.effect_manager = effect_manager

    def _kill_effect(self) -> None:
        pass

    def update(self) -> None:
        if (pygame.time.get_ticks() - self._start_time >= self._duration):
            self._kill_effect()
            self.kill()

class PointsMultiplier(PowerUp):
    def __init__(self, image: pygame.Surface,
                 effect_manager: "EffectManager",
                 droppable: Droppable,
                 centerx: int, centery: int,
                 caught_x: int, caught_y: int) -> None:
        super().__init__(image, effect_manager, droppable, centerx, centery,
                         caught_x, caught_y)
        self.effect_manager.add_points_multiplier(2)

    def _kill_effect(self) -> None:
        self.effect_manager.remove_points_multiplier(2)

class TurboBall(PowerUp):
    def __init__(self, image: pygame.Surface,
                 effect_manager: "EffectManager",
                 droppable: Droppable,
                 centerx: int, centery: int,
                 caught_x: int, caught_y: int) -> None:
        super().__init__(image, effect_manager, droppable, centerx, centery,
                         caught_x, caught_y)
        self.effect_manager.add_ballspeed_multiplier(2)
        
    def _kill_effect(self) -> None:
        self.effect_manager.remove_ballspeed_multiplier(2)

class PaddleDoubler(PowerUp):
    def __init__(self, image: pygame.Surface,
                 effect_manager: "EffectManager",
                 droppable: Droppable,
                 centerx: int, centery: int,
                 caught_x: int, caught_y: int) -> None:
        super().__init__(image, effect_manager, droppable, centerx, centery,
                         caught_x, caught_y)
        self.effect_manager.add_paddle_multiplier(2)
        
    def _kill_effect(self) -> None:
        self.effect_manager.remove_paddle_multiplier(2)

class PaddleArtist(PowerUp):
    def __init__(self, image: pygame.Surface,
                 effect_manager: "EffectManager",
                 droppable: Droppable,
                 centerx: int, centery: int,
                 caught_x: int, caught_y: int) -> None:
        super().__init__(image, effect_manager, droppable, centerx, centery, caught_x, caught_y)
        self._color = droppable.get_color()
        self.effect_manager.add_paddle_color(self._color, caught_x, caught_y)
        
    def _kill_effect(self) -> None:
        pass
        #self.effect_manager.remove_paddle_color(self._color)


class PowerupFactory:
    def __init__(self, effect_manager: "EffectManager") -> None:
        self._effect_manager = effect_manager
        image_folder: Path = Path("images")
        self._powerup_dict = {"point_doubler": {"callable": PointsMultiplier,
                                         "image": pygame.image.load(image_folder / "Coin.png")},
                              "turbo_ball": {"callable": TurboBall,
                                         "image": pygame.image.load(image_folder / "Gem.png")},
                              "paddle_doubler": {"callable": PaddleDoubler,
                                                 "image": pygame.image.load(image_folder / "one_santa.png")},
                              "color_paddle": {"callable": PaddleArtist,
                                                 "image": pygame.image.load(image_folder / "drop.png")}
                             }

    def get_powerup(self, powerup_str: str, droppable: Droppable,
                    x: int, y: int,
                    caught_x: int, caught_y: int) -> PowerUp | None:
        power_up: PowerUp | None = None
        if powerup_str in self._powerup_dict:
            attributes: dict = self._powerup_dict[powerup_str]
            power_up = attributes["callable"](attributes["image"],
                                              self._effect_manager,
                                              droppable,
                                              x, y, caught_x, caught_y)
        return power_up

