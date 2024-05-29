"""
    Turing machine parts.

    delta key is a tuple (state, symbol)
    delta value is a tuple (state, symbol / command)
"""


class TuringMachine():

    def __init__(self, alphabet: list,
                 states: list,
                 start_state: str,
                 delta: dict) -> None:
        self._alphabet = alphabet
        self._state = states
        self._start_state = start_state
        self._delta = delta

    def run(self, tape: list) -> None:
        state: str
        symbol: str
        value: tuple
        i = 0

        state = self._start_state
        symbol = tape[i]
        print("From ({},{}) ".format(state, symbol), end="")
        value = self._delta[(state, symbol)]
        state = value[0]
        symbol = value[1]
        print("To ({},{}).".format(state, symbol))
        while state != "h":
            if symbol == "L":
                i -= 1
                if i < 0:
                    print("Error, moving off the left of the tape.")
                    state = "h"
                else:
                    symbol = tape[i]
            elif symbol == "R":
                i += 1
                symbol = tape[i]
            else:
                tape[i] = symbol
            print("From ({},{}) ".format(state, symbol), end="")
            value = self._delta[(state, symbol)]
            state = value[0]
            symbol = value[1]
            print("To ({},{}).".format(state, symbol))
        print(tape)


##tm = TuringMachine(["a","#"], ["q0", "q1"], "q0",
##                   {("q0", "a"): ("q1", "#"),
##                    ("q0", "#"): ("h", "#"),
##                    ("q1", "a"): ("q0", "a"),
##                    ("q1", "#"): ("q0", "R")})
##tm.run(["a","a","a","#"])
            










tm2 = TuringMachine(["red","orange","yellow","#"], ["Red House", "Orange House", "Yellow House"],
                    "Red House",
                   {("Red House", "red"): ("Orange House", "R"),
                    ("Red House", "orange"): ("Red House", "red"),
                    ("Red House", "yellow"): ("Red House", "red"),
                    ("Red House", "#"): ("Red House", "red"),
                    ("Orange House", "red"): ("Orange House", "orange"),
                    ("Orange House", "orange"): ("Yellow House", "R"),
                    ("Orange House", "yellow"): ("Orange House", "orange"),
                    ("Orange House", "#"): ("Orange House", "orange"),
                    ("Yellow House", "red"): ("Yellow House", "yellow"),
                    ("Yellow House", "orange"): ("Yellow House", "yellow"),
                    ("Yellow House", "#"): ("Yellow House", "yellow"),
                    ("Yellow House", "yellow"): ("h", "yellow")})
tm2.run(["orange","red","yellow"])
tm2.run(["#","#","#"])
tm2.run(["yellow","red","orange"])




            
        
