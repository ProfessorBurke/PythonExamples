"""A less beautiful version of wordle that allows you to put letters
   where you want (you don't need to put them in order)."""

# Import and initialize pygame.
import pygame, time, datetime
pygame.init()


class GameMaster():
    """In charge of aspects of game play such as managing the word
       list, the letters eliminated by the player, and comparing
       guesses to the word."""

    _word: str
    _ordered_pair_word: set
    _words: set
    _eliminated_letters: list 

    def __init__(self) -> None:
        """Initialize fields from the list of words in the same directory
           as the program."""
        # Annotate variables
        words: list
        today: time.struct_time
        index: int

        super().__init__()
        # Open the file, read the words, and store as a set.
        try:
            with open("words") as f:
                words = f.readlines()
        except:
            words = ["error"]
        self._words = set(words)
        
        # We're going to consider 1/1/22 as the word at index 0
        today = time.gmtime()
        index = (datetime.date(today.tm_year, today.tm_mon, today.tm_mday)
                - datetime.date(2022, 1, 1)).days
        self._word = words[index].strip()
        print(self._word)
        self._ordered_pair_word = self._word_to_ordered_pairs(self._word)
        self._eliminated_letters = []
        #print(self._word)
        

    def _word_to_ordered_pairs(self, word: str) -> set:
        """Return the word as a set of ordered pairs of
           tuples of (letter, index)."""
        i: int = 0
        letter: str
        result: list = []
        for letter in word:
            result.append((i, letter))
            i += 1
        return set(result)

    def is_valid_word(self, word: str) -> bool:
        """It's a valid word if it's in the set, but note that the words in
           the set were read from a file and weren't stripped."""
        return (word.lower() + "\n") in self._words

    def get_status(self, guess_word: str) -> tuple:
        """Compare user guess to word and return a list of statuses
           organized by index for each letter in the word."""
        won: bool = False
        # Intersect the sets to find letters in the correct place,
        # then sort the sets (converted to lists) by index to put
        # them in word order
        user_guess: set = self._word_to_ordered_pairs(guess_word.lower())
        green_letters: set = self._ordered_pair_word & user_guess
        other_letters: set = user_guess - green_letters
        other_letters_ordered: list = list(other_letters)
        other_letters_ordered.sort()

        # Create a result of LetterBox.RIGHT codes; one for each
        # correct letter.
        result: list = [LetterBox.RIGHT] * len(green_letters)

        # If there are other letters, find which ones
        # are in the word but in the wrong place
        # and add to the result.
        if len(other_letters_ordered) > 0:
            answer_word: list = []
            remaining_letters_word: set = self._ordered_pair_word - green_letters
            for pair in remaining_letters_word:
                answer_word.append(pair[1])
            for pair in other_letters_ordered:
                if pair[1] in answer_word:
                    result.insert(pair[0], LetterBox.RIGHT_NOT_THERE)
                    answer_word.remove(pair[1])
                else:
                    result.insert(pair[0], LetterBox.WRONG)
                    self._eliminated_letters.append(pair[1])
                other_letters_ordered = other_letters_ordered[1:]
        else:
            won = True

        # Sort the eliminated letters alphabetically and print
        # This could be improved to be part of an enhanced system
        # that stores eliminated letters for individual LetterBox's.
        # It should be converted to a set to remove duplicates, but
        # in the current system it's not really used.
        self._eliminated_letters.sort()
        #print(self._eliminated_letters)
        
        return result, won

    
