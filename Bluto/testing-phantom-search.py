import time
import datetime
import os
import argparse
import pwd
import shutil
import subprocess
import getpass
import sys
import traceback
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from bs4 import BeautifulSoup
from pyvirtualdisplay import Display




def worker(server_list, username, password, group, browser, display, today, data_dir, logg_server):

	for server in server_list:
		try:
			count_list = []
			filename = str(server.split('.')[:1]) + '-' + today + '.html'
			filename = filename.replace("['", "").replace("']", "")
			browser.get('https://' + server)


			username1 = browser.find_element_by_name("username")
			password1 = browser.find_element_by_name("password")
			select = Select(browser.find_element_by_id("labelDomain"))

			username1.send_keys(username)
			password1.send_keys(password)
			select.select_by_visible_text(group)

			submit_button = browser.find_element_by_id("btn-signin").click()
			info('Logged In')
			time.sleep(5)

			browser.switch_to_frame('menu')
			browser.switch_to_frame(browser.find_element_by_tag_name("iframe"))
			time.sleep(5)

			html = browser.page_source

			write_html(data_dir, today, filename, html)

			soup = BeautifulSoup(html, "lxml")

			data = soup.find('div', {'class': 'data_view'})

			tr_data = data.findAll('tr', {'class': 'item'})
			tr_data2 = data.findAll('tr', {'class': 'item even last_row'})

			for tr in tr_data:
				if tr.find('td', {'title': 'Smart Scan Agent Pattern'}):
					s_title = tr.find('td', {'title': 'Smart Scan Agent Pattern'})
					rate = tr.find('td', {'class': 'update_rate_column'})
					if tr.find('a', {'class': 'drill_down_link warning'}):
						count1 = tr.find('a', {'class': 'drill_down_link warning'})
						info((s_title.text, rate.text, count1.text))
						count_list.append((count1.text, 'Smart Scan Agent Pattern'))

						if int(str(rate.text).replace('%', '')) <= 101:
							for count in count_list:
								browser.find_element_by_link_text(count[0].replace("u'","")).click()
								time.sleep(5)
								message_send = avcheck_syslog.syslog_av_check((str(server.split('.')[:1]) + ' smart scan agent pattern ' + str(rate.text).replace("u", "") + ' ' + str(count1.text).replace("u", "")) , logg_server)
								message_send.message((str(server.split('.')[:1]) + ' smart scan agent pattern ' + str(rate.text).replace("u", "") + ' ' + str(count1.text).replace("u", "")), logg_server)
								screenshot_filename = str(server.split('.')[:1]) + '-' +count[1] + '-' + today + '.png'
								screenshot_filename = screenshot_filename.replace("['", "").replace("']", "")
								browser.save_screenshot(data_dir + today + '/' + screenshot_filename)
								browser.back()
								time.sleep(5)
								count_list = []
								browser.switch_to_frame('menu')
								browser.switch_to_frame(browser.find_element_by_tag_name("iframe"))
								time.sleep(5)

			soup = BeautifulSoup(html, "lxml")

			data = soup.find('div', {'class': 'data_view'})

			tr_data = data.findAll('tr', {'class': 'item'})
			tr_data2 = data.findAll('tr', {'class': 'item even last_row'})

			for tr in tr_data:
				if tr.find('td', {'title': 'OfficeScan Agent (32-bit)'}):
					v_title = tr.find('td', {'title': 'OfficeScan Agent (32-bit)'})
					rate2 = tr.find('td', {'class': 'update_rate_column'})
					if tr.find('a', {'class': 'drill_down_link warning'}):
						count2 = tr.find('a', {'class': 'drill_down_link warning'})
						info((v_title.text, rate2.text, count2.text))
						count_list.append((count2.text, 'OfficeScan Agent (32-bit)'))

						if int(str(rate2.text).replace('%', '')) <= 101:
							for count in count_list:
								message_send = avcheck_syslog.syslog_av_check((str(server.split('.')[:1]) + ' officeScan agent (32-bit) ' + str(rate2.text).replace("u", "") + ' ' + str(count2.text).replace("u", "")), logg_server)
								message_send.message((str(server.split('.')[:1]) + ' officeScan agent (32-bit) ' + str(rate2.text).replace("u", "") + ' ' + str(count2.text).replace("u", "")), logg_server)
								browser.find_element_by_link_text(count[0].replace("u'","")).click()
								time.sleep(5)
								screenshot_filename = str(server.split('.')[:1]) + '-' +count[1] + '-' + today + '.png'
								screenshot_filename = screenshot_filename.replace("['", "").replace("']", "")
								browser.save_screenshot(data_dir + today + '/' + screenshot_filename)
								browser.back()
								time.sleep(5)
								count_list = []
								browser.switch_to_frame('menu')
								browser.switch_to_frame(browser.find_element_by_tag_name("iframe"))
								time.sleep(5)

			soup = BeautifulSoup(html, "lxml")

			data = soup.find('div', {'class': 'data_view'})

			tr_data = data.findAll('tr', {'class': 'item'})
			tr_data2 = data.findAll('tr', {'class': 'item even last_row'})

			for tr2 in tr_data:
				if tr2.find('td', {'title': 'OfficeScan Agent (64-bit)'}):
					v_title2 = tr2.find('td', {'title': 'OfficeScan Agent (64-bit)'})
					rate3 = tr.find('td', {'class': 'update_rate_column'})
					info((v_title2.text, rate3.text))
					if tr.find('a', {'class': 'drill_down_link warning'}):
						count3 = tr.find('a', {'class': 'drill_down_link warning'})
						info((count3.text))
						count_list.append((count3.text, 'OfficeScan Agent (64-bit)'))

						if int(str(rate3.text).replace('%', '')) <= 95:
							for count in count_list:
								message_send = avcheck_syslog.syslog_av_check((str(server.split('.')[:1]) + ' officescan agent (64-bit) ' + str(rate3.text).replace("u", "") + ' ' + str(count3.text).replace("u", "")), logg_server)
								message_send.message((str(server.split('.')[:1]) + ' officescan agent (64-bit) ' + str(rate3.text).replace("u", "") + ' ' + str(count3.text).replace("u", "")),logg_server)
								browser.find_element_by_link_text(count[0].replace("u'","")).click()
								time.sleep(5)
								screenshot_filename = str(server.split('.')[:1]) + '-' +count[1] + '-' + today + '.png'
								screenshot_filename = screenshot_filename.replace("['", "").replace("']", "")
								browser.save_screenshot(data_dir + today + '/' + screenshot_filename)
								browser.back()
								time.sleep(5)
								count_list = []

			info('Data Grabbing Completed For: ' + server)
		except Exception,e:
			info(e)
			continue


display = Display(visible=0, size=(1024, 768))
display.start()
browser = webdriver.Chrome()

worker(server_list, browser, display)

browser.stop_client()
display.stop()
