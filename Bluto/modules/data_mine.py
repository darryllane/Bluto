import pdfminer
import requests
import urllib2
import oletools.thirdparty.olefile as olefile
import os
import traceback
import time
import re
import random
import sys
import Queue
import threading
from termcolor import colored
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from bs4 import BeautifulSoup
from bluto_logging import info, error, INFO_LOG_FILE, ERROR_LOG_FILE
from get_file import get_user_agents
from search import doc_bing, doc_exalead



def action_download(doc_list, docs):
	info('Document Download Started')
	i = 0
	download_list = []
	initial_count = 0
	print 'Gathering Live Documents For Metadata Mining\n'
	for doc in doc_list:
		initial_count += 1
		try:
			r = requests.get(doc)
			if r.status_code == 404:
				r.raise_for_status()
			if re.search('filename="(.*)"', r.headers['content-disposition']):
				filename_t = re.search('filename="(.*)"', r.headers['content-disposition'])
				filename = filename_t.group(1)
			else:
				continue
			with open(docs + filename, "w") as code:
				i += 1
				code.write(r.content)
				code.close()
				print('\tDownload Count: {}\r'.format(str(initial_count))),
				download_list.append(doc)
				info(doc)

		except IOError:
			pass
		except requests.exceptions.HTTPError:
			error('Error: File Not Found Server Side')
			error(doc)
		except requests.exceptions.ConnectionError:
			error('Error: File Not Found Server Side')
			error(doc)
			continue
		except KeyError:
			temp = str(doc).rsplit('.', 1)[1]
			ext = re.sub(r'\?.*', r'', temp)
			filename = "file{}.{}".format(i, ext.replace('?T', ''))
		try:
			with open(docs + filename, "w") as code:
				i += 1
				code.write(r.content)
				code.close()
				print('\tDownload Count: {}\r'.format(str(initial_count))),
				info(doc)
				download_list.append(doc)

			continue
		except IOError:
			pass
		except Exception:
			error('An Unhandled Exception Has Occured, Please Check The Log For Details' + ERROR_LOG_FILE, exc_info=True)
			error(doc)
			error(r.headers)
			continue
	if i < 1:
		sys.exit()

	info('Documents Downloaded: {}'.format(initial_count))
	return download_list


def doc_search(domain, USERAGENT_F, prox):
	q1 = Queue.Queue()
	q2 = Queue.Queue()
	t1 = threading.Thread(target=doc_bing, args=(domain, USERAGENT_F, prox, q1))
	t2 = threading.Thread(target=doc_exalead, args=(domain, USERAGENT_F, prox, q2))
	t1.start()
	t2.start()
	t1.join()
	t2.join()
	bing = q1.get()
	exalead = q2.get()
	list_d = bing + exalead
	return list_d


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
				oddity = re.match('(\s\w\s+(\w\s+)+\w)', person)
				if oddity:
					oddity = str(oddity.group(1)).replace(' ', '')
					user_names.append(str(oddity).title())
				else:
					user_names.append(str(person).title())
			if software:
				oddity2 = re.match('(\s\w\s+(\w\s+)+\w)', software)
				if oddity2:
					oddity2 = str(oddity2.group(1)).replace(' ', '')
					software_list.append(oddity2)
				else:
					software_list.append(software)
		except pdfminer.pdfparser.PDFSyntaxError:
			pass
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
				oddity = re.match('(\s\w\s+(\w\s+)+\w)', author)
				if oddity:
					oddity = str(oddity.group(1)).replace(' ', '')
					user_names.append(str(oddity).title())
				else:
					user_names.append(str(author).title())
			if software:
				oddity2 = re.match('(\s\w\s+(\w\s+)+\w)', software)
				if oddity2:
					oddity2 = str(oddity2.group(1)).replace(' ', '')
					software_list.append(oddity2)
				else:
					software_list.append(software)

			if save_by:
				oddity3 = re.match('(\s\w\s+(\w\s+)+\w)', save_by)
				if oddity3:
					oddity3 = str(oddity3.group(1)).replace(' ', '')
					user_names.append(str(oddity3).title())
				else:
					user_names.append(str(save_by).title())

		except Exception:
			pass
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
	doc_list = doc_search(domain, USERAGENT_F, prox)

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
