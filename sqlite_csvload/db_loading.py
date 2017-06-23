import sys, os
import sqlite3
import glob

def is_file_type(file, ext):
	""" Checks if file has a given extension 
	>>> is_file_type('one.csv', 'csv')
	True
	>>> is_file_type('path\\to\\one.csv', 'csv')
	True
	>>> is_file_type('one.doc', 'doc')
	True
	>>> is_file_type('one', 'csv')
	False
	"""
	split_file = file.split('.')
	if len(split_file) != 2:
		return False
	return split_file[1] == ext

def get_files_of_type(files, ext):
	""" Returns a list of files with a given extension
	>>> files = ['one.csv', 'dir\\two.csv', 'folder', 'test.txt', 'three.csv']
	>>> get_files_of_type(files, 'csv')
	['one.csv', 'dir\\two.csv', 'three.csv']
	"""
	return [f for f in files if is_file_type(f, ext)]

def get_file_name(path):
	""" Get a file name from a path 
	>>> get_file_name('one.csv')
	'one'
	>>> get_file_name(os.path.join('dir', 'file.txt'))
	'file'
	"""
	head, tail = os.path.split(path)
	return tail.split('.')[0]
	
def sqlify_row(row):
	""" Clean up and convert a row of data from the csv file 
		for inserting into sql string. 
		To do: don't treat all values as strings???
		
	>>> sqlify_row('"ID","SURNAME","FORENAME","DATE_OF_BIRTH","EMAIL_ADDRESS"')
	'"ID", "SURNAME", "FORENAME", "DATE_OF_BIRTH", "EMAIL_ADDRESS"'
	>>> sqlify_row('96867,1988-12-09 00:00,1993-07-02,"TEST"\\n')
	'"96867", "1988-12-09 00:00", "1993-07-02", "TEST"'
	>>> sqlify_row('"id","surname","EMAIL\\n"')
	'"id", "surname", "EMAIL"'
	"""
	chars = ['\n','\'','"'] # characters to strip out
	values = row.split(',')
	for c in chars:
		values = [i.replace(c, '') for i in values]
	values = ['"{}"'.format(i) for i in values] # re-wrap it in quotes
	return ', '.join(values)

def load_csv(cur, f_path):
	""" Load csv from f_path to db table """
	table_name = get_file_name(f_path)
	with open(f_path) as f:
		cols_string = sqlify_row(f.readline())
		cur.execute("CREATE TABLE {0} ({1});".format(table_name, cols_string))
		for row in f:
			row_string = sqlify_row(row)
			cur.execute("INSERT INTO {0} ({1}) VALUES ({2});".format(table_name, cols_string, row_string))

def create_db(db_name, source_dir):
	""" Creates a new db and loads all csv file from source_dir
		into it.
	"""
	if os.path.exists(db_name):	os.remove(db_name)
	file_list = glob.glob(os.path.join(source_dir, '*'))
	files = get_files_of_type(file_list, 'csv')
	con = sqlite3.connect(db_name)
	cur = con.cursor()
	for f in files:	
		load_csv(cur, f)
	con.commit()
	con.close()

def check_results(db):
	""" Summarise the results of the data load
	"""
	results = 'The following databases have been created:\n\n'
	con = sqlite3.connect(db_name)
	cur = con.cursor()
	query = cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
	tables = []
	for row in query:
		tables.append(row[0])
	for table in tables:
		row_count = cur.execute("SELECT count(*) FROM " + table)
		row_count = str(list(row_count)[0][0])
		results += ' * {0} ({1} rows)'.format(table, row_count)
		results += '\n'
	con.close()
	return results;

if __name__ == "__main__":
	if sys.argv[1] == '-t':
		import doctest
		doctest.testmod()
		sys.exit()	
	db_name = sys.argv[1]
	source_dir = sys.argv[2]
	create_db(db_name, source_dir)
	results = check_results(db_name)
	print(results)
