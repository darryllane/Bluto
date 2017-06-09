
from bluto_logging import info
import subprocess
import re
from termcolor import colored
import sys

def updateCheck():
	command_check = (["pip list -o"])
	process_check = subprocess.Popen(command_check, shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
	output_check = process_check.communicate()[0]
	line = output_check.splitlines()
	for i in line:
		if 'bluto' in str(i).lower():
			match = re.match('Bluto\s\(.*\)\s\-\sLatest\:\s(.*?)\s\[sdist\]', i)
			found = True
			return (found, match.group(1))
		else:
			found = False

	return (found, 'NONE')


def update():
	command_check = (["pip install bluto --upgrade"])
	process_check = subprocess.Popen(command_check, shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
	output_check = process_check.communicate()[0]
	lines = output_check.splitlines()
	info(lines)
	print lines[:-1]
	if 'Successfully installed' in lines[:-1]:
		print colored('\nUpdate Successfull!', 'green')
		sys.exit()
	else:
		print colored('\nUpdate Failed, Please Check The Logs For Details', 'red')

