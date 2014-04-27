import sys

class Add(object):

	def add(self, x, y):
		return x + y

if __name__ == "__main__":

	if len(sys.argv) != 3:
		print "Usage: python add.py <int> <int>"
	else:	
		arg1 = int(sys.argv[1])
		arg2 = int(sys.argv[2])

		print add.add(arg1, arg2)