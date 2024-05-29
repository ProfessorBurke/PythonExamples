"""A quick Turing Machine-based puzzle using pygame and pygame_gui."""

# Import and initialize pygame and pygame_gui.
import pygame
import pygame_gui
from pygame_gui.core import ObjectID

pygame.init()

# Background image color
BACKGROUND_COLOR: tuple = (147, 198, 224)

class PuzzleTable(pygame.sprite.Sprite):
    """The table representing the function delta for the
       Turing machine."""

    # Annotate object-level fields
    _states: list
    _symbols: list
    _font: pygame.font.Font
    _manager: pygame_gui.UIManager
    _symbols_gui_choices: list
    _states_gui_choices: list
    _users_delta: dict

    def __init__(self, loc: tuple, states: list, symbols: list,
                 manager: pygame_gui.UIManager) -> None:
        """Create the PuzzleTable puzzle from parameters."""
        # Initialize the sprite components.
        super().__init__()
        # Initialize fields from parameters.
        self._states = states
        self._symbols = symbols
        self._manager = manager
        self._users_delta = {}
        # Make the image
        self._font = pygame.font.SysFont("Courier New", 18)
        self.image = pygame.Surface((600, 60 + 30 * len(states) * len(symbols)))
        self.image.fill(BACKGROUND_COLOR)
        # Put the table in the image
        y: int = 0
        temp: pygame.Surface
        temp = self._font.render("{:<25s}{}".format("In", "Out"), True, (0, 0, 0))
        self.image.blit(temp, (0, y))
        y += 30
        temp = self._font.render("{:<15s}{:<10s}{:<15s}{:s}".format("State", "Symbol", "State", "Symbol"), True, (0, 0, 0))
        self.image.blit(temp, (0, y))
        y += 30
        self._symbols_gui_choices = []
        self._states_gui_choices = []
        for state in states:
            for symbol in symbols:
                # Put the static text in for in state (state / symbol)
                temp = self._font.render("{:<15s}{:s}".format(state, symbol), True, (0, 0, 0))
                self.image.blit(temp, (0, y))
                # Add drop-downs for state and symbol for out state, add to lists
                # of GUI components, and add to user's delta dictionary.
                self._states_gui_choices.append(
                    pygame_gui.elements.UIDropDownMenu(
                        options_list=states + ["Halt"],
                        starting_option=states[0],
                        relative_rect=pygame.Rect((280 + loc[0], y + loc[1]), (150, 30)),
                        manager=manager))
                self._symbols_gui_choices.append(
                    pygame_gui.elements.UIDropDownMenu(
                        options_list= symbols + ["L", "R"],
                        starting_option=symbols[0],
                        relative_rect=pygame.Rect((440 + loc[0], y + loc[1]), (150, 30)),
                        manager=manager))
                self._users_delta[(state, symbol)] = (states[0], symbols[0])
                y += 30
        self.rect = self.image.get_rect()
        self.rect.topleft = loc

    def new_state(self, from_state: tuple) -> tuple:
        """Return the state from the user's delta given the from_state."""
        return self._users_delta[from_state]

    def update(self) -> None:
        """Create a delta function from the currently selected options in the table."""
        # Index into the gui components lists.
        index: int
        # Index into the lists of states and symbols.
        i: int
        j: int
        # Iterate, composing the dictionary from the user's choices.
        for i in range(len(self._states)):
            for j in range(len(self._symbols)):
                index = i*3+i+j
                self._users_delta[(self._states[i], self._symbols[j])] = (self._states_gui_choices[index].selected_option[0],
                  self._symbols_gui_choices[index].selected_option[0])

class State(pygame.sprite.Sprite):
    """A graphical representation of the states and the current state."""

    # Class-level constant, a dictionary of arrow degrees by state.
    ROTATIONS = {"Red House": 90, "Orange House": 0, "Yellow House": 270,
                 "Halt": 180}

    # Object-level fields.
    _raw_image: pygame.Surface
    _raw_arrow: pygame.Surface
    _text_state: str
    
    def __init__(self, loc: tuple, start_state: str) -> None:
        """Load the image of states and the arrow."""
        # Initialize the Sprite components
        super().__init__()
        # A Surface to blit for the arrow.
        arrow: pygame.Surface
        # Set the text version of the start state from parameter.
        self._text_state = start_state
        # Load the images and locate the sprite.
        self._raw_image = pygame.image.load("state.jpg")
        self.image = pygame.image.load("state.jpg")
        self.rect = self.image.get_rect()
        self.rect.topleft = loc
        self._raw_arrow = pygame.image.load("arrow_smaller.png").convert_alpha()
        arrow = pygame.transform.rotate(self._raw_arrow, State.ROTATIONS[start_state])
        self.image.blit(arrow, (0, 0))

    def change_state(self, new_state: str) -> None:
        """Redraw the image based on the new state, set the text state field."""
        # A Surface to blit for the arrow.
        arrow: pygame.Surface
        # Set the text state field.
        self._text_state = new_state
        # Draw the image.
        self.image.blit(self._raw_image,(0, 0))
        arrow = pygame.transform.rotate(self._raw_arrow, State.ROTATIONS[new_state])
        self.image.blit(arrow, (0, 0))

    def get_text(self) -> str:
        """Return the text field."""
        return self._text_state
    

