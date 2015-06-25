import string

numbers = "zero one two three four five six seven eight nine".split()
numbers.extend("ten eleven twelve thirteen fourteen fifteen sixteen".split())
numbers.extend("seventeen eighteen nineteen".split())
numbers.extend(tens if ones == "zero" else (tens + "-" + ones) 
for tens in "twenty thirty forty fifty sixty seventy eighty ninety".split()
for ones in numbers[0:10])

def numToWord(i):
	if i > 99 or i < 0: return "Value out of range"
	return numbers[i]