class LetterBox(pygame.sprite.Sprite):
    """A box with a letter in it.  Begins white, but once the guess
       is established, changes to appropriate color based on status of
       the letter in the guess."""

    # Annotate class-level fields
    # Define status constants and size constants
    NEUTRAL: int = 0
    RIGHT: int = 1
    WRONG: int = 2
    RIGHT_NOT_THERE: int = 3
    SIZE: int = 60
    SELECTED_SIZE: int = 68
    BORDER_WIDTH: int = 3

    # Define font and colors
    # Internal box colors are indexed by the constants above
    _font: pygame.font.Font = pygame.font.SysFont("Helvetica", 48)
    _border_color: tuple = (0, 0, 0)
    colors: list = [(255, 255, 255), (167, 229, 112), (180, 180, 180), (244, 237, 130)]

    # Define surfaces for the different statuses
    # Surfaces are indexed by the constants above
    surface: pygame.Surface
    _surfaces: list = []
    for i in range(NEUTRAL, RIGHT_NOT_THERE + 1):
        surface = pygame.Surface((SIZE - BORDER_WIDTH * 2,
                                  SIZE - BORDER_WIDTH * 2))
        surface.fill(colors[i])
        _surfaces.append(surface)
    _selected: pygame.Surface = pygame.Surface((SELECTED_SIZE - BORDER_WIDTH * 2,
                                                SELECTED_SIZE - BORDER_WIDTH * 2))
    _selected.fill(colors[NEUTRAL])

          
    # Annotate object-level fields
    _letter: str
    _inside: pygame.Surface
    _status: int
    _selected: bool
    _selected_image: pygame.Surface
    _unselected_image: pygame.Surface

    def __init__(self, location: tuple) -> None:
        super().__init__()
        # Create a neutral-colored surface with a black border
        self.image = pygame.Surface((LetterBox.SIZE, LetterBox.SIZE))
        self._unselected_image = self.image
        self._selected_image = pygame.Surface((LetterBox.SELECTED_SIZE, LetterBox.SELECTED_SIZE))
        self.image.fill(LetterBox._border_color)
        self._inside = LetterBox._surfaces[LetterBox.NEUTRAL]
        self.image.blit(self._inside, (LetterBox.BORDER_WIDTH, LetterBox.BORDER_WIDTH))
        self.rect = self.image.get_rect()
        self.rect.topleft = location
        # No letter, neutral status, not selected
        self._letter = ""
        self._status = LetterBox.NEUTRAL
        self._selected = False

    def get_clone_location(self) -> tuple:
        return(self.rect.left, self.rect.top + self.image.get_height() + 20)

    def _draw_letter(self) -> None:
        """Draw the box's letter to its surface."""
        offset: int = (LetterBox.SELECTED_SIZE - LetterBox.SIZE) / 2
        font_surf = LetterBox._font.render(self._letter, True, (0,0,0))
        if self._selected:
            self.image.blit(font_surf, (15 + offset, offset))
        else:
            self.image.blit(font_surf, (15, 0))

    def _draw_box(self) -> None:
        """Draw the box outline and color background."""
        # Fill the inner part of the letter with the appropriate color
        self._inside = LetterBox._surfaces[self._status]     
        if self._selected:
            self._inside = LetterBox._selected
        self.image.blit(self._inside, (3, 3))

    def set_letter(self, letter: str) -> None:
        """Set the box's letter and draw."""
        self._letter = letter
        self._draw_box()
        self._draw_letter()

    def get_letter(self) -> str:
        """Return the current letter."""
        return self._letter

    def set_status(self, status: int) -> None:
        """Set the status of the box and draw."""
        if self._status == LetterBox.NEUTRAL:
            self._status = status
            self._draw_box()
            self._draw_letter()

    def change_select_status(self, selected: bool) -> None:
        """Set the select status and draw."""
        offset: int = (LetterBox.SELECTED_SIZE - LetterBox.SIZE) / 2
        if self._selected != selected:
            self._selected = selected
            # Change to the selected image and adjust the location
            location: tuple = self.rect.topleft
            if selected:
                self.image = self._selected_image
                self.rect.topleft = (location[0] - offset, location[1] - offset)
            else:
                self.image = self._unselected_image
                self.rect.topleft = (location[0] + offset, location[1] + offset)
            # Draw
            self._draw_box()
            self._draw_letter()



