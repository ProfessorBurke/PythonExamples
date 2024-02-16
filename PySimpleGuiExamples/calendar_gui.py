import PySimpleGUI as sg

sg.theme('DarkAmber')   # Add a touch of color
# All the stuff inside your window.
layout = [  [sg.Text('Some text on Row 1')],
            [sg.Text('Enter something on Row 2'), sg.InputText()],
            [sg.Spin([x for x in range(31)])],
            [sg.FileBrowse()],
            [sg.Button('Ok'), sg.Button('Cancel')] ]
running: bool = True
event: str
values: dict

# Create the Window
window = sg.Window('Window Title', layout)
# Event Loop to process "events" and get the "values" of the inputs
while running:
    event, values = window.read()
    if event == sg.WIN_CLOSED: 
        running = False
    print('You entered ', values[0])

window.close()
