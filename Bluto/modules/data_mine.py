
import requests
import urllib2
import oletools.thirdparty.olefile as olefile
import os
import traceback
import time
import re
import random
import sys
from termcolor import colored
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from bs4 import BeautifulSoup
from bluto_logging import info, error, INFO_LOG_FILE, ERROR_LOG_FILE
from get_file import get_user_agents


def action_download(doc_list, docs):
	info('Document Download Started')
	i = 0
	download_list = []
	print '\nGathering Live Documents For Metadata Mining\n'
	for doc in doc_list:
		try:
			r = requests.get(doc)
			if r.status_code == 404:
				r.raise_for_status()
			filename = re.search('filename="(.*)"', r.headers['content-disposition']).group(1)
			with open(docs + filename, "w") as code:
				i += 1
				code.write(r.content)
				code.close()
				print '\t' + doc
				download_list.append(doc)
				info(doc)
		except requests.exceptions.HTTPError:
			error('Error: File Not Found Server Side')
			error(doc)
		except requests.exceptions.ConnectionError:
			error('Error: File Not Found Server Side')
			error(doc)
		except KeyError:
			temp = str(doc).rsplit('.', 1)[1]
			ext = re.sub(r'\?.*', r'', temp)
			filename = "file{}.{}".format(i, ext.replace('?T', ''))
			with open(docs + filename, "w") as code:
				i += 1
				code.write(r.content)
				code.close()
				print '\t' + doc
				info(doc)
				download_list.append(doc)
			continue
		except Exception:
			error('An Unhandled Exception Has Occured, Please Check The Log For Details' + ERROR_LOG_FILE, exc_info=True)
			error(doc)
			error(r.headers)
			continue
	if i < 1:
		sys.exit()

	download_count = len(download_list)
	info('Documents Downloaded: {}'.format(download_count))
	print colored('\n\tDocuments Downloaded: {}', 'red').format(download_count)
	return download_list


def action_documents(domain, USERAGENT_F, prox):
	document_list = []
	uas = get_user_agents(USERAGENT_F)
	info('Document Search Started')
	for start in range(0,80,10):
		ua = random.choice(uas)
		link = 'http://www.exalead.com/search/web/results/?search_language=&q=(filetype:xls+OR+filetype:doc+OR++filetype:pdf+OR+filetype:ppt)+site:{}&search_language=&elements_per_page=10&start_index={}'.format(domain, start)
		if prox == True:
			proxy = {'http' : 'http://127.0.0.1:8080'}
		else:
			pass
		try:
			headers = {"Connection" : "close",
			           "User-Agent" : ua,
			           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
			           'Accept-Language': 'en-US,en;q=0.5',
			           'Accept-Encoding': 'gzip, deflate'}
			if prox == True:
				response = requests.get(link, headers=headers, proxies=proxy)
			else:
				response = requests.get(link, headers=headers)
			soup = BeautifulSoup(response.text, "lxml")
			if soup.find('label', {'class': 'control-label', 'for': 'id_captcha'}):
				print colored("\tSo you don't like spinach?", "blue")
				print "\n\tCaptchas are preventing any more potential document searches."
				break
			for div in soup.findAll('li', {'class': 'media'}):
				document = div.find('a', href=True)['href']
				document = urllib2.unquote(document)
				document_list.append(document)
			time.sleep(10)
		except Exception:
			error('An Unhandled Exception Has Occured, Please Check The Log For Details' + ERROR_LOG_FILE, exc_info=True)
			continue
	potential_docs = len(document_list)
	info('Document Search Finished')
	print '\nGathered Potentialy Useful Documents'
	info('Potential Documents Found: {}'.format(potential_docs))
	print colored('\n\tPotential Document Count: {}', 'red').format(potential_docs)
	return document_list


