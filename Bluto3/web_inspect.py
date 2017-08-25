from pyvirtualdisplay import Display
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from bs4 import BeautifulSoup
import os
import pwd
import datetime
import time


def worker(browser):
	url = 'www.google.co.uk'
	today = datetime.datetime.today().strftime('%d-%b-%Y')
	dir_path = os.path.dirname(os.path.realpath(__file__))
	protos = ['https://', 'http://']
	for protocol in protos:
		browser.get(protocol + url)
		screenshot_filename = str(protocol).split(':')[0] + url + '-' + today + '.png'
		screenshot_filename = screenshot_filename.replace("['", "").replace("']", "")
		browser.get_screenshot_as_file(dir_path + '/' + screenshot_filename)
		time.sleep(3)
		print 'done'
	browser.close()

if os.getuid() == 0:
	try:
		print 'Running as root\nAttempting to change User: '
		cron_user = pwd.getpwnam()
		cron_user_gid = pwd.getpwnam()
		os.seteuid(cron_user_id)
	except Exception, e:
		print e
else:
	print os.getuid()


display = Display(visible=0, size=(1024, 768))
display.start()
browser = webdriver.Chrome()

worker(browser)

browser.stop_client()
display.stop()
