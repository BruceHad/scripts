def read_file(filename):
	"""Reads a textfile and returns it as a list (of strings)
		
	>>> read_file('test.txt')
	['10000', '99999']
	"""
	f = open(filename, 'r')
	results = []
	for line in f:
		number = line.rstrip('\n')
		results.append(number)
		
	f.close()
	return results

def get_numbers(exclude):
	"""Provides a list of unique numbers (as strings), 5 digits long
		exluding any that start with zero and any provide 
		by in the 'exclude' list

	>>> len(get_numbers(['10000', '99999']))
	89998
	"""	
	numbers = []
	for i in range(10000, 100000):
		if str(i) not in exclude:
			numbers.append(str(i))
	return numbers
	

	
def hammingDistance(s1, s2):
    """Return the Hamming distance between equal-length sequences
	"""
    if len(s1) != len(s2):
        raise ValueError("Undefined for sequences of unequal length")
    return sum(bool(ord(ch1) - ord(ch2)) for ch1, ch2 in zip(s1, s2))

def analyse_number(number, active_numbers):
	"""Check the number against all the active numbers and 
		return the count of distances
	"""

	analysis = {
		'results': [0, 0, 0, 0, 0, 0],
		'ones': []
	}
	number = str(number)
	for acn in active_numbers:
		dist = hammingDistance(number, acn)
		analysis['results'][dist] += 1
		if dist == 1: analysis['ones'].append(acn)
		#elif dist == 2: analysis['twos'].append(acn)
	return analysis

def compare_numbers(active_numbers, available_numbers):
	"""Run a comparison between all available numbers and 
		active numbers and generate a results file
	"""
	f = open('results.csv', 'w')
	f.write('list_number,zeros,ones,twos,threes,fours,fives, \n')
	for avn in available_numbers:
		results = analyse_number(avn, active_numbers)
		zero, one, two, three, four, five = results['results']
		f.write('%s, %s, %s, %s, %s, %s, %s, \n' % (avn, str(zero), str(one), str(two), str(three), str(four), str(five)))
		if int(avn) > 15000: 
			break
	f.close()



	
if __name__ == '__main__':
	import doctest, time
	print(doctest.testmod())
	print(time.clock())
	
	active_numbers = read_file('active_ln.txt')
	all_numbers = read_file('all_ln.txt')
	#available_numbers = get_numbers(all_numbers)
	print(time.clock())
	
	print(analyse_number(10001, active_numbers))
	print(time.clock())
	
	#compare_numbers(active_numbers, available_numbers)
	#print(time.clock())