class KeyboardLetter():
    """A letter in the KeyboardHints sprite."""
    
    LETTER_SIZE: int = 30
    _NEUTRAL_COLOR: tuple = (220, 220, 220)
    _font: pygame.font.Font = pygame.font.SysFont("Helvetica", 24)
    _image: pygame.Surface
    _letter: str

    def __init__(self, letter: str) -> None:
        """Create the surface."""
        self._image = pygame.Surface((self.LETTER_SIZE, self.LETTER_SIZE))
        self._image.fill(self._NEUTRAL_COLOR)
        text: pygame.Surface = self._font.render(letter, True, (0,0,0))
        self._image.blit(text, (5, 5))
        self._letter = letter

    def get_image(self) -> pygame.Surface:
        """Return the image."""
        return self._image

    def change_status(self, status: int) -> None:
        """Redraw according to the new status."""
        color: tuple
        color = LetterBox.colors[status]
        self._image.fill(color)
        text: pygame.Surface = self._font.render(self._letter, True, (0,0,0))
        self._image.blit(text, (5, 5))
        

class KeyboardHints(pygame.sprite.Sprite):
    """All letters showing which are in the word, which have been eliminated,
       and which haven't been put in the right place yet."""

    _letters: list

    def __init__(self, location: tuple) -> None:
        super().__init__()
        self._init_letters()
        self._draw_image()
        self.rect = self.image.get_rect()
        self.rect.topleft = location

    def _init_letters(self) -> None:
        """Create 26 letter surfaces."""
        # Annotate and initialize variables
        letter_code: int
        self._letters = []
        # Make 26 surfaces for the letters and store in a list
        # Not qwerty at this time :(
        for letter_code in range(65, 91):
            self._letters.append(KeyboardLetter(chr(letter_code)))

    def _draw_image(self) -> None:
        """Draw the 26 letters to the image surface."""
        # Annotate and initialize variables
        x: int = 0
        y: int = 0
        i: int
        # Create the image surface.
        self.image = pygame.Surface((350, 105))
        self.image.fill((255, 255, 255))
        # Iterate through the letters and blit them to the image.
        for i in range(10):
            self.image.blit(self._letters[i].get_image(), (x, y))
            x += KeyboardLetter.LETTER_SIZE + 5
        x = 0
        y += KeyboardLetter.LETTER_SIZE + 5
        for i in range(10, 19):
            self.image.blit(self._letters[i].get_image(), (x, y))
            x += KeyboardLetter.LETTER_SIZE + 5
        x = 0
        y += KeyboardLetter.LETTER_SIZE + 5
        for i in range(19, 26):
            self.image.blit(self._letters[i].get_image(), (x, y))
            x += KeyboardLetter.LETTER_SIZE + 5

    def set_letter_status(self, letter: str, status: int) -> None:
        """Change the color of the letter to reflect its new status."""
        self._letters[ord(letter) - 65].change_status(status)
        self._draw_image()

        

def make_window(width: int, height: int, caption: str) -> pygame.Surface:
    """Create and return a pygame window."""
    screen: pygame.Surface
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(caption)
    return screen

def change_selected_letter(deselect: LetterBox, select: LetterBox) -> None:
    """Change the selected letter."""
    select.change_select_status(True)
    deselect.change_select_status(False)

