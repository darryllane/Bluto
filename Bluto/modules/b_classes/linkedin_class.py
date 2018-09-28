"""

Class to discover and report staff members of a target organisation from LinkedIn

"""

import re
import time
import os
import socket
import traceback
import sys
import json
import pythonwhois
import multiprocessing as mp

from ..logger_ import info, error
from tqdm import tqdm
from pyvirtualdisplay import Display
from termcolor import colored
from selenium import webdriver
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

			username, password = args.la.split(args.deli)
			domain = args.domain
			cpage, page = page_limits.split(':')

			self.username = username
			self.password = password
			self.domain = domain
			self.company_page = int(cpage)

			self.company_details = company_details
			self.company_name = company
			self.staff_page = int(page)
			self.company_number = company_number

			display = Display(visible=0, size=(800, 600))
			display.start()
			executable = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../../doc/driver/chromedriver'))
			browser = webdriver.Chrome(executable_path=executable)
			self.browser = browser
			time.sleep(1)
			self.browser.get('https://www.linkedin.com/uas/login')
			time.sleep(3)
			username1 = browser.find_element_by_name("session_key")
			password1 = browser.find_element_by_name("session_password")
			username1.send_keys(self.username)
			password1.send_keys(str(self.password))
			time.sleep(0.5)
			browser.find_element_by_id("btn-primary").click()
			time.sleep(1)

			if 'alert error' in self.browser.page_source:
				raise NotLoggedIn('You have had an error logging in')

			session_id = self.browser.session_id
			self.session_id = session_id

		except NotLoggedIn:
			info('failed to login')
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
			temp_company = input('\nPlease Supply The Company Name\n\nThis Will Be Used To Query LinkedIn: ')
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


	def result_accept(self, company, result):

		"""
		Confirmation of WHOIS response as company search string
		"""

		if result:
			try:
				print('\nThe Whois Results Look Promising!')
				while True:
					tmp = colored('{}\n', 'green').format(company)

					confirmed = input('\nIs The Search Term sufficient? ' +
					                  tmp + colored('(y|n)', 'yellow') + ': ')

					if confirmed.lower() in ('y', 'yes'):
						print('\nSearching LinkedIn Companies for {}\n'.format(company))
						self.company_name = company
						return
					elif confirmed.lower() in ('n', 'no'):
						self.company_name = self.supply_company()
						return
					else:
						self.negative(confirmed)

			except Exception:
				print('An Unhandled Exception Has Occured, Please Check The Log For Details')
				info('An Unhandled Exception Has Occured, Please Check The Log For Details')
				info(traceback.print_exc())

		else:
			try:
				print(colored("\nThe Whois Results Don't Look Very Promissing: '{}'", "red").format(company))
				self.supply_company()
				return

			except Exception:
				print('An Unhandled Exception Has Occured, Please Check The Log For Details')
				info('An Unhandled Exception Has Occured, Please Check The Log For Details')
				info(traceback.print_exc())


	def company(self):

		"""
		Company identification function
		"""

		try:
			whois_things = pythonwhois.get_whois(self.domain)
			try:
				company = whois_things['contacts']['registrant']['name']
			except Exception:
				print('\nThere seems to be no Registrar for this domain.')
				company = self.domain

			splitup = company.lower().split()
			patern = re.compile('|'.join(splitup))

			if patern.search(self.domain):
				result = True
				company = self.result_accept(company, result)
			else:
				result = False
				company = self.result_accept(company, result)


		except pythonwhois.shared.WhoisException:
			print(traceback.print_exc())
		except socket.error:
			print(traceback.print_exc())
		except KeyError:
			print(traceback.print_exc())
		except Exception as e_rror:
			print(e_rror.args)
			print(colored('\nWhoisError: You may be behind a proxy or firewall preventing whois lookups. \
			            Please supply the registered company name, if left blank the domain name ' +
			              '"' + self.domain + '"' + ' will be used for the Linkedin search. The results may \
			                not be as accurate.', 'red'))

			temp_company = input(colored('\nRegistered Company Name: ', 'green'))
			if temp_company == '':
				company = self.domain
			else:
				company = temp_company

			print(traceback.print_exc())


		if 'company' not in locals():
			company = self.supply_company()
			return company

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
							confirmed = input('\n{}'.format(tmp) + '{}\n{}'.format(company_type, company_people) + '\n\n' + colored('(y|n)','yellow') )
							if confirmed.lower() in ('y', 'yes'):
								tmp = colored(company_name, 'green')
								print('\nTarget Company Identified:\n')
								print('\t' + str(company_name))
								print('\t' + str(company_type))
								print('\t' + str(company_people))
								print('\nSearching LinkedIn for ' + tmp + ' staff members\n')
								self.company_number = company_number
								self.company_found = True
								return
							elif confirmed.lower() in ('n', 'no'):
								continue
							else:
								self.negative(confirmed)

					except Exception as e_rror:
						print('An Unhandled Exception Has Occured, Please Check The Log For Details')
						info('An Unhandled Exception Has Occured, Please Check The Log For Details')
						info(traceback.print_exc())

			self.company_details = company_details
			company_number = self.not_exact()
			self.company_found = True
			return

		except Exception:
			print('An Unhandled Exception Has Occured, Please Check The Log For Details')
			info('An Unhandled Exception Has Occured, Please Check The Log For Details')
			info(traceback.print_exc())


	def people(self):

		"""
		Gather Staff Members
		"""

		global SEEN

		i = 0
		people_details = []

		for page in tqdm(range(1, self.staff_page)):
			self.browser.get('https://www.linkedin.com/search/results/people/?facetCurrentCompany={}&page={}'.format(self.company_number, page))

			time.sleep(4)
			html = self.browser.page_source
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
								if re.match('.*url\(\"(http[s|]\:\/\/.*?)\"\).*', str(img_url_tmp)):
									img_url = re.match('.*url\(\"(http[s|]\:\/\/.*?)\"\).*', str(img_url_tmp)).group(1)
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
							info('An Unexpected Exception Has Occured, Please Check The Log For Details')
							info(traceback.print_exc())
					except UnboundLocalError as e_rror:
						if 'name' in e_rror:
							name = None
						if 'job' in e_rror:
							job = None
						if 'location' in e_rror:
							location = None
						continue
					except TypeError as e:
						print(traceback.print_exc())
						continue
					except Exception:
						print(traceback.print_exc())
						info('An Unhandled Exception Has Occured, Please Check The Log For Details')
						info(traceback.print_exc())
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

		self.output.put(people_details)
