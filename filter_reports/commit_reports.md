Filter  Reports
===============

2017-06-07

Script to separate report files based on the location id contained in the filename.

Each report is a separate file and the location number is part of the filename, making it relatively easy to identify the reports location.

The script checks report files against a list of locations (produce by sql query). If a match is found, the report should be copied to a new directory.

Run the script. 

<pre>python commitreport.py locations.csv commitment/reports</pre>

Requires two parameters:
	
1. Locations Path - the path to the .csv file listing the locations.
2. Reports Path - the path to the directory containing all the report files.

The script should run and all the paper report files that should be printed will be copied to a new director called paper_reports