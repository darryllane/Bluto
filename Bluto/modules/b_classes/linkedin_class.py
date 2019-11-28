"""

Class to discover and report staff members of a target organisation from LinkedIn

"""
import platform
import re
import random
import time
import os
import socket
import traceback
import sys
import json
import requests
import multiprocessing as mp
from fake_useragent import UserAgent
from ..logger_ import error, info, INFO_LOG_FILE, ERROR_LOG_FILE
from ..email_ import Search
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

	def __init__(self, args, page_limits, company_details, company, company_number, type_=''):
		try:
			self.args = args
			obj = Search(self.args)
			self.pattern = obj.pattern			
			
			if type_ == 'linkedIna':
				
				output = mp.Queue()
				self.output = output
				self.operating_system = platform.system()	
				username, password = args.la.split(args.deli)
				domain = args.domain
				cpage, page = page_limits.split(':')
				
				
				ua_dirname = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../../doc/'))
				self.ua_filename = ua_dirname + 'user_agents.txt'				
				
				self.username = username
				self.password = password
				self.domain = domain
				self.company_page = int(cpage)
	
				self.company_details = company_details
				self.company_name = company
				self.staff_page = int(page)
				self.company_number = company_number
				dirname = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../../doc/driver/'))
				dirname_chrome = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../../doc/browser/'))
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
						display = Display(visible=1, size=(1280, 1280))
					else:
						opt.add_argument('headless')
						info('headless: on')
						display = Display(visible=0, size=(1280, 1280))
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
				
					
				ua = UserAgent()
				userAgent = ua.ff
				opt.add_argument(f'user-agent={userAgent}')
				
				browser = webdriver.Chrome(options=opt, executable_path=exec_path)
				
				self.browser = browser
				time.sleep(1)
				self.browser.get('https://www.linkedin.com/uas/login')
				time.sleep(2)
				
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
			
			elif type_ == 'linkedInp':
				output = mp.Queue()
				
				
				self.output = output
				self.operating_system = platform.system()	
				domain = args.domain
				self.domain = domain
				self.company_details = company_details
				self.company_name = company
				
					
				
		
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
			if self.args.debug:
				print(traceback.print_exc())
			info('An unhandled exception has occured, please check the \'Error log\' for details')
			error('An Unhandled Exception Has Occured, Please Check The Log For Details' + ERROR_LOG_FILE, exc_info=True)			
			return
		
	
	def get_file(self):
		filename = self.ua_filename
		if not os.path.exists(filename):
			print('The file does not exist: {}'.format(filename))
			sys.exit()
		else:
			data = [line.rstrip('\n') for line in open(filename)]
			self.user_agents = data
	
	
	def get_person(self, person_url):
		ua = random.choice(self.user_agents)
		link = person_url
		
		headers = {"User-Agent": ua,
				   "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
				   "Accept-Language": "en-GB,en;q=0.5",
				   "Accept-Encoding": "gzip, deflate",
				   "Referer": "https://www.bing.com/"}
		
		if self.args.proxy:
			proxy = {'https' : 'https://{}'.format(args.proxy)}
		else:
			pass
		
		try:		
			with requests.Session() as sesh:
				self.sesh = sesh			
				if self.args.proxy:
					response = sesh.get(link, headers=headers, verify=False, proxies=proxy, timeout=60)
				else:
					response = sesh.get(link, headers=headers, verify=False, timeout=60)
				response.text.encode('utf-8')
				soup = BeautifulSoup(response.text, "lxml")
				
				if soup.find('span', {'class': 'top-card__subline-item'}):
					location = soup.find('span', {'class': 'top-card__subline-item'}).text
				else:
					location = None
				if soup.find('img', {'class': 'entity-image'}):
					img_url = soup.find('img', {'class': 'entity-image'})['data-delayed-url']
				else:
					img_url = None
				
				return img_url, location
		except Exception:
			if self.args.debug:
				print(traceback.print_exc())
			info('An unhandled exception has occured, please check the \'Error log\' for details')
			error('An Unhandled Exception Has Occured, Please Check The Log For Details' + ERROR_LOG_FILE, exc_info=True)		
	
	
		
	def linkedin_pa(self):
		ua_dirname = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../../doc/'))
		self.ua_filename = ua_dirname + '/user_agents.txt'
		self.get_file()
		
		self.company_name = self.supply_company()
		people_details = []
		confirmed_email = []		
		searchfor = 'site:linkedin.com/in ' + '"' + self.company_name + '"'
		
		for start in range(1,50,1):
			ua = random.choice(self.user_agents)
			pwn_data = []
			if self.args.proxy:
				proxy = {'https' : 'https://{}'.format(args.proxy)}
			else:
				pass
			try:
				headers = {"Connection" : "close",
						   "User-Agent" : ua,
						   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
						   'Accept-Language': 'en-US,en;q=0.5',
						   'Accept-Encoding': 'gzip, deflate'}
				payload = { 'q': searchfor, 'first': start}
				link = 'https://www.bing.com/search'
				if self.args.proxy:
					response = requests.get(link, headers=headers, params=payload, proxies=proxy, verify=False)
				else:
					response = requests.get(link, headers=headers, params=payload, verify=False)
	
				response.text.encode('utf-8')
				soup = BeautifulSoup(response.text, "lxml")
				
				for div in soup.findAll('li', {'class': 'b_algo'}):

					person_url = div.find('a')['href']
					img_url, location = self.get_person(person_url)
					title_temp = div.find('a').text
					name = title_temp.split(' - ')[0]
					job = title_temp.split(' - ')[1]
					url = div.find('cite').text
					
					
					if hasattr(self, 'pattern'):
						email_address = self.email_matching(name)
					else:
						email_address = None
					
	
					if email_address:
						pwn_data = self.confirm_email(email_address)
					if pwn_data:
						confirmed_email.append(email_address)									
						confirmed = True
					else:
						confirmed = False
	
					if ("name:{}".format(name).strip(), "role:{}".format(job).strip(), \
						"location:{}".format(location).strip(), "image:{}".format(img_url), \
						"email:{}".format(email_address).lower(), "confirmed:{}".format(confirmed), \
						'pwn_data:{}'.format(pwn_data)) in people_details:
						pass
					else:
				
						people_details.append(("name:{}".format(name).strip(), "role:{}".format(job).strip(),
											   "location:{}".format(location).strip(), "image:{}".format(img_url),
											   "email:{}".format(email_address).lower(), "confirmed:{}".format(confirmed),
											   'pwn_data:{}'.format(pwn_data)))								
	
					#entries_tuples.append((url, person.title(), job))
			except Exception:
				if self.args.debug:
					print(traceback.print_exc())
					info('An unhandled exception has occured, please check the \'Error log\' for details')
					error('An Unhandled Exception Has Occured, Please Check The Log For Details' + ERROR_LOG_FILE, exc_info=True)
				continue
		
		self.output.put(self.return_data(people_details))
		
	def scroll_page(self):
		count = 2
		while count:
			scheight = .1
			while scheight < 20.0:
				self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight/{});".format(scheight))
				scheight += .02
			count -= 1
			
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

	def confirm_email(self, email):
		time.sleep(2.6)
		info('Compromised Account Enumeration Search Started')
		pwend_data = []
		seen = set()
		link = 'https://haveibeenpwned.com/api/v3/breachedaccount/{}?truncateResponse=false'.format(email)
		try:
			headers = {"User-Agent" : "BlutoDNS v2.4.15",
					   'hibp-api-key': 'db192f959742455f98106687df692c68'}

			response = requests.get(link, headers=headers, verify=False)
			if response.status_code == 200:
				json_data = response.json()
				
				if json_data:
					if email in seen:
						pass
					else:
						for item in json_data:
							breach_data = ' '
							seen.add(email)
							email_address = email
							breach_domain = item['Domain']
							data = item['DataClasses']
							for value in data:
								breach_data = breach_data + value + ', '
							breach_data = breach_data.strip().strip(',')[:-1]    
							breach_date = item['BreachDate']
							breach_added = item['AddedDate']
							breach_description = item['Description']
							pwend_data.append((email_address, breach_domain, breach_data, breach_date, breach_added, breach_description))		
			else:
				if self.args.debug:
					print('pwned failure: {}'.format(response.reason))		
				info('pwned failure: {}'.format(response.reason))					
		
		except ValueError:
			if self.args.debug:
				print(traceback.print_exc())
			pass
		except Exception:
			if self.args.debug:
				print(traceback.print_exc())
			info('An unhandled exception has occured, please check the \'Error log\' for details')
			error('An Unhandled Exception Has Occured, Please Check The Log For Details' + ERROR_LOG_FILE, exc_info=True)
	
		info('Compromised Account Enumeration Search Completed')
		return pwend_data	


	
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

	
	def companyGet_details(self):
		# Company URL == Company Numner		
		# https://www.linkedin.com/company/7437/
		
		# About URL, Gather Overview etc
		#'https://www.linkedin.com/company/7437/about'		
		
		self.browser.get('https://www.linkedin.com/company/7437/about')
		
		#self.browser.get('https://www.linkedin.com/company/{c}/'.format(c=self.company_number))		
		time.sleep(1)
		html = self.browser.page_source
		soup = BeautifulSoup(html, "lxml")		
		
		self.browser.get('https://www.linkedin.com/company/7437/'.format(c=self.company_name, p=page))		
		html = self.browser.page_source
		soup = BeautifulSoup(html, "lxml")
		
		
		over_view = soup.find('p', {'class': 'break-words white-space-pre-wrap mb5 t-14 t-black--light t-normal'}).text		
		company_site = soup.find('a', {'data-control-name': 'page_details_module_website_external_link'}).href
		# STRING TO CAPTURE HREF FOR COMPANY SITE
		'<a data-control-name="top_card_view_website_custom_cta_btn"'
		
		
		
		# Overiew Grab Text
		'<p class="break-words white-space-pre-wrap mb5 t-14 t-black--light t-normal">'
		
		# External Web Stie Link, Grab href
		'<a data-control-name="page_details_module_website_external_link"'
		
		# Companies House https://beta.companieshouse.gov.uk/
		# Search
		'https://beta.companieshouse.gov.uk/search?q={}' 'saga+plc'
		
		# Company People (Directors etc), iterate all grab details, grab person URL grab all details (nested)
		'https://beta.companieshouse.gov.uk/company/{}/officers' 'company number: 08804263'
	
		
		
	def company(self):

		"""
		Company identification function
		"""

		self.company_name = self.supply_company()
			
		no_interest = ['Upgrade to Premium today', 'seem like a power searcher']
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
					# no_interest = ['Upgrade to Premium today', 'seem like a power searcher']
					if not any(v in str(each) for v in no_interest):
						try:
						
							company_item = each.find('div', {'class': 'search-result__info'})

							if 'search-result__title' in str(company_item):
								if company_item.find('h3', {'class':'search-result__title'}):
									company_name = company_item.find('h3', {'class':'search-result__title'}).text.replace('.', '').replace('\n', '').strip()								
								#print company_name
							if 'subline-level-1' in str(company_item):
								company_type = company_item.find('p', {'class':'subline-level-1'}).text.replace('.', '').replace('\n', '').strip()
								#print company_type
							else:
								company_type = None
							if 'subline-level-2' in str(company_item):
								company_people = company_item.find('p', {'class':'subline-level-2'}).text.replace('.', '').replace('\n', '').strip()
								#print company_people
							else:
								company_people = None
								
							if 'search_srp_result' in str(company_item):
								data = company_item.find('a', href=True)
								company_url = 'https://www.linkedin.com' + data['href']
								company_number = data['href'].replace('/company/', '').replace('/', '')
							#print '\n'
	
							company_details.append((company_name, company_type, company_people, company_number, company_url))
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
									print('\n')
									print('Searching LinkedIn for ' + tmp + ' staff members\n')
									self.company_number = company_number
									self.company_found = True
									# GET COMPANY DETAILS
									
									self.browser.get(company_url)
									time.sleep(1)
									html = self.browser.page_source
									soup = BeautifulSoup(html, "lxml")									
									data = soup.find('a', {'data-control-name': 'topcard_see_all_employees'})['href']
									if soup.find('a', {'data-control-name': 'top_card_view_website_custom_cta_btn'}):
										company_site = soup.find('a', {'data-control-name': 'top_card_view_website_custom_cta_btn'})['href']
									else:
										company_site = ''
									
									self.company_site = company_site
									self.company_people_search = 'https://www.linkedin.com' + data
									
									#js = "var aa=document.getElementsByClassName('org-top-card-primary-actions')[0];aa.parentNode.removeChild(aa)"
									#js2 = "var bb=document.getElementsByClassName('org-top-card__right-col')[0];bb.parentNode.removeChild(bb)"
									#js3 = "var bb=document.getElementsByClassName('org-top-card__secondary-actions-container')[0];bb.parentNode.removeChild(bb)"
									#js4 = "var bb=document.getElementsByClassName('org-top-card-summary__info-list')[0];bb.parentNode.removeChild(bb)"
									
									#self.browser.execute_script(js)
									#self.browser.execute_script(js2)
									#self.browser.execute_script(js3)
									#self.browser.execute_script(js4)
									
									#element = self.browser.find_element_by_class_name('org-top-card')
									#element.screenshot('CompanyBanner.png')
									
									#self.browser.get(company_url + 'about/')
									#time.sleep(1)
									return
								elif confirmed.lower() in ('n', 'no'):
									continue
								else:
									self.negative(confirmed)
						except AttributeError:
							print(traceback.print_exc())
						except Exception as e_rror:
							print(traceback.print_exc())
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
			self.browser.get(self.company_people_search + '&page=1')
			
			self.scroll_page()
			time.sleep(2)
			self.browser.refresh
			html = self.browser.page_source
			
			soup = BeautifulSoup(html, "lxml")
			result_page = soup.find('ul', {'class': 'artdeco-pagination__pages artdeco-pagination__pages--number'})
			if result_page:
				li_list = result_page.findAll('li', {'class': 'artdeco-pagination__indicator artdeco-pagination__indicator--number'})
				
				for li in li_list:
					
					if '.' in li.span.text:
						pass
					elif '\u2026' in li.span.text:
						pass
					else:
						numbers.append(int(li.span.text))
			else:
				return 50
		except AttributeError as error_:
			info('An "AttributeError" error has occured, please check the \'Error log\' for details: {}'.format(ERROR_LOG_FILE))
			error('An "AttributeError" error has occured, Please Check The Log For Details' + ERROR_LOG_FILE, exc_info=True)
			return 50
		except Exception:
			info('An unhandled exception has occured, please check the \'Error log\' for details')
			error('An Unhandled Exception Has Occured, Please Check The Log For Details' + ERROR_LOG_FILE, exc_info=True)
			return 50
		
		if numbers:
			#return 2
			return max(numbers)
		else:
			info('no numbers found')
			info('returning default: 50')
			return 50
	
	
	def email_pattern(self):
		info('Pattern Search Started')
		link = 'https://api.hunter.io/v2/domain-search?domain={0}&api_key={1}'.format(self.args.domain, random.choice(self.hunter_keys))
		if self.args.proxy == True:
			proxy = {'http' : 'http://127.0.0.1:8080'}
		else:
			pass
		try:
			headers = {"User-Agent" : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
			           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
			    'Accept-Language': 'en-US,en;q=0.5',
			    'Accept-Encoding': 'gzip, deflate'}            
			if self.args.proxy == True:
				response = requests.get(link, headers=headers, proxies=proxy, verify=False)
			else:
				response = requests.get(link, headers=headers, verify=False)
			if response.status_code == 200:
				json_data = response.json()
			
				if json_data['data']['pattern']:
					info('Pattern Search Started')
					self.pattern = json_data['data']['pattern']

			elif response.status_code == 401:
				json_data = response.json()
			
				if json_data['message'] =='Too many calls for this period.':
					print(colored("\tError:\tIt seems the Hunter API key being used has reached\n\t\tit's limit for this month.", 'red'))
					print(colored('\tAPI Key: {}\n'.format(self.args.api),'red'))
					q.put(None)
					return None
				if json_data['message'] == 'Invalid or missing api key.':
					print(colored("\tError:\tIt seems the Hunter API key being used is no longer valid", 'red'))
					print(colored('\tAPI Key: {}\n'.format(self.args.api),'red'))
					print(colored('\tWhy don\'t you grab yourself a new one (they are free)','green'))
					print(colored('\thttps://hunter.io/api_keys','green'))
					q.put(None)
					return None
				else:
					raise Valueerror('No Response From Hunter')

		except UnboundLocalError:
			error('An UnboundLocalError Exception Has Occured, Please Check The Log For Details' + ERROR_LOG_FILE, exc_info=True)
		except KeyError:
			pass
		except ValueError:
			pass
		except Exception:
			info('An unhandled exception has occured, please check the \'Error log\' for details')
			error('An Unhandled Exception Has Occured, Please Check The Log For Details' + ERROR_LOG_FILE, exc_info=True)   	
	
	
	def email_matching(self, name):
		if '{first}.{last}' in self.pattern:
			if ' ' in name:
				name = re.sub('\(.*?\)', '', name)
				split = name.lower().rstrip().strip().split(' ')
				if len(split) == 2:
					firstname, lastname = split
					email_address = firstname + '.' + lastname + '@' + self.domain
				else:
					email_address = None
			else:
				email_address = None
		
		elif '{first}' in self.pattern:
			if ' ' in name:
				name = re.sub('\(.*?\)', '', name)
				split = name.lower().rstrip().strip().split(' ')
				if len(split) == 2:
					firstname, lastname = split
					email_address = firstname + '@' + self.domain
				else:
					email_address = None
			else:
				email_address = None			
		else:
			email_address = None	
		
		return email_address
		
	
	
	def return_data(self, people_details):
		people_details = sorted(people_details, key=lambda tup: tup[4])
		return (people_details)	
	
		
	def people(self):

		"""
		Gather Staff Members
		"""

		global SEEN
		
		i = 0

		people_details = []
		confirmed_email = []
		if self.staff_page == 20:
			data = self.result_pages()
			if isinstance(data, int):
				self.staff_page = data
			else:
				print(colored('\n\nUser account reached search limit!', 'red'))
				error('User account reached search limit!')
				info('User account reached search limit!')
				self.output.put(self.return_data(people_details))
				self.browser.close()				
				return
			
		for page in tqdm(range(1, self.staff_page)):
			
			self.browser.get(self.company_people_search + '&page={}'.format(page))

			time.sleep(2)
			html = self.browser.page_source	
			
			try:
				limit = ['You’ve reached the monthly limit for profile searches', 'No results found']
				if any(v in self.browser.page_source for v in limit):
				#if any(limit) in self.browser.page_source:
					raise NoMoreData("No more results found")
			except NoMoreData as e_rror:
				print('\n\nNo further results possible\n')
				print('{} staff members found\n'.format(len(SEEN)))
				print('Confirmed accounts: {}'.format(len(confirmed_email)))
				error('No further results possible')
				info('No further results possible')
				self.output.put(self.return_data(people_details))
				self.browser.close()				
				return					
				
			soup = BeautifulSoup(html, "lxml")

			data = soup.find('ul', {'class': 'search-results__list'})
			#print data.contents
			
			if self.args.api:
				self.args.email = True
				self.email_pattern()
				
			if data:
				
				li_list = data.findAll('li', {'class': 'search-result search-result__occluded-item ember-view'})

				for li_item in li_list:
					pwn_data = []
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

								if name.lower() in SEEN:
									pass
								else:
									SEEN.append(name.lower())
									
									
									if hasattr(self, 'pattern'):
										email_address = self.email_matching(name)
									else:
										email_address = None
										
									if email_address:
										pwn_data = self.confirm_email(email_address)
									if pwn_data:
										confirmed_email.append(email_address)									
										confirmed = True
									else:
										confirmed = False
									
									if ("name:" + name.strip(), "role:" + job.strip(), "location:" + location.strip(), "image:" + img_url, \
										"email:" + str(email_address).lower(), "confirmed:{}".format(confirmed), 'pwn_data:{}'.format(pwn_data)) in people_details:
										pass
									else:
									
										people_details.append(("name:" + name.strip(),
																  "role:" + job.strip(),
																  "location:" + location.strip(),
																  "image:" + img_url,
																  "email:" + str(email_address).lower(),
																  "confirmed:{}".format(confirmed),
																  'pwn_data:{}'.format(pwn_data)))


								if li_item.find('div', {'class', 'search-result__profile-blur'}):
									print(colored('\nYou\'ve Reached The Limit Imposed by LinkedIn', 'yellow'))
									print('{} staff members found\n'.format(len(SEEN)))
									print('Confirmed accounts: {}'.format(len(confirmed_email)))
									error('User account reached search limit!')
									info('User account reached search limit!')
									self.output.put(self.return_data(people_details))
									self.browser.close()				
									return	

					except KeyError as e_rror:
						if 'src' in e_rror.args:
							pass
						else:
							info('An unhandled exception has occured, please check the \'Error log\' for details')
							error('An Unhandled Exception Has Occured, Please Check The Log For Details' + ERROR_LOG_FILE, exc_info=True)							
					except UnboundLocalError as e_rror:
						if 'name' in e_rror.args:
							name = None
						if 'job' in e_rror.args:
							job = None
						if 'location' in e_rror.args:
							location = None
						continue
					except TypeError:
						print(traceback.print_exc())
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
						self.output.put(self.return_data(people_details))
						return
					
			else:
				time.sleep(2)
				continue
			
			if 'upgrade to Premium to continue searching' in html:
				print(colored('\nYou\'ve Reached The Limit Imposed by LinkedIn', 'yellow'))
				print('{} staff members found\n'.format(len(SEEN)))
				print('Confirmed accounts: {}'.format(len(confirmed_email)))
				error('User account reached search limit!')
				info('User account reached search limit!')
				self.output.put(self.return_data(people_details))
				self.browser.close()				
				return	
			
		print('{} staff members found\n'.format(len(SEEN)))
		print('Confirmed accounts: {}'.format(len(confirmed_email)))
		try:
			self.output.put(self.return_data(people_details))
			self.browser.close()
		except Exception:
			print(traceback.print_exc())
			print('')
			
