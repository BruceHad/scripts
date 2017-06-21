import sys, os
import sqlite3
import glob

def strip_list(list):
	"""Strip quotes and non printable characters from items in a list
	>>> strip_list(['"one"', '"1"', '"2000-01-01 00:00"', '"2000-01-01"', '"true"', '"two"'])
	['one', '1', '2000-01-01 00:00', '2000-01-01', 'true', 'two']
	"""
	return [i.strip('"\n') for i in list]


def get_columns(file):
	""" Reads columns from a .csv file and determines the type """
	with open(file) as f:
		headings = f.readline().split(',')
		# first_row = strip_list(f.readline().split(','))
	return headings

def create_db(db_name, source_dir):
	""" Creates a new db """
	if os.path.exists(db_name):
		os.remove(db_name)
	con = sqlite3.connect(db_name)
	cur = con.cursor()
	for f_path in glob.glob( os.path.join(source_dir, '*') ):
		if f_path.split('.')[1] == 'csv':
			table_name = f_path.split('.')[0].split('\\')[-1]
			with open(f_path) as f:
				cols = [c.strip('\n') for c in f.readline().split(',')]
				cols_string = ', '.join(cols)
				cur.execute("CREATE TABLE {0} ({1});".format(table_name, cols_string))
				print("CREATE TABLE {0} ({1});".format(table_name, cols_string))
				for row in f:
					row = [i.strip('"\n') for i in row.split(',')]
					row = ['"{}"'.format(i) for i in row]
					row_string = ', '.join(row)
					# print("INSERT INTO {0} ({1}) VALUES ({2});".format(table_name, cols_string, row_string))
					cur.execute("INSERT INTO {0} ({1}) VALUES ({2});".format(table_name, cols_string, row_string))
	con.commit()
	con.close()
	
if __name__ == "__main__":
	db_name = sys.argv[1]
	source_dir = sys.argv[2]
	create_db(db_name, source_dir)
