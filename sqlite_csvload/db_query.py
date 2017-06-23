import sqlite3
import sys, os

DB = 'test.db' # default db
OUTPUT_DIR = 'output'

def get_query_name(query, i):
	""" Determines if the query string has a name
	
	>>> get_query_name("-- Test\\n Select...", 0)
	'Test.csv'
	>>> get_query_name("Select...", 1)
	'output_1.csv'
	>>> get_query_name("\\n-- Test Query\\n Select...", 0)
	'TestQuery.csv'
	"""
	lines = query.split('\n')
	lines = [l for l in lines if len(l) > 0]
	first_line = lines[0]
	if first_line[:2] == '--':
		for c in (' -'):
			first_line = first_line.replace(c, '')
		return  first_line + '.csv'
	else: 
		return 'output_{}.csv'.format(i)

def format_query(query_path):
	""" Takes an sql file and split into correct format
	"""
	query_list = []
	with open(query_path) as q:
		queries = q.read()
		i = 0
		for query in queries.split(';'):
			if len(query) > 0:
				query_details = {
					'name': get_query_name(query, i),
					'query': query}
				query_list.append(query_details)
				i += 1
	return query_list

def get_results(query_string):
	""" Run query against database and return results in format:
	{'header': ['column', 'headings'], 
	 'rows': [['row','data'],[...]]}
	"""
	con = sqlite3.connect(DB)
	cur = con.cursor()
	rows = cur.execute(query_string);
	results = {}
	results['header'] = [i[0] for i in rows.description]
	results['rows'] = []
	for row in rows:
		results['rows'].append([i for i in row])
	con.close()
	return results

def write_results(results, output_file):
	""" Write the results of the query to a file
	"""
	if not os.path.exists(OUTPUT_DIR):
		os.makedirs(OUTPUT_DIR)
		os.chmod(OUTPUT_DIR, 0o666)
		
	cur_dir = os.getcwd()
	os.chdir(OUTPUT_DIR)
	
	with open(output_file, 'w') as f:
		f.write(', '.join(results['header']))
		f.write('\n')
		for row in results['rows']:
			f.write(', '.join(row))
			f.write('\n')
			
	os.chdir(cur_dir)
	
def run_query(query):
	""" Runs a query (list) against the DB. 
		Query can be either a file path or a string.
		Results are written to an output file
	"""	
	# Read the query from file or set as string.
	if os.path.exists(query):
		query_list = format_query(query)
	else:
		query_list = [{'name': 'output_0.csv',
					   'query': query}]			
	for query in query_list:
		results = get_results(query['query'])
		write_results(results, query['name'])
		print_rows(results, 5)

def print_rows(results, n):
	""" Prints the first n rows of the query. 
	"""
	print(', '.join(results['header']))
	i = 0
	for row in results['rows']:
		print(', '.join(row))
		i += 1
		if i > n: 
			print('...')
			return
	
def set_db(db):
	global DB
	if not os.path.exists(db): sys.exit('DB cannot be found')
	DB = db
	
if __name__ == "__main__":
	if sys.argv[1] == '-t':
		import doctest
		doctest.testmod()
		sys.exit()
	set_db(sys.argv[1])
	query = sys.argv[2]
	run_query(query)
	# print_rows(results, 10)