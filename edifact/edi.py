import string
from collections import OrderedDict

def write_file(filename, data):
	f = open(filename, 'w')
	first = True
	line = ''
	
	# Print column headings
	for column in data:
		line += column
		line += ','
		if('claim_count' not in locals()):
			claim_count = len(data[column])
		else:
			assert(claim_count == len(data[column]))
	f.write(line+'\n')
	
	for i in range(claim_count):
		line = ''
		for column in data:
			line += data[column][i]
			line += ','
		f.write(line+'\n')
	f.close()
	
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

def get_segments(data):
	"""First pass at parsing edifact.
	reads data from file and seperates the edifact segments
	
		edifact.src first line of the file (source email address)
		edifact.claims - List of segments for each claim
		edifact.unb & unz - transmission wrapper data
	
	"""
	
	edifact = {}
	edifact['src'] = data[0]
	segments = string.split(data[1], "'")
	edifact['claims'] = []
	first = False;
	for s in segments:
		segment_name = s[:3]
		if(segment_name == ''): 
			continue
		if(segment_name in ['UNB','UNZ']):
			edifact[segment_name] = string.split(s[4:], '+')
			continue
		if(segment_name == 'UNH'):
			# First segment of new claim so
			# push any previous claim to claims list
			if('claim' in locals()): edifact['claims'].append(claim)
			# and reset claim to start again
			claim = {}
		claim[segment_name] = string.split(s[4:], '+')
	# remember and push last claim
	if('claim' in locals()): edifact['claims'].append(claim)
	
	# i = 0
	# for claim in edifact['claims']:
		# print(i)
		# for segment in claim:
			# print(segment, claim[segment])
		# i += 1
		
	return edifact

def get_components(edifact):
	""" Second pass at parsing file. Cleans up parsed edifact and extract relevant data to csv for printing
	"""
	# Set up results file (with common data fields)
	results = OrderedDict()
	results['source'] = []
	results['unb_sender_id'] = []
	results['unb_date_time'] = []
	# results['unb_interchange'] = []
	# results['unb_app_reference'] = []
	# results['unz_count'] = []
	# results['unz_reference'] = []
	
	
	# Define claim segments required
	segments = {
		'PNA': ['Party Qualifier', 'List Number', 'Pin No', 'BLANK'],
		'PAT': ['CHI', 'Surname', 'Forename', 'Sex', 'Title', 'Address','Previous Surname','DOB'],
		'RFF': ['Reference number'],
		'CED': ['BLANK', 'PMS'],
		'TDA': ['Treatment Dates', 'Claim Type', 'Treatment Type', 'Declaration'],
		'CHX': ['Patient Charge', 'Amount Claimed', 'ER Code']
	}
	claims = edifact['claims']
	for i in range(len(claims)):	
		# Add in all the wrapper information
		results['source'].append(edifact['src'])
		results['unb_sender_id'].append(edifact['UNB'][1])
		results['unb_date_time'].append(edifact['UNB'][3])
		# results['unb_interchange'].append(edifact['UNB'][4])
		# results['unb_app_reference'].append(edifact['UNB'][6])
		# results['unz_count'].append(edifact['UNZ'][0])
		# results['unz_reference'].append(edifact['UNZ'][1])
		
		for s in segments:
			seg_headings = segments[s]
			data = claims[i][s]
			for j in range(len(seg_headings)):
				heading = seg_headings[j]
				if heading == 'BLANK': 
					continue
				value = data[j] if j < len(data) else ''
				if(heading not in results):
					results[heading] = [value]
				else:
					results[heading].append(value)
	return results

def get_specials(edifact):
	"""Special cases like 
	return data
	"""
	claims = edifact['claims']
	results = OrderedDict()
	results['Treatments'] = []
	for i in range(len(claims)):
		if 'TST' not in claims[i]:
			t = ''
		else: 
			t = ' '.join(claims[i]['TST'])
		results['Treatments'].append(t)
	return results
	
def merge(x, y):
	""" Merge two dicts
	"""
	z = x.copy()
	z.update(y)
	return z

	
	
	
if __name__ == '__main__':
	filename = 'src/105078 1604301741002262 GP17 0.txt';
	file = read_file(filename)
	segments = get_segments(file)
	components = get_components(segments)
	specials = get_specials(segments)
	write_file('results.csv', merge(components, specials))
