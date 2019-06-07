"""

Class to discover and report staff members of a target organisation from LinkedIn

"""
import platform
import re
import time
import os
import socket
import traceback
import sys
import json

import multiprocessing as mp

from ..logger_ import error, info, INFO_LOG_FILE, ERROR_LOG_FILE
from tqdm import tqdm
from pyvirtualdisplay import Display
from termcolor import colored
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

global SEEN

SEEN = []


class NoMoreData(Exception):

	"""
	Error thrown when no more data is found.
	"""

	def __init__(self, *args, **kwargs):
		Exception.__init__(self, *args, **kwargs)

class NotLoggedIn(Exception):
	"""
		Error thrown if not logged in.
	"""

	def __init__(self, *args, **kwargs):
		Exception.__init__(self, *args, **kwargs)
		
		
class NotInternetAccess(Exception):
	"""
		Error thrown if network error.
	"""

	def __init__(self, *args, **kwargs):
		Exception.__init__(self, *args, **kwargs)

class BreakOut(Exception):

	"""
		Called to carry out breakout.
	"""

	pass


class FindPeople(object):

	"""
	Class to discover and report staff members of a target organisation from LinkedIn
	"""

	def __init__(self, args, page_limits, company_details, company, company_number):
		try:
			output = mp.Queue()
			self.output = output
			self.operating_system = platform.system()	
			username, password = args.la.split(args.deli)
			domain = args.domain
			cpage, page = page_limits.split(':')
			
			self.args = args
			self.username = username
			self.password = password
			self.domain = domain
			self.company_page = int(cpage)

			self.company_details = company_details
			self.company_name = company
			self.staff_page = int(page)
			self.company_number = company_number
			dirname = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../../doc/driver/'))
			opt = Options()
			
			if args.proxy:
				opt.add_argument('--proxy-server=https://{}'.format(args.proxy))
				opt.add_argument('--proxy-server=http://{}'.format(args.proxy))
				info('proxy enabled: {}'.format(args.proxy))
			
			opt.add_argument("--disable-notifications")
			opt.add_argument('--no-sandbox')
			
			if self.operating_system == 'Linux':
				if args.verbose:
					info('verbose: on')				
					display = Display(visible=1, size=(1280, 720))
				else:
					opt.add_argument('headless')
					info('headless: on')
					display = Display(visible=0, size=(1280, 720))
					info('verbose: off')
				exec_path = dirname + '/chromedriverLINUX'
				display.start()
			elif self.operating_system == 'Darwin':
				if args.verbose:
					if args.debug:
						opt.add_argument('--remote-debugging-port=9222')
						info('debug enabled: http://localhost:9222')
					info('verbose: on')	
				else:
					#opt.add_argument('headless')
					info('headless: not currently working in OSX')
					if args.debug:
						opt.add_argument('--remote-debugging-port=9222')
						info('debug enabled: http://localhost:9222')
					info('verbose: off')
				exec_path = dirname + '/chromedriverMAC'
			
		
			browser = webdriver.Chrome(options=opt, executable_path=exec_path)
			
			self.browser = browser
			time.sleep(1)
			self.browser.get('https://www.linkedin.com/uas/login')
			time.sleep(3)
			
			if 'No Internet' in browser.page_source:
				error('internet down!')
				raise NotInternetAccess('Error: No internet access')
			
			username1 = browser.find_element_by_name("session_key")
			password1 = browser.find_element_by_name("session_password")
			username1.send_keys(self.username)
			password1.send_keys(str(self.password))
			time.sleep(0.5)
			
			
			if browser.find_element_by_class_name("btn__primary--large"):
				browser.find_element_by_class_name("btn__primary--large").click()
				
			elif browser.find_element_by_id("btn-primary"):
				browser.find_element_by_id("btn-primary").click()
			
			else:
				error('no button')
				raise NotLoggedIn('Error: No login button found')
	
			time.sleep(1)
			
			
			if 'alert error' in self.browser.page_source or 'that\'s not the right password' in self.browser.page_source:
				raise NotLoggedIn('You have had an error logging in')

			session_id = self.browser.session_id
			self.session_id = session_id
		
		except NotInternetAccess:
			info('not internet access')
			error('not internet access')
			print(colored('You dont seem to have any network connectivity!', 'red'))
			os._exit(1)
		except NotLoggedIn as e:
			info('failed to login')
			error('failed to login')
			answer = ['yes', 'y', 'no', 'n']
			while True:
				if 'No login button found' in e:
					print('Error: No login found')
					sys.exit()
				response = input('\nLinkedIn Password is incorrect.\nWould you like to quit and re-enter the credentials?\n\n').lower()
				if response in answer:
					if response in ['y', 'yes']:
						info('User quitting..')
						print('\nUser quitting..')
						os._exit(0)
					else:
						info('User continuing..')
						print('\ncontinuing..')
						break
				else:
					print('You need to enter 1 of the following: (y | yes | n | no)\nNot \'{}\''.format(response))
			return
	
		except Exception:
			print('An Unhandled Exception Has Occured, Please Check The \'Error log\' For Details')
			info('An Unhandled Exception Has Occured, Please Check The \'Error log\' For Details')
			error(traceback.print_exc())
			return


	def not_exact(self):

		"""
		If no direct match is found in an automated fashion a manual check is presented.
		"""
		info('an exact match was not found')
		print(colored('An Exact Match was not found\n', 'red'))
		while True:
			input('A list of companies and their details will be displayed\n' + \
			      colored('\nPlease press enter to continue\n', 'yellow'))
			for item in self.company_details:
				print(item[0])
				print(item[1])
				print(item[2])
				company_number = colored(item[3], 'green')
				print('{}'.format(company_number) + '\n')

			company_number = input('Please enter the company number of the bussiness you wish to search\nCompany No: ')
			while True:
				tmp = colored('{}\n', 'green').format(company_number)
				confirmed = input('Confirm ' + tmp + colored('(y|n)', 'yellow') + ': ')
				if confirmed.lower() in ('y', 'yes', ''):
					try:
						for item in self.company_details:
							if item[3] == company_number:
								company = item[0]
								company = colored(company, 'green')
								print('\nSearching LinkedIn for {} staff members\n'.format(company))
								self.company_number = company_number
								return
						raise NoMoreData('CompanyNotFound')
					except NoMoreData:
						print('Company Not Found! Report This Please')
						info('no company found')
						return


	def supply_company(self):

		"""
		Supply comany name manually
		"""

		i = 0
		while True:
			if i > 0:
				os.system('clear')
			temp_company = input('Please Supply The Company Name\n\nThis Will Be Used To Query LinkedIn: ')
			confirmed = input(colored('\nConfirm search for: "{}"? '.format(temp_company), 'yellow'))
			if confirmed.lower() in ('y', 'yes'):
				company = temp_company
				print('\nSearching LinkedIn companies for {}\n'.format(company.title()))
				self.company_name = company
				return company
			elif confirmed.lower() in ('n', 'no'):
				continue
			else:
				self.negative(confirmed)
				i += 1


	def negative(self, confirmed):

		"""
		Called when a confirmation containing anything other than y or n is supplied
		"""

		print(colored('\nThe Options Are yes|no Or y|no\nNot: '), colored('{}', 'red').format(confirmed))
		for j in range(10, 1, -1):
			time.sleep(0.5)
			j = str(j)+" \r"
			color = colored(j, 'yellow')
			sys.stdout.write(color)
			sys.stdout.flush()
			sys.stdout.flush()



	def company(self):

		"""
		Company identification function
		"""

		self.company_name = self.supply_company()
			

		company_details = []

		try:
			for page in range(1, self.company_page):
				self.browser.get('https://www.linkedin.com/search/results/companies/?keywords={c}&origin=\
				SWITCH_SEARCH_VERTICAL&page={p}'.format(c=self.company_name, p=page))

				time.sleep(3)
				html = self.browser.page_source
				soup = BeautifulSoup(html, "lxml")
				
				
				try:
					if 'No results found' in self.browser.page_source:
						raise NoMoreData("No more results found")
				except NoMoreData as e_rror:
					self.company_details = company_details
					company_number = self.not_exact()
					self.company_found = True
					return

				data = soup.find('div', {'class': 'search-results ember-view'})
				
				if 'Make the most of your professional life' in html:
					raise NotLoggedIn('login failure!')
				
				li_list = data.findAll('li', {'class': 'search-result search-result__occluded-item ember-view'})

				for each in li_list:
					try:
						company_item = each.find('div', {'class': 'search-result__info'})
						if company_item.find('h3', {'class':'search-result__title'}):
							company_name = company_item.find('h3', {'class':'search-result__title'}).text.replace('.', '').replace('\n', '').strip()
							#print company_name
						if company_item.find('p', {'class':'subline-level-1'}):
							company_type = company_item.find('p', {'class':'subline-level-1'}).text.replace('.', '').replace('\n', '').strip()
							#print company_type
						else:
							company_type = None
						if company_item.find('p', {'class':'subline-level-2'}):
							company_people = company_item.find('p', {'class':'subline-level-2'}).text.replace('.', '').replace('\n', '').strip()
							#print company_people
						else:
							company_people = None
						if company_item.find('a', {'data-control-name': 'search_srp_result'}):
							data = company_item.find('a', href=True)
							company_number = data['href'].replace('/company/', '').replace('/', '')
						#print '\n'

						company_details.append((company_name, company_type, company_people, company_number))
						if self.company_name.lower() in company_name.lower():
							print('Is This the correct company?')
							tmp = colored('{}\n', 'green').format(company_name)
							if company_people == None:
								company_people = ''
							confirmed = input('\n{}'.format(tmp) + '{}\n{}'.format(company_type, company_people) + '\n' + colored('(y|n)','yellow') )
							if confirmed.lower() in ('y', 'yes'):
								tmp = colored(company_name, 'green')
								print('\nTarget Company Identified:\n')
								print('\t' + str(company_name))
								print('\t' + str(company_type))
								print('\t' + str(company_people))
								print('Searching LinkedIn for ' + tmp + ' staff members\n')
								self.company_number = company_number
								self.company_found = True
								return
							elif confirmed.lower() in ('n', 'no'):
								continue
							else:
								self.negative(confirmed)
					except AttributeError:
						print(traceback.print_exc())
					except Exception as e_rror:
						info('An unhandled exception has occured, please check the \'Error log\' for details')
						error('An Unhandled Exception Has Occured, Please Check The Log For Details' + ERROR_LOG_FILE, exc_info=True)

			self.company_details = company_details
			company_number = self.not_exact()
			self.company_found = True
			return

		except Exception:
			info('An unhandled exception has occured, please check the \'Error log\' for details')
			error('An Unhandled Exception Has Occured, Please Check The Log For Details' + ERROR_LOG_FILE, exc_info=True)


	def result_pages(self):
		numbers = []
		try:
			self.browser.get('https://www.linkedin.com/search/results/people/?facetCurrentCompany={}&page={}'.format(self.company_number, '1'))
			
			last_height = self.browser.execute_script("return document.body.scrollHeight")
			
			while True:
				# Scroll down to bottom
				self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			
				# Wait to load page
				time.sleep(1)
			
				# Calculate new scroll height and compare with last scroll height
				new_height = self.browser.execute_script("return document.body.scrollHeight")
				if new_height == last_height:
					break
				last_height = new_height			
			
			html = self.browser.page_source
			soup = BeautifulSoup(html, "lxml")
			result_page = soup.find('ul', {'class': 'artdeco-pagination__pages artdeco-pagination__pages--number'})
			li_list = result_page.findAll('li', {'class': 'artdeco-pagination__indicator artdeco-pagination__indicator--number'})
			for li in li_list:
				if '.' in li.span.text:
					pass
				elif '\u2026' in li.span.text:
					pass
				else:
					numbers.append(int(li.span.text))
		except AttributeError:
			if 'upgrade to Premium to continue searching' in html:
				info('your linkedin account has reached its search limit')
				return 'limit reach'
		except Exception:
			info('An unhandled exception has occured, please check the \'Error log\' for details')
			error('An Unhandled Exception Has Occured, Please Check The Log For Details' + ERROR_LOG_FILE, exc_info=True)
			return 20
		
		if self.args.debug:
			info('debug data return: 10')
			return (10)
		else:
			if numbers:
				return max(numbers)
			else:
				return 'none'
		
	def people(self):

		"""
		Gather Staff Members
		"""

		global SEEN

		i = 0
		people_details = []
		if self.staff_page == 20:
			data = self.result_pages()
			if isinstance(data, int):
				self.staff_page = data
			else:
				print(colored('\nUser account reached search limit!', 'red'))
				error('User account reached search limit!')
				info('User account reached search limit!')
				self.output.put(people_details)
				self.browser.close()				
				return
			
		for page in tqdm(range(1, self.staff_page)):
			self.browser.get('https://www.linkedin.com/search/results/people/?facetCurrentCompany={}&page={}'.format(self.company_number, page))

			time.sleep(2)
			html = self.browser.page_source
			
			if 'upgrade to Premium to continue searching' in html:
				print(colored('User account reached search limit!', 'red'))
				error('User account reached search limit!')
				info('User account reached search limit!')
				self.output.put(people_details)
				self.browser.close()				
				return		
			
			try:
				if 'No results found' in self.browser.page_source:
					raise NoMoreData("No more results found")
			except NoMoreData as e_rror:
				print('No further results possible\n')
				self.output.put(people_details)
				print('{} staff members found\n'.format(len(SEEN)))
				return
			soup = BeautifulSoup(html, "lxml")

			data = soup.find('ul', {'class': 'search-results__list'})
			#print data.contents
			if data:
				
				li_list = data.findAll('li', {'class': 'search-result search-result__occluded-item ember-view'})

				for li_item in li_list:
					try:
						if li_item.find('img', {'class', 'lazy-image ghost-person loaded'}):
							pass
						else:

							if li_item.find('span', {'class', 'name actor-name'}):
								
								name = li_item.find('span', {'class', 'name actor-name'}).text.replace('\n', '').rstrip()
								img_url_tmp = li_item.find('div', {'class', 'presence-entity presence-entity--size-4 ember-view'})
								
								if re.match('.*src\=\"(.*?)\".*', str(img_url_tmp)):
									img_url = re.match('.*src\=\"(.*?)\".*', str(img_url_tmp)).group(1)
								else:
									img_url = 'None'
								#print name
								if name.lower() == 'LinkedIn Member'.lower():
									i += 1
								if li_item.find('p', {'class', 'subline-level-1'}):
									job = li_item.find('p', {'class', 'subline-level-1'}).text.replace('\n', '').rstrip()
									#print job
								if li_item.find('p', {'class', 'subline-level-2'}):
									location = li_item.find('p', {'class', 'subline-level-2'}).text.replace('\n', '').rstrip()
									#print location

								if name in SEEN:
									pass
								else:
									SEEN.append(name)
									people_details.append(("name:" + name.strip(),
										                      "role:" + job.strip(),
										                      "location:" + location.strip(),
										                      "image:" + img_url))


								if li_item.find('div', {'class', 'search-result__profile-blur'}):
									print(colored('\nYou\'ve Reached The Limit Imposed by LinkedIn', 'yellow'))
									print('\nReturning Any Results Found\n')
									self.output.put(people_details)
									print('{} staff members found'.format(len(SEEN)))
									return

					except KeyError as e_rror:
						if 'src' in e_rror.args:
							pass
						else:
							info('An unhandled exception has occured, please check the \'Error log\' for details')
							error('An Unhandled Exception Has Occured, Please Check The Log For Details' + ERROR_LOG_FILE, exc_info=True)							
					except UnboundLocalError as e_rror:
						if 'name' in e_rror:
							name = None
						if 'job' in e_rror:
							job = None
						if 'location' in e_rror:
							location = None
						continue
					except TypeError:
						continue
					except Exception:
						info('An unhandled exception has occured, please check the \'Error log\' for details')
						error('An Unhandled Exception Has Occured, Please Check The Log For Details' + ERROR_LOG_FILE, exc_info=True)
					try:
						if i > 3:
							raise NoMoreData("No more results found")
						if 'No results found' in self.browser.page_source:
							raise NoMoreData("No more results found")
						if 'you’ve reached the commercial use limit' in self.browser.page_source:
							raise NoMoreData("you’ve reached the commercial use limit")
					except NoMoreData as e_rror:
						if 'you’ve reached the commercial use limit' in e_rror.args:
							print(colored('\n\nYou’ve reached the commercial use limit on this linkedIn account!', 'red'))
						self.output.put(people_details)
						return
			else:
				time.sleep(2)
				continue
			
		print('{} staff members found\n'.format(len(SEEN)))
		self.output.put(people_details)
		self.browser.close()
