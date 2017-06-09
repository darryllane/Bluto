
from bluto_logging import info
import subprocess

def updateCheck():
	command_check = (["pip", "list", "-o", "--format=freeze"])
	process_check = subprocess.Popen(command_check, shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
	output_check = process_check.communicate()[0]
	line = output_check.splitlines()
	for i in line:
		if 'bluto' in str(i).lower():
			found = True
			return found
		else:
			found = False

	return found


def update():
	command_check = (["sudo -H pip install bluto --upgrade"])
	process_check = subprocess.Popen(command_check, shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
	output_check = process_check.communicate()[0]
	lines = output_check.splitlines()
	for line in lines:
		print line
