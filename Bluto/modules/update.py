
from bluto_logging import info
import subprocess
import re
from termcolor import colored
import sys

def updateCheck(VERSION):
	command_check = (["pip list -o"])
	process_check = subprocess.Popen(command_check, shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
	output_check = process_check.communicate()[0]
	line = output_check.splitlines()
	for i in line:
		if 'bluto' in str(i).lower():
			new_version = re.match('Bluto\s\(.*\)\s\-\sLatest\:\s(.*?)\s\[sdist\]', i).group(1)
			found = True
		else:
			found = False

	if found:
		info('update availble')
		print(colored('\nUpdate Available!', 'red'), colored('{}'.format(new_version), 'green'))
		print(colored('Would you like to attempt to update?\n', 'green'))
		while True:
			answer = raw_input('Y|N: ').lower()
			if answer in ('y', 'yes'):
				update()
				print ('\n')
				break
			elif answer in ('n', 'no'):
				print ('\n')
				break
			else:
				print ('\nThe Options Are yes|no Or Y|N, Not {}'.format(answer))
	else:
		print (colored('You are running the latest version:','green'), colored('{}\n'.format(VERSION),'blue'))


def update():
	command_check = (["pip install bluto --upgrade"])
	process_check = subprocess.Popen(command_check, shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
	output_check = process_check.communicate()[0]
	lines = output_check.splitlines()
	info(lines)
	if 'Successfully installed' in lines[:-1]:
		print (colored('\nUpdate Successfull!', 'green'))
		sys.exit()
	else:
		print (colored('\nUpdate Failed, Please Check The Logs For Details', 'red'))
		info('Update Failed, Please Check The Logs For Details', Please Check The \'Error\' For Details')
		error(traceback.print_exc())		

