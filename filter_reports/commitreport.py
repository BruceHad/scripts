import os, sys, stat
import glob
from shutil import copyfile

def get_location(filename):
	""" Gets the location id (string) from the filename
	>>> get_location('Q_NHS_gen201635319_41129')
	'5319'
	>>> get_location('Q_NHS_ort20163166_37881')
	'166'
	"""
	location = filename.split('_')[2][8:]
	return location

if __name__ == "__main__":
	if sys.argv[1] == '-t':
		import doctest
		doctest.testmod()
		sys.exit(0)

	locations_path = sys.argv[1]
	reports_path = sys.argv[2]
		
	# Read in locations file
	with open(locations_path) as f:
		locations = f.read().splitlines()
	
	# Create new directory
	output_path = os.path.join(reports_path, 'paper_reports')
	print(output_path)
	if( not os.path.exists(output_path)):
		os.mkdir(output_path)
		os.chmod(output_path, 0o666)
		print(output_path, " created")
		
	# Check for files and move any paper location to new directory
	for f_path in glob.glob( os.path.join(reports_path, '*') ):
		print("Checking {0}".format(f_path))
		if(os.path.isdir(f_path)):
			# Ignore directory
			print("{0} is a directory. Skipping.".format(f_path))
			continue		
		f_name = os.path.split(f_path)[1]
		loc = get_location(f_name)
		if(loc in locations):
			copyfile(f_path, os.path.join(output_path, f_name))
			print("Match found for location {0} and {1} copied to {2}".format(loc, f_name, output_path))
		else:
			print("No match found for location {0}".format(loc))