def main() -> None:
    """Add a function description."""
    # Annotate and initialize variables
    WIDTH: int = 640
    HEIGHT: int = 640
    kb_hints_x: int = 20 # 145?
    kb_hints_y: int = 500
    screen: pygame.Surface
    background: pygame.Surface
    letter: LetterBox
    group: pygame.sprite.Group
    user_quit: bool = False
    e: pygame.event.Event
    guess_status: list
    won: bool = False
    num_guesses: int = 0
    caption: str = "Play my more helpful wordl!"
    kb_hints: KeyboardHints
    game_master: GameMaster

    # Set up assets.
    screen = make_window(WIDTH, HEIGHT, caption)
    background = pygame.Surface((WIDTH, HEIGHT))
    background.fill((255, 255, 255))
    screen.blit(background, (0, 0))

    group = pygame.sprite.Group()
    box_x = 20
    box_y = 20
    current_letters: list = []
    for i in range(5):
        letter = LetterBox((box_x, box_y))
        box_x += LetterBox.SIZE + 10
        current_letters.append(letter)
        group.add(letter)
        
    active_letter_index: int = 0
    current_letters[active_letter_index].change_select_status(True)
    
    clock: pygame.time.Clock = pygame.time.Clock()
    
    game_master = GameMaster()
    kb_hints = KeyboardHints((kb_hints_x, kb_hints_y))
    group.add(kb_hints)

    # Process events until the user chooses to quit.
    while not user_quit:
        # Loop 30 times per second
        clock.tick(30)
        for e in pygame.event.get():
            # Process a quit choice.
            if e.type == pygame.QUIT:
                user_quit = True
            # If the user's typed a key, they haven't won, and we're still playing,
            # process the keypress.
            elif e.type == pygame.KEYDOWN and not won and num_guesses < 6:
                # For a letter, install it in the active letterbox.
                if (e.__dict__["key"] >= pygame.K_a
                    and e.__dict__["key"] <= pygame.K_z):
                    current_letters[active_letter_index].set_letter(e.__dict__["unicode"].upper())
                    if active_letter_index < len(current_letters) - 1:
                        active_letter_index += 1
                        change_selected_letter(current_letters[active_letter_index - 1],
                                               current_letters[active_letter_index])
                # For the arrow keys, change the active box.
                elif (e.__dict__["key"] == pygame.K_LEFT):
                    if active_letter_index != 0:
                        active_letter_index -= 1
                        change_selected_letter(current_letters[active_letter_index + 1],
                                               current_letters[active_letter_index])
                elif (e.__dict__["key"] == pygame.K_RIGHT):
                    if active_letter_index < len(current_letters) -1:
                        active_letter_index += 1
                        change_selected_letter(current_letters[active_letter_index - 1],
                                               current_letters[active_letter_index])
                # For the backspace, delete the letter and change the active box.
                elif (e.__dict__["key"] == pygame.K_BACKSPACE):
                    current_letters[active_letter_index].set_letter("")
                    if active_letter_index != 0:
                        active_letter_index -= 1
                        change_selected_letter(current_letters[active_letter_index + 1],
                                               current_letters[active_letter_index])
                # For return, collect the letters into a word, check if it's valid,
                # and if it is, get the status of each letter, set the status of the
                # current letters, and make a new set of current letters if it wasn't
                # the last guess.
                elif (e.__dict__["key"] == pygame.K_RETURN):
                    word: str = ""
                    for letter in current_letters:
                        word += letter.get_letter()
                    if (len(word)) == len(current_letters) and game_master.is_valid_word(word):
                        num_guesses += 1
                        guess_status, won = game_master.get_status(word)
                        for i in range(len(guess_status)):
                            current_letters[i].change_select_status(False)
                            current_letters[i].set_status(guess_status[i])
                            kb_hints.set_letter_status(current_letters[i].get_letter(),
                                                       guess_status[i])
                        if num_guesses < 6 and not won:
                            # Create the new set of letters
                            new_current_letters: list = []
                            for i in range(5):
                                letter = LetterBox(current_letters[i].get_clone_location())
                                new_current_letters.append(letter)
                                group.add(letter)
                            current_letters = new_current_letters
                            active_letter_index = 0
                            current_letters[active_letter_index].change_select_status(True)
                    
                    
        # Draw the background.
        group.clear(screen, background)
        group.update(screen)
        group.draw(screen)
                
        # Show the display.
        pygame.display.flip()
    pygame.quit()

main()
