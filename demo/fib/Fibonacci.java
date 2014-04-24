// Calculates the nth Fibonacci number
// Starts with fib(0) = 0 and fib(1) = 1
public class Fibonacci {
	public static int fib(int n){
		if (n == 0){
			return 0;
		} else if (n== 1){
			return 1;
		} else {
			return fib(n-1) + fib(n-2);
		}
	}
}