class Tape(pygame.sprite.Sprite):
    """A Tape object has a reading head and an ordered list of
       uniformly-sized colors."""

    # Class-level constants
    WIDTH: int = 40
    HEIGHT: int = 40
    HEAD_HEIGHT: int = 10
    COLORS: list = [(200, 30, 30),
                    (240, 160, 80),
                    (240, 240, 150),
                    (255, 255, 255)]
    COLOR_NAMES: list = ["red", "orange", "yellow", "#"]

    # Object-level fields
    _current: int
    _head: pygame.Surface
    _colors: list

    def __init__(self, colors: list, loc: tuple) -> None:
        """Create the tape from the list of colors passed, locate at loc."""
        # Initialize the sprite components.
        super().__init__()
        # Create and locate the Surface.
        self.image = pygame.Surface((len(colors)*Tape.WIDTH, Tape.HEIGHT + Tape.HEAD_HEIGHT))
        self.image.fill(BACKGROUND_COLOR)
        self.rect = self.image.get_rect()
        self.rect.topleft = loc
        # Draw the tape colors.
        x: int = 0
        color: int
        for color in colors:
            pygame.draw.rect(self.image, Tape.COLORS[color], (x, Tape.HEAD_HEIGHT, Tape.WIDTH, Tape.HEIGHT))
            x += Tape.WIDTH
        # Draw the head.
        self._head = pygame.image.load("head.png").convert_alpha()
        self._current = 0
        self.image.blit(self._head, (self._current * Tape.WIDTH +
                                     (Tape.WIDTH / 2 - self._head.get_rect().width / 2), 0))
        # Store the tape contents from parameter.
        self._colors = colors

    def move_right(self) -> bool:
        """Move the head to the right, return True if successful,
           False otherwise."""
        success: bool = False
        # Determine whether it's possible to move right and if so,
        # move right.
        if self._current < len(self._colors) - 1:
            self._current += 1
            success = True
        return success

    def move_left(self) -> bool:
        """Move the head to the left, return True if successful,
           False otherwise."""
        success: bool = False
        # Determine whether it's possible to move left and if so,
        # move left.
        if self._current > 0:
            self._current -= 1
            success = True
        return success

    def change_color(self, color: str) -> None:
        """Change the color under the head to the color passed."""
        self._colors[self._current] = Tape.COLOR_NAMES.index(color)

    def get_current_color(self) -> str:
        """Return the current color name."""
        return self._colors[self._current]

    def update(self) -> None:
        """Draw the tape."""
        # Fill with the background color and then redraw.
        self.image.fill(BACKGROUND_COLOR)
        x: int = 0
        color: int
        for color in self._colors:
            pygame.draw.rect(self.image, Tape.COLORS[color], (x, Tape.HEAD_HEIGHT, Tape.WIDTH, Tape.HEIGHT))
            x += Tape.WIDTH
        # Draw the head.
        self.image.blit(self._head, (self._current * Tape.WIDTH +
                                    (Tape.WIDTH / 2 - self._head.get_rect().width / 2), 0))
        

def make_window(size: tuple, caption: str) -> pygame.Surface:
    """Create and return a pygame window."""
    screen: pygame.Surface
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption(caption)
    return screen

def main() -> None:
    """Draw the sprite and gui components and process events."""
    # Annotate and initialize variables
    HEIGHT: int = 930
    WIDTH: int = 700
    screen: pygame.Surface
    background: pygame.Surface
    user_quit: bool = False
    e: pygame.event.Event
    caption: str = "Change the rules to make a rainbow"
    # Turing sprites and group.
    state: State
    puzzle_table: PuzzleTable
    tape: Tape
    turing_elements_group: pygame.sprite.Group
    # Manager for the GUI components and components.
    manager: pygame_gui.UIManager
    step: pygame_gui.elements.UIButton

    # Set up assets.
    screen = make_window((WIDTH, HEIGHT), caption)
    background = pygame.image.load("background.jpg").convert()
    screen.blit(background, (0, 0))
    clock: pygame.time.Clock = pygame.time.Clock()

    # Set up the GUI manager.
    manager = pygame_gui.UIManager((WIDTH, HEIGHT), "button_theme.json")

    # Create the Turing sprites and group.
    state = State((50, 110), "Red House")
    tape = Tape([2,1,0], (450, 125))
    puzzle_table = PuzzleTable((50,450), 
                               ["Red House", "Orange House", "Yellow House"],
                               ["red","orange","yellow","#"],
                               manager)
    turing_elements_group = pygame.sprite.Group([tape, puzzle_table, state])
    
    # Create the button
    step = pygame_gui.elements.ui_button.UIButton(
        relative_rect=pygame.Rect((450, 200), (83, 63)),
        text='',
        manager=manager,
        tool_tip_text='Advance simulation by one step',
        object_id = ObjectID(class_id = "@control_button",
                             object_id='#step_button')
    )


    # Process events until the user chooses to quit.
    while not user_quit:
        # Loop 30 times per second
        time_delta = clock.tick(60)/1000.0
        for e in pygame.event.get():
            # Process a quit choice.
            if e.type == pygame.QUIT:
                user_quit = True

            if e.type == pygame_gui.UI_BUTTON_PRESSED:
                if e.ui_element == step:
                    color_index = tape.get_current_color()
                    new_state, symbol = puzzle_table.new_state((state.get_text(), Tape.COLOR_NAMES[color_index]))
                    state.change_state(new_state)
                    if symbol == "R":
                        if not tape.move_right():
                            print("Error!")
                    elif symbol == "L":
                        if not tape.move_left():
                            print("Error!")
                    else:
                        tape.change_color(symbol)
                    if new_state == "Halt":
                        print("Finished!")

            # Let the UI Manager handle UI events
            manager.process_events(e)
                    
        # Clear, update, draw.
        manager.update(time_delta)
        turing_elements_group.clear(screen, background)
        turing_elements_group.update()

        # This seems to be necessary for the UI elements --
        # not sure if this can be done with a clear.
        screen.blit(background, (0, 0))
        
        turing_elements_group.draw(screen)
        manager.draw_ui(screen)
                
        # Show the display.
        pygame.display.flip()
    pygame.quit()

main()
