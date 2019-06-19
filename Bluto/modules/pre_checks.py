import os
import sys
import subprocess

def install_chrome():
	wget = "wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -O /tmp/google-chrome-stable_current_amd64.deb"
	install = 'dpkg -i /tmp/google-chrome-stable_current_amd64.deb'

	commands = [wget, install]
	for cmd in commands:
		if 'wget' in cmd:
			print('Attempting to download latest stable google-chrome')
		elif 'dpkg' in cmd:
			print('Attempting to install google-chrome')

		process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		output = process.communicate()

		for line in output:
			if 'wget' in cmd:
				if b'100%' in line:
					print('Downloaded Chrome')
			if 'dpkg' in cmd:
				if b'Processing triggers for man-db' in line:
					print('Installed Successfully')


def check_prerequisite():
	print('Checking pre-requisites')
	cmd="which google-chrome"
	process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	output = process.communicate()[0].replace(b'\n', b'')
	if b'google-chrome' in output:
		print('Chrome installed: {}'.format(output.decode()))
	else:
		print('Chrome not installed')
		install_chrome()

check_prerequisite()