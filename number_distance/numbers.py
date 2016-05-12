import random, os.path

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

def write_file(filename, data):
	f = open(filename, 'w')
	for line in data:
		f.write(line+'\n')
	f.close()

def write_data(data, filename, append = False, header = False):
	"""Writes a list of dicts to a csv file.
	Option to:
		append to existing file or create a new file
		include a header based on dict keys

	e.g write_data([{'one': 1, 'two': 2}, {'one': 1, 'two': 2}])
	"""
	first = True	
	if append:	f = open(filename+'.csv', 'a')
	else: f = open(filename+'.csv', 'w')
	for line in data:
		if first and header:
			count = 0
			for key,value in line.items():
				f.write(str(key) + ',')
				count += 1
				if(count == len(line)):
					first = False
					break;
			f.write('\n')
		for key, value in line.items():
			# print rest of data
			f.write('\"' + str(value) + '\",')
		f.write('\n')
	f.close()

def get_numbers(exclude, cache = True):
	"""Provides a list of unique numbers (as strings), 5 digits long
		exluding any that start with zero and any provide 
		by in the 'exclude' list

		If cache true, check for existing file first. If not available, generate list and write to cache file for next
		run.
		
	>>> len(get_numbers(['10000', '99999'], False))
	89998
	"""	
	filename = 'get_numbers_cache.txt'
	numbers = []
	if cache and os.path.isfile(filename):
		numbers = read_file(filename)
	else:
		for i in range(10000, 100000):
			if str(i) not in exclude:
				numbers.append(str(i))	
	if cache:
		write_file(filename, numbers)
		
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
		'number': number,
		'zero_transform': 0,
		'one_transform': 0,
		'two_transform': 0,
		'three_transform': 0,
		'four_transform': 0,
		'five_transform': 0,
		'one_transform_numbers': []
	}
	number = str(number)
	for acn in active_numbers:
		dist = hammingDistance(number, acn)
		if dist == 0: 
			analysis['zero_transform'] += 1
		elif dist == 1: 
			analysis['one_transform'] += 1
			analysis['one_transform_numbers'].append(acn)
		elif dist == 2: 
			analysis['two_transform'] += 1
		elif dist == 3: 
			analysis['three_transform'] += 1
		elif dist == 4: 
			analysis['four_transform'] += 1
		elif dist == 5: 
			analysis['five_transform'] += 1
		else:
			console.log('Error: distance > 5')
	return analysis

def compare_numbers(compare_nos, candidate_nos, reinclude_candidates = True):
	"""Run a comparison between all available numbers and 
		active numbers and generate a results file
	"""
	print('Approx. Comparisons: %d' % (len(candidate_nos) * len(compare_nos)))
	print('Available Numbers: %d' % len(candidate_nos))
	
	segments = 2000
	filename = 'results3_'+str(len(candidate_nos))
	results, count, runs = [], 0, 1
	for candidate in candidate_nos:
		count += 1
		result = analyse_number(candidate, compare_nos)
		if(result):
			results.append(result)
			if reinclude_candidates and result['one_transform'] == 0: 
				compare_nos.append(candidate)
		if count == segments:
			print(runs, runs * segments)
			if runs == 1: write_data(results, filename, False, True)
			else: write_data(results, filename, True, False)
			results, count = [], 0
			runs += 1
	# Print final set
	print(runs, (runs-1) * segments + count)
	write_data(results, filename, True, False)
	


		
def test_performance(comparison_numbers):
	n = 1000
	#test hammingDistance
	a = time.clock()
	x, y = str(random.randrange(10000,99999)), str(random.randrange(10000,99999))
	
	for i in range(n):		
		hammingDistance(x, y)
	b = time.clock() - a
	print(n, b, b/n)

	# test analyse_number
	a = time.clock()
	for i in range(n):
		analyse_number(x, comparison_numbers)
	b = time.clock() - a
	print(n*len(comparison_numbers), b, b/(n*len(comparison_numbers)))
	
	
	
if __name__ == '__main__':
	import doctest, time
	print(doctest.testmod())

	active_numbers = read_file('active_ln.txt') 
	all_numbers = read_file('all_ln.txt') 
	candidates = get_numbers(all_numbers, True)
	
	# Test performance of hammingDistance
	#test_performance(active_numbers)	
	
	# Lets check active numbers against themselves
	# test_numbers = read_file('test_numbers.txt')
	#comparison = compare_numbers(active_numbers, active_numbers, False)
	compare_numbers(active_numbers, candidates, True)
	
	