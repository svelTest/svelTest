// Runs the Fibonacci number generator
// Takes an integer as input from user, outputs result to stdout
public class FibonacciMain {
	public static void main(String[] args) {
		int whichOne = Integer.parseInt(args[0]);

		System.out.println(Fibonacci.fib(whichOne));
	}
}