import sys, os

positions = [1,3,10,13,28,36,54,65,68,71,79,87,91,98,105,112,119,126,133,140,146,154,161,163,165]	
headings = ['NSR3.CARD.TYPE','NSR3.SUP.NUM','NSR3.EMP.NUM','NSR3.PAY.REF','NSR3.DOB','NSR3.SURNAME',
	'NSR3.FORENAME','NSR3.INITIALS','NSR2.WT.DAYS','NSR3.PEN.PAY','NSR3.EMPR.REM','NSR3.CONTS.RATE',
	'NSR3.EMPE.CONTS','NSR3.EMPR.CONTS','NSR3.AY.CONTS.PRE83','NSR3.ULS.CONTS.PRE83','NSR3.AY.CONTS.POST83',
	'NSR3.ULS.CONTS.POST83','NSR3.SAL.RATE','NSR3.NI.EARNINGS','NSR3.START.DATE','NSR3.DOM.FEES',
	'NSR3.GRP.CODE','NSR3.SERV.TYPE','NSR3.CONTS.ARREARS']	

def get_files(path):
	path = os.path.abspath(path)
	files = os.listdir(path)
	file_paths = []
	for file in files:
		file_paths.append(os.path.join(path, file))
	return file_paths
	
def format_line(line):
	data = []
	for i in range(len(positions)):
		if i == len(positions)-1:
			data.append(line[positions[i]-1:])
		else:
			data.append(line[positions[i]-1:positions[i+1]-1])
	return ','.join(map(str, data))

def convert_file(file):
	result = ''
	count = 0
	f = open(file, 'r')
	lines = f.readlines()
	length = len(lines)
	for line in lines:
		if len(line.strip()) > 50:
			result += format_line(line)
			count += 1
	print("File length: %s \t Lines Printed: %s"%(length, count))
	return result
	
def concat_files(files, filename):
	count = 0
	header = ','.join(headings)
	full_file = open(filename, "w")
	full_file.write(header +'\n')
	for f in files:
		full_file.write(convert_file(f))
		count += 1
	full_file.close()
	return count

if __name__ == '__main__':
	path = sys.argv[1]
	filename = sys.argv[2]
	files = get_files(sys.argv[1])
	count = concat_files(files, filename)
	print('%s files concatenated'%count)