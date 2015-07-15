from test import Test

class Tester(object):
	def __init__(self):
		return

	def run(self):
		print("Testing...")
		test = Test()
		test.run()
		print 0

def main():
	print("Running program...")
	tester = Tester()
	tester.run()
	print("Program complete!")
	return 0

print main()
