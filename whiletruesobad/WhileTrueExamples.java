/**
	Examples of while(true) loops, original, imagined, and fixed.
*/

import java.util.Scanner;

class WhileTrueExamples {
	
	/**
	   Method to determine if the loop should still run based on
	   the values of a, b, and c.
	   @param a an integer
	   @param b an integer
	   @param c an integer
	   @return whether we're still running, a boolean
	*/
	public static boolean stillRunning(int a, int b, int c) {
		return a > 0 && b > 0 && c > 0;
	}
	
	
	public static void main(String[] args) {
		
		Scanner keyboard = new Scanner(System.in);
		int inputValue = 1, inputValue2 = 1, inputValue3 = 1;
		

		// The pseudocode from the question
		//do{
			//get some input.
			//if the input meets my conditions, break;
			//Otherwise ask again.
		//} while(true)
			
		
		// The initial example from the question, rewritten with
		// the logical condition at the end, rather than as an if
		// statement and break in the middle
		do {
			System.out.print("Please enter a number between 1 and 10: ");
			inputValue = keyboard.nextInt();
			if (1 > inputValue || inputValue > 10)
				System.out.println("The number must be between 1 and 10.");
		} while(1 > inputValue || inputValue > 10);
		

		// A strawman argument about why we shouldn't use a flag
		// It seemed like several of the commenters who offered reasons why
		// while(true) was good could only imagine basically the same code
		// but with a flag inserted for the break, rather than writing
		// the logic at the top of the loop.  This is a straw man or a false
		// dichotomy because there are more than two possible ways to write the
		// loop, and the one they're not including is the best way.
		
		// The example I pulled out of the comments didn't make a whole lot
		// of sense to me, because there seemed to be a lot of other code in
		// the example mixed in with the input validation, but without context.
		
		//while (true)
		//{
			//doStuffNeededAtStartOfLoop();
			//int input = getSomeInput();
			//if (testCondition(input))
			//{
				//break;
			//}
			//actOnInput(input);
		//}
		
		// The flag version:
		//boolean running = true;
		//while (running)
		//{
		//	doStuffNeededAtStartOfLoop();
		//	int input = getSomeInput();
		//	if (testCondition(input))
		//	{
		//		running = false;
		//	}
		//	else
		//	{
		//		actOnInput(input);
		//	}
		//}

		// My imagined loop as a while(true)
		while (true) {
			System.out.print("Please enter a positive number: ");
			inputValue = keyboard.nextInt();
			System.out.print("Please enter another positive number: ");
			inputValue2 = keyboard.nextInt();
			System.out.print("Please enter a third positive number: ");
			inputValue3 = keyboard.nextInt();
			if (inputValue <= 0 || inputValue2 <= 0 || inputValue3 <= 0) {
				break;
			}
			System.out.println("Congratulations!  You entered three positive numbers.");
		}
		
		System.out.println("You've made it past the second loop.");
		
		inputValue = 1;
		inputValue2 = 1;
		inputValue3 = 1;
		
		// The imagined loop reimagined without while(true) or the flag.
		while (stillRunning(inputValue, inputValue2, inputValue3)) {
			System.out.print("Please enter a positive number: ");
			inputValue = keyboard.nextInt(); 
			System.out.print("Please enter another positive number: ");
			inputValue2 = keyboard.nextInt();
			System.out.print("Please enter a third positive number: ");
			inputValue3 = keyboard.nextInt();
			if (stillRunning(inputValue, inputValue2, inputValue3)) {
				System.out.println("Congratulations!  You entered three positive numbers.");
			}
		}
		
	}
	
}