#Extract Author PDF
def pdf_read(pdf_file_list):
	info('Extracting PDF MetaData')
	software_list = []
	user_names = []
	for filename in pdf_file_list:
		try:

			fp = open(filename, 'rb')
			parser = PDFParser(fp)
			doc = PDFDocument(parser)
			software = re.sub('[^0-9a-zA-Z]+', ' ', doc.info[0]['Creator'])
			person = re.sub('[^0-9a-zA-Z]+', ' ', doc.info[0]['Author'])
			if person:
				user_names.append(str(person).title())
			if software:
				software_list.append(software)
		except PDFSyntaxError:
			error('This doesnt seem to be a PDF' + filename, exc_info=True)
		except KeyError:
			continue
		except TypeError:
			pass
		except Exception:
			error('An Unhandled Exception Has Occured, Please Check The Log For Details' + ERROR_LOG_FILE, exc_info=True)
			continue
	info('Finished Extracting PDF MetaData')
	return (user_names, software_list)



#Extract Author MS FILES
def ms_doc(ms_file_list):
	software_list = []
	user_names = []
	info('Extracting MSDOCS MetaData')
	for filename in ms_file_list:
		try:
			data = olefile.OleFileIO(filename)
			meta = data.get_metadata()
			author = re.sub('[^0-9a-zA-Z]+', ' ', meta.author)
			company  = re.sub('[^0-9a-zA-Z]+', ' ', meta.company)
			software  = re.sub('[^0-9a-zA-Z]+', ' ', meta.creating_application)
			save_by = re.sub('[^0-9a-zA-Z]+', ' ', meta.last_saved_by)
			if author:
				user_names.append(str(author).title())
			if software:
				software_list.append(software)
			if save_by:
				user_names.append(str(save_by).title())

		except Exception:
			error('An Unhandled Exception Has Occured, Please Check The Log For Details' + ERROR_LOG_FILE, exc_info=True)
	info('Finished Extracting MSDOC MetaData')
	return (user_names, software_list)

#Modules takes in DOMAIN, PROX, USERAGENTS outputs user_names, software_list
def doc_start(domain, USERAGENT_F, prox, q):
	ms_list_ext = ('.docx', '.pptx', '.xlsx', '.doc', '.xls', '.ppt')
	ms_file_list = []
	pdf_file_list = []
	info('Let The Hunt Begin')
	domain_r = domain.split('.')
	if not os.path.exists(os.path.expanduser('~/Bluto/doc/{}'.format(domain_r[0]))):
		os.makedirs(os.path.expanduser('~/Bluto/doc/{}'.format(domain_r[0])))

	location = os.path.expanduser('~/Bluto/doc/{}/'.format(domain_r[0]))
	info('Data Folder Created ' + location)
	docs = os.path.expanduser(location)
	doc_list = action_documents(domain, USERAGENT_F, prox)

	if doc_list == []:
		q.put(None)
		return
	download_list = action_download(doc_list, docs)
	download_count = len(download_list)

	for root, dirs, files in os.walk(docs):
		for filename in files:
			if str(filename).endswith(ms_list_ext):
				ms_file_list.append(os.path.join(root, filename))
			if str(filename).endswith('.pdf'):
				pdf_file_list.append(os.path.join(root, filename))

	if ms_file_list and pdf_file_list:
		user_names_ms, software_list_ms = ms_doc(ms_file_list)
		user_names_pdf, software_list_pdf = pdf_read(pdf_file_list)
		user_names_t = user_names_ms + user_names_pdf
		software_list_t = software_list_ms + software_list_pdf

	elif ms_file_list:
		user_names_ms, software_list_ms = ms_doc(ms_file_list)
		user_names_t = user_names_ms
		software_list_t = software_list_ms

	elif pdf_file_list:
		user_names_pdf, software_list_pdf = pdf_read(pdf_file_list)
		user_names_t = user_names_pdf
		software_list_t = software_list_pdf
	else:
		user_names_t = []
		software_list_t = []

	if user_names_t and software_list_t:
		user_names = sorted(set(user_names_t))
		software_list = sorted(set(software_list_t))
		info('The Hunt Ended')
		q.put((user_names, software_list, download_count))

	elif software_list_t:
		software_list = sorted(set(software_list_t))
		user_names = []
		info('The Hunt Ended')
		q.put((user_names, software_list, download_count))

	elif user_names_t:
		user_names = sorted(set(user_names_t))
		software_list = []
		info('The Hunt Ended')
		q.put((user_names, software_list, download_count))
