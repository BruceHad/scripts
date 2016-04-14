ExcelComp requires Java1.6 or higher.

	$ java -version
	java version "1.6.0_03"
	
Usage:

	excel_cmp file_1 file_2
	
## Setup

Download [ExcelComp](https://github.com/na-ka-na/ExcelCompare) and extract to an appropriate folder.

You can set the bin/ folder is in the Windows PATH variable and run the excel_cmp command or just run the file directly.

	set PATH=%PATH%;C:\path\to\bin

Or

	/path/to/bin/excel_cmp file_1 file_2
	
But we are going to be running it via a script which assumes the later, and that the bin folder is in a folder called excelcompare\bin\.

Script also assumes that the reports to be compared will have the same names and will be in different folders. e.g.

	before/
		report_1
		report_2
		report_3
	after/
		report_1
		report_2
		report_3

Then you can just supply path/to/before and path/to/after/ and the script will find the reports and run the comparisons.

Now you can run the script



