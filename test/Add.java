public class Add {
	public static void main(String[] args) {
		int z = add(1, 2);
		System.out.println("The sum of 1 and 2 is " + z);

		/*int a = Integer.parseInt(args[0]);
		int b = Integer.parseInt(args[1]);
		int c = add(a, b);
		System.out.println("Your sum is " + c);*/
	}

	public static int add(int x, int y) {
		return x+y;
	}
}
