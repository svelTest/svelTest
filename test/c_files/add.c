#include <stdio.h>
#include <stdlib.h>

int add(int x, int y) {
	return x + y;
}

int main(int argc, char *argv[]) {
	int first = atoi(argv[1]);
	int second = atoi(argv[2]);

	int result = first + second;

	printf("%d\n", result);
}