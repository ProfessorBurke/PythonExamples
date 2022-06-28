import { addExercise, Code, Frame, Terminal } from 'https://horstmann.com/codecheck/script/codecheck_tracer.js'
addExercise(function*(sim, state) {


const code = sim.add(0, 0, new Code(`
`))

const term = sim.add(15, 0, new Terminal())
const vars = sim.add(14, 5, new Frame())

// Start the simulation -- yield sim.start(state)
// Jump to a line -- code.go(#)
// Ask the user what line -- yield code.ask(#)
// Note to the user -- yield sim.next("Note")
// Terminal methods: term.print(), term.println(), yield term.ask
// Assigning a variable: let varName =


})


/*
Public URL (for your students): 
Edit URL (for you only): 
*/