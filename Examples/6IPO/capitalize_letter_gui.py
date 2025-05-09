"""
    Write a GUI program that allows the user to type letters into
    boxes.  Each letter should be converted to uppercase
    before being shown in the box.

"""
import PySimpleGUI as sg

# Annotate variables
CASE_SHIFT: int =  ord("A") - ord("a")
user_quit: bool
event: str                     
values: dict[str, str]         
i: int                         
val: str                       
char: str                      
current_index: int             
layout: list[list[sg.Element]]

# Create five input boxes with a size suitable to hold a single uppercase letter.
layout = [
    [
        sg.Input("", key=f"-IN{i}-", size=(2, 1), justification="center", font=("Courier New", 24), enable_events=True)
        for i in range(5)
    ]
]

# Create a window for the boxes.
window = sg.Window("Letter Boxes", layout, finalize=True)

# Focus on the first input.
current_index = 0
window[f"-IN{current_index}-"].set_focus()

# Now handle typing events until the user chooses to quit.
user_quit = False
while not user_quit:

    # Get the event.
    event, values = window.read()

    # If they chose to quit, we're done.
    if event == sg.WIN_CLOSED:
        user_quit = True

    # Otherwise, loop through the boxes to find which has the focus -- that's the
    # box we'll put the character in if the user has typed.
    for i in range(5):
        if event == f"-IN{i}-":
            val = values[f"-IN{i}-"]
            if val:
                # Only keep the first character, and convert to uppercase.
                if len(val) > 0:
                    char = val[0]
                    # Conver the character to uppercase
                    char = chr((ord(char) + CASE_SHIFT))
                    window[f"-IN{i}-"].update(char)
                    if char.isalpha() and current_index < 4:
                        current_index = i + 1
                        window[f"-IN{current_index}-"].set_focus()
            elif current_index > 0:
                # If input is empty after a backspace, move back
                current_index = max(0, i - 1)
                window[f"-IN{current_index}-"].update("")
                window[f"-IN{current_index}-"].set_focus()

window.close()
