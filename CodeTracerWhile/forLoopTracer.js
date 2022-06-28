import { addExercise, Code, Frame, Terminal } from 'https://horstmann.com/codecheck/script/codecheck_tracer.js'
addExercise(function*(sim, state) {

// Create the code block in the upper left.
const code = sim.add(0, 0, new Code(`
"""Obtain three numbers and report the sum.
"""

# Annotate and initialize variables.
i: int
num: int
total: int = 0

# Obtain three numbers and total them.
for i in range(3):
    num = int(input("Please enter a whole number: "))
    total += num

# Display the total.
print("The total of your values is {}.".format(total))
`))

// Create a terminal for console input and output in the upper right.
const term = sim.add(15, 0, new Terminal())

// Create a frame for the variables below the terminal.
const vars = sim.add(13, 5, new Frame())


// Start the simulation when the user clicks start.
yield sim.start(state)

// Jump down to first variable annotation and pause for the user
// to click next.
code.go(5)
yield sim.next("Annotate variables.")

// Jump down to initialization of total and pause for the user
// to click next and give total its initial value.
code.go(7); yield sim.next("Initialize the accumulator total to zero.")
vars.total = 0

// Now ask the user which line executes next -- the loop header.
yield code.ask(10)
vars.i = 0

// Obtain and sum three numbers in a loop.
while (vars.i < 3) {
	// Ask the user which line executes next -- the first line of
	// the loop three times.
	yield code.ask(11)
	// Obtain the number from the user
	term.print("Please enter a whole number: ")
	vars.num = parseInt(yield term.ask())
	// Jump to the line in which the number is added to the accumulator
	// and ask the user to enter the new total.
	code.go(12)
	vars.total = parseInt(yield sim.ask(vars.total + vars.num, "Please enter the new value for total."))
	// Ask the user which line executes next (the loop header).
	yield code.ask(10)
	vars.i = vars.i + 1
}

// Ask the user which line executes next -- the first line after
// the loop when the loop is no longer entered.
yield code.ask(15)

term.println(`The total of your values is ${vars.total}.`)

})


/*
Public URL (for your students): https://codecheck.io/tracer/2206272232aufgx0satrza6xzi52e8ptjlz
Edit URL (for you only): https://codecheck.io/private/problem/2206272232aufgx0satrza6xzi52e8ptjlz/541YKAPY2T3AG49GBWLEAY11W
*/