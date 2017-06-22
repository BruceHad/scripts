import sqlite3
import sys, os

DB = 'test.db' # default db

def run_query(query):
	""" Runs a query against the DB. 
		Query can be either a file path or a string.
		Results is a Dict containing two items, headers and rows.
	"""	
	# Read the query from file or set as string.
	if os.path.exists(query):
		with open(query) as q:
			query_string = q.read()
	else:
		query_string = query

	con = sqlite3.connect(DB)
	cur = con.cursor()
	query = cur.execute(query_string);
	results = {}
	results['header'] = [i[0] for i in query.description]
	results['rows'] = []
	for row in query:
		results['rows'].append([i for i in row])
	con.close()
	
	return results

def write_results(results, output_file):
	""" Write the results of the query to a file
	"""
	with open(output_file, 'w') as f:
		f.write(', '.join(results['header']))
		f.write('\n')
		for row in results['rows']:
			f.write(', '.join(row))
			f.write('\n')

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
	set_db(sys.argv[1])
	query = sys.argv[2]
	results = run_query(query)
	write_results(results, 'output_file.csv')
	print_rows(results, 10)