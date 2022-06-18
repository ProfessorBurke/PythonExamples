import { addExercise, Code, Frame, Terminal } from 'https://horstmann.com/codecheck/script/codecheck_tracer.js'
addExercise(function*(sim, state) {


const code = sim.add(0, 0, new Code(`
plane_answer: str
packing_list: str = ""

# Obtain the answer to the air travel question from the user.
plane_answer = input("Are you traveling by plane? (yes / no): ")

# Determine what should be packed based on the travel answer.
if plane_answer == "yes":
    packing_list += "headphones\\nreading material"

# Display the packing list to the user.
if packing_list != "":
    print(packing_list)
`))

const term = sim.add(15, 0, new Terminal())
const vars = sim.add(14, 5, new Frame())

yield sim.start(state)
code.go(2)
vars.packing_list = ""
yield sim.next("Initialize packing_list to the empty string.")

code.go(5)
term.print("Are you traveling by plane? (yes / no): ")
let plane_answer = yield term.ask()
vars.plane_answer = plane_answer


yield code.ask(8)

if (plane_answer === "yes") {
	yield code.ask(9)
	vars.packing_list = "headphones\nreading material"

	code.go(12)
	yield sim.pause()
	code.go(13)
	term.println("headphones")
	term.println("reading material")
} else {
	yield code.ask(12)
}

})